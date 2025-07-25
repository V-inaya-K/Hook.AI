# ⚓Hook.ai
 1. Hook.ai is a Flask web app that creates viral and SEO-friendly Titles(or captions), Hashtags, and Descriptions for any Video file.<br/>
 2. Hook.ai is developed using LangChain, Groq (Llama2-8b-8192), Few-shot prompting and LLM Prompt Engineering techniques.<br/>
 3. Hook.ai helps content get viral and top the charts!!
## ✨Demo Images

## 🧲Tech Stack

 - Flask – handles backend web routing and file uploading.
 - FasterWhisper – For quick and accurate multilingual transcription of uploaded audio/video.
 - LangChain – Manages prompt chaining and LLM integration for formatted output.
 - Groq (Llama2-8b-8192) – Extremely fast LLM for title, description, and hashtag creation.
 - RecursiveCharacterTextSplitter – Divides long transcripts into bite-sized chunks for better LLM comprehension.
 - HTML5 & CSS3 – Builds the responsive frontend and user interface.
 - JavaScript – Adds interactivity.

## 🌀Workflow
 1. User selects a video file.
 2. ffmpeg encodes the uploaded video into 16kHz mono WAV format.
 3. FasterWhisper (distil-small.en) translates the audio into words.
 4. Large texts are divided into smaller logical portions by RecursiveCharacterTextSplitter.
 5. A tailored LangChain prompt is designed through prompt engineering skills.
 6. Groq LLM (LLaMA 2 8B 8192) executes the transcript and generates Viral title, description andtrending hashtags
 7. Everything that is created is showcased on the frontend.

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


