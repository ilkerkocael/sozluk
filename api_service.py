import google.generativeai as genai
from config import Config
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)

def get_definition(word, source_lang, target_lang):
    """
    Fetches the definition, context, and examples for a word using Gemini AI.
    Implements a fallback mechanism between a primary and a secondary model.
    """
    
    prompt = f"""
    Act as a professional dictionary editor. 
    I need the closest equivalents/translations of the word "{word}" from {source_lang} to {target_lang}.
    
    IMPORTANT RULES:
    1. **Semantic Disambiguation (Anlam Ayrımı):**
       - Analyze the exact meaning of the source word "{word}" in {source_lang}.
       - If the target word in {target_lang} has multiple meanings, ONLY provide the meaning that strictly matches the source word.
       - Filter out unrelated meanings (false positives). For example, if the word is "kaşımak" (scratch an itch), do NOT include meanings related to "scraping" or "peeling" (like "gratter" in the sense of scraping).
    2. **Naturalness & Collocation (Doğallık ve Eşdizimlilik):**
       - **Strict Collocation Check:** You must verify that the source word "{word}" is the *standard* and *natural* verb used in the context of the target definition.
       - **Example Validation:** If the target word (e.g., "expulser") typically pairs with a different source verb (e.g., "atmak") instead of "{word}" (e.g., "fırlatmak"), **DISCARD** that definition.
       - **Prohibited:** Do NOT force "{word}" into a sentence where it sounds awkward. For example, "Hakem oyuncuyu fırlattı" is WRONG; it should be "Hakem oyuncuyu attı". Since "attı" is not "{word}", do not include this meaning.
    3. The 'meaning' field MUST contain the closest equivalents or translations of the word in {target_lang} (NOT a descriptive definition).
    4. The 'example' field MUST be a sentence in {source_lang} (the language of the word "{word}").
    4. The 'translation' field MUST be the translation of that example into {target_lang}.
    
    Please provide the output STRICTLY in the following JSON format:
    {{
        "word": "{word}",
        "definitions": [
            {{
                "meaning": "The closest equivalent(s) or translation(s) of the word in {target_lang}.",
                "example": "An example sentence in {source_lang} containing the word '{word}'.",
                "translation": "Translation of the example sentence in {target_lang}."
            }}
        ],
        "contexts": [
            {{
                "context": "A specific context (e.g., formal, slang, medical) in {target_lang}.",
                "explanation": "Explanation of how the word is used in this context (in {target_lang})."
            }}
        ]
    }}
    
    Ensure the JSON is valid and contains no markdown formatting (like ```json).
    """

  generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,  # <--- BURAYI 1024'TEN 8192'YE ÇIKARDIK
        "response_mime_type": "application/json",
    }

    def call_model(model_name):
        try:
            logger.info(f"Attempting to call model: {model_name}")
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.warning(f"Failed to get response from {model_name}: {e}")
            return None

    # Try Primary Model
    result_text = call_model(Config.PRIMARY_MODEL)
    
    # Fallback if Primary fails
    if not result_text:
        logger.info("Switching to fallback model...")
        result_text = call_model(Config.FALLBACK_MODEL)

    if not result_text:
        logger.error("Both models failed.")
        return {"error": "Service unavailable. Please try again later."}

    try:
        # --- YENİ TEMİZLİK KODU BAŞLANGICI ---
        # Gelen metni temizle
        cleaned_text = result_text.strip()
        
        # İlk süslü parantezi '{' ve son süslü parantezi '}' bul.
        # Böylece model en başa "İşte cevabınız:" yazsa bile onları görmezden geliriz.
        start_index = cleaned_text.find('{')
        end_index = cleaned_text.rfind('}')

        if start_index != -1 and end_index != -1:
            # Sadece { ile } arasındaki gerçek JSON verisini al
            cleaned_text = cleaned_text[start_index : end_index + 1]
        
        return json.loads(cleaned_text)
        # --- YENİ TEMİZLİK KODU BİTİŞİ ---

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        # Hata durumunda loglara gelen ham metni bas ki ne geldiğini görelim
        logger.error(f"Raw text received: {result_text}") 
        return {"error": "Invalid response format from AI."}

