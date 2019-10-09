import requests
import sys, time, json, os, argparse, random, re
from bs4 import BeautifulSoup
from datetime import datetime
from os import listdir
from PIL import Image, ImageDraw, ImageFont
import telepot

with open('config.json', 'r', encoding='UTF-8') as config: # read config file
    data = config.read()
    configData = json.loads(data)
    targetFile = configData['DATASET']['target']
    fontPathKO = configData['DATASET']['fontPathKO']
    fontPathEN = configData['DATASET']['fontPathEN']
    #for x in range(3):
    BGColors = [configData['DATASET']['colors']['1'],configData['DATASET']['colors']['2'],configData['DATASET']['colors']['3'],configData['DATASET']['colors']['4']]
        # print(configData['DATASET']['colors'][str(x+1)])
    try:
        filePath = configData['WordSpaces'][targetFile]['Path']
    except:
        filePath = configData['WordSpaces']['words.txt']['Path']
    dayInterval = configData['DATASET']['interval']

parser = argparse.ArgumentParser() # args parser
parser.add_argument("-show", help="list config file-DATASET", action="store_true")
parser.add_argument("-n", help="create new word space", action="store_true")
parser.add_argument("-l", help="list word spaces", action="store_true")
parser.add_argument("-m", help="migrate config file", action="store_true")
parser.add_argument("-rm", help="remove wordSpace",action="store_true")
parser.add_argument("-make", help="make words to Image",action="store_true")
parser.add_argument("-test", help="test args", action="store_true")
parser.add_argument("-checkout", help="change target file", action="store_true")

args = parser.parse_args()

if args.show: # show config data
    print("-------------------------------------\n")
    print("target : " + targetFile)
    print("dayInterval : " + str(dayInterval) + "\n")
    print("-------------------------------------")
    sys.exit()

if args.n: # create new word space
    newFileName = input("새로운 WordSpace의 이름을 aa입력하세요>")
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
        tmp = {newFileName+".txt":{"CreateDay":createDate[0:8],"Path":newFilePath,"resultPath":"res/word/"+newFileName, "wordCount":0}}
        configData['WordSpaces'].update(tmp)
        with open('config.json', 'w', encoding='UTF-8') as config: # read config file
            json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
    except:
        print("[LOG]" + newFilePath + "가 이미 존재 합니다.")

    sys.exit()

if args.rm:
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

if args.l: # list wordspace
    wordList = os.listdir('res/word')
    for fileName in wordList:
        print(fileName)
    sys.exit()

if args.checkout: # change target workspace
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
        print("there is no such a file name : " + checkout)
    sys.exit()

if args.test:
    print(BGColors)
    # for x in range(1):
    #     print(BGColors)
    sys.exit()

if args.make:
    wordSpace = open(configData['WordSpaces'][targetFile]['Path'],'r',encoding='UTF-8')
    resultPath = configData['WordSpaces'][targetFile]['resultPath']
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
        wordCard = Image.new(mode = "RGB", size = (200, 400), color=(BGColors[BGrandom][0],BGColors[BGrandom][1],BGColors[BGrandom][2]))
        # wordCard.text((50,50), word, font=fontPathKO, fill=(255,0,0))
        wordCard.save(resultPath+'/'+word+'.png')
    sys.exit()

if args.m:
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

if __name__ == "__main__":
    while(True): 
        with open('config.json', 'r', encoding='UTF-8') as config: # read config file
            data = config.read()
            configData = json.loads(data) # load json file
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d/%H:%M")
        targetFileName = configData['DATASET']['target']
        word = input("단어를 입력하세요(현재:"+targetFileName+')>')

        if word == "exit()": # interrupt
            sys.exit()

        url = "http://endic.naver.com/search.nhn?query=" + word
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        
        f = open(filePath, "a+", encoding="UTF-8") # open file append mode

        newWord = date_time + ", " + word + ", "
        
        try:
            newWord += soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text() +"\n"
            configData['WordSpaces'][targetFileName]['wordCount'] += 1
            with open('config.json', 'w', encoding='UTF-8') as config: # read config file
                json.dump(configData, config, ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
            f.write(newWord)
            f.close()
        except:
            newWord += "네이버 사전에 등재되어 있지 않아요 ㅠㅠ\n"
        print(newWord[0:-1])
