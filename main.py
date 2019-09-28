import requests
import sys, time, json, os, argparse
from bs4 import BeautifulSoup
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-m", help="migrate functions", action="store_true")
args = parser.parse_args()

if args.m:
    print("here is argparser 'm'")

with open('config.json') as json_file:
    data = json.load(json_file)

    wordFilePath = str(data['Path']['wordFile'])

while(True):
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y/%H:%M")

    word = input("단어를 입력하세요>")
    if word == "@":
        sys.exit()

    url = "http://endic.naver.com/search.nhn?query=" + word
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    filePath = "res/word/words.txt"
    f = open(filePath, "r", encoding="UTF-8")
    # print(f.read())

    result = date_time + ", " + word + ", "
    try:
        result += soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text()
    except:
        result = "네이버 사전에 등재되어 있지 않습니다."
    print(result)
