## Repository-specific guidance for AI coding assistants

Keep this short and actionable. Focus on the code paths and conventions in this repository so an agent can be productive quickly.

- Project layout (big picture):
  - `main/prod/` — production entrypoints and runtime services (e.g. `app.py`, `app_delist.py`, `app_update_account_balances.py`, `tradingBot.py`, `telegram_bot.py`). These scripts are executed inside containers by `docker-compose.yml` (see `app`, `delist`, `update_account_balances` services).
  - `main/backtest/` — backtesting app and managers (run with `python main/backtest/app.py` or through the `backtest` service).
  - `main/common/` — shared domain models, DAOs, utilities and strategy base classes. Important files: `common/dao/database_operations.py`, `common/util.py`, `common/strategy*.py`.
  - `main/prod/released_strategies/` — dynamically imported strategy classes. Code uses runtime import to instantiate strategies from DB names.

- How code is wired (data flows & runtime):
  - At startup `main/prod/app.py` imports released strategies (`import_all_strategies`) then loads enabled strategies from DB with `get_enabled_strategies_by_type` and instantiates them via `get_strategies_by_type` (see `common/util.py`).
  - `TradingBot` (in `main/prod/tradingBot.py`) is the main loop: it reads active pairs and strategies from the DB, fetches candles via `prod.candle_data.CandleData`, composes datasets (`Dataset`) and delegates to `StrategyManager` to open/close positions.
  - Exchange credentials are stored encrypted in DB (`exchange_config` table). `prod/login.Login` reads a secret (mounted under `/run/secrets/`) to derive a Fernet key and decrypt API keys.
  - Database access is via lightweight DAOs in `main/common/dao/*.py` using `psycopg` and a connection string from `config.config` (DEV_ENV_CON/PROD env vars).

- Important runtime conventions:
  - Secrets: Docker Compose mounts `decrypt_secret_trading` and `decrypt_secret_delist` (see `docker-compose.yml`). In prod these are expected under `/run/secrets/*` inside containers. Login flows depend on that file.
  - Strategy discovery: new strategy classes are loaded dynamically from `prod/released_strategies` and must expose a class with the same name stored in DB `strategy.name`. If the class name doesn't match, the strategy will be skipped (logged in `common/util.get_strategies_by_type`).
  - Time/interval logic: `TradingBot.should_run_strategy` uses `management.time_intervals_to_minutes` and rounds next execution to the hour — be careful when changing intraday intervals lower than 1h.

- Developer workflows & quick commands:
  - Run the app locally (container): `docker-compose up --build app` or `docker-compose run --rm --service-ports app` (see `docker-compose.yml` comments).
  - Start API: `docker-compose run --rm api` or `uvicorn main.prod.api:api --host=0.0.0.0` (API expects `PYTHONPATH=/noshirt/main`).
  - Run backtests: `docker-compose run --rm backtest` or `python main/backtest/app.py`.
  - Inspect DB: `docker exec -it noshirt-postgres psql -U postgres -d noshirt` (container name from compose file).
  - Tests: repository uses simple integration-style tests in `main/tests/` (not a strict pytest configuration). Run an individual test file as a script (e.g. `python main/tests/test_update_account_balances.py`) — many tests perform real API calls and DB updates.

- Patterns and conventions to follow when editing code:
  - Prefer using provided DAOs for DB interactions (e.g. `common/dao/database_operations.py`, `strategy_dao.py`) instead of raw SQL in new code.
  - Use `import_all_strategies(STRATEGIES_PATH_PROD, STRATEGIES_MODULE_PROD, globals())` when writing modules that need runtime-discovered strategies.
  - When adding new runtime configuration values, place them in `initial_config` DB table rather than ad-hoc env variables; code reads `db.get_initial_config()` in `app.py` and `Env_setup`.
  - Logging: use `prod.logger` / `aws_logger` patterns already present; exceptions are often reported to users via `prod.notify.send_message_alert`.

- Integration points & external deps to be aware of:
  - Binance exchange calls are wrapped by `main/prod/binance.py` and used throughout (leverage, account info, orders). Tests may call the real API.
  - Telegram notifications: `prod/telegram_notify.py` and `prod/telegram_bot.py` send alerts — check these for message formats when changing alerts.
  - Postgres DB: schema is under `main/prod/resources/db` and mounted into the `db` service. DAOs rely on certain tables (strategy, pair, exchange_config, trade, order_control, bot_execution_control, initial_config).

- Small examples (copy-paste friendly):
  - Instantiate strategies currently enabled for trading: see `common/util.get_strategies_by_type` — it expects DB rows from `strategy_dao.get_enabled_strategies_by_type`.
  - Decrypt stored exchange key in code: `fernet = Login(...).create_cryptography_key(); id, sk = Login(...).get_sign_pair(fernet)` (used in `Login.login_database`).

- What not to change lightly:
  - The dynamic strategy loading + DB name-matching contract. Renaming a class without updating the DB will silently skip strategies.
  - `TradingBot.should_run_strategy` timing logic — subtle rounding to hour exists.
  - Secrets handling (`/run/secrets/*`) — tests and containers depend on this location.

If anything is unclear or you want the instructions organized differently (for example: more examples, quick-reference commands, or adding a checklist for PRs), tell me what to change and I'll iterate.
