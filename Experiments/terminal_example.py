# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
bot = ChatBot("Al",
              logic_adapters=[{
                  'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                  'threshold': 0.65,
                  'default_response': 'Я не совсем тебя понимаю.'
              }])

bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("../corpus")

while True:
    try:
        answer = input("Я: ")
        bot_input = bot.get_response(answer)
        print("Р: {}".format(bot_input))

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
