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
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    receipts.append((fname, data))
            except Exception as e:
                print(f"Error loading {fname}: {e}")
    return receipts


def print_receipt_summary(filename, receipt):
    """Print a formatted summary of a single receipt."""
    print(f"\n===== {filename} =====")
    print(f"Receipt ID:     {receipt.get('receiptId', 'N/A')}")
    print(f"Purchase Date:  {receipt.get('purchaseDate', 'N/A')}")
    items = receipt.get('items', [])
    print(f"Number of items: {len(items)}")

    for i, item in enumerate(items, 1):
        print(f"  {i}. {item.get('name', 'Unnamed Item')}")
        print(f"     ID: {item.get('id', 'N/A')}")
        print(f"     Quantity: {item.get('quantity', 'N/A')} {item.get('unit', '')}")
        
        expiry_raw = item.get('expiryDate', 'N/A')
        try:
            datetime.fromisoformat(expiry_raw.replace('Z', ''))
            expiry_display = expiry_raw
        except Exception:
            expiry_display = "Invalid date format"
        print(f"     Expiry: {expiry_display}")
        
        cost = item.get('cost', 0.0)
        print(f"     Cost: €{cost:.2f}")
        
        allergens = ', '.join(item.get('allergens', [])) or 'None'
        tags = ', '.join(item.get('dietaryTags', [])) or 'None'
        print(f"     Allergens: {allergens}")
        print(f"     Dietary Tags: {tags}")


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
