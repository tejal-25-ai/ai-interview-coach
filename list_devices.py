import sounddevice as sd

print("\n🎙️ Available audio input/output devices:\n")
print(sd.query_devices())
