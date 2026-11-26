"""Speech-to-text — Poetry Wall 2.0."""
from __future__ import annotations

import speech_recognition as sr


def transcribe(wav_path: str, language: str = "es-ES") -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language=language)
