import requests
import sys, time, json, os, argparse, random, re
from bs4 import BeautifulSoup
from datetime import datetime
from os import listdir
from PIL import Image, ImageDraw, ImageFont
import telepot
import pyttsx3

def print_and_message(id, string):
    print(string)
    bot.sendMessage(id, string)

def json_load(): # json file load
    with open('config.json', 'r', encoding='UTF-8') as config:
        global data
        data = config.read()
        global configData
        configData = json.loads(data)
        global targetFile
        targetFile = configData['DATASET']['target']
        global fontPathKO
        fontPathKO = configData['DATASET']['fontPathKO']
        global fontPathEN
        fontPathEN = configData['DATASET']['fontPathEN']
        global cardWidth
        cardWidth = configData['DATASET']['cardWidth']
        global cardHeight
        cardHeight = configData['DATASET']['cardHeight']
        global BGColors
        BGColors = [configData['DATASET']['colors']['1'],configData['DATASET']['colors']['2'],configData['DATASET']['colors']['3'],configData['DATASET']['colors']['4']]
        # try:
        global filePath
        filePath = configData['WordSpaces'][targetFile]['Path']
        # except:
        #     # global targetFilePath
        #     filePath = configData['WordSpaces']['default.txt']['Path']
        global dayInterval
        dayInterval = configData['DATASET']['interval']
    with open('token.json', 'r', encoding='UTF-8') as private_config:
        global private_data
        private_data = private_config.read()
        global private_configData
        private_configData = json.loads(private_data)
        global token
        token = private_configData['Bot']['token']
        global userId
        userId = private_configData['Bot']['userID']['master']
    print("[LOG]json file loaded successfully!")

def chatbot_init():
    global bot
    bot = telepot.Bot(token) # init bot
    print_and_message(userId, "안녕하세요 저는 와이즈 입니다!")

def args_init(): # arguments
    global parser
    parser = argparse.ArgumentParser() # args parser 
    parser.add_argument("-show", help="list config file-DATASET", action="store_true")
    parser.add_argument("-n", help="create new word space", action="store_true")
    parser.add_argument("-l", help="list word spaces", action="store_true")
    parser.add_argument("-m", help="migrate config file", action="store_true")
    parser.add_argument("-rm", help="remove wordSpace",action="store_true")
    parser.add_argument("-make", help="make words to Image",action="store_true")
    parser.add_argument("-test", help="test args", action="store_true")
    parser.add_argument("-alter", help="change target file", action="store_true")
    print("[LOG]args loaded successfully!")

def list_config(): # List config Data
    print("-------------------------------------\n")
    print_and_message(userId, "지금 당신의 타겟 wordSpace는 : '" + targetFile + "' 입니다.")
    print(userId, "dayInterval : " + str(dayInterval) + "\n")
    print("-------------------------------------")
    sys.exit()

def create_wordSpace(wordSpaceName): # Create new Word Space
    newFileName = wordSpaceName
    newFilePath = "res/word/" + newFileName + ".txt"
    try:
        try:
            os.mkdir("res/result/"+newFileName)
            print_and_message(userId, "'res/result/"+newFileName+"'을 생성하였습니다.")
        except:
            print_and_message(userId, "'res/result/"+newFileName+"'이 이미 존재합니다.(파일 생성 실패)")
        newFile = open(newFilePath, "x", encoding="UTF-8")
        print_and_message(userId,"[LOG] '" + newFilePath + "' 가 생성되었습니다.")
        newFile = open(newFilePath, "w", encoding="UTF-8")
        now = datetime.now()
        createDate = now.strftime("%Y%m%d\n")
        newFile.write(createDate)
        tmp = {newFileName+".txt":{"CreateDay":createDate[0:8],"Path":newFilePath,"resultPath":"res/result/"+newFileName, "wordCount":0}}
        configData['WordSpaces'].update(tmp)
        with open('config.json', 'w', encoding='UTF-8') as config: # read config file
            json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
    except:
        print_and_message(userId,"[LOG]" + newFilePath + "가 이미 존재 합니다.")

    sys.exit()

def remove_wordSpace(wordSpaceName): # remove a wordspace
    rmFileName = wordSpaceName
    rmFileName += ".txt"
    # permission = input("'"+rmFileName+"'을 정말 삭제 하시겠습니까?(y/n) ")
    # if(permission == 'y' or permission == 'Y'):
    for wordFile in os.listdir('res/word'):
        # print_and_message(userId,wordFile)
        if(wordFile == rmFileName):
            # remove
            try:
                os.remove("res/word/" + rmFileName)
                del configData['WordSpaces'][rmFileName]
                with open('config.json', 'w', encoding='UTF-8') as config: # read config file
                    json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
                try: # rmdir
                    os.rmdir("res/result/"+rmFileName[0:-3])
                    print_and_message(userId,"'res/result/"+rmFileName[0:-3]+"'를 성공적으로 제거했습니다.")
                except:
                    print_and_message(userId,"'res/result/"+rmFileName[0:-3]+"'제거에 실패하였습니다.")
            except:
                print_and_message(userId,"'"+rmFileName+"'이 존재하지 않습니다.")
                exit()
            print_and_message(userId,"'"+rmFileName+"'를 성공적으로 제거했습니다.")
            exit()
    # elif(permission == 'n' or permission == 'N'):
    #     print_and_message(userId,"'" + rmFileName + "'제거를 취소하셨습니다.")
    # #     exit()
    # else:
    #     print_and_message(userId,"잘못된 입력, " + permission)
    exit()

