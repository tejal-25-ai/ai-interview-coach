# 🧠 AI Interview Coach Chatbot

A voice-based, real-time AI Interview Coach that listens to your answers, provides constructive feedback, and asks intelligent follow-up questions — just like a real interviewer.

Built for the **Unstop Hackathon - Agentic Chatbot Track**, this prototype uses cutting-edge technologies like Whisper for speech-to-text (STT), Groq's LLaMA3 LLM for contextual understanding, and pyttsx3 for emotional TTS — all wrapped in a Gradio web interface.

---

## 🚀 Features

✅ Real-time voice input using microphone  
✅ Accurate transcription via Faster-Whisper  
✅ Smart feedback and follow-up from Groq's LLaMA3-70b  
✅ Emotion-infused text-to-speech with Indian-accent voices  
✅ In-memory conversation context (multi-turn support)  
✅ Web interface using Gradio (one-click launch)  

---

## 🛠️ Tech Stack

| Feature          | Technology               |
|------------------|--------------------------|
| UI               | Gradio                   |
| LLM              | Groq (LLaMA3-70b-8192)   |
| STT              | Faster Whisper           |
| TTS              | pyttsx3                  |
| Backend          | Python                   |
| Memory Mgmt      | In-session memory        |
| Hosting          | Localhost or Gradio Live |

---

## 🖥️ Demo

### ▶️ [Demo Video Link](https://your-video-link-here.com)

Or run it locally:

```bash
git clone https://github.com/your-username/ai-interview-coach.git
cd ai-interview-coach
python -m venv env
env\Scripts\activate  # or source env/bin/activate on Mac/Linux
pip install -r requirements.txt
