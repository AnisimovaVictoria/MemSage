import psycopg2
import sys


def con_db():
    try:
        conn = psycopg2.connect(dbname='memsa', user='postgres', host='localhost', port='54321', password='scattered')
        return conn
    except psycopg2.DatabaseError:
        print("Error")
        sys.exit(1)


def cursor(conn):
    return conn.cursor()


def print_names(cursor):
    try:
        cursor.execute('Select type from memes')
        names = cursor.fetchall()
        print(names[0])
    except psycopg2.DatabaseError:
        print("Error")
        sys.exit(1)


def user_introducer():
    print("Hey! What's your name?")
    imya = input()
    print("It took 1 look and now we're not the same))) \n And where are you from?")
    city = input()
    print("Oh, I was there, it's beautiful place:)\n Кстати, как к тебе обращаться?")
    print(" Выбери пол, наиболее подходящий твоим внутренним ощущениям, ответь номером из предлож. списка")
    print("""Вот список:
        0 - ЛИНОЛЕУМ,
        1 - ЛАМИНАТ,
        2 - КОВРОЛИН,
        3 - КЕРАМОГРАНИТ,
        4 - ПАРКЕТ,
        5 - БРЕВЕНЧАТЫЙ,
        6 - НАЛИВНОЙ""")
    floor = input()
    numb_to_gend = {
        '0': 'linoleum',
        '1': 'laminate',
        '2': 'kovrolin',
        '3': 'keramogranit',
        '4': 'parquet',
        '5': 'hardwood',
        '6': 'self-leveling'
    }
    gender = numb_to_gend[floor]
    print("""Alright! Now let's move on to your occupation. Type\n0 if you're a preschooler,\n 1 if you're schoolchild,
        2 if you're a fiztech, \n 3 if u've got your bachelor's """)
    occ = input()
    numb_to_occ = {
        '0': 'pre!shkolyar',
        '1': 'shkolyar',
        '2': 'fiztech!shkolyar',
        '3': 'post!shkolyar',
    }
    shk = numb_to_occ[occ]
    print("final question: \nDo you have that special someone who makes your heart GO DOKI-DOKI??? \nANSWER YES OR NO")
    ans = input()
    ans_to_sp = {'YES': 'IN LOVE', 'NO': 'forever alone'}
    sp = ans_to_sp[ans]
    result_list = []
    result_list.append(imya)
    result_list.append(sp)
    result_list.append(shk)
    result_list.append(city)
    result_list.append(gender)
    print(result_list)
    return result_list


if __name__ == '__main__':
    conn = con_db()
    curs = cursor(conn)
    print_names(curs)
    res = user_introducer()
    try:
        curs.execute("INSERT INTO bros(name, sp, occupation, city, gender) VALUES (%s, %s, %s, %s, %s);",
                     res)
    except psycopg2.DatabaseError:
        print("length of some word is too big")
        sys.exit(1)
    else:
        conn.commit()
    curs.close()
    if (conn):
        conn.close()
