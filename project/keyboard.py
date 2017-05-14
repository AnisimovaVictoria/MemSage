from telebot import types
from python_db import *

back = "Назад 🔙"

menu_list = ["Посмотреть мем", "Добавить мем"]
mem_types = ['Хот', 'Свежак', 'Популярное']
popular_types = ["Категорий", "Жителей города на выбор",
                 "Представителей одного из полов",
                 "Коллег", "Людей с одним сп"]

mem_categories = ["Кошки", "Собаки", "Другие животные", "Люди", "Учеба",
                  "Странное", "Смешные", "Крутые", "Фильмы"]
gender_types = ['ЛИНОЛЕУМ', 'ЛАМИНАТ', 'КОВРОЛИН', 'КЕРАМОГРАНИТ', 'ПАРКЕТ',
                'БРЕВЕНЧАТЫЙ', 'НАЛИВНОЙ']
sp_types = ["FOREVER ALONE((", "IN LOVE", "ЕСТЬ ЕДА", "ВСЕ ОЧЕНЬ СЛОЖНА"]
occupation_types = ['pre!shkolyar', 'shkolyar', 'fiztech!shkolyar',
                    'post!shkolyar']
popular_dict = {popular_types[0]: mem_categories,
                popular_types[1]: get_all_cities,
                popular_types[2]: gender_types,
                popular_types[3]: occupation_types,
                popular_types[4]: sp_types}
popular_func = {popular_types[0]: most_popular_by_category}
mem_resp = ["◀", "❤", "▶"]


def mem():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("◀", "❤", "▶")
    markup.add(back)
    return markup


def markup_with_back(args):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    for s in args:
        markup.add(s)
    markup.add(back)
    return markup


def make_markup(args):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    for s in args:
        markup.add(s)
    return markup


rem = types.ReplyKeyboardRemove()
interview_markup = [rem, make_markup(gender_types), make_markup(sp_types),
                    make_markup(occupation_types), rem,
                    make_markup(['Да', 'НЕТ']), make_markup(menu_list)]
