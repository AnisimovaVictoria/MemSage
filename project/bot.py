import sys
import config
import telebot
import text
import os
from python_db import *
from keyboard import *

conn = ''
curs = ''
bot = telebot.TeleBot(config.token)
memes = {} #кешированные мемы
curr_mem = {} #текущий мем каждого польователя


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


def interview(i, res):
    def ask_question(mes):
        res.append(mes.text)
        msg = bot.send_message(mes.chat.id, text.questions[i],
                               reply_markup=interview_markup[i])
        if i == len(text.questions) - 1:
            print(res)
            if res[-1] == "Да":  #потому что is_hikka != хочу находить друзей(
                res[-1] = False
            else:
                res[-1] = True

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
                                   reply_markup=make_markup(mem_types))
            bot.register_next_step_handler(msg, choose_mem)
        # Добавить мемес
        if mes.text == menu_list[1]:
            msg = bot.send_message(mes.chat.id, "Ура! Новые мемы)))"
                                                "Первым делом скажи, к какой"
                                                "категории отнемти этот мем?",
                                   reply_markup=make_markup(mem_categories))
            bot.register_next_step_handler(msg, add_mem)
        # Найти друзей
        if mes.text == menu_list[2]:
            find_friend(mes)
            bot.register_next_step_handler(mes.chat.id, main_menu)


def choose_mem(mes):
    if mes.text in mem_types:
        # пользователь нажал "Назад"
        c = mes.chat.id
        if mes.text == mem_types[-1]:
            msg = bot.send_message(c, "Что ты хочешь?",
                             reply_markup=make_markup(menu_list))
            bot.register_next_step_handler(msg, main_menu)
            return

        if mes.text == mem_types[-2]:
            msg = bot.send_message(c, "Популярное среди чего?",
                                   reply_markup=make_markup(popular_types))
            bot.register_next_step_handler(msg, popular)
            return

        funcs = {mem_types[0]: find_hot_stuff, mem_types[1]: find_trending_stuff,
                 mem_types[2]: find_trending_stuff}
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
                                   reply_markup=make_markup(mem_types))
            bot.register_next_step_handler(msg, choose_mem)
    else:
        bot.register_next_step_handler(mes, choose_mem)


def popular(mes):
    if mes.text in mem_types:
        # пользователь нажал "Назад"
        c = mes.chat.id
        if mes.text == mem_types[-1]:
            msg = bot.send_message(c, "Что ты хочешь?",
                             reply_markup=make_markup(menu_list))
            bot.register_next_step_handler(msg, main_menu)
            return

        memes[c] = most_popular_by_category(mes.text, curs)
        if len(memes[c]) > 0:
            curr_mem[c] = 0
            msg = bot.send_photo(c, memes[c][0][0], reply_markup=mem())
            bot.register_next_step_handler(msg, memming)
        else:
            msg = bot.send_message(c, "Тут пока ничего нет("
                                      "Выбери что-то другое",
                                   reply_markup=make_markup(mem_types))
            bot.register_next_step_handler(msg, choose_mem)
    else:
        bot.register_next_step_handler(mes, choose_mem)


def memming(mes):
    c = mes.chat.id
    if mes.text not in mem_resp:
        msg = bot.send_message(c, "что-то я не понял( попробуй еще раз",
                               reply_markup=mem())
        bot.register_next_step_handler(msg, memming)
        return
    if mes.text == mem_resp[-1]:
        msg = bot.send_message(c, "Выбери",
                               reply_markup=make_markup(mem_types))
        bot.register_next_step_handler(msg, choose_mem)
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
    if mes.text not in mem_categories:
        msg = bot.send_message(c, "Выбери одну из предложенных категорий",
                         reply_markup=make_markup(mem_categories))
        bot.register_next_step_handler(msg, add_mem)
    else:
        if mes.text == mem_categories[-1]:
            msg = bot.send_message(c, "Что ты хочешь?",
                                   reply_markup=make_markup(menu_list))
            bot.register_next_step_handler(msg, main_menu)
            return

        msg = bot.send_message(c, "Теперь отправь картинку)")
        bot.register_next_step_handler(msg, add_mem2(mes.text))


def add_mem2(category):
    def final_adding(mes):
        res = [mes.photo[-1].file_id, category, 0]
        set_mem(res, curs,conn)
    return final_adding


def find_friend(mes):
    res = find_bros_memes(find_fav_mem(mes.from_user.id, curs, conn), mes.from_user.id, curs)
    txt = "Думаю ты сдружишься с:\n"
    for i in res:
        txt += str(i)+'\n'
    bot.send_message(mes.chat.id, txt)
    bot.send_message(mes.chat.id, "Продолжаем разговор", reply_markup=make_markup(menu_list))
    bot.register_next_step_handler(mes, main_menu)

if __name__ == '__main__':
    conn = con_db()
    curs = conn.cursor()
    bot.polling(none_stop=True)
    curs.close()
