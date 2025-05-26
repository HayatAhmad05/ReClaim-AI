import json
import os
from models import FraudData

DATA_FILE = 'data.json'

def load_receipts():
    """Load all stored receipts from data.json."""
    if not os.path.exists(DATA_FILE):
        print("Data file doesn't exist, returning empty list")
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            print(f"Loaded data type: {type(data)}")
            
            # Handle case where data.json contains a single object instead of array
            if isinstance(data, dict):
                print("Data is a single dict, wrapping in array")
                return [data]
            elif isinstance(data, list):
                print(f"Data is a list with {len(data)} items")
                return data
            else:
                print("Data is neither dict nor list, returning empty list")
                return []
    except Exception as e:
        print(f"Error loading receipts: {e}")
        return []

def save_receipts(receipts):
    """Save receipts back to data.json."""
    with open(DATA_FILE, 'w') as f:
        json.dump(receipts, f, indent=4)

def receipts_are_equal(receipt1, receipt2):
    """Check if two receipts are the same, comparing only date and amount."""
    print(f"\n=== COMPARING RECEIPTS ===")
    print(f"Receipt1 merchant: {receipt1.get('merchant')}")
    print(f"Receipt2 merchant: {receipt2.get('merchant')}")
    
    # Check if both receipts exist
    if not receipt1 or not receipt2:
        print("One or both receipts are empty")
        return False
    
    # Only compare date and amount
    date1 = receipt1.get('date')
    date2 = receipt2.get('date')
    amount1 = receipt1.get('total_amount')
    amount2 = receipt2.get('total_amount')
    
    print(f"Comparing date: '{date1}' vs '{date2}'")
    print(f"Comparing total_amount: '{amount1}' vs '{amount2}'")
    
    if date1 != date2:
        print("Date field doesn't match")
        return False
    
    if amount1 != amount2:
        print("Total amount field doesn't match")
        return False
    
    print("Date and amount match - receipts are equal")
    return True

def is_duplicate(new_receipt, receipts):
    """Return True if new_receipt is already in receipts."""
    print(f"\n=== CHECKING FOR DUPLICATES ===")
    print(f"Checking new receipt against {len(receipts)} existing receipts")
    
    for i, old_receipt in enumerate(receipts):
        print(f"\nChecking against receipt {i}:")
        if receipts_are_equal(old_receipt, new_receipt):
            print(f"DUPLICATE FOUND at index {i}!")
            return True
    
    print("No duplicates found")
    return False

def process_receipt(new_receipt):
    print(f"\n=== PROCESSING RECEIPT ===")
    # Ensure we're working with a dict, not a string
    if isinstance(new_receipt, str):
        try:
            new_receipt = json.loads(new_receipt)
        except:
            return {"error": "Invalid receipt format"}
    
    receipts = load_receipts()
    print(f"Loaded {len(receipts)} existing receipts")
    
    if is_duplicate(new_receipt, receipts):
        print("SETTING FRAUD CHECK TO TRUE")
        # Create FraudData object and convert to dict
        fraud_data = FraudData(fraud_detected=True, fraud_type="duplicate")
        new_receipt['fraud_check'] = [fraud_data.dict()]
        # Do not save, just return
    else:
        print("SETTING FRAUD CHECK TO FALSE - SAVING RECEIPT")
        new_receipt['fraud_check'] = []  # Empty list means no fraud detected
        receipts.append(new_receipt)
        save_receipts(receipts)
    
    return new_receipt

# ---- Usage ----
# new_receipt = { ... }  # Your receipt JSON here
# result = process_receipt(new_receipt)
# print(result)
