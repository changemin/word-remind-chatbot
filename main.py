import module
import telepot
from datetime import datetime
import json, time
from telepot.loop import MessageLoop

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
    # if id == module.userId:
    if content == 'text':
        if msg[content] == '/migrate':
            module.migrate_config()
            exit()
        if msg[content] == '/show':
            module.list_config()
            exit()
        if msg[content][0:4] == '/new':
            wordSpaceName = msg[content][5:]
            module.create_wordSpace(wordSpaceName)
            exit()
        if msg[content][0:7] == '/remove':
            wordSpaceName = msg[content][8:]
            module.remove_wordSpace(wordSpaceName)
            exit()
        if msg[content] == '/list':
            module.list_wordSpace()
            exit()
        if msg[content][0:9] == '/checkout':
            wordSpaceName = msg[content][10:]
            module.alter_target(wordSpaceName)
            exit()
        if msg[content] == '/make':
            module.create_wordCard()
            exit()
        if msg[content] == '/help':
            module.list_function()
            exit()
        
        word = msg[content]
        module.add_word(word)
        # print(msg[content])
        # print(msg[content][0:7])
        # print(msg[content][8:])
    else:
        module.bot.sendMessage(id, '아 뭐래')

MessageLoop(module.bot, BotHandle).run_as_thread()

while(True):
    time.sleep(10)
