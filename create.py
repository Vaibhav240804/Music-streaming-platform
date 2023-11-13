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

# cursor.execute(sql_query)
cursor.execute("INSERT INTO admin VALUES ('adii', 'adii123', 'test@gmail.com', '123', 1)")

conn.commit()
