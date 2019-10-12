import module
import telepot
from datetime import datetime
import json, time

module.json_load() # load json data
module.args_init() # load args

bot = telepot.Bot(module.token) # init bot

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
