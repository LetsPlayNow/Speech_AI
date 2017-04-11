# Библиотеки распознавания и синтеза речи
import speech_recognition as sr
from gtts import gTTS

# TODO
# Воспроизведение текстов
# Распознавание и отправка команд
# ROS node чтобы получать запросы от ноды распознавания препятствий и других интересностях
# * отправка файлов роботу для воспроизведения

# Воспроизведение речи
import pygame
from pygame import mixer
mixer.init()

import os
import time

# Библиотека Chatterbot для простого лингвистического ИИ
# https://github.com/gunthercox/ChatterBot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

class Speech_AI:
    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

        self.google_threshold = 0.5
        self.chatterbot_treshold = 0.45
        self.bot = ChatBot(name="Robby",
            logic_adapters=[{
                                'import_path' : 'chatterbot.logic.BestMatch'
                            },
                            {
                                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                                'threshold': self.chatterbot_treshold,
                                'default_response': 'Как интересно. А расскажешь еще что - нибудь?'
                            },
                            {
                                'import_path': 'chatterbot.logic.MathematicalEvaluation'
                            }],
            storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
            filters=["chatterbot.filters.RepetitiveResponseFilter"],
            database="./database.json"
        )

        self.train()

        self._mp3_name = "speech.mp3"



    def work(self):
        print("Минутку тишины, пожалуйста...")
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

        while True:
            print("Скажи что - нибудь!")
            with self._microphone as source:
                audio = self._recognizer.listen(source)
            print("Понял, идет распознавание...")
            statement = self.recognize(audio)
            print("Вы сказали: ", statement)
            result = self.process_statement(statement)
            print(self.bot.name, " ответил: ", statement)

            self.say(str(result))

    # recognize google can return
    # [{'transcript' : 'asdad', 'confidence' : 0.5}, ...] or [{'transcript': 0.5},...] or empty array
    # todo add timeout for request and better error escaping
    def recognize(self, audio):
        best_statement = None
        try:
            statements = self._recognizer.recognize_google(audio, language="ru_RU", show_all=True)
            if len(statements) is not 0:
                best_statement = self.choose_best_statement(statements)
        except sr.UnknownValueError:
            print("Упс! Кажется, я тебя не понял")
        except sr.RequestError as e:
            print("Не могу получить данные от сервиса Google Speech Recognition; {0}".format(e))
        return best_statement

    def choose_best_statement(self, statements):
        best_statement = None
        max_confidence = 0
        for alternative in statements:
            if 'confidence' not in alternative:
                alternative['confidence'] = 0.8

            if alternative['confidence'] > max_confidence:
                max_confidence = alternative['confidence']
                best_statement = alternative
        return best_statement

    # A lot of cool possibilities can be impemented here (IoT, CV, ...)
    def process_statement(self, statement):
        if statement is None or statement['confidence'] < self.google_threshold:
            answer = "Простите, вас плохо слышно"
        else:
            answer = self.make_answer(statement['transcript'])

    def say(self, phrase):
        # Synthesize answer
        tts = gTTS(text=phrase, lang="ru")
        tts.save(self._mp3_name)

        # Play answer
        mixer.music.load(self._mp3_name)
        mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def make_answer(self, statement):
        return self.bot.get_response(statement)

    # TODO if database exists we should not learn
    def train(self):
        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train("corpus")
        print("Обучение завершено")

    def shutdown(self):
        # self.bot.trainer.export_for_training('corpus/last_session_corpus.json')
        # self._clean_up()
        print("Пока!")

    def clean_up(self):
        os.remove(self._mp3_name)


def main():
    ai = Speech_AI()
    try:
        ai.work()
    except KeyboardInterrupt:
        ai.shutdown()

main()