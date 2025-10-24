# 🐳 Docker-Based Integration Tests - UPDATED!

## ✅ Problem Solved!

You're now running tests **inside Docker containers** instead of on the host server. This means:

- ✅ **No dependencies on server** - All Python packages in container
- ✅ **Consistent environment** - Same everywhere (local, AWS, CI/CD)
- ✅ **Isolated** - Won't pollute server with installations
- ✅ **Portable** - Works on any machine with Docker
- ✅ **Matches production** - Same environment as other services

---

## 🚀 How to Use (Updated)

### ⚡ Option 1: Run All Tests (Easiest)

```bash
./main/tests/integration/run_tests.sh
```

**What it does:**
1. Starts all Docker services (db, api, delist, etc.)
2. Runs tests **inside a Docker container**
3. Shows results
4. Cleanup

**No Python installation needed on host!** 🎉

### 🔧 Option 2: Manual Single Test

```bash
# Create a test announcement
./main/tests/integration/run_single_test.sh \
  "Binance Will Delist BTC, ETH on 2025-12-31" \
  2025-12-31 BTC ETH

# Watch it being processed
docker-compose logs -f delist
```

### 🎛️ Option 3: Direct Docker Compose

```bash
# Start services
export ENVIRONMENT=TEST
docker-compose up -d db api delist

# Run tests in container
docker-compose run --rm integration_test

# With arguments
docker-compose run --rm integration_test \
  python main/tests/integration/delist_integration_test.py --no-cleanup

# Manual test
docker-compose run --rm integration_test \
  python main/tests/integration/quick_test.py list
```

---

## 📦 Docker Compose Service

A new `integration_test` service was added to `docker-compose.yml`:

```yaml
integration_test:
  build: .
  container_name: noshirt_integration_test
  volumes:
    - .:/noshirt
  environment:
    - PYTHONPATH=/noshirt/main
    - POSTGRES_DB=noshirt
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
    - POSTGRES_HOST=db              # Connects to db service
    - API_BASE_URL=http://api:80    # Connects to api service
    - ENVIRONMENT=TEST
  command: python main/tests/integration/delist_integration_test.py
  depends_on:
    - db
    - api
    - delist
  profiles:
    - test  # Only runs when explicitly called
```

**Key points:**
- `POSTGRES_HOST=db` - Connects to database service
- `API_BASE_URL=http://api:80` - Connects to API service
- `profiles: [test]` - Won't start with `docker-compose up` (only when explicitly run)
- All dependencies installed in container (from `requirements.txt`)

---

## 🔄 What Changed

### 1. Test Runner (`run_tests.sh`)

**Before:**
```bash
python3 main/tests/integration/delist_integration_test.py "$@"
```

**After:**
```bash
docker-compose run --rm integration_test \
  python main/tests/integration/delist_integration_test.py "$@"
```

### 2. Test Script (`delist_integration_test.py`)

**Before:**
```python
BASE_URL = "http://localhost:8000"
DB_CONNECTION_STRING = "host=localhost port=5432 ..."
```

**After:**
```python
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# ... reads from environment variables
```

### 3. Quick Test Helper (`quick_test.py`)

**Before:**
```python
BASE_URL = "http://localhost:8000"
```

**After:**
```python
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

---

## 🎯 Usage Examples

### Run All Tests

```bash
# On AWS server or locally
./main/tests/integration/run_tests.sh

# With options
./main/tests/integration/run_tests.sh --no-cleanup
./main/tests/integration/run_tests.sh --csv custom_tests.csv
```

### Create Single Test Announcement

```bash
# Easy way
./main/tests/integration/run_single_test.sh \
  "Binance Will Delist SOL on 2025-12-31" \
  2025-12-31 SOL

# Or using Docker directly
docker-compose run --rm integration_test \
  python main/tests/integration/quick_test.py create \
  "Binance Will Delist SOL on 2025-12-31" \
  2025-12-31 SOL
```

### List Test Announcements

```bash
docker-compose run --rm integration_test \
  python main/tests/integration/quick_test.py list
```

### Cleanup Test Data

```bash
docker-compose run --rm integration_test \
  python main/tests/integration/quick_test.py cleanup
```

### Debug Mode (No Cleanup)

```bash
./main/tests/integration/run_tests.sh --no-cleanup

