from flask import Flask, render_template, jsonify, request, redirect, url_for # <-- Added request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename # <-- New import

app = Flask(__name__)

MEME_FOLDER = os.path.join('static', 'memes')
MEME_JSON = 'memes.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # <-- New variable

# Ensure the upload folder exists
os.makedirs(MEME_FOLDER, exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def index_memes():
    memes = []
    for filename in os.listdir(MEME_FOLDER):
        if allowed_file(filename): # <-- Use allowed_file to filter
            # Check if meme already in JSON to preserve existing descriptions/tags
            existing_meme_data = {}
            try:
                with open(MEME_JSON, 'r') as f:
                    existing_memes = json.load(f)
                    for m in existing_memes:
                        if m['filename'] == filename:
                            existing_meme_data = m
                            break
            except (FileNotFoundError, json.JSONDecodeError):
                pass # No existing JSON or empty/invalid

            memes.append({
                'filename': filename,
                'path': f'memes/{filename}',
                'description': existing_meme_data.get('description', '$FWOG meme by @groowut: Community vibes! 🐸'), # Preserve existing or use default
                'tags': existing_meme_data.get('tags', ['fwog', 'solana', '@groowut', 'crypto', 'meme']) # Preserve existing or use default
            })
    with open(MEME_JSON, 'w') as f:
        json.dump(memes, f, indent=4)
    return memes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memes')
def get_memes():
    # Always re-index on request to get latest memes if new ones were added outside of /upload
    # For performance on a very busy site, you might want to optimize this.
    # For now, it ensures consistency.
    index_memes()
    with open(MEME_JSON, 'r') as f:
        memes = json.load(f)
    return jsonify(memes)

# New route for uploading memes
@app.route('/upload', methods=['POST'])
def upload_meme():
    if 'meme_image' not in request.files:
        # No file part in the request
        return redirect(url_for('home'))

    file = request.files['meme_image']

    if file.filename == '':
        # No selected file
        return redirect(url_for('home'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(MEME_FOLDER, filename)) # Save to UPLOAD_FOLDER (which is MEME_FOLDER)

        # Update memes index with the new meme's details
        description = request.form.get('description', '')
        tags_raw = request.form.get('tags', '')
        tags = [tag.strip() for tag in tags_raw.split(',') if tag.strip()]
        if not tags: # Provide default tags if none are given
            tags = ['fwog', 'meme', 'community']

        # Reload existing memes, add new one, save
        try:
            with open(MEME_JSON, 'r') as f:
                memes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            memes = [] # Start with empty list if file doesn't exist or is corrupt

        memes.append({
            'filename': filename,
            'path': f'memes/{filename}',
            'description': description,
            'tags': tags,
        })
        with open(MEME_JSON, 'w') as f:
            json.dump(memes, f, indent=4)

    # Redirect back to the home page after upload
    return redirect(url_for('home'))


if __name__ == '__main__':
    if not os.path.exists(MEME_JSON):
        index_memes()
    app.run(host='0.0.0.0', port=8080)
