# -*- coding: utf-8 -*-

# Speech recognition and text to speech libraries
import speech_recognition as sr
from gtts import gTTS

# Library to play mp3
from pygame import mixer

mixer.init()

# Microphone and recognition
r = sr.Recognizer()
m = sr.Microphone()

try:
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source:
            audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            statement = r.recognize_google(audio, language="ru_RU")

            # Synthesize speech from bot answer
            tts = gTTS(text=str(statement), lang="ru")
            tts.save("speach.mp3")

            # Play answer
            mixer.music.load('speach.mp3')
            mixer.music.play()

            print("You said {}".format(statement))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
