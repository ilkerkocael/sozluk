from api_service import get_definition
import logging
import json

# Enable logging
logging.basicConfig(level=logging.INFO)

def test_naturalness():
    print("Testing search for 'Fırlatmak' (TR -> FR)...")
    result = get_definition("Fırlatmak", "Turkish", "French")
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Check for forbidden content
    result_str = json.dumps(result, ensure_ascii=False).lower()
    if "hakem" in result_str and "fırlattı" in result_str:
        print("\n[FAIL] Found unnatural sentence: 'Hakem... fırlattı'")
    else:
        print("\n[PASS] No unnatural 'Hakem... fırlattı' sentence found.")

if __name__ == "__main__":
    test_naturalness()