# Then inspect database
docker exec -it noshirt-postgres psql -U postgres -d noshirt
SELECT * FROM test_delist_announcement;
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           AWS Server (or Local)             │
│  ┌────────────────────────────────────────┐ │
│  │         Docker Network                 │ │
│  │                                        │ │
│  │  ┌──────────┐  ┌──────────┐         │ │
│  │  │    db    │  │   api    │         │ │
│  │  │ postgres │  │  :80     │         │ │
│  │  └─────▲────┘  └─────▲────┘         │ │
│  │        │             │                │ │
│  │        │             │                │ │
│  │  ┌─────┴─────────────┴─────┐        │ │
│  │  │   integration_test      │        │ │
│  │  │  - Runs Python tests    │        │ │
│  │  │  - Has all dependencies │        │ │
│  │  │  - Connects to db & api │        │ │
│  │  └─────────────────────────┘        │ │
│  │                                        │ │
│  │  ┌──────────┐                        │ │
│  │  │  delist  │  ← Tested service     │ │
│  │  └──────────┘                        │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**All communication happens inside Docker network!**
- No need for exposed ports (except for debugging)
- Services connect by service name (e.g., `http://api:80`)
- Fast, isolated, secure

---

## 🐛 Troubleshooting

### Cannot Connect to Database

**Problem:** `psycopg.OperationalError: could not connect to server`

**Solution:**
```bash
# Check database is running
docker-compose ps db

# Test connection inside container
docker-compose run --rm integration_test \
  python -c "import psycopg; psycopg.connect('host=db dbname=noshirt user=postgres password=postgres')"
```

### Cannot Reach API

**Problem:** `requests.exceptions.ConnectionError`

**Solution:**
```bash
# Check API is running
docker-compose ps api

# Test from inside container
docker-compose run --rm integration_test \
  curl http://api:80/docs
```

### Tests Still Try localhost

**Problem:** Tests connect to `localhost` instead of Docker services

**Solution:** Ensure environment variables are set:
```bash
docker-compose run --rm \
  -e API_BASE_URL=http://api:80 \
  -e POSTGRES_HOST=db \
  integration_test
```

### Profile Warning

**Problem:** `service "integration_test" is not targeted by any profile`

**Solution:** This is normal! The service only runs when explicitly called with `docker-compose run`.

---

## 📊 Benefits of Docker Approach

| Aspect | Before (Host) | After (Docker) |
|--------|--------------|----------------|
| **Setup** | Install Python, pip, psycopg, requests | Just Docker |
| **Dependencies** | Manual install on each server | Auto from requirements.txt |
| **Consistency** | May differ per environment | Identical everywhere |
| **Isolation** | Pollutes host | Isolated in container |
| **Portability** | OS-specific | Works anywhere |
| **Maintenance** | Update each server | Update Dockerfile once |
| **CI/CD** | Complex setup | Simple, consistent |

---

## 🎓 Best Practices

### 1. Always Use Docker for Tests on Server

```bash
# ✅ Good (Docker)
./main/tests/integration/run_tests.sh

# ❌ Bad (Host)
python3 main/tests/integration/delist_integration_test.py
```

### 2. Use Service Names in Docker Network

```python
# ✅ Good (inside Docker)
API_BASE_URL = "http://api:80"
POSTGRES_HOST = "db"

# ❌ Bad (breaks in Docker)
API_BASE_URL = "http://localhost:8000"
POSTGRES_HOST = "localhost"
```

### 3. Keep Containers Lightweight

```bash
# ✅ Good (remove after run)
docker-compose run --rm integration_test

# ❌ Bad (leaves container)
docker-compose run integration_test
```

### 4. Use Profiles for Test Services

```yaml
# ✅ Good (won't start by default)
profiles:
  - test

# ❌ Bad (always starts)
# (no profiles)
```

---

## 🚀 Quick Command Reference

```bash
# Run all tests
./main/tests/integration/run_tests.sh

# Run with options
./main/tests/integration/run_tests.sh --no-cleanup

# Single test announcement
./main/tests/integration/run_single_test.sh "Title" 2025-12-31 BTC ETH

# List announcements
docker-compose run --rm integration_test \
  python main/tests/integration/quick_test.py list

# Cleanup
docker-compose run --rm integration_test \
  python main/tests/integration/quick_test.py cleanup

# Watch delist logs
docker-compose logs -f delist

# Check database
docker exec -it noshirt-postgres psql -U postgres -d noshirt

# View test container logs
docker-compose logs integration_test
```

---

## ✨ Summary

**You now have a Docker-based integration test framework that:**

1. ✅ **Runs in containers** - No host dependencies
2. ✅ **Uses Docker network** - Services connect by name
3. ✅ **Reads from environment** - Flexible configuration
4. ✅ **Works everywhere** - Local, AWS, CI/CD
5. ✅ **Easy to maintain** - Update Dockerfile, done
6. ✅ **Isolated** - Won't pollute server
7. ✅ **Consistent** - Same environment everywhere

**Just run:**
```bash
./main/tests/integration/run_tests.sh
```

**On AWS, local, or anywhere with Docker!** 🐳🎉

---

## 📚 Related Files

- `docker-compose.yml` - Service definition
- `run_tests.sh` - Main test runner
- `run_single_test.sh` - Single test helper
- `delist_integration_test.py` - Test framework
- `quick_test.py` - Manual test helper

All updated to work in Docker! ✅
