import random
import sqlite3

# СУБД - Система управления базой данных
# SQL = Structured Query Language


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS ivan "
               "(id INTEGER PRIMARY KEY, username TEXT, "
               "name TEXT, age INTEGER, gender TEXT, "
               "region TEXT, photo TEXT)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO ivan VALUES "
                       "(?, ?, ?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM ivan").fetchall()
    random_user = random.choice(result)
    await message.answer_photo(
        random_user[6],
        caption=f"{random_user[2]} {random_user[3]} {random_user[4]} "
                f"{random_user[5]}\n{random_user[1]}"
    )


async def sql_command_all():
    return cursor.execute("SELECT * FROM ivan").fetchall()


async def sql_command_delete(user_id):
    cursor.execute("DELETE FROM ivan WHERE id = ?", (user_id,))
    db.commit()

