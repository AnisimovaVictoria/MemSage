import sys
import config
import telebot
import text
import os
import time
from python_db import *
from keyboard import *

memes = {}  # кешированные мемы
curr_mem = {}  # текущий мем каждого польователя
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
# обработка команды /start
def start(mes):
    msg = bot.send_message(mes.chat.id, text.hello + text.questions[0])
    bot.register_next_step_handler(msg, interview(1, [mes.from_user.id]))


@bot.message_handler(commands=['continue'])
def cont(mes):
    msg = bot.send_message(mes.chat.id, "И снова здравствуйте! Чем изволите"
                                        " себя развлекать?",
                           reply_markup=make_markup(menu_list))
    bot.register_next_step_handler(msg, main_menu)


@bot.message_handler(commands=['add_memes'])
def cont(mes):
    for category in mem_categories:
        for file in os.listdir('C:/Users/1/Downloads/' + category + '/'):
            if file.split('.')[-1] in config.image_types:
                f = open('C:/Users/1/Downloads/' + category + '/' + file, 'rb')
                msg = bot.send_photo(mes.chat.id, f)
                res = [msg.photo[-1].file_id, category, 0]
                set_mem(res, curs, conn)
                time.sleep(1)


def interview(i, res):
    def ask_question(mes):
        res.append(mes.text)
        msg = bot.send_message(mes.chat.id, text.questions[i],
                               reply_markup=interview_markup[i])
        if i == len(text.questions) - 1:
            print(res)
            if res[-1] == "Да":  #потому что is_hikka != хочу находить друзей
                res[-1] = False
            else:
                res[-1] = True
            res[-2] = text_format.transliterate(res[-2])

            set_user(res, curs=curs, conn=conn)
            bot.register_next_step_handler(msg, main_menu)
        else:
            bot.register_next_step_handler(msg, interview(i+1, res))
    return ask_question


def main_menu(mes):
    if mes.text not in menu_list:
        bot.register_next_step_handler(mes, main_menu)
    else:
        # Посмотреть мемес
        if mes.text == menu_list[0]:
            msg = bot.send_message(mes.chat.id, "Выбери тип:",
                                   reply_markup=markup_with_back(mem_types))
            bot.register_next_step_handler(msg, choose_mem)
        # Добавить мемес
        if mes.text == menu_list[1]:
            msg = bot.send_message(mes.chat.id, "Ура! Новые мемы)))"
                                                "Первым делом скажи, к какой"
                                                "категории отнемти этот мем?",
                                   reply_markup=markup_with_back(mem_categories))
            bot.register_next_step_handler(msg, add_mem)


def choose_mem(mes):
    c = mes.chat.id
    if mes.text == back:
        msg = bot.send_message(c, "Что ты хочешь?",
                               reply_markup=make_markup(menu_list))
        bot.register_next_step_handler(msg, main_menu)
        return
    if mes.text in mem_types:
        if mes.text == mem_types[-1]:
            msg = bot.send_message(c, "Популярное среди чего?",
                                   reply_markup=markup_with_back(popular_types))
            bot.register_next_step_handler(msg, popular)
            return

        funcs = {mem_types[0]: find_hot_stuff, mem_types[1]: find_new_stuff}
        func = funcs[mes.text]
        i = func(curs)
        memes[c] = i
        if len(memes[c]) > 0:
            curr_mem[c] = 0
            msg = bot.send_photo(c, memes[c][0][0], reply_markup=mem())
            bot.register_next_step_handler(msg, memming)
        else:
            msg = bot.send_message(c, "Тут пока ничего нет("
                                      "Выбери что-то другое",
                                   reply_markup=markup_with_back(mem_types))
            bot.register_next_step_handler(msg, choose_mem)
    else:
        bot.register_next_step_handler(mes, choose_mem)


def popular(mes):
    c = mes.chat.id
    if mes.text == back:
        msg = bot.send_message(c, "Что ты хочешь?",
                               reply_markup=make_markup(menu_list))
        bot.register_next_step_handler(msg, main_menu)
        return

    if mes.text in popular_types:
        bot.send_message(c, "Выбери", reply_markup=markup_with_back(popular_dict[mes.text]))
        bot.register_next_step_handler(mes, popular2(mes.text))
        return
    else:
        bot.register_next_step_handler(mes, choose_mem)


def popular2(pop_type):
    def handle(mes):
        c = mes.chat.id
        if mes.text == back:
            bot.send_message(mes.chat.id, "не понял(",
                             reply_markup=markup_with_back(popular_types))
            bot.register_next_step_handler(mes, popular)
            return

        memes[c] = popular_func[pop_type](mes.text, curs)
        if len(memes[c]) > 0:
            curr_mem[c] = 0
            msg = bot.send_photo(c, memes[c][0][0], reply_markup=mem())
            bot.register_next_step_handler(msg, memming)
        else:
            msg = bot.send_message(c, "Тут пока ничего нет("
                                      "Выбери что-то другое",
                                   reply_markup=markup_with_back(popular_types))
            bot.register_next_step_handler(msg, popular)

    return handle


def memming(mes):
    c = mes.chat.id
    if mes.text == back:
        msg = bot.send_message(c, "Выбери",
                               reply_markup=markup_with_back(mem_types))
        bot.register_next_step_handler(msg, choose_mem)
        return

    if mes.text not in mem_resp:
        msg = bot.send_message(c, "что-то я не понял( попробуй еще раз",
                               reply_markup=mem())
        bot.register_next_step_handler(msg, memming)
        return
    if mes.text == mem_resp[1]:
        like(mes.from_user.id, memes[c][curr_mem[c]][1], curs, conn)
        bot.register_next_step_handler(mes, memming)
        return

    n = len(memes[c])
    if mes.text == mem_resp[0]:
        curr_mem[c] = (curr_mem[c]-1+n) % n
    if mes.text == mem_resp[2]:
        curr_mem[c] = (curr_mem[c]+1) % n

    msg = bot.send_photo(c, memes[c][curr_mem[c]][0], reply_markup=mem())
    bot.register_next_step_handler(msg, memming)


def add_mem(mes):
    c = mes.chat.id
    if mes.text == back:
        msg = bot.send_message(c, "Что ты хочешь?",
                               reply_markup=make_markup(menu_list))
        bot.register_next_step_handler(msg, main_menu)
        return

    if mes.text not in mem_categories:
        msg = bot.send_message(c, "Выбери одну из предложенных категорий",
                         reply_markup=markup_with_back(mem_categories))
        bot.register_next_step_handler(msg, add_mem)
    else:
        msg = bot.send_message(c, "Теперь отправь картинку)")
        bot.register_next_step_handler(msg, add_mem2(mes.text))


def add_mem2(category):
    def final_adding(mes):
        res = [mes.photo[-1].file_id, category, 0]
        set_mem(res, curs,conn)
        bot.send_message(mes.chat.id, "Ура! Новый мемес) "
                                      "Го ещё))000", reply_markup=markup_with_back(mem_categories))
        bot.register_next_step_handler(mes, add_mem)
    return final_adding


if __name__ == '__main__':
    conn = con_db()
    curs = conn.cursor()
    bot.polling(none_stop=True)
    curs.close()

