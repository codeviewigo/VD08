from flask import Flask, render_template, jsonify
import requests
from translate import Translator

app = Flask(__name__)
translator = Translator(to_lang="ru")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_quote')
def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        response.raise_for_status()
        data = response.json()
        original_text = data['content']
        author = data['author']

        translated_text = translator.translate(original_text)

        return jsonify({
            "original_text": original_text,
            "author": author,
            "translated_text": translated_text
        })
    except Exception as e:
        return jsonify({
            "original_text": "Ошибка при получении цитаты.",
            "author": "Неизвестный",
            "translated_text": f"Ошибка при переводе: {str(e)}"
        })


if __name__ == '__main__':
    app.run(debug=True, port=8888)
