import psycopg2
import text_format
import sys

number_of_memes = 40

def con_db():
    try:
        conn = psycopg2.connect(
            "dbname='Memsage' user='postgres' host='127.0.0.1' password='postgres'")
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


def set_user(res, curs, conn):
    try:
        curs.execute("""INSERT INTO bros(bro_id, name, gender, sp, occupation, city, is_hikka)
    VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                     res)
    except psycopg2.DatabaseError as err:
        print("set_user error", err)
        sys.exit(1)
    else:
        conn.commit()


def delete_user(user_id, cursor, conn):
    try:
        a = [user_id]
        cursor.execute("""
        DELETE FROM bros
        WHERE bro_id = %s
        """, a)
    except psycopg2.DatabaseError:
        print("length of some word is too big")
        sys.exit(1)
    else:
        conn.commit()


def like(user_id, mem_id, cursor, conn):
    try:
        a = [mem_id, user_id]
        cursor.execute("SELECT * "
                       "FROM megustas "
                       "WHERE mem_id = %s "
                       "AND bro_id = %s",
                       a)
        b = cursor.fetchall()
        if len(b) > 0:
            remove_like(user_id, mem_id, cursor, conn)
        else:
            set_like(user_id, mem_id, cursor, conn)
    except psycopg2.DatabaseError as err:
        print("Database Error", err)
        sys.exit(1)
    else:
        conn.commit()


def set_like(user_id, mem_id, cursor, conn):
    try:
        a = [mem_id, user_id]
        cursor.execute("INSERT INTO megustas (mem_id, bro_id) VALUES (%s, %s);",
                       a)
        a.pop()
        print(a)
    except psycopg2.DatabaseError as err:
        print("Database Error", err)
        sys.exit(1)
    else:
        conn.commit()


def remove_like(user_id, mem_id, cursor, conn):
    try:
        a = [mem_id, user_id]
        cursor.execute(
            "DELETE FROM megustas WHERE (mem_id = %s AND bro_id = %s);", a)
        a = [mem_id]
        print(a)
        conn.commit()
    except psycopg2.DatabaseError as err:
        print("remove_like Error", err)
        sys.exit(1)


def find_fav_mem(user_id, cursor, conn):
    try:
        a = [user_id]
        cursor.execute("""
        SELECT memes.type
        FROM megustas NATURAL JOIN memes
        WHERE megustas.bro_id = %s
        GROUP BY type
        ORDER BY COUNT(memes.type) DESC
        LIMIT 1;
        """, a)
        b = cursor.fetchall()[0][0]
        a = [b, user_id]
        print(a)
        cursor.execute("""
        UPDATE bros
            SET fav_mem = %s
            WHERE bro_id = %s
        """, a)
        conn.commit()
        return a[0]
    except psycopg2.DatabaseError:
        print("Database Error\n")
        sys.exit(1)


def find_hot_stuff(cursor):
    try:
        cursor.execute("""
        SELECT file_id, mem_id
        FROM memes
        ORDER BY gustas DESC
        LIMIT 40;
        """)
        b = cursor.fetchall()
        return b
    except psycopg2.DatabaseError as err:
        print("Database Error", err)
        sys.exit(1)


def find_trending_stuff(cursor):
    try:
        cursor.execute("""
        SELECT file_id, mem_id
        FROM memes
        NATURAL JOIN megustas
        WHERE (megustas.data > (current_date - INTERVAL'1 week')::date)
        ORDER BY gustas DESC
        LIMIT 40;
        """)
        b = cursor.fetchall()
        return b
    except psycopg2.DatabaseError as err:
        print("Database Error", err)
        sys.exit(1)


def find_new_stuff(cursor):
    try:
        cursor.execute("""
        SELECT file_id, mem_id
        FROM memes
        ORDER BY mem_id DESC
        LIMIT 40;
        """)
        b = cursor.fetchall()
        return b
    except psycopg2.DatabaseError as err:
        print("Database Error", err)
        sys.exit(1)


def find_bratans_memes(fav_meme_category, user_id, cursor):
    try:
        a = [fav_meme_category, user_id]
        cursor.execute("""
        SELECT bro_id
        FROM bros
        WHERE (fav_mem = %s) AND NOT(bro_id = %s ) AND (is_hikka = FALSE);
        """, a)
        b = cursor.fetchall()
        return b
    except psycopg2.DatabaseError:
        print("Database Error\n")


def find_bros_cities(city_name, useless_id, cursor):
    """Показать братанов по городу"""
    try:
        b = text_format.transliterate(city_name)
        # на случай фигни какой-то
        if b == '':
            return []
        a = [b, useless_id]
        cursor.execute("""
        SELECT bro_id
        FROM bros
        WHERE (city = %s) AND NOT (bro_id = %s ) AND (is_hikka = FALSE);
        """, a)
        c = cursor.fetchall()
        return c
    except psycopg2.DatabaseError:
        print("Database Error\n")
        sys.exit(1)


def most_popular_by_category(mem_category, cursor):
    try:
        a = [mem_category]
        cursor.mogrify("""
        SELECT mem_id
        FROM memes
        WHERE type = %s
        ORDER BY gustas DESC
        LIMIT 10;
        """, a)
        c = cursor.fetchall()
        return c
    except psycopg2.DatabaseError:
        print("Database Error\n")
        sys.exit(1)


def set_mem(res, curs, conn):
    try:
        curs.execute("""INSERT INTO public.memes(file_id, mem_type, gustas)
        VALUES (%s, %s, %s);""", res)

    except psycopg2.DatabaseError as err:
        print("set_mem error", err)
        sys.exit(1)
    else:
        conn.commit()


def close_conn(conn):
    if (conn):
        conn.close()


if __name__ == '__main__':
    conn = con_db()
    curs = cursor(conn)

    curs.close()
    if (conn):
        conn.close()
