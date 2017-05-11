from telebot import types


start_menu = ["Посмотреть мем", "Добавить мем", "Найти друзей)"]
mem_types = ['Хот', "Трендинг", 'Свежак', 'По категориям', "Назад 🔙"]
mem_categories = ['Кошки', 'Пепе', 'Мопсы', "Назад 🔙"]


def start():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    for s in start_menu:
        markup.add(s)
    return markup


def choose_mem():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    for s in mem_types:
        markup.add(s)
    return markup


def mem():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    markup.add("◀", "❤", "▶")
    markup.add("Назад 🔙")
    return markup

rem = types.ReplyKeyboardRemove

interview = [rem, rem, rem, rem, rem, start]
