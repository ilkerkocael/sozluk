from api_service import get_definition
import logging

# Enable logging to see the fallback in action
logging.basicConfig(level=logging.INFO)

def test_search():
    print("Testing search for 'Kalp' (TR -> FR)...")
    result = get_definition("Kalp", "Turkish", "French")
    print("Result:", result)
    
    if "error" in result:
        print("Test Failed or API Key missing.")
    else:
        print("Test Passed!")
        defs = result.get('definitions', [])
        if defs:
            print(f"Meaning (Should be 'Cœur' or similar): {defs[0]['meaning']}")

if __name__ == "__main__":
    test_search()
