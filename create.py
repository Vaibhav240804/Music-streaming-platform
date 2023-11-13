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

sql_query = """CREATE TABLE uploadsong(
title text,
artist text,
duration int,
date text,
lyrics text,
isAdmin int
)"""

# cursor.execute("DROP TABLE IF EXISTS uploadsong")
cursor.execute(sql_query)
# cursor.execute(
#     "INSERT INTO uploadsong VALUES ('Song Title', 'Artist Name', 240, '2023-11-13', 'Lyrics go here', 0)"
# )

# conn.commit()
