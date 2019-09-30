import requests
import sys, time, json, os, argparse
from bs4 import BeautifulSoup
from datetime import datetime

with open('config.json') as json_file: # read config file
    data = json.load(json_file)
    wordFilePath = str(data['Path']['wordFile'])
    dayInteval = int(data['DATASET']['interval'])

parser = argparse.ArgumentParser() # args parser
parser.add_argument("-show", help="how json file", action="store_true")
parser.add_argument("-n", help="create new word space", action="store_true")
parser.add_argument('FileName', action='store', type=str, help='The text to parse.')
args = parser.parse_args()

if args.show: # show config data
    print("-------------------------------------\n")
    print("WordFilePath : " + wordFilePath)
    print("dayInterval : " + str(dayInteval) + "\n")
    print("-------------------------------------")

if args.n: # create new word space
    newFilePath = "res/word/" + args.FileName + ".txt"
    newFile = open(newFilePath, "a+", encoding="UTF-8")

while(True): 
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y/%H:%M")

    word = input("단어를 입력하세요>")
    if word == "exit()":
        sys.exit()

    url = "http://endic.naver.com/search.nhn?query=" + word
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    filePath = "res/word/words.txt"
    f = open(filePath, "a+", encoding="UTF-8") # open file append mode

    newWord = date_time + ", " + word + ", "
    
    try:
        newWord += soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text() +"\n"
        f.write(newWord)
        f.close()
    except:
        newWord += "네이버 사전에 등재되어 있지 않아요 ㅠㅠ\n"

    print(newWord)
