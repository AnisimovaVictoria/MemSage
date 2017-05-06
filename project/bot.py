import telebot
import os
import time
import config
import keyboard
from telebot import types
from enum import Enum
import text
bot = telebot.TeleBot(config.token)

st = Enum('st', 'start interview choosing adding')
status = {}
curr_question = {}
curr_mem_type = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = keyboard.start()
    bot.send_message(message.chat.id, "Что ты хочешь?", reply_markup=markup)
    status[message.chat.id] = st.start


@bot.message_handler(func=lambda message: True, content_types=['text'])
def request(message):
    c = message.chat.id
    if c not in status:
        status[c] = st.start

    if message.text in keyboard.start_buttons and status[c] == st.start:
        if message.text == keyboard.start_buttons[0]:
            status[c] = st.interview
            curr_question[c] = 0
            bot.send_message(c, text.questions[0],
                             reply_markup=types.ReplyKeyboardRemove())
        if message.text == keyboard.start_buttons[1]:
            status[c] = st.choosing
            bot.send_message(c, "Выбери тип:",
                             reply_markup=keyboard.choose_mem())
        if message.text == keyboard.start_buttons[2]:
            status[c] = st.adding
        return

    if status[c] == st.interview:
        # кидать ошибку если номер текущего вопроса больше, чем нужно
        # заносить данные в базу
        curr_question[c] += 1
        q = curr_question[c]
        bot.send_message(c, text.questions[q],
                         reply_markup=keyboard.interview[q]())
        if q == len(text.questions) - 1:
            status[c] = st.start

    if message.text in keyboard.mem_types and status[c] == st.choosing:
        if message.text == keyboard.mem_types[-1]:
            status[c] = st.start
            bot.send_message(c, "Что ты хочешь?", reply_markup=keyboard.start())
        else:
            curr_mem_type[c] = message.text
            for file in os.listdir('C:/Users/1/Downloads/' + message.text + '/'):
                if file.split('.')[-1] in config.image_types:
                    f = open('C:/Users/1/Downloads/' + message.text + '/' + file, 'rb')
                    res = bot.send_photo(c, f)
                    for i in res.photo:
                        print(i.file_id, i.width, i.height)
                time.sleep(1)
            bot.send_message(c, "Продолжаем разговор", reply_markup=keyboard.choose_mem())


if __name__ == '__main__':
    bot.polling(none_stop=True)
