import module
import telepot
from datetime import datetime
import json, time

module.json_load() # load json data
module.args_init() # load args
module.chatbot_init()
# bot = telepot.Bot(module.token) # init bot

status = True

args = module.parser.parse_args()

if args.show: # show config data
    module.list_config()

if args.n: # create new word space
    module.create_wordSpace()

if args.rm: # remove word space
    module.remove_wordSpace()

if args.l: # list wordspace
    module.list_wordSpace()

if args.alter: # change target workspace
    module.alter_target()

if args.test: # exist for testing
    module.test_fuction()

if args.make: # create word cards with word space data
    module.create_wordCard()

if args.m: # migrate json data
    module.migrate_config()

def BotHandle(msg):
    content, chat, id = telepot.glance(msg)
    print(content, chat, id)
    if content == 'text':
        if msg[content] == '/migrate':
            module.migrate_config()
            exit()
        word = msg[content]
        module.add_word(word)
    else:
        module.bot.sendMessage(id, '아 뭐래')

module.bot.message_loop(BotHandle)

while(True):
    time.sleep(10)
