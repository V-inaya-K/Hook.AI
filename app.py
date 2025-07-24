import os
import logging
import subprocess
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from groq import Groq

# Setup logging
logging.basicConfig(level=logging.INFO)

load_dotenv() # Load environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Flask setup Starts
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

whisper_model = WhisperModel("medium", compute_type="int8")  # Load Whisper model


# Initialize Groq client
groq_client = Groq(api_key=groq_api_key)

#video/audio  Conversion to WAV
def convert_to_wav(input_path, output_path):
    cmd = ["ffmpeg", "-i", input_path, "-ar", "16000", "-ac", "1", output_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Generate YouTube metadata
def generate_youtube_metadata(transcript: str) -> str:
    examples = [
        {    #Few Shot Prompting starts
            "transcript": "Yaar kal maine ek movie dekhi – full dhamaka tha, literally! Plot twist ne hilake rakh diya.",
            "title": "🔥 Kal Ki Movie Ka Review – Full Dhamaka! | Must Watch or Skip?",
            "description": "Dosto, aaj ki video mein discuss karenge kal ki blockbuster film ka honest review. Ending ne hila diya! Dekho ya na dekho? Bataunga sab kuch candidly! 🍿",
            "hashtags": "#MovieReview #BollywoodTalks #FullDhamaka"
        },
        {
            "transcript": "Aaj ke podcast mein baat karenge Indian startup culture ke bare mein – kya sach mein sab hype hai?",
            "title": "🇮🇳 Indian Startup Bubble – Sach Ya Hype? 🤔",
            "description": "Kya Indian startups sirf funding ke liye ban rahe hain? Ya hai asli innovation? Aaj ke episode mein deep dive karte hain Indian tech world ke andar. 💼💡",
            "hashtags": "#StartupIndia #TechTalk #HustleCulture"
        }
    ] #Few Shot Prompting ends

    # Create prompt
    few_shot_prompt = "\n".join([
        f"Transcript:\n{ex['transcript']}\nTitle: {ex['title']}\nDescription: {ex['description']}\nHashtags: {ex['hashtags']}\n"
        for ex in examples
    ])

    #Using Shots input
    full_prompt = f"""{few_shot_prompt} 
Transcript:
{transcript}

Now generate Title, Description and Hashtags in the same Hinglish style.
Format:
Title: ...
Description: ...
Hashtags: ...
"""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a YouTube content expert who generates highly clickable and SEO-friendly titles, descriptions, and hashtags. "
                "Always use Hinglish or Hindi-style language to make it fun and viral for Indian audiences."
            )
        },
        {"role": "user", "content": full_prompt}
    ]

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        timeout=60
    )
    return response.choices[0].message.content.strip()


@app.route('/', methods=['GET', 'POST'])
def index():
    title = description = hashtags = error = transcript = None

    if request.method == 'POST':
        video = request.files.get('video')
        if video:
            filename = secure_filename(video.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(input_path)

            try:
                logging.info("Video converting to wav")
                wav_path = input_path.rsplit(".", 1)[0] + ".wav"
                convert_to_wav(input_path, wav_path)

                logging.info("Transcription in Process")
                segments, _ = whisper_model.transcribe(wav_path)
                transcript = " ".join(segment.text for segment in segments)
                logging.info("Transcribed Successfully")

                logging.info("Generating metadata")
                metadata = generate_youtube_metadata(transcript)
                logging.info("Generation Successful")

                lines = metadata.splitlines()
                title = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("title")), "")
                description = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("description")), "")
                hashtags = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("hashtags")), "")

            except Exception as e:
                logging.error(f"❌ Error: {e}")
                error = f"Error: {str(e)}"

    # return render_template("index.html", title=title, description=description, hashtags=hashtags, transcript=transcript, error=error)
    return render_template("index.html", title=title, description=description, hashtags=hashtags, error=error)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
