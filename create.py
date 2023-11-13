import sqlite3

conn = sqlite3.connect("user_data.db")

cursor = conn.cursor()

# sql_query = """CREATE TABLE user(
# name text, 
# username text,
# email text,
# password text
# )"""

# cursor.execute(sql_query)
cursor.execute("INSERT INTO user VALUES ('adii', 'adii123', 'test@gmail.com', '123')")

conn.commit()
