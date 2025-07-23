
import os
import whisper
import google.generativeai as genai
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Flask + Whisper setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
whisper_model = whisper.load_model("base")

# Generate YouTube Metadata using Gemini 1.5 Pro
def generate_youtube_metadata(transcript):
    prompt = f"""
You're a YouTube SEO expert. Based on the following video transcript, generate:
1. A viral YouTube video title (max 100 characters)
2. An SEO-optimized video description (2-3 sentences)
3. A list of up to 10 relevant hashtags

Transcript:
{transcript}

Format the output like:
Title: ...
Description: ...
Hashtags: ...
"""
    # Use correct model name
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating metadata: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    title = description = hashtags = None

    if request.method == 'POST':
        video = request.files['video']
        if video:
            filename = secure_filename(video.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(filepath)

            # Transcribe with Whisper
            result = whisper_model.transcribe(filepath)
            transcript = result['text']

            # Get metadata from Gemini
            metadata = generate_youtube_metadata(transcript)

            try:
                lines = metadata.splitlines()
                title = next(line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("title"))
                description = next(line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("description"))
                hashtags = next(line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("hashtags"))
            except Exception:
                title = "Error parsing metadata"
                description = metadata
                hashtags = ""

    return render_template("index.html", title=title, description=description, hashtags=hashtags)

if __name__ == '__main__':
    app.run(debug=True)
