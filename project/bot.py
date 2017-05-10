import telebot
import os
from telebot import types
import time
import config
import keyboard
import text
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
# обработка команды /start
def start(mes):
    msg = bot.send_message(mes.chat.id, text.hello,
                           reply_markup=keyboard.start())
    bot.register_next_step_handler(msg, first_step)


def first_step(mes):
    if mes.text not in keyboard.start_menu:
        #норм?
        bot.register_next_step_handler(mes, first_step)
    else:
        # если пользователь на стартовой странице и ввел что-то адекватное
        if mes.text == keyboard.start_menu[0]:
            # Познакомиться
            msg = bot.send_message(mes.chat.id, text.questions[0],
                                   reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, interview(1))

        # Посмотреть мемес
        if mes.text == keyboard.start_menu[1]:
            msg = bot.send_message(mes.chat.id, "Выбери тип:",
                                   reply_markup=keyboard.choose_mem())
            bot.register_next_step_handler(msg, choose_mem)
        # Добавить мемес
        if mes.text == keyboard.start_menu[2]:
            msg = bot.send_message(mes.chat.id, "Я пока этого не умею(")
            bot.register_next_step_handler(msg, add_mem)


def interview(i):
    def ask_question(mes):
        # кидать ошибку если номер текущего вопроса больше, чем нужно
        # вот тут нужно заносить данные в базу, а не просто печатать
        print(mes.text)
        msg = bot.send_message(mes.chat.id, text.questions[i],
                               reply_markup=keyboard.interview[i]())
        if i == len(text.questions) - 1:
            bot.register_next_step_handler(msg, first_step)
        else:
            bot.register_next_step_handler(msg, interview(i+1))
    return ask_question


def choose_mem(mes):
    pass


def add_mem(mes):
    pass

if __name__ == '__main__':
    # возможно без none_stop = True
    bot.polling(none_stop=True)
