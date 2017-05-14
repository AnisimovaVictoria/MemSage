from telebot import types


menu_list = ["Посмотреть мем", "Добавить мем", "Найти друзей)"]
mem_types = ['Хот', "Трендинг", 'Свежак', 'Популярное',
             "Назад 🔙"]
popular_types = ["Категорий", "Жителей города на выбор", "Представителей одного из полов",
                 "Коллег", "Людей с однаковым сп", "Назад 🔙"]

mem_categories = ['Кошки', 'Пепе', 'Мопсы', "Назад 🔙"]
gender_types = ['ЛИНОЛЕУМ', 'ЛАМИНАТ', 'КОВРОЛИН', 'КЕРАМОГРАНИТ', 'ПАРКЕТ',
                'БРЕВЕНЧАТЫЙ', 'НАЛИВНОЙ']
sp_types = ["FOREVER ALONE((", "IN LOVE", "ЕСТЬ ЕДА", "ВСЕ ОЧЕНЬ СЛОЖНА"]
occupation_types = ['pre!shkolyar', 'shkolyar', 'fiztech!shkolyar', 'post!shkolyar']
mem_resp = ["◀", "❤", "▶", "Назад 🔙"]

def mem():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("◀", "❤", "▶")
    markup.add("Назад 🔙")
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
