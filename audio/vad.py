import numpy as np

def collect_chunks(audio: np.ndarray, speech_timestamps: list) -> np.ndarray:
    """
    Extracts the speech segments from the full audio using timestamp ranges.
    """
    if not speech_timestamps:
        return np.array([])

    speech_chunks = []
    for segment in speech_timestamps:
        start = segment['start']
        end = segment['end']
        chunk = audio[start:end]
        speech_chunks.append(chunk)

    return np.concatenate(speech_chunks, axis=0)
