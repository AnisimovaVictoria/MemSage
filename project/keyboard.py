from telebot import types


main_menu = ["Посмотреть мем", "Добавить мем", "Найти друзей)"]
mem_types = ['Хот', "Трендинг", 'Свежак', 'По категориям', "Назад 🔙"]
mem_categories = ['Кошки', 'Пепе', 'Мопсы', "Назад 🔙"]
gender_types = ['ЛИНОЛЕУМ', 'ЛАМИНАТ', 'КОВРОЛИН', 'КЕРАМОГРАНИТ', 'ПАРКЕТ',
                'БРЕВЕНЧАТЫЙ', 'НАЛИВНОЙ']
sp_types = ["forever alone", "IN LOVE", "есть еда", "Все сложно"]
occupation_types = ["Студент", "Школяр", "Работаю", "Все сложно"]


def mem():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
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
                    make_markup(['Да', 'НЕТ']),make_markup(main_menu)]
