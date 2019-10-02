import requests
import sys, time, json, os, argparse
from bs4 import BeautifulSoup
from datetime import datetime
from os import listdir

with open('config.json', 'r', encoding='UTF-8') as config: # read config file
    data = config.read()
    configData = json.loads(data)
    targetFile = configData['DATASET']['target']
    filePath = configData['WordSpaces'][targetFile]['Path']
    dayInterval = configData['DATASET']['interval']

parser = argparse.ArgumentParser() # args parser
parser.add_argument("-show", help="list config file-DATASET", action="store_true")
parser.add_argument("-n", help="create new word space", action="store_true")
parser.add_argument("-l", help="list word spaces", action="store_true")
parser.add_argument("-m", help="migrate config file", action="store_true")
# parser.add_argument("-test", help="test args", action="store_true")
parser.add_argument("-checkout", help="change target file", action="store_true")

args = parser.parse_args()

if args.show: # show config data
    print("-------------------------------------\n")
    print("target : " + targetFile)
    print("dayInterval : " + str(dayInterval) + "\n")
    print("-------------------------------------")
    sys.exit()

if args.n: # create new word space
    newFileName = input("새로운 파일의 이름을 입력하세요>")
    newFilePath = "res/word/" + newFileName + ".txt"
    try:
        newFile = open(newFilePath, "x", encoding="UTF-8")
        print("[LOG] '" + newFilePath + "' 가 생성되었습니다.")
        newFile = open(newFilePath, "w", encoding="UTF-8")
        now = datetime.now()
        createDate = now.strftime("%Y%m%d")
        newFile.write(createDate)
    except:
        print("[LOG]" + newFilePath + "가 이미 존재 합니다.")

    sys.exit()

if args.l: # list wordspace
    wordList = os.listdir('res/word')
    for fileName in wordList:
        print(fileName)
    sys.exit()

if args.checkout: # change target workspace
    isExist = False
    checkout = input("checkout>")
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

if args.m:
    for wordFile in os.listdir('res/word'):
        wordFilePath = 'res/word/'+wordFile
        f = open(wordFilePath, 'r', encoding='UTF-8')
        createDay = f.readline()
        # print(createDay[0:8])
        wordCount = 0
        for line in f:
            wordCount += 1
        tmp = {wordFile:{"CreateDay":createDay[0:8],"Path":"res/word/"+wordFile,"wordCount":wordCount}}
        configData['WordSpaces'].update(tmp)
        print("Word space update : " + wordFile)
        with open('config.json', 'w', encoding='UTF-8') as config: # read config file
            json.dump(configData, config,ensure_ascii=False, indent=4, sort_keys=True) # save Korean name
    sys.exit()
    
while(True): 
    configData = json.loads(data) # load json file
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d/%H:%M")

    word = input("단어를 입력하세요(현재:"+configData['DATASET']['target']+')>')

    if word == "exit()": # interrupt
        sys.exit()

    url = "http://endic.naver.com/search.nhn?query=" + word
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    
    f = open(filePath, "a+", encoding="UTF-8") # open file append mode

    newWord = date_time + ", " + word + ", "
    
    try:
        newWord += soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text() +"\n"
        f.write(newWord)
        f.close()
    except:
        newWord += "네이버 사전에 등재되어 있지 않아요 ㅠㅠ\n"

    print(newWord[0:-1])
