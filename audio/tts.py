import pyttsx3
import re
import time

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 165)  # Indian English is usually medium-paced

# === Voice Setup ===
voices = engine.getProperty("voices")

# Try to get Indian voice
indian_voice = None
for voice in voices:
    if "en-in" in voice.id.lower() or "Indian" in voice.name:
        indian_voice = voice.id
        break

# Use fallback if Indian voice not found
default_voice = indian_voice if indian_voice else voices[0].id
alt_voice = voices[1].id if len(voices) > 1 else default_voice

# === Speak Function ===
def speak(text):
    print("🔊 Speaking response...")

    # Split response into logical parts
    def split_sections(text):
        sections = {"strengths": "", "improvements": "", "follow_up": ""}
        current = None
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if "strengths" in line.lower():
                current = "strengths"
            elif "areas for improvement" in line.lower():
                current = "improvements"
            elif "follow-up question" in line.lower() or "follow up question" in line.lower():
                current = "follow_up"
            elif current:
                sections[current] += " " + line
        return sections

    # Remove markdown symbols
    def clean_text(t):
        return re.sub(r"[*_`]+", "", t).strip()

    # Speak a section
    def speak_part(part_text, voice_id):
        if part_text.strip():
            engine.setProperty("voice", voice_id)
            engine.say(clean_text(part_text))
            engine.runAndWait()
            time.sleep(0.5)  # slight pause for realism

    # Process and speak
    sections = split_sections(text)
    speak_part(sections["strengths"], default_voice)
    speak_part(sections["improvements"], alt_voice)
    speak_part(sections["follow_up"], default_voice)


