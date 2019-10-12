import requests
import sys, time, json, os, argparse, random, re
from bs4 import BeautifulSoup
from datetime import datetime
from os import listdir
from PIL import Image, ImageDraw, ImageFont
import telepot
import pyttsx3
import module

module.json_load()
module.args_init()

bot = telepot.Bot(module.token)

status = True

args = module.parser.parse_args()

if args.show: # show config data
    module.list_config()

if args.n: # create new word space
    module.create_wordSpace()

if args.rm:
    module.remove_wordSpace()

if args.l: # list wordspace
    module.list_wordSpace()

if args.checkout: # change target workspace
    module.alter_target()

if args.test:
    module.test_fuction()

if args.make:
    module.create_wordCard()

if args.m:
    module.migrate_config()

def BotHandle(msg):
    # print(filePath)
    content, chat, id = telepot.glance(msg)
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d/%H:%M")
    print(content, chat, id)
    if content == 'text':
        if msg[content] == '/migrate':
            print('migrate fuction activated')
            bot.sendMessage(id, 'migrate fuction activated')
            # migrate
            exit()
        word = msg[content]
        wordMeaing = module.isMeaning(word)
        newWord = date_time + ", " + word + ", "
        newWord += module.isMeaning(word)
        module.configData['WordSpaces'][module.targetFile]['wordCount'] += 1
        with open('config.json', 'w', encoding='UTF-8') as config: # read config file
            json.dump(module.configData, config, ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
        print(module.configData['WordSpaces'][module.targetFile]['wordCount'])
        f = open(module.filePath, "a+", encoding='UTF-8')
        f.write(newWord)
        f.close()
        print(wordMeaing)
        print(newWord)
        bot.sendMessage(id, module.isMeaning(word))
    else:
        bot.sendMessage(id, '아 뭐래')

bot.message_loop(BotHandle)

while(True):
    time.sleep(10)
