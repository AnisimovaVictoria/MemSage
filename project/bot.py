import sys
import config
import psycopg2
import telebot
import text
import keyboard


def con_db():
    try:
        conn = psycopg2.connect("dbname='Memsage' user='postgres' host='127.0.0.1' password='postgres'")
        return conn
    except psycopg2.DatabaseError:
        print("Error")
        sys.exit(1)

conn = con_db()
curs = conn.cursor()

bot = telebot.TeleBot(config.token)


if (conn):
    conn.close()


@bot.message_handler(commands=['start'])
# обработка команды /start
def start(mes):
    msg = bot.send_message(mes.chat.id, text.hello + text.questions[0])
    bot.register_next_step_handler(msg, interview(1))


def interview(i):
    def ask_question(mes):
        print(mes.text)
        msg = bot.send_message(mes.chat.id, text.questions[i],
                                   reply_markup=keyboard.interview[i]())
        if i == len(text.questions) - 1:
            bot.register_next_step_handler(msg, main_menu)
        else:
            bot.register_next_step_handler(msg, interview(i+1))
    print("here", i)
    return ask_question


def main_menu(mes):
    if mes.text not in keyboard.start_menu:
        bot.register_next_step_handler(mes, main_menu)
    else:
        # Посмотреть мемес
        if mes.text == keyboard.start_menu[0]:
            msg = bot.send_message(mes.chat.id, "Выбери тип:",
                                   reply_markup=keyboard.choose_mem())
            bot.register_next_step_handler(msg, choose_mem)
        # Добавить мемес
        if mes.text == keyboard.start_menu[1]:
            msg = bot.send_message(mes.chat.id, "Я пока этого не умею(")
            bot.register_next_step_handler(msg, add_mem)
        # Найти друзей
        if mes.text == keyboard.start_menu[2]:
            msg = bot.send_message(mes.chat.id, "Я пока этого не умею(")
            bot.register_next_step_handler(msg, find_friend)


def choose_mem(mes):
    pass


def add_mem(mes):
    pass


def find_friend(mes):
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
    curs.close()
