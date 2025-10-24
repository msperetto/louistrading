# Delist Integration Tests

End-to-end integration tests for the delist service that run against real Docker services in TEST mode.

## Overview

These tests simulate the complete delist workflow:
1. Create test announcements via API
2. Wait for delist service to process them
3. Validate results in database and logs
4. Clean up test data

## Prerequisites

### 1. Docker and Docker Compose

Ensure Docker and Docker Compose are installed:

```bash
docker --version
docker-compose --version
```

That's it! All Python dependencies are installed inside the Docker container.

### 2. Database Setup

Ensure the `test_delist_announcement` table exists:

```sql
CREATE TABLE IF NOT EXISTS test_delist_announcement (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    announcement_date DATE NOT NULL,
    coins TEXT[] NOT NULL,
    processed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE INDEX idx_test_delist_processed ON test_delist_announcement(processed);
```

### 3. Configuration

Ensure your `docker-compose.yml` has the delist service configured for TEST mode:

```yaml
delist:
  build: .
  container_name: noshirt_delist
  volumes:
    - .:/noshirt
  environment:
    - ENVIRONMENT=TEST  # Important!
    - PYTHONPATH=/noshirt/main
    - POSTGRES_HOST=db
  command: python main/prod/app_delist.py
  depends_on:
    - db
```

## Running Tests

### Basic Usage (Docker-based)

```bash
# Run all tests with default settings (in Docker container)
./main/tests/integration/run_tests.sh
```

### Advanced Usage

```bash
# Use custom test cases file
./main/tests/integration/run_tests.sh --csv path/to/custom_tests.csv

# Skip cleanup (for debugging)
./main/tests/integration/run_tests.sh --no-cleanup

# Run directly with docker-compose
docker-compose run --rm integration_test

# Run with custom arguments
docker-compose run --rm integration_test \
  python main/tests/integration/delist_integration_test.py --no-cleanup
```

## Test Cases

Test cases are defined in CSV format (`Delist tests - TestCases1.csv`):

| Column | Description |
|--------|-------------|
| TEST CASE | Description of what's being tested |
| COINS | Comma-separated list of coins |
| COINS IN FUTURES | Which coins are available in Binance Futures |
| BINANCE BALANCE | Account balance (for planning) |
| REAL TRADE | Whether to execute real trades (always "No" in TEST) |
| Expected Result | What should happen |
| API POST CALL | curl command to create the test announcement |

### Example Test Cases

1. **Valid delist with futures coins**
   - Title: "Binance Will Delist EPX, FORTH, KEY Trading Pairs on 2025-12-31"
   - Expected: Open positions only for FORTH (only futures coin)

2. **Invalid title (NOT Delist)**
   - Title: "Binance Will NOT Delist BLESS, YB, ARDR Trading Pairs on 2025-12-31"
   - Expected: No positions opened

3. **No futures coins**
   - Title: "Binance Will Delist ALCX, ATM Trading Pairs on 2025-12-31"
   - Expected: No positions opened (spot-only coins)

## What Gets Tested

### 1. Title Validation
- ✅ "Binance Will Delist" → Process
- ❌ "Binance Will NOT Delist" → Ignore
- ❌ Case sensitivity → "Binance will delist" should work

### 2. Coin Filtering
- ✅ Only futures-available coins processed
- ✅ Spot-only coins ignored
- ✅ Non-existent coins ignored

### 3. Database State
- ✅ `test_delist_announcement` marked as processed
- ✅ `delist_announcement` entries created for valid coins
- ✅ No real `trade` records in TEST mode

### 4. TEST Mode Behavior
- ✅ Simulates positions without creating trades
- ✅ Logs detailed position information
- ✅ Uses orderbook data for simulation

## Test Workflow

```
1. Load test cases from CSV
   ↓
2. For each test case:
   ├── Create test announcement via API
   ├── Wait for delist service to process (up to 3 minutes)
   ├── Validate:
   │   ├── Announcement marked as processed
   │   ├── Correct coins in delist_announcement table
   │   ├── No real trades in TEST mode
   │   └── Logs contain expected information
   ├── Wait 2 minutes before next test
   └── Record result (PASSED/FAILED)
   ↓
3. Cleanup:
   ├── Delete test announcements
   ├── Delete delist announcements
   └── Delete any test trades
   ↓
4. Print summary report
```

## Troubleshooting

### Tests Timeout

If tests timeout waiting for processing:
- Check delist service logs: `docker-compose logs delist`
- Verify ENVIRONMENT=TEST is set
- Ensure delist service is running: `docker-compose ps delist`

### Database Connection Errors

- Verify database is accessible: `docker-compose ps db`
- Check connection string matches your setup
- Use `--db-conn` to override connection string

### API Not Accessible

- Ensure API service is running: `docker-compose up -d api`
- Check port mapping in docker-compose.yml
- Try accessing http://localhost:8000/docs in browser

### Tests Fail Validation

- Use `--no-cleanup` flag to inspect database state after tests
- Check delist service logs for errors
- Verify test case expected results match actual behavior

## Continuous Integration

To run in CI/CD pipeline:

```bash
#!/bin/bash
set -e

# Start services
export ENVIRONMENT=TEST
docker-compose up -d db api delist

# Wait for services to be ready
sleep 10

# Run tests
python main/tests/integration/delist_integration_test.py

# Tests will exit with code 0 if all pass, 1 if any fail
```

## Adding New Test Cases

1. Edit `Delist tests - TestCases1.csv`
2. Add new row with:
   - Test description
   - Coins list
   - Which coins are in futures
   - Expected result
   - curl command (use existing format)
3. Run tests to verify

## Extending Tests

To add custom validations, edit `delist_integration_test.py`:

```python
def validate_test_result(self, test_case: Dict, announcement_id: int) -> bool:
    # Add custom validation logic here
    # Return True if validation passes, False otherwise
    pass
```

## Performance

- Each test takes ~2-3 minutes (waiting for processing)
- Total runtime depends on number of test cases
- 5 test cases = ~10-15 minutes
- 15 test cases = ~30-45 minutes

## Best Practices

1. **Run tests before deploying** to production
2. **Add test case for every bug fix** to prevent regression
3. **Keep test data realistic** (use actual coin symbols)
4. **Review logs** when tests fail, not just database
5. **Run with cleanup** in CI, without cleanup for debugging
