import requests
import sys, time, json, os, argparse, random, re
from bs4 import BeautifulSoup
from datetime import datetime
from os import listdir
from PIL import Image, ImageDraw, ImageFont
import telepot
import pyttsx3

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
        try:
            global filePath
            filePath = configData['WordSpaces'][targetFile]['Path']
        except:
            # global filePath
            filePath = configData['WordSpaces']['words.txt']['Path']
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

def list_config(): # List config Data
    print("-------------------------------------\n")
    print("target : " + targetFile)
    print("dayInterval : " + str(dayInterval) + "\n")
    print("-------------------------------------")
    sys.exit()

def create_wordSpace(): # Create new Word Space
    newFileName = input("새로운 WordSpace의 이름을 입력하세요>")
    newFilePath = "res/word/" + newFileName + ".txt"
    # os.mkdir("res/result/", newFileName)
    try:
        try:
            os.mkdir("res/result/"+newFileName)
            print("'res/result/"+newFileName+"'을 생성하였습니다.")
        except:
            print("'res/result/"+newFileName+"'이 이미 존재합니다.(파일 생성 실패)")
        newFile = open(newFilePath, "x", encoding="UTF-8")
        print("[LOG] '" + newFilePath + "' 가 생성되었습니다.")
        newFile = open(newFilePath, "w", encoding="UTF-8")
        now = datetime.now()
        createDate = now.strftime("%Y%m%d\n")
        newFile.write(createDate)
        tmp = {newFileName+".txt":{"CreateDay":createDate[0:8],"Path":newFilePath,"resultPath":"res/result/"+newFileName, "wordCount":0}}
        configData['WordSpaces'].update(tmp)
        with open('config.json', 'w', encoding='UTF-8') as config: # read config file
            json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
    except:
        print("[LOG]" + newFilePath + "가 이미 존재 합니다.")

    sys.exit()

def remove_wordSpace(): # remove a wordspace
    rmFileName = input("지울 WordSpace의 이름을 입력하세요>")
    rmFileName += ".txt"
    permission = input("'"+rmFileName+"'을 정말 삭제 하시겠습니까?(y/n) ")
    if(permission == 'y' or permission == 'Y'):
        for wordFile in os.listdir('res/word'):
            # print(wordFile)
            if(wordFile == rmFileName):
                # remove
                try:
                    os.remove("res/word/" + rmFileName)
                    del configData['WordSpaces'][rmFileName]
                    with open('config.json', 'w', encoding='UTF-8') as config: # read config file
                        json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
                    try: # rmdir
                        os.rmdir("res/result/"+rmFileName[0:-3])
                        print("'res/result/"+rmFileName[0:-3]+"'를 성공적으로 제거했습니다.")
                    except:
                        print("'res/result/"+rmFileName[0:-3]+"'제거에 실패하였습니다.")
                except:
                    print("'"+rmFileName+"'이 존재하지 않습니다.")
                    sys.exit()
                print("'"+rmFileName+"'를 성공적으로 제거했습니다.")
                sys.exit()
    elif(permission == 'n' or permission == 'N'):
        print("'" + rmFileName + "'제거를 취소하셨습니다.")
        sys.exit()
    else:
        print("잘못된 입력, " + permission)
    sys.exit()

def list_wordSpace(): # list wordspaces
    wordList = os.listdir('res/word')
    for fileName in wordList:
        print(fileName)
    sys.exit()

def alter_target(): # checkout target
    isExist = False
    checkout = input("이동할 WordSpace의 이름을 입력하세요>")
    checkout += ".txt"
    for wordFile in os.listdir('res/word'):
        # print(wordFile)
        if(wordFile == checkout):
            configData['DATASET']['target'] = checkout
            with open('config.json', 'w', encoding='UTF-8') as config: # read config file
                json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
                print("now your target : " + checkout)
                isExist = True
                exit()
    if(isExist == False):
        print("[ERROR]there is no such a file name : " + checkout)
    sys.exit()

def test_fuction(): # existing for testing
    print('test')
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
        # print(word)
        wordData = word.split(',')
        word = wordData[1]
        meaning = wordData[2]
        # print(wordData)
        print(word)
        print(meaning)
        BGrandom = random.randrange(1,4)
        # wordCard = Image.new(mode = "RGB", size = (cardWidth, cardHeight), color=(BGColors[BGrandom][0],BGColors[BGrandom][1],BGColors[BGrandom][2]))
        wordCard = Image.new(mode = "RGB", size = (cardWidth, cardHeight), color=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
        drawingLayer = ImageDraw.Draw(wordCard)
        drawingLayer.text((30, 30), targetFile, font=wordSpaceFont, fill=(0,0,0))
        drawingLayer.text((30,60), word, font=wordFont, fill = (0,0,0))
        drawingLayer.text((50,140), meaning, font=meaningFont, fill=(0,0,0))
        # drawingLayer.text((50,50), str(word), font=fontPathKO, fill=(255,0,0))
        wordCard.save(resultPath+'/'+word+'.png')
    sys.exit()

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
        print("Word space update : " + wordFile)
        with open('config.json', 'w', encoding='UTF-8') as config: # read config file
            json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
    sys.exit()

def isMeaning(word2find):
    url = "http://endic.naver.com/search.nhn?query=" + word2find
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    try:
        meaning = soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text() +"\n"
        return meaning
    except:
        return '그런 단어는 없습니다 ㅠㅠ\n'