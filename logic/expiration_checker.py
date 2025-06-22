#!/usr/bin/env python3
# /logic/expiration_checker.py

from datetime import datetime
import json
import os

# --- Configuration ---
THRESHOLD_DAYS = 3
TODAY = datetime(2025, 6, 16)  # fixed “today” for consistency

def load_receipt(path):
    """Load a single receipt JSON and return its 'items' list."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('items', [])

def find_soon_to_expire(items):
    """Return list of items expiring within THRESHOLD_DAYS."""
    soon = []
    for item in items:
        exp_str = item.get('expiryDate')
        try:
            exp = datetime.fromisoformat(exp_str.replace('Z',''))
        except Exception:
            continue  # skip invalid dates
        days_left = (exp - TODAY).days
        if 0 <= days_left <= THRESHOLD_DAYS:
            soon.append({
                'id': item['id'],
                'name': item['name'],
                'daysLeft': days_left
            })
    return soon

def main():
    receipts_dir = os.path.join(os.path.dirname(__file__), '../assets/mock_data/receipts')
    for fname in sorted(os.listdir(receipts_dir)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(receipts_dir, fname)
        items = load_receipt(path)
        soon = find_soon_to_expire(items)
        print(f"{fname}: {len(soon)} expiring soon")
        for s in soon:
            print(f"  - {s['name']} (in {s['daysLeft']} day(s))")

if __name__ == "__main__":
    main()
