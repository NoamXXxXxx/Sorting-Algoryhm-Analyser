import sqlite3

db_name = 'database.db'


def init_db():
    con = sqlite3.connect(db_name)
    con.execute("""CREATE TABLE IF NOT EXISTS tier_list (name TEXT, file TEXT, bars_count INTEGER, elapsed_time REAL, comparisons INTEGER)""")
    con.commit()
    con.close()

def save_res(name, file, bars_count, elapsed_time, comparisons):
    con = sqlite3.connect(db_name)
    con.execute("""INSERT INTO tier_list VALUES (?, ?, ?, ?, ?)""", (name, file, bars_count, elapsed_time, comparisons))
    con.commit()
    con.close()

def get_tier_list():
    con = sqlite3.connect(db_name)
    rows = con.execute("""SELECT name, file, bars_count, elapsed_time, comparisons FROM tier_list ORDER BY elapsed_time ASC""").fetchall()
    con.close()
    return rows