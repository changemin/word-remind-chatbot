import requests
import sys, time, json, os, argparse
from bs4 import BeautifulSoup
from datetime import datetime

parser = argparse.ArgumentParser()
#parser.add_argument("-m", help="migrate functions", action="store_true")
args = parser.parse_args()

# if args.m:
#     print("here is argparser 'm'")

with open('config.json') as json_file: # read config file
    data = json.load(json_file)
    wordFilePath = str(data['Path']['wordFile'])

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
