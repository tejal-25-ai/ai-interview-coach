import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import os
import pyttsx3
from faster_whisper import WhisperModel
from groq import Groq
import re

# === Settings ===
samplerate = 16000
channels = 1
device_index = None
output_file = "manual_voice.wav"
recording = True
frames = []

# === Initialize AI components ===
whisper = WhisperModel("base", compute_type="int8", device="cpu")
groq = Groq(api_key="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")

# === Initialize TTS ===
tts = pyttsx3.init()
tts.setProperty("rate", 170)
voices = tts.getProperty("voices")
default_voice = voices[0].id
alt_voice = voices[1].id if len(voices) > 1 else voices[0].id

# === Conversation memory ===
conversation_history = [
    {
        "role": "system",
        "content": "You are an expert job interview coach. You evaluate the user's spoken answers, give constructive feedback in a friendly tone, and always ask one helpful follow-up interview question. If the input seems like a song, joke, or completely off-topic, kindly point that out and guide the user back to a professional interview response."
    }
]


# === Define speak() function ===
def speak(text):
    def split_sections(text):
        sections = {"strengths": "", "improvements": "", "follow_up": ""}
        current = None
        for line in text.splitlines():
            if "strengths" in line.lower():
                current = "strengths"
            elif "areas for improvement" in line.lower():
                current = "improvements"
            elif "follow-up" in line.lower():
                current = "follow_up"
            elif current:
                sections[current] += " " + line.strip()
        return sections

    def clean_text(t):
        return re.sub(r"[*_`]+", "", t).strip()

    def speak_part(text_part, voice_id):
        if text_part.strip():
            tts.setProperty("voice", voice_id)
            tts.say(clean_text(text_part))

    sections = split_sections(text)
    speak_part(sections["strengths"], default_voice)
    speak_part(sections["improvements"], alt_voice)
    speak_part(sections["follow_up"], default_voice)
    tts.runAndWait()

# === Stop recording on Enter ===
def stop_recording():
    input("⏹️ Press ENTER to stop recording...\n")
    global recording
    recording = False

threading.Thread(target=stop_recording).start()
print("🎙️ Interview mode started. Speak your answer...")

# === Start mic recording ===
try:
    with sd.InputStream(samplerate=samplerate, channels=channels, dtype='int16', device=device_index) as stream:
        while recording:
            chunk, _ = stream.read(1024)
            frames.append(chunk)
except Exception as e:
    print(f"❌ Error: {e}")

# === Save audio ===
if frames:
    audio_data = np.concatenate(frames, axis=0)
    sf.write(output_file, audio_data, samplerate)
    print(f"✅ Audio saved to {output_file}")
else:
    print("⚠️ No audio captured.")
    exit()

# === Transcribe speech ===
print("🧠 Transcribing your answer...")
segments, _ = whisper.transcribe(output_file)
transcription = " ".join([seg.text for seg in segments]).strip()
print(f"📝 You said: {transcription}")

# === Add to conversation memory ===
conversation_history.append({"role": "user", "content": transcription})

# === Query Groq LLM ===
print("🤖 Thinking...")
try:
    response = groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=conversation_history,
        temperature=0.7
    )

    if response.choices:
        reply = response.choices[0].message.content.strip()
        print(f"\n🤖 AI Coach: {reply}")
        conversation_history.append({"role": "assistant", "content": reply})
    else:
        print("❌ No choices returned from Groq API.")
        reply = "Sorry, I didn't get a response. Please try again."

except Exception as e:
    print(f"❌ Error while calling Groq API: {e}")
    reply = "There was an error getting feedback from the AI."

# === Speak response ===
print("🔊 Speaking response...")
speak(reply)




