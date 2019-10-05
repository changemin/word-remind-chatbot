import telegram,json
from telegram.ext import  Updater, CommandHandler
import sys
import chatBotModel

def proc_rolling(bot, update):
    wise.sendMessage('데구르르..')
    sound = firecracker()
    wise.sendMessage(sound)
    wise.sendMessage('르르..')

def proc_hello(bot, update):
    wise.sendMessage('안녕하세요! 저는 와이즈입니다.\n당신의 단어 찾기를 도와드릴거에요!')

def proc_stop(bot, update):
    wise.sendMessage('와이즈가 잠듭니다.')
    wise.stop()

def firecracker():
    return '팡팡!'

wise = chatBotModel.Wise()
wise.add_handler('rolling', proc_rolling)
wise.add_handler('stop', proc_stop)
wise.add_handler('hello', proc_hello)
wise.start()