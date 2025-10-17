# Delist Integration Test Framework - Complete Guide

## 🎯 Overview

A comprehensive end-to-end integration test framework for the delist service that:
- ✅ Tests against real Docker services in TEST mode
- ✅ Validates complete workflow from announcement to position simulation
- ✅ Driven by CSV test cases for easy maintenance
- ✅ Automatic cleanup after tests
- ✅ Detailed colored console output
- ✅ CI/CD ready with GitHub Actions
- ✅ Supports debugging mode (skip cleanup)

## 📁 Files Created

```
main/tests/integration/
├── delist_integration_test.py    # Main test runner
├── run_tests.sh                   # Quick start script
├── README.md                      # Detailed documentation
└── resources/
    └── delist_test_cases.csv      # Test cases (improved version)

.github/workflows/
└── delist_integration_tests.yml   # CI/CD workflow
```

## 🚀 Quick Start

### Option 1: Using the Shell Script (Recommended)

```bash
# Make script executable (already done)
chmod +x main/tests/integration/run_tests.sh

# Run all tests
./main/tests/integration/run_tests.sh

# Run with custom CSV
./main/tests/integration/run_tests.sh --csv path/to/tests.csv

# Skip cleanup for debugging
./main/tests/integration/run_tests.sh --no-cleanup
```

### Option 2: Manual Steps

```bash
# 1. Start Docker services in TEST mode
export ENVIRONMENT=TEST
docker-compose up -d db api delist telegram update_account_balances

# 2. Wait for services
sleep 15

# 3. Run tests
python main/tests/integration/delist_integration_test.py
```

## 📋 Test Cases

### Included Test Scenarios

The improved test cases (`delist_test_cases.csv`) cover:

1. **✅ Valid Delist with Partial Futures**
   - Mix of futures and spot coins
   - Only futures coins should be processed

2. **✅ Title Validation**
   - "Binance Will Delist" → Process
   - "Binance Will NOT Delist" → Skip
   - Lowercase "binance will delist" → Process (case insensitive)
   - Wrong format → Skip

3. **✅ Coin Types**
   - All coins in futures → Process all
   - No coins in futures → Process but skip all
   - Single coin → Process single

4. **✅ Date Extraction**
   - Extract date from title format "on YYYY-MM-DD"
   - Fall back to stored date if extraction fails

### Test Case Format

```csv
TEST CASE,COINS,COINS IN FUTURES,BINANCE BALANCE,REAL TRADE,Expected Result,TEST OK,API POST CALL
"Description","COIN1, COIN2","FUTURE1, FUTURE2",$0.00,No,Expected behavior,,curl command
```

## 🔍 What Gets Validated

For each test case, the framework validates:

1. **Announcement Processing**
   - ✅ Created in `test_delist_announcement` table
   - ✅ Marked as `processed = true` after delist service processes it

2. **Title Validation**
   - ✅ "Binance Will Delist" triggers processing
   - ✅ "NOT Delist" is skipped
   - ✅ Case insensitive matching

3. **Coin Filtering**
   - ✅ Only futures-available coins inserted into `delist_announcement`
   - ✅ Spot-only coins are skipped
   - ✅ Correct pairs built (e.g., "FORTH" → "FORTHUSDT")

4. **TEST Mode Behavior**
   - ✅ No real trade records created (when REAL TRADE = No)
   - ✅ Simulated positions logged with details
   - ✅ Orderbook data fetched and logged

5. **Database State**
   - ✅ Correct entries in `delist_announcement`
   - ✅ No duplicate announcements
   - ✅ Proper cleanup after tests

## 📊 Test Output

### Console Output

```
[2025-10-17 10:00:00] [HEADER] ================================================================================
[2025-10-17 10:00:00] [HEADER] TEST 1/10: Title: 'Binance Will Delist' | 3 coins | 1 in futures
[2025-10-17 10:00:00] [HEADER] ================================================================================
[2025-10-17 10:00:01] [INFO] Coins: EPX, FORTH, KEY
[2025-10-17 10:00:01] [INFO] Coins in Futures: FORTH
[2025-10-17 10:00:01] [INFO] Expected Result: Open simulated position only for FORTH
[2025-10-17 10:00:02] [SUCCESS] Created test announcement ID: 123
[2025-10-17 10:00:02] [INFO] Waiting for announcement 123 to be processed...
[2025-10-17 10:01:30] [SUCCESS] Announcement processed in 88.2 seconds
[2025-10-17 10:01:30] [INFO] Validating test results...
[2025-10-17 10:01:31] [INFO] Coins inserted into delist_announcement: ['FORTH']
[2025-10-17 10:01:31] [SUCCESS] Correctly simulated trades without creating records (TEST mode)
[2025-10-17 10:01:31] [SUCCESS] Test validation PASSED
```

