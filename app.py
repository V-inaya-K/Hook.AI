import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from groq import Groq

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Flask setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load Whisper model
whisper_model = WhisperModel("base")

# Initialize Groq client
groq_client = Groq(api_key=groq_api_key)

# Summarizer function
def summarize_transcript(transcript: str) -> str:
    messages = [
        {"role": "system", "content": "Summarize this transcript into a concise 200-word summary for metadata generation."},
        {"role": "user", "content": transcript}
    ]
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Metadata generator
def generate_youtube_metadata(summary: str) -> str:
    messages = [
        {"role": "system", "content": "You are a YouTube SEO expert who generates viral titles, descriptions, and hashtags. Use Hinglish or Hindi slang if appropriate."},
        {"role": "user", "content": f"""
Transcript Summary:
{summary}

Generate:
Title: ...
Description: ...
Hashtags: ...
"""}
    ]
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )
    return response.choices[0].message.content.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    title = description = hashtags = error = None

    if request.method == 'POST':
        video = request.files.get('video')
        if video:
            filename = secure_filename(video.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(filepath)

            try:
                # Transcribe video
                segments, _ = whisper_model.transcribe(filepath)
                transcript = " ".join(segment.text for segment in segments)

                # Summarize transcript
                summary = summarize_transcript(transcript)

                # Generate metadata
                metadata = generate_youtube_metadata(summary)

                # Parse output
                lines = metadata.splitlines()
                title = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("title")), "")
                description = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("description")), "")
                hashtags = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("hashtags")), "")

            except Exception as e:
                error = f"❌ {str(e)}"

    return render_template("index.html", title=title, description=description, hashtags=hashtags, error=error)

if __name__ == '__main__':
    app.run(debug=True)
