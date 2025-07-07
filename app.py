from flask import Flask, render_template, jsonify
import os
import json

app = Flask(__name__)

MEME_FOLDER = os.path.join('static', 'memes')
MEME_JSON = 'memes.json'

def index_memes():
    memes = []
    for filename in os.listdir(MEME_FOLDER):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            memes.append({
                'filename': filename,
                'path': f'memes/{filename}',
                'description': f'$FWOG meme by @groowut: Community vibes! 🐸',
                'tags': ['fwog', 'solana', '@groowut', 'crypto', 'meme']
            })
    with open(MEME_JSON, 'w') as f:
        json.dump(memes, f, indent=4)
    return memes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memes')
def get_memes():
    if not os.path.exists(MEME_JSON):
        index_memes()
    with open(MEME_JSON, 'r') as f:
        memes = json.load(f)
    return jsonify(memes)

if __name__ == '__main__':
    if not os.path.exists(MEME_JSON):
        index_memes()
    app.run(host='0.0.0.0', port=8080)