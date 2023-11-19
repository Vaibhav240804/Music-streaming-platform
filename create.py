import sqlite3

conn = sqlite3.connect("user_data.db")

cursor = conn.cursor()

# -------- user login register ---------
# sql_query = """CREATE TABLE user(
# name text,
# username text,
# email text  PRIMARY KEY,
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
# artist text,
# email text,
# genre text
# )"""

# -------- album table ------------

# sql_query = """CREATE TABLE Albums (
#   Album_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#   Artist_ID INTEGER,
#   Album_name TEXT NOT NULL,
#   Release_Date DATE,
#   FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID)
# )"""


# ----------- playlists ----------

# sql_query = """CREATE TABLE Playlists (
#   Playlist_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#   username TEXT,
#   Name TEXT NOT NULL,
#   FOREIGN KEY (username) REFERENCES user(username)
# )
# """

# --------- playlists-track table -------

# sql_query = """CREATE TABLE Playlist_Tracks (
#   Playlist_ID INT,
#   Track_ID INT,
#   PRIMARY KEY (Playlist_ID, Track_ID),
#   FOREIGN KEY (Playlist_ID) REFERENCES Playlists(Playlist_ID),
#   FOREIGN KEY (Track_ID) REFERENCES Tracks(Track_ID)
# )"""

# --------- Likes table ---------

# sql_query = """CREATE TABLE Likes (
#   username TEXT,
#   uploadsong_id INT,
#   Rating INT,
#   Like_Date_Time DATETIME,
#   PRIMARY KEY (username, uploadsong_id),
#   FOREIGN KEY (username) REFERENCES user(username),
#   FOREIGN KEY (uploadsong_id) REFERENCES uploadsong(uploadsong_id)
# )"""

# cursor.execute("DROP TABLE IF EXISTS Likes")


# to clear all the data
# cursor.execute("DELETE FROM Likes")


# cursor.execute(sql_query)
try:
    cursor.execute(
        "INSERT INTO Likes (username, uploadsong_id, Rating, Like_Date_Time) VALUES ('test1234', 5, 4, '2023-11-19 00:12:23')"
    )
    conn.commit()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

conn.commit()
