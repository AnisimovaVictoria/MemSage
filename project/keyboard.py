from telebot import types


start_buttons = ["Познакомиться", "Посмотреть мем", "Добавить мем"]
mem_types = ['кошки', 'Пепе', 'мопсы', "Назад"]


def start():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for s in start_buttons:
        markup.add(s)
    return markup


def choose_mem():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for s in mem_types:
        markup.add(s)
    return markup

rem = types.ReplyKeyboardRemove

interview = [rem, rem, rem, rem, rem, start]