import gradio as gr
import os
import re
import pyttsx3
from faster_whisper import WhisperModel
from groq import Groq

# === Initialize Groq, Whisper, and pyttsx3 ===
groq = Groq(api_key="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")  # 🔁 Replace with your actual API key
whisper = WhisperModel("base", compute_type="int8", device="cpu")
tts = pyttsx3.init()

# === TTS Voice Settings ===
voices = tts.getProperty("voices")
default_voice = voices[0].id
alt_voice = voices[1].id if len(voices) > 1 else default_voice
tts.setProperty("rate", 170)

# === Text-to-Speech with Emotional Parts ===
def speak(text):
    print("🔊 Speaking response...")

    def split_sections(text):
        sections = {"strengths": "", "improvements": "", "follow_up": ""}
        current = None
        for line in text.splitlines():
            if "strengths" in line.lower():
                current = "strengths"
            elif "areas for improvement" in line.lower():
                current = "improvements"
            elif "follow-up question" in line.lower():
                current = "follow_up"
            elif current:
                sections[current] += " " + line.strip()
        return sections

    def clean_text(t):
        return re.sub(r"[*_`]+", "", t).strip()

    def speak_part(part_text, voice_id):
        if part_text.strip():
            tts.setProperty("voice", voice_id)
            tts.say(clean_text(part_text))

    sections = split_sections(text)
    speak_part(sections["strengths"], default_voice)
    speak_part(sections["improvements"], alt_voice)
    speak_part(sections["follow_up"], default_voice)

    tts.runAndWait()

# === Process Audio and Get AI Feedback ===
def process(audio_path):
    print("📥 Received audio input.")
    try:
        # audio_path is already a path to the .wav file
        segments, _ = whisper.transcribe(audio_path)
        transcription = " ".join([seg.text for seg in segments]).strip()
        print(f"📝 Transcribed text: {transcription}")
    except Exception as e:
        print(f"❌ Error in transcription: {e}")
        return "Sorry, could not transcribe your voice. Please try again."

    try:
        conversation = [
            {
                "role": "system",
                "content": "You are an expert job interview coach. Give feedback in an emotionally supportive tone and ask one follow-up question. Use natural and simple language."
            },
            {"role": "user", "content": transcription}
        ]
        response = groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=conversation,
            temperature=0.7
        )
        if response.choices:
            reply = response.choices[0].message.content.strip()
            print(f"🤖 AI Coach: {reply}")
        else:
            reply = "Sorry, no response from the AI."
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        reply = "Error reaching AI coach. Please check your key or model."

    try:
        speak(reply)
    except Exception as e:
        print(f"⚠️ TTS failed: {e}")
        reply += "\n\n(Speech playback failed. See console logs.)"

    return reply

# === Gradio Interface ===
with gr.Blocks(title="AI Interview Coach") as demo:
    gr.Markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <h1 style="font-size: 2.5em; font-weight: bold; background: linear-gradient(to right, #007cf0, #00dfd8); -webkit-background-clip: text; color: transparent;">
                🧠 AI Interview Coach
            </h1>
            <p style="font-size: 1.1em; color: #555;">
                Upload your voice answer to a job interview question. <br>
                The AI will transcribe, analyze, and give helpful feedback — and speak it with emotion!
            </p>
        </div>
        """
    )

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="🎙️ Upload your answer (WAV format)", show_label=True)
        output_text = gr.Textbox(label="🤖 AI Coach Feedback", lines=8, interactive=False)

    with gr.Row():
        submit_btn = gr.Button("🔍 Analyze")
        clear_btn = gr.Button("🧹 Clear")

    def wrapped_process(audio_path):
        return process(audio_path)

    submit_btn.click(wrapped_process, inputs=audio_input, outputs=output_text)
    clear_btn.click(lambda: ("", ""), inputs=[], outputs=[audio_input, output_text])

demo.launch(share=True)


