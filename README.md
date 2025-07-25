# ⚓Hook.ai
 1. Hook.ai is a Flask web app that creates viral and SEO-friendly Titles(or captions), Hashtags, and Descriptions for any Video file.<br/>
 2. Hook.ai is developed using LangChain, Groq (Llama2-8b-8192), Few-shot prompting and LLM Prompt Engineering techniques.<br/>
 3. Hook.ai helps content get viral and top the charts!!
## ✨Demo Images

## 🧲Tech Stack

 - Flask – Handles backend web routing and file uploads.
 - FasterWhisper – For fast and accurate multilingual transcription of uploaded audio/video.
 - LangChain – Manages prompt chaining and integration with the LLM for structured output.
 - Groq (Llama2-8b-8192) – Lightning-fast LLM for generating titles, descriptions, and hashtags.
 - RecursiveCharacterTextSplitter – Breaks long transcripts into digestible chunks for better LLM comprehension.
 - HTML5 & CSS3 – Builds the responsive frontend and user interface.
 - JavaScript – Adds interactivity.

## 🌀Workflow
 - User selects a video file.
 - ffmpeg encodes the uploaded video into 16kHz mono WAV format.
 - FasterWhisper (distil-small.en) translates the audio into words.
 - Large texts are divided into smaller logical portions by RecursiveCharacterTextSplitter.
 - A tailored LangChain prompt is designed through prompt engineering skills.
 - Groq LLM (LLaMA 2 8B 8192) executes the transcript and generates Viral title, description andtrending hashtags
 - Everything that is created is showcased on the frontend.

## 🌊Run on your System

**Step1:** git clone https://github.com/V-inaya-K/Hook.ai.git<br />
**Step2:** cd yt caption<br />
**Step3:** create .env file with your grop Api key(GROQ_API_KEY=YOUR_KEY)<br />
**Step4:** pip install -r requirements.txt<br />
**Step5:** python app.py<br />

## 🚀Future Ambitions

 1. Transition to complete multilingual Whisper model for native Hindi/Hinglish transcription.
 2. Train an LLM from scratch on Indian YouTube title/descriptions that go viral to optimize cultural relevance.
 3. Enable authors to upload pre-existing videos and compare generated versus original metadata.
 4. Implement login/signup to store history, previous uploads, and create content in bulk.


