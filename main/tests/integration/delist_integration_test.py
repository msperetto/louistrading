"""
Integration Test for Delist Service
=====================================
Runs end-to-end tests against real Docker services in TEST mode.
Tests are driven by CSV file with test cases.

Prerequisites:
- Docker services running: db, api, delist, telegram, update_account_balances
- ENVIRONMENT=TEST in docker-compose or .env
- API accessible at http://localhost:8000 (or configured BASE_URL)

Usage:
    python main/tests/integration/delist_integration_test.py
    
    # With custom test cases file:
    python main/tests/integration/delist_integration_test.py --csv path/to/tests.csv
    
    # Skip cleanup (for debugging):
    python main/tests/integration/delist_integration_test.py --no-cleanup
"""

import requests
import time
import csv
import argparse
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional
import psycopg
from pathlib import Path

# Test configuration
import os

# Get configuration from environment variables (Docker-friendly)
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")  # API endpoint
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "noshirt")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

DB_CONNECTION_STRING = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"

TEST_DELAY_SECONDS = 120  # 2 minutes between tests
DELIST_CHECK_INTERVAL = 10  # Check delist logs every 10 seconds
MAX_WAIT_SECONDS = 180  # Max 3 minutes to wait for delist to process

# Color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DelistIntegrationTest:
    def __init__(self, csv_file: str, base_url: str, db_conn: str, cleanup: bool = True):
        self.csv_file = csv_file
        self.base_url = base_url
        self.db_conn = db_conn
        self.cleanup = cleanup
        self.test_results = []
        self.test_announcement_ids = []
        
    def log(self, message: str, level: str = "INFO"):
        """Print colored log messages"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if level == "ERROR":
            color = Colors.FAIL
        elif level == "SUCCESS":
            color = Colors.OKGREEN
        elif level == "WARNING":
            color = Colors.WARNING
        elif level == "HEADER":
            color = Colors.HEADER + Colors.BOLD
        else:
            color = Colors.OKBLUE
            
        print(f"{color}[{timestamp}] [{level}] {message}{Colors.ENDC}")
    
    def load_test_cases(self) -> List[Dict[str, Any]]:
        """Load test cases from CSV file"""
        self.log(f"Loading test cases from {self.csv_file}", "INFO")
        test_cases = []
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows or rows without API POST CALL
                if not row.get('API POST CALL') or not row['API POST CALL'].strip():
                    continue
                    
                test_cases.append({
                    'test_case': row.get('TEST CASE', ''),
                    'coins': row.get('COINS', ''),
                    'coins_in_futures': row.get('COINS IN FUTURES', ''),
                    'binance_balance': row.get('BINANCE BALANCE', '$0.00'),
                    'real_trade': row.get('REAL TRADE', 'No'),
                    'expected_result': row.get('Expected Result', ''),
                    'curl_command': row.get('API POST CALL', '')
                })
        
        self.log(f"Loaded {len(test_cases)} test cases", "SUCCESS")
        return test_cases
    
    def extract_curl_data(self, curl_command: str) -> Optional[Dict[str, Any]]:
        """Extract JSON data from curl command"""
        try:
            # Find the JSON part in the curl command
            import re
            json_match = re.search(r"'{([^}]+)}'", curl_command)
            if not json_match:
                return None
            
            json_str = '{' + json_match.group(1) + '}'
            # Parse the JSON
            import json
            # Clean up the JSON string
            json_str = json_str.replace('\n', '').replace('    ', '')
            data = json.loads(json_str)
            
            # Ensure notes field exists (API expects it, even if None)
            if 'notes' not in data:
                data['notes'] = None
            
            return data
        except Exception as e:
            self.log(f"Failed to extract curl data: {e}", "ERROR")
            return None
    
    def create_test_announcement(self, data: Dict[str, Any]) -> Optional[int]:
        """Create a test announcement via API"""
        try:
            self.log(f"Sending POST to {self.base_url}/test-announcements", "INFO")
            self.log(f"Data: {data}", "INFO")
            
            response = requests.post(
                f"{self.base_url}/test-announcements",
                json=data,
                timeout=10
            )
            
            # Log response details
            self.log(f"Response status: {response.status_code}", "INFO")
            self.log(f"Response body: {response.text}", "INFO")
            
            response.raise_for_status()
            result = response.json()
            
            # Check if request was successful
            if result.get('status') == 'error':
                self.log(f"API returned error: {result.get('message')}", "ERROR")
                return None
            
            # API returns 'announcement_id', not 'id'
            announcement_id = result.get('announcement_id') or result.get('id')
            
            if announcement_id:
                self.test_announcement_ids.append(announcement_id)
                self.log(f"Created test announcement ID: {announcement_id}", "SUCCESS")
                return announcement_id
            else:
                self.log(f"No 'announcement_id' in response: {result}", "ERROR")
                return None
                
        except requests.exceptions.HTTPError as e:
            self.log(f"HTTP error creating announcement: {e}", "ERROR")
            self.log(f"Response: {response.text if 'response' in locals() else 'N/A'}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Failed to create announcement: {e}", "ERROR")
            return None
    
    def get_test_announcement(self, announcement_id: int) -> Optional[Dict]:
        """Get test announcement from database"""
        try:
            with psycopg.connect(self.db_conn) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, title, announcement_date, coins, processed, created_at
                        FROM test_delist_announcement
                        WHERE id = %s;
                    """, (announcement_id,))
                    row = cur.fetchone()
                    if row:
                        return {
                            'id': row[0],
                            'title': row[1],
                            'announcement_date': row[2],
                            'coins': row[3],
                            'processed': row[4],
                            'created_at': row[5]
                        }
        except Exception as e:
            self.log(f"Failed to get announcement: {e}", "ERROR")
        return None
    
    def check_delist_announcements_inserted(self, coins: List[str]) -> List[str]:
        """Check which coins were inserted into delist_announcement table"""
        try:
            with psycopg.connect(self.db_conn) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT coin FROM delist_announcement
                        WHERE coin = ANY(%s);
                    """, (coins,))
                    results = cur.fetchall()
                    return [row[0] for row in results]
        except Exception as e:
            self.log(f"Failed to check delist announcements: {e}", "ERROR")
        return []
    
    def check_trades_opened(self, coins: List[str]) -> List[Dict]:
        """Check if trades were opened for coins"""
        try:
            pairs = [f"{coin}USDT" for coin in coins]
            with psycopg.connect(self.db_conn) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT t.id, t.pair, t.open_time, t.side, t.strategy_id,
                               oc.entry_price, oc.quantity
                        FROM trade t
                        LEFT JOIN order_control oc ON oc.trade_id = t.id
                        WHERE t.pair = ANY(%s) AND t.open = true
                        ORDER BY t.open_time DESC;
                    """, (pairs,))
                    results = cur.fetchall()
                    return [{
                        'id': row[0],
                        'pair': row[1],
                        'open_time': row[2],
                        'side': row[3],
                        'strategy_id': row[4],
                        'entry_price': row[5],
                        'entry_quantity': row[6]
                    } for row in results]
        except Exception as e:
            self.log(f"Failed to check trades: {e}", "ERROR")
        return []
    
    def wait_for_processing(self, announcement_id: int, max_wait: int = MAX_WAIT_SECONDS) -> bool:
        """Wait for announcement to be processed"""
        self.log(f"Waiting for announcement {announcement_id} to be processed...", "INFO")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            announcement = self.get_test_announcement(announcement_id)
            if announcement and announcement['processed']:
                elapsed = time.time() - start_time
                self.log(f"Announcement processed in {elapsed:.1f} seconds", "SUCCESS")
                return True
            
            time.sleep(DELIST_CHECK_INTERVAL)
        
        self.log(f"Timeout waiting for announcement processing", "WARNING")
        return False
    
    def validate_test_result(self, test_case: Dict, announcement_id: int) -> bool:
        """Validate test results against expected outcomes"""
        self.log("Validating test results...", "INFO")
        
        # Parse expected result
        expected = test_case['expected_result'].lower()
        coins_list = [c.strip() for c in test_case['coins'].split(',')]
        coins_in_futures = [c.strip() for c in test_case['coins_in_futures'].split(',') if c.strip()]
        
        # Check if announcement was processed
        announcement = self.get_test_announcement(announcement_id)
        if not announcement:
            self.log("Announcement not found in database", "ERROR")
            return False
        
        if not announcement['processed']:
            self.log("Announcement not processed", "ERROR")
            return False
        
        # Check title validation
        title = announcement['title']
        should_process = "binance will delist" in title.lower()
        
        if not should_process and "not delist" in title.lower():
            self.log("Correctly ignored announcement with 'NOT Delist'", "SUCCESS")
            # Should not have inserted delist announcements
            inserted_coins = self.check_delist_announcements_inserted(coins_list)
            if inserted_coins:
                self.log(f"ERROR: Coins inserted when they shouldn't be: {inserted_coins}", "ERROR")
                return False
            return True
        
        if not should_process:
            self.log(f"Title validation issue: '{title}'", "WARNING")
        
        # Check which coins were inserted into delist_announcement
        inserted_coins = self.check_delist_announcements_inserted(coins_list)
        self.log(f"Coins inserted into delist_announcement: {inserted_coins}", "INFO")
        
        # Should only insert coins that are in futures
        expected_inserted = [c for c in coins_list if c in coins_in_futures]
        
        if sorted(inserted_coins) != sorted(expected_inserted):
            self.log(f"Mismatch: Expected {expected_inserted}, got {inserted_coins}", "ERROR")
            return False
        
        # Check if in TEST mode (no real trades)
        if test_case['real_trade'].lower() == 'no':
            # In TEST mode, should not create actual trade records
            trades = self.check_trades_opened(coins_in_futures)
            if trades:
                self.log(f"ERROR: Real trades found in TEST mode: {trades}", "ERROR")
                return False
            else:
                self.log("Correctly simulated trades without creating records (TEST mode)", "SUCCESS")
        
        # All validations passed
        self.log("Test validation PASSED", "SUCCESS")
        return True
    
    def cleanup_test_data(self):
        """Clean up test data from database"""
        self.log("Starting cleanup...", "INFO")
        
        try:
            with psycopg.connect(self.db_conn) as conn:
                with conn.cursor() as cur:
                    # Delete test announcements
                    if self.test_announcement_ids:
                        cur.execute("""
                            DELETE FROM test_delist_announcement
                            WHERE id = ANY(%s);
                        """, (self.test_announcement_ids,))
                        self.log(f"Deleted {len(self.test_announcement_ids)} test announcements", "INFO")
                    
                    # Delete delist announcements created during tests
                    cur.execute("""
                        DELETE FROM delist_announcement
                        WHERE announcement_date >= CURRENT_DATE;
                    """)
                    
                    # Delete any test trades (if created)
                    cur.execute("""
                        DELETE FROM trade
                        WHERE created_at >= CURRENT_DATE;
                    """)
                    
                    conn.commit()
                    self.log("Cleanup completed successfully", "SUCCESS")
        except Exception as e:
            self.log(f"Cleanup failed: {e}", "ERROR")
    
    def run_test_case(self, test_case: Dict, test_num: int, total_tests: int) -> bool:
        """Run a single test case"""
        self.log("=" * 80, "HEADER")
        self.log(f"TEST {test_num}/{total_tests}: {test_case['test_case']}", "HEADER")
        self.log("=" * 80, "HEADER")
        
        self.log(f"Coins: {test_case['coins']}", "INFO")
        self.log(f"Coins in Futures: {test_case['coins_in_futures']}", "INFO")
        self.log(f"Expected Result: {test_case['expected_result']}", "INFO")
        
        # Extract data from curl command
        data = self.extract_curl_data(test_case['curl_command'])
        if not data:
            self.log("Failed to extract announcement data from curl command", "ERROR")
            return False
        
        # Create test announcement
        announcement_id = self.create_test_announcement(data)
        if not announcement_id:
            self.log("Failed to create test announcement", "ERROR")
            return False
        
        # Wait for delist service to process
        processed = self.wait_for_processing(announcement_id)
        if not processed:
            self.log("Announcement was not processed in time", "WARNING")
            # Continue with validation anyway
        
        # Validate results
        success = self.validate_test_result(test_case, announcement_id)
        
        return success
    
    def run_all_tests(self):
        """Run all test cases"""
        self.log("=" * 80, "HEADER")
        self.log("DELIST INTEGRATION TEST SUITE", "HEADER")
        self.log("=" * 80, "HEADER")
        
        # Load test cases
        test_cases = self.load_test_cases()
        if not test_cases:
            self.log("No test cases found", "ERROR")
            return False
        
        # Check services are running
        self.log("Checking if services are accessible...", "INFO")
        
        # Retry API connection up to 5 times (services may still be starting)
        max_retries = 5
        retry_delay = 5
        
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(f"{self.base_url}/docs", timeout=10)
                self.log("API service is accessible", "SUCCESS")
                break
            except Exception as e:
                if attempt < max_retries:
                    self.log(f"API not ready yet (attempt {attempt}/{max_retries}), retrying in {retry_delay}s...", "WARNING")
                    time.sleep(retry_delay)
                else:
                    self.log(f"API service not accessible after {max_retries} attempts: {e}", "ERROR")
                    self.log("Please ensure Docker services are running with: docker-compose up -d", "ERROR")
                    return False
        
        # Run each test case
        total_tests = len(test_cases)
        passed = 0
        failed = 0
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                success = self.run_test_case(test_case, i, total_tests)
                
                if success:
                    passed += 1
                    self.test_results.append({
                        'test_case': test_case['test_case'],
                        'status': 'PASSED',
                        'message': 'Test passed successfully'
                    })
                else:
                    failed += 1
                    self.test_results.append({
                        'test_case': test_case['test_case'],
                        'status': 'FAILED',
                        'message': 'Test validation failed'
                    })
                
                # Wait between tests (except for last test)
                if i < total_tests:
                    self.log(f"Waiting {TEST_DELAY_SECONDS} seconds before next test...", "INFO")
                    time.sleep(TEST_DELAY_SECONDS)
                    
            except Exception as e:
                failed += 1
                self.log(f"Test exception: {e}", "ERROR")
                self.test_results.append({
                    'test_case': test_case['test_case'],
                    'status': 'ERROR',
                    'message': str(e)
                })
        
        # Cleanup
        if self.cleanup:
            self.cleanup_test_data()
        else:
            self.log("Skipping cleanup (--no-cleanup flag set)", "WARNING")
        
        # Print summary
        self.print_summary(passed, failed, total_tests)
        
        return failed == 0
    
    def print_summary(self, passed: int, failed: int, total: int):
        """Print test summary"""
        self.log("=" * 80, "HEADER")
        self.log("TEST SUMMARY", "HEADER")
        self.log("=" * 80, "HEADER")
        
        for result in self.test_results:
            status_color = Colors.OKGREEN if result['status'] == 'PASSED' else Colors.FAIL
            print(f"{status_color}[{result['status']}]{Colors.ENDC} {result['test_case']}")
            if result['status'] != 'PASSED':
                print(f"  → {result['message']}")
        
        self.log("=" * 80, "HEADER")
        self.log(f"Total: {total} | Passed: {passed} | Failed: {failed}", "HEADER")
        
        if failed == 0:
            self.log("ALL TESTS PASSED! ✅", "SUCCESS")
        else:
            self.log(f"{failed} TEST(S) FAILED ❌", "ERROR")


def main():
    parser = argparse.ArgumentParser(description='Run Delist Integration Tests')
    parser.add_argument('--csv', default='main/tests/resources/Delist tests - TestCases1.csv',
                        help='Path to test cases CSV file')
    parser.add_argument('--base-url', default=BASE_URL,
                        help='Base URL for API')
    parser.add_argument('--db-conn', default=DB_CONNECTION_STRING,
                        help='Database connection string')
    parser.add_argument('--no-cleanup', action='store_true',
                        help='Skip cleanup after tests (for debugging)')
    
    args = parser.parse_args()
    
    # Run tests
    test_runner = DelistIntegrationTest(
        csv_file=args.csv,
        base_url=args.base_url,
        db_conn=args.db_conn,
        cleanup=not args.no_cleanup
    )
    
    success = test_runner.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
