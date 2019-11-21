import module
import telepot
from datetime import datetime
import json, time
from telepot.loop import MessageLoop

module.LoadJson() # load json data
module.args_init() # load args
module.chatbot_init()
# bot = telepot.Bot(module.token) # init bot

status = True

args = module.parser.parse_args()

if args.show: # show config data
    module.list_config()

if args.n: # create new word space
    wordSpaceName = input("새로운 wordspace의 이름을 입력하세요>")
    module.create_wordSpace(wordSpaceName)

if args.rm: # remove word space
    wordSpaceName = input("삭제할 wordspace의 이름을 입력하세요>")
    module.remove_wordSpace(wordSpaceName)

if args.l: # list wordspace
    module.list_wordSpace()

if args.alter: # change target workspace
    wordSpaceName = input("checkout할 wordspace의 이름을 입력하세요>")
    module.alter_target(wordSpaceName)

if args.test: # exist for testing
    module.test_fuction()

if args.make: # create word cards with word space data
    module.create_wordCard()

if args.m: # migrate json data
    module.migrate_config()

def BotHandle(msg):
    content, chat, id = telepot.glance(msg)
    print(content, chat, id)
    
    module.LoadJson()
    # if id == module.userId:
    if content == 'text':
        if msg[content] == '/migrate':
            module.migrate_config()
            exit()
        elif msg[content] == '/show':
            module.list_config()
            exit()
        elif msg[content][0:4] == '/new':
            wordSpaceName = msg[content][5:]
            module.create_wordSpace(wordSpaceName)
            exit()
        elif msg[content][0:7] == '/remove':
            wordSpaceName = msg[content][8:]
            module.remove_wordSpace(wordSpaceName)
            exit()
        elif msg[content] == '/list':
            module.list_wordSpace()
            exit()
        elif msg[content][0:9] == '/checkout':
            wordSpaceName = msg[content][10:]
            module.alter_target(wordSpaceName)
            exit()
        elif msg[content] == '/make':
            module.create_wordCard()
            # exit()
        elif msg[content] == '/help':
            module.list_function()
            exit()
        elif msg[content] == 'word':
            module.list_words()
        else:
            word = msg[content]
            module.add_word(word)
    else:
        module.bot.sendMessage(id, '아 뭐래')

module.bot.message_loop(BotHandle, run_forever=True)

while(True):
    time.sleep(10)
