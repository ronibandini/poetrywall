# Poetry Wall
# Speech Recon example 
# Roni Bandini, Buenos Aires, March 2023

import os
import time
import speech_recognition as sr

r = sr.Recognizer()
audio_file = sr.AudioFile('test.wav')
with audio_file as source: 
   r.adjust_for_ambient_noise(source) 
   audio = r.record(source)
result = r.recognize_google(audio,language="es-ES")
print(result) 
with open('test.txt',mode ='w') as file: 
   file.write("Recognized text:") 
   file.write("\n") 
   file.write(result) 
   print("ready!")