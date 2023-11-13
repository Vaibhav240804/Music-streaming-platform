import sqlite3
from flask import Flask, jsonify, redirect, render_template, request
import sqlite3

app = Flask(__name__)
app.static_folder = "static"

app.secret_key = "__privatekey__"

# Route for displaying the user login page
# @app.route("/loginuser")
# def userlogin():
#     return render_template("loginUser.html")

conn = sqlite3.connect("user_data.db", check_same_thread=False)
cursor = conn.cursor()

# Route for handling user registration
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/loginuser", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        print(username, password)

        # Check credentials against database
        query = f"SELECT username, password from user WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)

        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            print("Sorry for the inconvenience. Wrong credentials provided")
            return render_template("loginUser.html")
        else:
            print("Login successful!")
            return redirect("/")

    return render_template("loginUser.html")


@app.route("/registeruser", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        # name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        # password = request.form["password"]
        # print(name, username, email, password)

        if request.form["name"] != "" and request.form["password"] != "":
            name = request.form["name"]
            password = request.form["password"]
            statement = (
                f"SELECT * from user where name='{name}' AND password = '{password}';"
            )
            cursor.execute(statement)
            data = cursor.fetchone()

            if data:
                return render_template("loginUser.html")
            else:
                if not data:
                    cursor.execute(
                        "INSERT INTO user (name, username, email, password, isAdmin) VALUES (?,?,?,?,0)",
                        (name, username, email, password),
                    )
                    conn.commit()
                    # conn.close()
                    return render_template("loginUser.html")
    elif request.method == "GET":
        return render_template("loginUser.html")

    # Redirect to login page after successful registration
    return redirect("/loginuser")


@app.route("/usercreatesalbum", methods=["GET", "POST"])
def create_album():
    if request.method == "GET":
        return render_template("usercreatesalbum.html")
    else:
        return render_template("usercreatesalbum.html")


@app.route("/userfetchesalbum", methods=["GET", "POST"])
def fetch_album():
    if request.method == "GET":
        return render_template("userfetchesalbum.html")
    else:
        return render_template("userfetchesalbum.html")


@app.route("/", methods=["GET"])
def lyrics():
    return render_template("home.html")


@app.route("/uploadsong", methods=["GET", "POST"])
def uploadSong():
    if request.method == "POST":
        title = request.form["title"]
        artist = request.form["artist"]
        duration = request.form["duration"]
        date = request.form["date"]
        lyrics = request.form["lyrics"]

        data = cursor.fetchone()
        if data:
            return render_template("uploadsong.html")
        else:
            if not data:
                cursor.execute(
                    "INSERT INTO uploadsong (title, artist, duration, date, lyrics, isAdmin) VALUES (?,?,?,?,?,0)",
                    (title, artist, duration, date, lyrics),
                )
                conn.commit()
                # conn.close()
                return render_template("home.html")

    elif request.method == "GET":
        return render_template("uploadsong.html")


@app.route("/creatorsdash", methods=["GET"])
def creatorsdash():
    return render_template("creatordash.html")


@app.route("/play", methods=["GET"])
def play():
    return render_template("lyricsnplay.html")


@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")


@app.route("/creator", methods=["GET"])
def creator():
    return render_template("creator.html")


@app.route("/tracklist", methods=["GET"])
def tracklist():
    return render_template("adminflag.html")


@app.route("/loginadmin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        print(username, password)

        # Check credentials against database
        query = f"SELECT username, password from admin WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)

        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            print("Sorry for the inconvenience. Wrong credentials provided")
            return render_template("loginAdmin.html")
        else:
            print("Login successful!")
            return redirect("/admin")

    return render_template("loginAdmin.html")


@app.route("/registeradmin", methods=["GET", "POST"])
def register_admin():
    if request.method == "POST":
        # name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        # password = request.form["password"]
        # print(name, username, email, password)

        if request.form["name"] != "" and request.form["password"] != "":
            name = request.form["name"]
            password = request.form["password"]
            statement = (
                f"SELECT * from admin where name='{name}' AND password = '{password}';"
            )
            cursor.execute(statement)
            data = cursor.fetchone()

            if data:
                return render_template("loginAdmin.html")
            else:
                if not data:
                    cursor.execute(
                        "INSERT INTO admin (name, username, email, password, isAdmin) VALUES (?,?,?,?,1)",
                        (name, username, email, password),
                    )
                    conn.commit()
                    # conn.close()
                    return render_template("loginAdmin.html")
    elif request.method == "GET":
        return render_template("loginAdmin.html")

    # Redirect to login page after successful registration
    return redirect("/loginadmin")


@app.route("/home")
def homepage():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
