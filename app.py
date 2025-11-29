from flask import Flask, render_template, request, jsonify
from api_service import get_definition
import os

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    word = data.get('word')
    lang_pair = data.get('lang_pair') # Expecting "fr-tr" or "tr-fr"

    if not word or not lang_pair:
        return jsonify({"error": "Missing word or language pair"}), 400

    if lang_pair == "fr-tr":
        source_lang, target_lang = "French", "Turkish"
    elif lang_pair == "tr-fr":
        source_lang, target_lang = "Turkish", "French"
    elif lang_pair == "en-tr":
        source_lang, target_lang = "English", "Turkish"
    elif lang_pair == "tr-en":
        source_lang, target_lang = "Turkish", "English"
    else:
        return jsonify({"error": "Invalid language pair"}), 400

    result = get_definition(word, source_lang, target_lang)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
