# Библиотеки распознавания и синтеза речи
import speech_recognition as sr
from gtts import gTTS

# TODO
# make corpus in lower case
# ROS node чтобы получать запросы от ноды распознавания препятствий и других интересностях

# Воспроизведение речи
from pygame import mixer
mixer.init()

import os, sys, time

# Библиотека Chatterbot для простого лингвистического ИИ
# https://github.com/gunthercox/ChatterBot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import logging

# Statement from SpeechRecognition.recognize_google()
# Because sometimes sr.recognize_google() fails due to field 'confidence' don't exists in json
# So we will get all statements in json style and beautify them
class Statement:
    def __init__(self, dict):
        self.confidence = dict['confidence']
        self.text = dict['transcript'].lower()

    def __repr__(self):
        return "[{}] {}".format(self.confidence, self.text)

    def __str__(self):
        return self.text

    def __gt__(self, other):
        return self.confidence > other.confidence


class Speech_AI:
    def __init__(self, google_treshold = 0.5, chatterbot_treshold = 0.45):
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

        self.google_treshold = google_treshold          # minimial allowed confidence in speech recognition
        self.chatterbot_treshold = chatterbot_treshold  # ---/--- in chatterbot

        is_need_train = not self.is_db_exists()
        self.bot = ChatBot(name="Robby",
            logic_adapters=[{
                                'import_path' : 'chatterbot.logic.BestMatch'
                            },
                            {
                                'import_path': 'chatterbot.logic.MathematicalEvaluation',
                                'math_words_language' : 'russian'
                            },
                            {
                                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                                'threshold': self.chatterbot_treshold,
                                'default_response': 'Как интересно. А расскажешь еще что-нибудь?'
                            }],
            storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
            filters=["chatterbot.filters.RepetitiveResponseFilter"],
            database="./database.json"
        )

        if is_need_train:
            print("Производится обучение на corpus данных")
            self.train()

        self._mp3_name = "speech.mp3"
        self.be_quiet = False


    def work(self):
        print('Минутку тишины, пожалуйста...')
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

        while True:
            print('Скажи что - нибудь!')
            with self._microphone as source:
                audio = self._recognizer.listen(source)
            print("Понял, идет распознавание...")
            statements = self.recognize(audio)
            print('Выражения ', statements)
            best_statement = self.choose_best_statement(statements)
            print('Вы сказали: ', best_statement)
            result = self.process_statement(best_statement, statements)
            print(self.bot.name, " ответил: ", result)

            if not self.be_quiet:
                self.say(str(result))

            print()

    # TODO add timeout
    # recognize google can return json if show_all is True
    # returns:
    # * on success: list of Statement objects
    # * on error: if error arises, return empty list
    def recognize(self, audio):
        statements = []
        try:
            json = self._recognizer.recognize_google(audio, language="ru_RU", show_all=True)
            statements = self.json_to_statements(json)
        except sr.UnknownValueError:
            print("[GoogleSR] Неизвестное выражение")
        except sr.RequestError as e:
            print("[GoogleSR] Не могу получить данные; {0}".format(e))
        return statements

    # json to statements (check class in beginning of this script)
    def json_to_statements(self, json):
        statements = []
        if len(json) is not 0:
            for dict in json['alternative']:
                if 'confidence' not in dict:
                    dict['confidence'] = self.google_treshold + 0.1  # must not be filtered
                statements.append(Statement(dict))
        return statements

    # choose best statement from list of statements
    # returns:
    # * on success: Statement object
    # * on error: None
    def choose_best_statement(self, statements):
        if statements:
            return max(statements, key=lambda s: s.confidence)
        else:
            return None

    # check one word from words in string
    def check_in_string(self, string, words):
        if any(word in string for word in words):
            return True
        return False

    # A lot of cool possibilities can be impemented here (IoT, CV, ...)
    def process_statement(self, best_statement, statements):
        if best_statement is None or best_statement.confidence < self.google_treshold:
            answer = "Простите, вас плохо слышно"
        else:
            # Some examples of commands
            # Check all received statements (even with smaller confidence)
            # Because we need more confidence in command will be recognized the first time
            command_recognized = False
            for st in statements:
                if self.check_in_string(st.text, ('вперёд', 'иди', 'шагай')):
                    answer = "Я знаю эту команду!"
                    command_recognized = True
                elif self.check_in_string(st.text, ('остановись', 'стоп', 'стой')):
                    answer = "Я знаю эту команду!"
                    command_recognized = True
                elif self.check_in_string(st.text, ('тихо', 'молчать', 'тишина', 'тише')):
                    self.be_quiet = True
                    command_recognized = True
                    answer = "Я буду вести себя тише"
                elif self.check_in_string(st.text, ('говори', 'громче')):
                    self.be_quiet = False
                    answer = "Я буду говорить громче"
                    command_recognized = True
            if not command_recognized:
                answer = self.make_answer(best_statement.text)  # takes many time to be executed
        return answer

    # Get synthesized mp3 and play it with pygame
    def say(self, phrase):
        # Synthesize answer
        # todo check exceptons there
        print("[GoogleTTS] Начало запроса")
        try:
            tts = gTTS(text=phrase, lang="ru")
            tts.save(self._mp3_name)
        except Exception as e:
            print("[GoogleTTS] Не удалось синтезировать речь: {}".format(e.strerror))
            return
        # Play answer
        mixer.music.load(self._mp3_name)
        mixer.music.play()

        while mixer.music.get_busy():
            time.sleep(0.1)

    def make_answer(self, statement):
        return self.bot.get_response(statement)

    # train chatterbot with our corpus (all files if ./corpus folder)
    def train(self):
        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train("corpus")
        print("Обучение завершено")

    # keyboard exception handler
    def shutdown(self, export=False):
        if export:
            self.bot.trainer.export_for_training('corpus/last_session_corpus.json')
            print("База данных экспортирована в корпус last_session_corpus.json")

        # self._clean_up()
        print("Завершение работы")

    def clean_up(self):
        os.remove(self._mp3_name)

    # if we have db already we don't need to train bot again
    def is_db_exists(self):
        db_path = os.getcwd() + '/database.json'
        return os.path.isfile(db_path)


def main():
    ai = Speech_AI()
    try:
        ai.work()
    except KeyboardInterrupt:
        ai.shutdown()

main()