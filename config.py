import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    
    PRIMARY_MODEL = "models/gemini-2.5-flash"
    
    FALLBACK_MODEL = "models/gemini-2.5-pro"

    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is not set in environment variables.")

