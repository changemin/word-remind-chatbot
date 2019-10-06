import telepot, time, os
import requests
from bs4 import BeautifulSoup

token = '842239728:AAHkLmG7HFQcswzOWuLeVO9RNoxNzkqGByA'
userId = '698241176'
bot = telepot.Bot(token)

bot.sendMessage(userId, "안녕하세요 저는 와이즈 입니다!")

status = True

def findWord(word):
    url = "http://endic.naver.com/search.nhn?query=" + word
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    meaning = soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text() +"\n"

    return meaning

def handle(msg):
    content, chat, id = telepot.glance(msg)
    print(content, chat, id)
    if content == 'text':
        word = content
        newWord = findWord(word)  
        print(findWord(word))
        bot.sendMessage(id, findWord(word))
        # if msg['text'] == 'word':
        #     bot.sendMessage(id, '오 단어를 찾고 싶으시군요')
    else:
        bot.sendMessage(id, '아 뭐래')

bot.message_loop(handle)

while(True):
    time.sleep(10)