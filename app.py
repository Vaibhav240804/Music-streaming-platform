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
            if "username" not in session:
                session["username"] = username
            if "email" not in session:
                cursor.execute(f"SELECT email from user WHERE username = '{username}'")
                email = cursor.fetchone()
                if email is not None:
                    email = email[0]
                    session["email"] = email
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
                    session["username"] = username
                    session["email"] = email
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
        if "email" in session:
            return render_template("uploadsong.html")
        else:
            return render_template("uploadsong.html", message="Please login first")
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
        else:
            return render_template("uploadsong.html", error="Please register as a creator first")

        cursor.execute(
            "SELECT Album_ID FROM Albums WHERE Album_name = ? AND Artist_ID = ? ", (Album_name, creator_id,)
        )
        album_id = cursor.fetchone()
        if album_id is not None:
            album_id = album_id[0]
        else:
            # creating new album if album not found, giving attributes Artist_ID, Album_name and Release_Date ( same as songs date)
            cursor.execute(
                "INSERT INTO Albums (Artist_ID, Album_name, Release_Date) VALUES (?, ?, ?)",
                (creator_id, Album_name, date,),
            )
            return render_template("uploadsong.html", message="Album not found, created one new by the name '"+Album_name+"' for you, now upload song with this album name if you want to add more songs to this album")
        
        if filename != "":
            uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            return render_template("uploadsong.html", message="Please upload a file")
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
        return render_template("uploadsong.html", message="Song uploaded successfully")



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


@app.route("/creator", methods=["GET","POST"])
def creator():
    # i want to check if user's email is in the table of artist from database or not, if yes then store the artist id in session, and if not then render message on screen to choose genre through jinja syntax and then take input by post and then store it in the database and then store the artist id in session and now the user can upload songs, and if the user is already in the database then just store the artist id in session and then the user can upload songs
    # users email is already stored in session, we will check if the email is in the artist table or not when get request is done on this route
    if request.method == "GET":
        if "email" in session:
            email = session["email"]
            cursor.execute("SELECT creator_id FROM creator WHERE email = ?", (email,))
            artist_id = cursor.fetchone()
            if artist_id is not None:
                artist_id = artist_id[0]
                session["artist_id"] = artist_id
                return render_template("creator.html")
            else:
                return render_template("creator.html", message="Please select a genre")
        else:
            return render_template("creator.html", error="Please login first")
    else:
        genre = request.form["genre"]
        email = session["email"]
        artist = request.form["artist"]
        if artist == "":
            return render_template("creator.html", error="Please enter artist name")
        if genre == "":
            return render_template("creator.html", error="Please select a genre")
        cursor.execute(
            "INSERT INTO creator (artist, email, genre) VALUES (?, ?, ?)",
            (artist, email, genre),
        )
        conn.commit()
        cursor.execute("SELECT creator_id FROM creator WHERE email = ?", (email,))
        artist_id = cursor.fetchone()
        if artist_id is not None:
            artist_id = artist_id[0]
            session["artist_id"] = artist_id
            return render_template("creator.html")
        else:
            return render_template("creator.html", error="Error in selecting genre")



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


# admin dash kiti genre aataparyant aale || no of filenames from uploasong || total albums from album_id Albums
# day wise eka genre madhe kiti songs aahet till that date or kahipn

#   aajchya data time chya saglya entries retrieve eka track id nusar group by or order by tya track id sathi total rating 

# date nusar  group by uploadsong table tya particular date sathi total number of tracks and albums

# creator dash
# creator_id = uploadsong table madhe jaun select uploadsong id je related aahe selected creator id sobat
# likes table madhe trackid


if __name__ == "__main__":
    app.run(debug=True)
