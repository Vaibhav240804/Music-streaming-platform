import sqlite3

connection = sqlite3.connect("user_data.db")
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS users(name TEXT, username TEXT, email TEXT, password TEXT)"""
