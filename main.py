import requests
import sys, time, json, os, argparse
from bs4 import BeautifulSoup
from datetime import datetime

with open('config.json', 'r') as config: # read config file
    data = config.read()
    configData = json.loads(data)
    targetFile = configData['DATASET']['target']
    filePath = configData['Words'][targetFile]['Path']
    dayInterval = configData['DATASET']['interval']

parser = argparse.ArgumentParser() # args parser
parser.add_argument("-show", help="how json file", action="store_true")
parser.add_argument("-n", help="create new word space", action="store_true")
parser.add_argument("-checkout", help="change file to edit", action="store_true")

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
    except:
        print("[LOG]" + newFilePath + "가 이미 존재 합니다.")

    sys.exit()

if args.checkout:
    print("checkout")
    sys.exit()
    
while(True): 
    configData = json.loads(data) # load json file
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y/%H:%M")

    word = input("단어를 입력하세요>")

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

    print(newWord)
