import random
import sqlite3

# СУБД - Система управления базой данных
# SQL = Structured Query Language


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.db")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS Mentors "
               "(id INTEGER PRIMARY KEY, "
               "name TEXT, course TEXT, age INTEGER, "
               "grop INTEGER, photo TEXT)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO mentors VALUES "
                       "(?, ?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM mentors").fetchall()
    random_user = random.choice(result)
    await message.answer_photo(
        random_user[5],
        caption=f"{random_user[2]} {random_user[3]} {random_user[4]} "
                f"{random_user[1]}"
    )


async def sql_command_all():
    return cursor.execute("SELECT * FROM mentors").fetchall()


async def sql_command_delete(user_id):
    cursor.execute("DELETE FROM mentors WHERE id = ?", (user_id,))
    db.commit()

