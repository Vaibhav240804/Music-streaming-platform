import sqlite3

conn = sqlite3.connect("user_data.db")

cursor = conn.cursor()

# -------- user login register ---------
# sql_query = """CREATE TABLE user(
# name text,
# username text PRIMARY KEY,
# email text,
# password text,
# isAdmin int
# )"""


# --------- admin login register----------
# sql_query = """CREATE TABLE admin(
# name text,
# username text PRIMARY KEY,
# email text,
# password text,
# isAdmin int
# )"""


# -------upload song ---------
# duration is in seconds

# sql_query = """
# CREATE TABLE uploadsong(
#     uploadsong_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT,
#     artist TEXT,
#     genre TEXT,
#     duration INT,
#     date TEXT,
#     filename TEXT,
#     lyrics TEXT,
#     isFlagged INT,
#     creator_id INTEGER,
#     album_id INTEGER,
#     FOREIGN KEY (creator_id) REFERENCES creator(creator_id),
#     FOREIGN KEY (album_id) REFERENCES album(album_id)
# )
# """


# -------- creator table -----

# sql_query = """CREATE TABLE creator(
# creator_id INTEGER PRIMARY KEY AUTOINCREMENT,
# name text,
# email text,
# artist text,
# genre text
# )"""

# -------- album table ------------
# sql_query = """CREATE TABLE Albums (
#   Album_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#   Artist_ID INTEGER,
#   Name TEXT NOT NULL,
#   Release_Date DATE,
#   Image TEXT,
#   FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID)
# )"""

# cursor.execute("DROP TABLE IF EXISTS uploadsong")
# cursor.execute(sql_query)
# try:
#     cursor.execute(
#         "INSERT INTO Albums (Album_ID, Artist_ID, Name, Release_Date, Image) VALUES ('1', '1', 'test-artist', '02-02-2002', 'image')"
#     )
#     conn.commit()
# except Exception as e:
#     print(f"Error: {e}")
#     conn.rollback()

# conn.commit()