### Summary Report

```
================================================================================
TEST SUMMARY
================================================================================
[PASSED] Title: 'Binance Will Delist' | 3 coins | 1 in futures
[PASSED] Title: 'Binance Will Delist' | 4 coins | 2 in futures
[PASSED] Title: 'Binance Will Delist' | 4 coins | 0 in futures (spot only)
[PASSED] Title: 'Binance Will NOT Delist' | 3 coins | 2 in futures
[FAILED] Title: lowercase 'binance will delist' | 3 coins | 2 in futures
  → Test validation failed
================================================================================
Total: 10 | Passed: 9 | Failed: 1
1 TEST(S) FAILED ❌
================================================================================
```

## 🛠️ Configuration

### Environment Variables

Set in `.env` or `docker-compose.yml`:

```bash
ENVIRONMENT=TEST              # Must be TEST for integration tests
POSTGRES_HOST=db             # Database host
POSTGRES_DB=noshirt          # Database name
POSTGRES_USER=postgres       # Database user
POSTGRES_PASSWORD=postgres   # Database password
```

### Test Configuration

Edit `delist_integration_test.py` to adjust:

```python
BASE_URL = "http://localhost:8000"       # API endpoint
DB_CONNECTION_STRING = "host=localhost..." # Database connection
TEST_DELAY_SECONDS = 120                 # Wait between tests (2 min)
MAX_WAIT_SECONDS = 180                   # Max wait for processing (3 min)
```

## 🔧 Troubleshooting

### Tests Timeout

**Problem**: Tests wait forever for announcement processing

**Solution**:
```bash
# Check delist service is running
docker-compose ps delist

# Check delist logs
docker-compose logs -f delist

# Verify ENVIRONMENT=TEST is set
docker-compose exec delist env | grep ENVIRONMENT
```

### Database Connection Failed

**Problem**: Cannot connect to database

**Solution**:
```bash
# Check database is running
docker-compose ps db

# Test connection manually
docker exec -it noshirt-postgres psql -U postgres -d noshirt

# Verify port mapping
docker-compose port db 5432
```

### API Not Accessible

**Problem**: Cannot reach API at http://localhost:8000

**Solution**:
```bash
# Check API is running
docker-compose ps api

# Check API logs
docker-compose logs api

# Test API manually
curl http://localhost:8000/docs

# If on remote server, use server IP instead of localhost
python main/tests/integration/delist_integration_test.py --base-url http://16.171.16.170:8000
```

### Tests Fail Validation

**Problem**: Tests run but validation fails

**Solution**:
```bash
# Run with no cleanup to inspect database
./main/tests/integration/run_tests.sh --no-cleanup

# Check database manually
docker exec -it noshirt-postgres psql -U postgres -d noshirt
SELECT * FROM test_delist_announcement;
SELECT * FROM delist_announcement;

# Check delist service logs for errors
docker-compose logs delist | grep ERROR
```

## 📈 Adding New Test Cases

### 1. Add to CSV File

Edit `main/tests/resources/delist_test_cases.csv`:

```csv
"Your test description","COIN1, COIN2","FUTURE1",$0.00,No,Expected result,,curl -X POST http://localhost:8000/test-announcements -H "Content-Type: application/json" -d '{"title": "Binance Will Delist COIN1, COIN2 on 2025-12-31", "announcement_date": "2025-12-31", "coins": ["COIN1", "COIN2"]}'
```

### 2. Run Tests

```bash
./main/tests/integration/run_tests.sh
```

### 3. Verify New Test Runs

Check console output for your new test case.

## 🤖 CI/CD Integration

### GitHub Actions

The workflow file `.github/workflows/delist_integration_tests.yml` runs tests automatically on:
- Push to `main` or `peretto/main/delist` branches
- Pull requests to `main`
- Manual trigger via GitHub UI

### Viewing Results

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Delist Integration Tests"
4. View test results and logs

### Running Manually on GitHub

1. Go to Actions tab
2. Select "Delist Integration Tests"
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow" button

