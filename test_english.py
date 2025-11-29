from api_service import get_definition
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

def test_english_support():
    print("Testing search for 'Book' (EN -> TR)...")
    result_en_tr = get_definition("Book", "English", "Turkish")
    print("Result EN-TR:", result_en_tr)
    
    print("\nTesting search for 'Kitap' (TR -> EN)...")
    result_tr_en = get_definition("Kitap", "Turkish", "English")
    print("Result TR-EN:", result_tr_en)

if __name__ == "__main__":
    test_english_support()
