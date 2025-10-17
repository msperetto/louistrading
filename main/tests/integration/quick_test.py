#!/usr/bin/env python3
"""
Quick test helper - Run a single announcement to test manually
"""
import requests
import sys
import json
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def create_announcement(title, date, coins):
    """Create a test announcement"""
    data = {
        "title": title,
        "announcement_date": date,
        "coins": coins
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/test-announcements",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        print(f"✅ Created announcement ID: {result['id']}")
        print(f"Title: {title}")
        print(f"Coins: {', '.join(coins)}")
        print(f"\nNow check delist logs:")
        print(f"  docker-compose logs -f delist")
        return result['id']
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

def list_announcements():
    """List all test announcements"""
    try:
        response = requests.get(f"{BASE_URL}/test-announcements", timeout=10)
        response.raise_for_status()
        announcements = response.json()
        
        if not announcements:
            print("No test announcements found")
            return
        
        print(f"\n{'ID':<5} {'Processed':<10} {'Coins':<30} {'Title'}")
        print("-" * 100)
        for ann in announcements:
            processed = "✅ Yes" if ann['processed'] else "❌ No"
            coins = ", ".join(ann['coins'])
            print(f"{ann['id']:<5} {processed:<10} {coins:<30} {ann['title'][:40]}")
    except Exception as e:
        print(f"❌ Failed: {e}")

def delete_announcement(ann_id):
    """Delete a test announcement"""
    try:
        response = requests.delete(
            f"{BASE_URL}/test-announcements/{ann_id}",
            timeout=10
        )
        response.raise_for_status()
        print(f"✅ Deleted announcement {ann_id}")
    except Exception as e:
        print(f"❌ Failed: {e}")

def cleanup_all():
    """Delete all test announcements"""
    try:
        response = requests.get(f"{BASE_URL}/test-announcements", timeout=10)
        response.raise_for_status()
        announcements = response.json()
        
        for ann in announcements:
            delete_announcement(ann['id'])
        
        print(f"✅ Cleaned up {len(announcements)} announcements")
    except Exception as e:
        print(f"❌ Failed: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create announcement:")
        print("    python quick_test.py create 'Binance Will Delist BTC, ETH on 2025-12-31' 2025-12-31 BTC ETH")
        print("  List all:")
        print("    python quick_test.py list")
        print("  Delete one:")
        print("    python quick_test.py delete <id>")
        print("  Cleanup all:")
        print("    python quick_test.py cleanup")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 5:
            print("Usage: python quick_test.py create 'Title' YYYY-MM-DD COIN1 COIN2 ...")
            sys.exit(1)
        title = sys.argv[2]
        date = sys.argv[3]
        coins = sys.argv[4:]
        create_announcement(title, date, coins)
    
    elif command == "list":
        list_announcements()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python quick_test.py delete <id>")
            sys.exit(1)
        ann_id = int(sys.argv[2])
        delete_announcement(ann_id)
    
    elif command == "cleanup":
        cleanup_all()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