## 🎓 Best Practices

### 1. Run Tests Before Deploying

```bash
# Before pushing to production
./main/tests/integration/run_tests.sh

# If all tests pass, safe to deploy
docker-compose -f docker-compose.prod.yml up -d delist
```

### 2. Add Test for Every Bug Fix

When fixing a bug:
1. Add test case that would catch the bug
2. Run tests (should fail)
3. Fix the bug
4. Run tests again (should pass)
5. Commit both fix and test

### 3. Keep Test Data Realistic

Use actual coin symbols from Binance, not fake ones. This ensures tests mirror production behavior.

### 4. Review Logs on Failure

Don't just look at test pass/fail. Check delist service logs to understand what happened:

```bash
docker-compose logs delist | tail -n 100
```

### 5. Use Debug Mode During Development

```bash
# Skip cleanup to inspect database after tests
./main/tests/integration/run_tests.sh --no-cleanup

# Then inspect manually
docker exec -it noshirt-postgres psql -U postgres -d noshirt
SELECT * FROM test_delist_announcement;
```

## 📝 Example Test Session

```bash
$ ./main/tests/integration/run_tests.sh

==========================================
Delist Integration Test - Quick Start
==========================================
Starting required Docker services...
[+] Running 5/5
 ✔ Container noshirt-postgres                   Running
 ✔ Container noshirt_api                        Running
 ✔ Container noshirt_delist                     Running
 ✔ Container noshirt_telegram                   Running
 ✔ Container noshirt_update_account_balances    Running

Waiting for services to be ready (15 seconds)...
Checking service status...
NAME                                 STATUS              PORTS
noshirt-postgres                     Up 2 minutes        0.0.0.0:5432->5432/tcp
noshirt_api                          Up 2 minutes        0.0.0.0:8000->80/tcp
noshirt_delist                       Up 2 minutes        
noshirt_telegram                     Up 2 minutes        
noshirt_update_account_balances      Up 2 minutes        

Checking API health...
✓ API is accessible
Checking delist service...
✓ Delist service is running

==========================================
Running Integration Tests
==========================================

[2025-10-17 10:00:00] [HEADER] ================================================================================
[2025-10-17 10:00:00] [HEADER] DELIST INTEGRATION TEST SUITE
[2025-10-17 10:00:00] [HEADER] ================================================================================
[2025-10-17 10:00:00] [INFO] Loading test cases from main/tests/resources/delist_test_cases.csv
[2025-10-17 10:00:00] [SUCCESS] Loaded 10 test cases
[2025-10-17 10:00:00] [INFO] Checking if services are accessible...
[2025-10-17 10:00:01] [SUCCESS] API service is accessible

... (tests run) ...

[2025-10-17 10:25:00] [INFO] Starting cleanup...
[2025-10-17 10:25:01] [SUCCESS] Cleanup completed successfully

[2025-10-17 10:25:01] [HEADER] ================================================================================
[2025-10-17 10:25:01] [HEADER] TEST SUMMARY
[2025-10-17 10:25:01] [HEADER] ================================================================================
[PASSED] Title: 'Binance Will Delist' | 3 coins | 1 in futures
[PASSED] Title: 'Binance Will Delist' | 4 coins | 2 in futures
... (all results) ...
[2025-10-17 10:25:01] [HEADER] ================================================================================
[2025-10-17 10:25:01] [HEADER] Total: 10 | Passed: 10 | Failed: 0
[2025-10-17 10:25:01] [SUCCESS] ALL TESTS PASSED! ✅
==========================================
All tests PASSED! ✅
==========================================
```

## 🎯 Summary

You now have a complete integration test framework that:

1. ✅ **Runs automatically** - Just execute one command
2. ✅ **Tests real behavior** - Against actual Docker services
3. ✅ **Easy to maintain** - CSV-driven test cases
4. ✅ **Good for CI/CD** - GitHub Actions ready
5. ✅ **Comprehensive** - Tests all critical scenarios
6. ✅ **Easy to debug** - Colored output, detailed logs, skip cleanup option
7. ✅ **Clean** - Automatic cleanup after tests
8. ✅ **Extensible** - Easy to add new test cases

**Next Steps:**
1. Run tests locally: `./main/tests/integration/run_tests.sh`
2. Add your specific test cases to the CSV
3. Push to GitHub to see CI/CD in action
4. Make it part of your deployment process

Happy testing! 🚀
