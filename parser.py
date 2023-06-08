import requests
from bs4 import BeautifulSoup as BS
import telebot
from telebot import types
import emoji

# ---КЛАСС ДЛЯ СПЕКТАКЛЕЙ---
class Shows(object):
    def __init__(self, i, d, m, d_o_w, n, s, h, img):
        self.num = i
        self.day = d
        self.month = m
        self.day_of_week = d_o_w
        self.name = n
        self.start = s
        self.href = h
        self.img = img

# ---ПАРСИНГ---

url = "https://www.opera21.ru/"

response = requests.get(url)

soup = BS(response.text, "lxml")

names = soup.find_all("div", class_="col-md-6 col-sm-6")
days = soup.find_all("div", class_="event-d mec-color")
months = soup.find_all("div", class_="event-f")
days_of_week = soup.find_all("div", class_="event-da")
starts = soup.find_all("div", class_="mec-event-loc-place")
hrefs = soup.find_all("a", class_="mec-color-hover")

imgs = []

for i in hrefs:
    urlD = i.get("href")

    resp = requests.get(urlD)

    txt = BS(resp.text, "lxml")

    temp = txt.find("img", class_="vc_single_image-img attachment-full lazyload")
    if temp != None:
        imgs.append(temp.get("data-src"))
    else:
        imgs.append('None')

for i in range(len(imgs)):
    start = -1
    count = 0
    while True:
        start = imgs[i].find(".", start+1)
        if start == -1:
            break
        count += 1
    if count != 3:
        imgs[i] = 'None'

count = len(names)

s = ""

shows = []

for i in range(count):
    day = days[i].text
    month = months[i].text
    day_of_week = days_of_week[i].text
    name = names[i].find("h4").text
    start = starts[i].text
    href = hrefs[i].get("href")
    img = imgs[i]
    shows.append(Shows(i+1, day, month, day_of_week, name, start, href, img))
    s = s + str(i+1) + ". " + day + " " + month + " " + day_of_week + "\n<b>" + name + "</b>\n" + start + "\n\n"
    

# ---БОТ---
bot = telebot.TeleBot('6274287639:AAEzFIb-ke9MMfL962C1dZWeDd9Gh3dLEi4')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    website = types.KeyboardButton('Сайт')
    information = types.KeyboardButton('Спектакли')

    markup.add(website, information)
    bot.send_message(message.chat.id, '<b>Спасибо за использование нашего бота. Мы ценим это!</b>', parse_mode='html',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Сайт':
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton('Перейти на сайт', url='https://www.opera21.ru/'))
        bot.send_message(message.chat.id, "Нажмите на кнопку ниже.", reply_markup=markup2)
    elif message.text == 'Спектакли':
        bot.send_message(message.chat.id, s, parse_mode='html')
    else:
        flag = True
        for i in range(len(shows)):
            if (message.text.isnumeric()) and (int(message.text) == shows[i].num):
                if shows[i].img != 'None':
                    image = shows[i].img
                    bot.send_photo(message.chat.id, photo=image, caption=shows[i].day + " " + shows[i].month + " " + shows[i].day_of_week + "\n<b>" + shows[i].name + "</b>\n" + shows[i].start, parse_mode='html')
                else:
                    bot.send_message(message.chat.id, shows[i].day + " " + shows[i].month + " " + shows[i].day_of_week + "\n<b>" + shows[i].name + "</b>\n" + shows[i].start, parse_mode='html')    
                flag = False
        if flag:
            bot.send_message(message.chat.id, '<b>Я не понимаю вашей команды!</b> ' + emoji.emojize(':alien_monster:'), parse_mode='html')    

bot.polling(none_stop=True)