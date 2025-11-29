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
        "max_output_tokens": 1024,
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
        # Clean up potential markdown code blocks if the model ignores the instruction
        cleaned_text = result_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        return {"error": "Invalid response format from AI."}
