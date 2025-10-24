#!/usr/bin/env python3
"""
Helper script to create test delist announcements for testing purposes.
Run this script to add fake announcements to the database.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000" 

def create_test_announcement(title, announcement_date, coins, notes=None):
    """Create a test announcement via API"""
    url = f"{API_BASE_URL}/test-announcements"
    data = {
        "title": title,
        "announcement_date": announcement_date,
        "coins": coins,
        "notes": notes
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Created test announcement: {title}")
            print(f"   ID: {result.get('announcement_id')}")
            print(f"   Coins: {coins}")
            print()
        else:
            print(f"❌ Error creating announcement: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")

def main():
    print("Creating test delist announcements...")
    print("=" * 50)
    
    # Example test announcements
    test_announcements = [
        {
            "title": "Binance Will Delist DOGE and SHIB on 2024-02-15",
            "announcement_date": "2024-02-15",
            "coins": ["DOGE", "SHIB"],
            "notes": "Test announcement for popular meme coins"
        },
        {
            "title": "Binance Will Delist BTC and ETH on 2024-02-20",
            "announcement_date": "2024-02-20", 
            "coins": ["BTC", "ETH"],
            "notes": "Test announcement for major cryptocurrencies"
        },
        {
            "title": "Binance Will Delist ADA, DOT, LINK on 2024-02-25",
            "announcement_date": "2024-02-25",
            "coins": ["ADA", "DOT", "LINK"],
            "notes": "Test announcement for altcoins"
        }
    ]
    
    # Create each test announcement
    for announcement in test_announcements:
        create_test_announcement(
            title=announcement["title"],
            announcement_date=announcement["announcement_date"],
            coins=announcement["coins"],
            notes=announcement["notes"]
        )
    
    print("=" * 50)
    print("Test announcements created! You can now:")
    print("1. Set NEGOCIATION_ENV = Environment_Type.TEST in config.py")
    print("2. Set USE_TEST_ANNOUNCEMENTS = True in config.py")
    print("3. Run your delist service to process these test announcements")
    print()
    print("API endpoints available:")
    print(f"- GET {API_BASE_URL}/test-announcements (view all)")
    print(f"- GET {API_BASE_URL}/test-announcements/unprocessed (view unprocessed)")
    print(f"- DELETE {API_BASE_URL}/test-announcements (clear all)")

if __name__ == "__main__":
    main()
