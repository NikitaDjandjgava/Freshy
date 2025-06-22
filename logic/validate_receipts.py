import json
import os
from datetime import datetime

# --- Settings ---
RECEIPTS_DIR = os.path.join(os.path.dirname(__file__), "../assets/mock_data/receipts")


def load_receipts(receipts_dir):
    """Load all receipt files in the given directory."""
    receipts = []
    for fname in sorted(os.listdir(receipts_dir)):
        if fname.endswith(".json"):
            path = os.path.join(receipts_dir, fname)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                receipts.append((fname, data))
    return receipts


def print_receipt_summary(filename, receipt):
    """Print a formatted summary of a single receipt."""
    print(f"\n===== {filename} =====")
    print(f"Receipt ID:     {receipt.get('receiptId')}")
    print(f"Purchase Date:  {receipt.get('purchaseDate')}")
    items = receipt.get('items', [])
    print(f"Number of items: {len(items)}")

    for i, item in enumerate(items, 1):
        print(f"  {i}. {item['name']}")
        print(f"     ID: {item['id']}")
        print(f"     Quantity: {item['quantity']} {item.get('unit', '')}")
        print(f"     Expiry: {item['expiryDate']}")
        print(f"     Cost: €{item['cost']:.2f}")
        print(f"     Allergens: {', '.join(item.get('allergens', [])) or 'None'}")
        print(f"     Dietary Tags: {', '.join(item.get('dietaryTags', [])) or 'None'}")


def main():
    print("Validating and printing receipt summaries...\n")
    receipts = load_receipts(RECEIPTS_DIR)
    if not receipts:
        print("No receipt files found.")
        return

    for fname, data in receipts:
        print_receipt_summary(fname, data)


if __name__ == "__main__":
    main()