def list_wordSpace(): # list wordspaces
    wordList = os.listdir('res/word')
    print_and_message(userId, "현재 wordSpace들의 목록입니다!")
    for fileName in wordList:
        print_and_message(userId, fileName)

def alter_target(wordSpaceName): # checkout target
    isExist = False
    # checkout = input("이동할 WordSpace의 이름을 입력하세요>")
    checkout = wordSpaceName
    checkout += ".txt"
    for wordFile in os.listdir('res/word'):
        if(wordFile == checkout):
            isExist = True
            configData['DATASET']['target'] = checkout
            with open('config.json', 'w', encoding='UTF-8') as config: # read config file
                json.dump(configData, config, ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
                print_and_message(userId,"now your target : " + checkout)
                exit()
    if(isExist == False):
        print_and_message(userId,"[ERROR]there is no such a file name : " + checkout)
    sys.exit()

def test_fuction(): # existing for testing
    print_and_message(userId,'test')
    sys.exit()

def create_wordCard():
    wordSpace = open(configData['WordSpaces'][targetFile]['Path'],'r',encoding='UTF-8')
    resultPath = configData['WordSpaces'][targetFile]['resultPath']
    wordFont = ImageFont.truetype(fontPathKO, 70)
    meaningFont = ImageFont.truetype(fontPathKO, 20)
    wordSpaceFont = ImageFont.truetype(fontPathKO, 15)
    print(wordSpace.readline())
    wordCount = configData['WordSpaces'][targetFile]['wordCount']
    for word in range(wordCount):
        word = wordSpace.readline()
        wordData = word.split(',')
        word = wordData[1]
        meaning = wordData[2]
        print(word)
        print(meaning)
        wordCard = Image.new(mode = "RGB", size = (cardWidth, cardHeight), color=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
        drawingLayer = ImageDraw.Draw(wordCard)
        drawingLayer.text((30, 30), targetFile, font=wordSpaceFont, fill=(0,0,0))
        drawingLayer.text((30,60), word, font=wordFont, fill = (0,0,0))
        drawingLayer.text((50,140), meaning, font=meaningFont, fill=(0,0,0))
        wordCard.save(resultPath+'/'+word+'.png')
        bot.sendPhoto(userId, photo=open(resultPath+'/'+word+'.png', 'rb'))

def migrate_config():
    for wordFile in os.listdir('res/word'):
        wordFilePath = 'res/word/'+wordFile
        f = open(wordFilePath, 'r', encoding='UTF-8')
        createDay = f.readline()
        wordCount = 0
        for line in f:
            wordCount += 1
        tmp = {wordFile:{"CreateDay":createDay[0:8],"Path":wordFilePath,"resultPath":"res/result/"+wordFile[0:-4],"wordCount":wordCount}}
        configData['WordSpaces'].update(tmp)
        print_and_message(userId, "Word space update : " + wordFile)
        with open('config.json', 'w', encoding='UTF-8') as config: # read config file
            json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name

def isMeaning(word2find):
    url = "http://endic.naver.com/search.nhn?query=" + word2find
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    try:
        meaning = soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text() +"\n"
        return meaning
    except:
        return '그런 단어는 없습니다 ㅠㅠ\n'

def add_word(word):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d/%H:%M")
    wordMeaing = isMeaning(word)
    newWord = date_time + ", " + word + ", "
    newWord += isMeaning(word)
    configData['WordSpaces'][targetFile]['wordCount'] += 1
    with open('config.json', 'w', encoding='UTF-8') as config: # read config file
        json.dump(configData, config, ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
    print(configData['WordSpaces'][targetFile]['wordCount'])
    f = open(filePath, "a+", encoding='UTF-8')
    f.write(newWord)
    f.close()
    print_and_message(userId, wordMeaing)
    print(newWord)

def list_function():
    print_and_message(userId, "/new - 새로운 Word Space를 만듭니다.")
    print_and_message(userId, "/remove - Word Space를 삭제합니다.")
    print_and_message(userId, "/list - 생성된 Word Space들을 보여줍니다.")
    print_and_message(userId, "/show - 사용자의 config data를 보여줍니다.")
    print_and_message(userId, "/checkout - 현재 단어를 추가하고 있는 Word Space를 변경합니다.")
    print_and_message(userId, "/make - Word Space를 기반으로 단어 카드를 제작합니다.")
    print_and_message(userId, "/new - 새로운 Word Space를 만듭니다.")
    print_and_message(userId, "/migrate - 오류가 있을 시 실제 데이터에 맞게 config data를 수정합니다.")

def BotHandle(msg):
    content, chat, id = telepot.glance(msg)
    print("new message")
    print(content, chat, id)
    return content
