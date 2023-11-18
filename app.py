import sqlite3
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    flash,
    session,
)
import sys
import sqlite3
import os

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
# app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"


# @app.route("/", methods=["GET"])
# def index():
#     return render_template("home.html")


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
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        # print(name, username, email, password)

        if request.form["username"] != "":
            username = request.form["username"]
            statement = f"SELECT * from user where username='{username}';"
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


@app.route("/logout", methods=["GET", "POST"])
def logout_user():
    # Clear the user session
    session.clear()

    # Flash a message for successful logout
    flash("Logout successful", "success")

    # Redirect to the login page
    return redirect("/loginuser")


@app.route("/usercreatesalbum", methods=["GET", "POST"])
def create_album():
    if request.method == "GET":
        return render_template("usercreatesalbum.html")
    else:
        return render_template("usercreatesalbum.html")

@app.route("/userfetchesalbum", methods=["GET"])
def fetch_album():
    try:
        cursor.execute("SELECT * FROM Albums")
        albums_data = cursor.fetchall()
        print(albums_data)
        sys.stdout.flush()
        return render_template("userfetchesalbum.html", albums_data=albums_data)
    except Exception as e:
        print("Error:", e)
        sys.stdout.flush()
        return "An error occurred while fetching data from the database."

@app.route("/")
def fetchedsongdata():
    try:
        conn = sqlite3.connect("user_data.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("SELECT title, artist, filename FROM uploadsong")
        data = cursor.fetchall()
        print(data)
        return render_template("home.html", data=data)

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        conn.close()


@app.route("/uploadsong", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("uploadsong.html")
    if request.method == "POST":
        title = request.form["title"]
        artist = request.form["artist"]
        genre = request.form["genre"]
        duration = request.form["duration"]
        Album_name = request.form["album_name"]
        date = request.form["date"]
        uploaded_file = request.files["file"]
        filename = uploaded_file.filename
        lyrics = request.form["lyrics"]

        cursor.execute("SELECT creator_id FROM creator WHERE artist = ?", (artist,))
        creator_id = cursor.fetchone()

        if creator_id is not None:
            creator_id = creator_id[0]

        cursor.execute(
            "SELECT album_id FROM Albums WHERE Album_name = ?", (Album_name,)
        )
        album_id = cursor.fetchone()
        if album_id is not None:
            album_id = album_id[0]

        cursor.execute(
            "INSERT INTO uploadsong (title, artist, genre, duration, date, filename, lyrics, isFlagged, creator_id, album_id) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?)",
            (
                title,
                artist,
                genre,
                duration,
                date,
                filename,
                lyrics,
                creator_id,
                album_id,
            ),
        )

        conn.commit()
        # conn.close()
        return render_template("home.html")
    else:
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return render_template("uploadsong.html", error="No file selected")

        if file:
            filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filename)
            return render_template(
                "uploadsong.html", message="File uploaded successfully"
            )


@app.route("/creatorsdash", methods=["GET"])
def creatorsdash():
    return render_template("creatordash.html")


@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


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
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        # print(name, username, email, password)

        if request.form["username"] != "":
            username = request.form["username"]
            statement = f"SELECT * from admin where username='{username}';"
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
