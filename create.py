import sqlite3

conn = sqlite3.connect("user_data.db")

cursor = conn.cursor()

# -------- user login register ---------
# sql_query = """CREATE TABLE user(
# name text,
# username text,
# email text,
# password text,
# isAdmin int
# )"""


# --------- admin login register----------
# sql_query = """CREATE TABLE admin(
# name text,
# username text,
# email text,
# password text,
# isAdmin int
# )"""


# -------upload song ---------
# duration is in seconds

# sql_query = """CREATE TABLE uploadsong(
# uploadsong_id INTEGER PRIMARY KEY AUTOINCREMENT,
# title text,
# artist text,
# genre text,
# duration int,
# date text,
# filename text,
# lyrics text,
# isFlagged int,
# creator_id INTEGER,
# FOREIGN KEY (creator_id) REFERENCES creator(creator_id)
# )"""


# -------- creator table -----

# sql_query = """CREATE TABLE creator(
# creator_id INTEGER PRIMARY KEY AUTOINCREMENT,
# name text,
# email text,
# artist text,
# genre text
# )"""

# cursor.execute("DROP TABLE IF EXISTS uploadsong")
# cursor.execute(sql_query)
try:
    cursor.execute(
        "INSERT INTO creator (name, email, artist, genre) VALUES ('test', 'test@gmail.com', 'test-artist', 'test-genre')"
    )
    conn.commit()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

# conn.commit()
