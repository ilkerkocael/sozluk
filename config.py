import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PRIMARY_MODEL = "models/gemini-1.5-flash"
    FALLBACK_MODEL = "models/gemini-1.5-pro"  

    if not GEMINI_API_KEY:
        # This is just a warning for development; in production, you might want to raise an error

        print("WARNING: GEMINI_API_KEY is not set in environment variables.")
