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
from collections import defaultdict
from datetime import datetime
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
        cursor.execute(
            "SELECT uploadsong_id,AVG(rating) FROM Likes GROUP BY uploadsong_id ORDER BY AVG(rating) DESC"
        )
        uploadsong_ids = cursor.fetchall()
        uploadsong_ids = [uploadsong_id[0] for uploadsong_id in uploadsong_ids]
        print(uploadsong_ids)
        print("\n")

        # now we will fetch all the songs from uploadsong table in the order of uploadsong_ids
        songs = []
        for uploadsong_id in uploadsong_ids:
            cursor.execute(
                "SELECT * FROM uploadsong WHERE uploadsong_id = ?", (uploadsong_id,)
            )
            # we also want to append avg rating of each song in songs list as follows
            song = cursor.fetchone()
            cursor.execute(
                "SELECT AVG(rating) FROM Likes WHERE uploadsong_id = ?",
                (uploadsong_id,),
            )
            avg_rating = cursor.fetchone()
            if avg_rating is not None:
                avg_rating = avg_rating[0]
                song = list(song)
                song.append(avg_rating)
                song = tuple(song)
                songs.append(song)
            else:
                song = list(song)
                song.append(0)
                song = tuple(song)
                songs.append(song)
        print(songs)
        # now we will append rest songs which are unrated
        cursor.execute(
            "SELECT * FROM uploadsong WHERE uploadsong_id NOT IN (SELECT uploadsong_id FROM Likes)"
        )
        unrated_songs = cursor.fetchall()
        for unrated_song in unrated_songs:
            songs.append(unrated_song)
        print(songs)

        cursor.execute("SELECT Album_name, Release_Date FROM Albums")
        albums_data = cursor.fetchall()

        cursor.execute("SELECT DISTINCT genre FROM uploadsong")
        genre_data = cursor.fetchall()

        # Fetch artist and date from uploadsong table
        cursor.execute("SELECT DISTINCT artist FROM uploadsong")
        artist_date_data = cursor.fetchall()

        return render_template(
            "home.html",
            data=songs,
            album_data=albums_data,
            genre_data=genre_data,
            artist_date_data=artist_date_data,
        )

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
            return render_template(
                "uploadsong.html", error="Please register as a creator first"
            )

        cursor.execute(
            "SELECT Album_ID FROM Albums WHERE Album_name = ? AND Artist_ID = ? ",
            (
                Album_name,
                creator_id,
            ),
        )
        album_id = cursor.fetchone()
        if album_id is not None:
            album_id = album_id[0]
        else:
            # creating new album if album not found, giving attributes Artist_ID, Album_name and Release_Date ( same as songs date)
            cursor.execute(
                "INSERT INTO Albums (Artist_ID, Album_name, Release_Date) VALUES (?, ?, ?)",
                (
                    creator_id,
                    Album_name,
                    date,
                ),
            )
            return render_template(
                "uploadsong.html",
                message="Album not found, created one new by the name '"
                + Album_name
                + "' for you, now upload song with this album name if you want to add more songs to this album",
            )

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
    cursor.execute(
        "SELECT strftime('%Y-%m-%d', Like_Date_Time) as like_date, Rating FROM Likes"
    )

    likes_data = cursor.fetchall()

    ratings_by_date = defaultdict(list)

    for like_entry in likes_data:
        ratings_by_date[like_entry[0]].append(like_entry[1])

    average_ratings = {
        date: sum(ratings) / len(ratings) for date, ratings in ratings_by_date.items()
    }
    print(average_ratings)
    formatted_ratings = {
        date: round(rating, 3) for date, rating in average_ratings.items()
    }

    dates = list(formatted_ratings.keys())
    ratings = list(formatted_ratings.values())
    for date, average_rating in average_ratings.items():
        print(f"Date: {date}, Average Rating: {average_rating}")

    if "email" in session:
        email = session["email"]
        cursor.execute("SELECT creator_id FROM creator WHERE email = ?", (email,))
        creator_ids = cursor.fetchall()

    title_count = 0
    album_name_count = 0
    for creator_id in creator_ids:
        cursor.execute(
            "SELECT COUNT(title) FROM uploadsong WHERE creator_id = ?", creator_id
        )

        title_count = cursor.fetchone()[0]

        print(f"Creator ID: {creator_id[0]}, Songs Count: {title_count}")
    creator_id = creator_ids[0]
    cursor.execute(
        "SELECT * FROM uploadsong WHERE creator_id = ?", creator_id
    )
    songs = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM Albums WHERE Artist_ID = ?", creator_id
    )
    albums = cursor.fetchall()
    for creator_id in creator_ids:
        cursor.execute(
            "SELECT album_id FROM uploadsong WHERE creator_id = ?", creator_id
        )

        album_ids = cursor.fetchall()

        for album_id in album_ids:
            cursor.execute(
                "SELECT COUNT(Album_name) FROM Albums WHERE Album_ID = ?", album_id
            )

            album_name_count = cursor.fetchone()[0]

            print(
                f"Creator ID: {creator_id[0]}, Album ID: {album_id[0]}, Album Name Count: {album_name_count}"
            )
    songs = [song for song in songs]
    albums = [album for album in albums]
    print(albums)
    return render_template(
        "creatordash.html",
        dates=dates,
        ratings=ratings,
        title_count=title_count,
        album_count=album_name_count,
        songs=songs,
        albums=albums,
    )


@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/useraccount", methods=["GET"])
def useraccount():
    return render_template("useraccount.html")


@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        search = request.form["search"]
        cursor.execute(
            "SELECT * FROM uploadsong WHERE title LIKE ? OR artist LIKE ?",
            ("%" + search + "%", "%" + search + "%"),
        )
        data = cursor.fetchall()
        print(data)
        return render_template("home.html", data=data)


@app.route("/adminsearch", methods=["POST"])
def adminsearch():
    search = request.form["adminsearch"]
    # we want to exclude those songs from this adminflag.html template which are not similar to my search query, so code will be same as tracklist route

    cursor.execute(
        "SELECT DISTINCT genre FROM uploadsong WHERE title LIKE ? OR artist LIKE ?",
        ("%" + search + "%", "%" + search + "%"),
    )
    genres = cursor.fetchall()
    genres = [genre[0] for genre in genres]

    genre_songs = {}
    for genre in genres:
        cursor.execute(
            "SELECT * FROM uploadsong WHERE genre = ? AND title LIKE ? OR artist LIKE ?",
            (genre, "%" + search + "%", "%" + search + "%"),
        )
        songs = cursor.fetchall()
        songs = [song for song in songs]
        genre_songs[genre] = songs

    return render_template("adminflag.html", genresnsongs=genre_songs)


@app.route("/play/<id>", methods=["GET", "POST"])
def play(id):
    if request.method == "GET":
        cursor.execute("SELECT * FROM uploadsong WHERE uploadsong_id = ?", (id,))
        data = cursor.fetchone()
        if "username" in session:
            username = session["username"]
            cursor.execute(
                "SELECT rating FROM Likes WHERE username = ? AND uploadsong_id = ?",
                (username, id),
            )
            rating = cursor.fetchone()
            if rating is not None:
                rating = rating[0]
                return render_template("lyricsnplay.html", data=data, rating=rating)
            else:
                return render_template("lyricsnplay.html", data=data)
    else:
        print("Received rating data from client")
        rating = request.form["rate"]
        print(f"Received rating: {rating}")
        # save this to database if present already by this user then update else insert
        if "username" in session:
            username = session["username"]
            cursor.execute(
                "SELECT rating FROM Likes WHERE username = ? AND uploadsong_id = ?",
                (username, id),
            )
            rating_data = cursor.fetchone()
            if rating_data is None:
                # i want to insert rating, uploadsong_id, username and like_date_time(which will be current date and time)
                cursor.execute(
                    "INSERT INTO Likes (rating, uploadsong_id, username, Like_Date_Time) VALUES (?, ?, ?, datetime('now'))",
                    (rating, id, username),
                )
                conn.commit()
            else:
                # i want to update rating and like_date_time(which will be current date and time)
                cursor.execute(
                    "UPDATE Likes SET rating = ?, Like_Date_Time = datetime('now') WHERE username = ? AND uploadsong_id = ?",
                    (rating, username, id),
                )
                conn.commit()
            return redirect("/play/" + id)
    return render_template("lyricsnplay.html", data=data)


@app.route("/admin", methods=["GET"])
def admin():
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Query to get genre counts
    cursor.execute(
        "SELECT genre, COUNT(*) as genre_count FROM uploadsong WHERE date <= ? GROUP BY genre",
        (current_date,),
    )
    genre_counts = cursor.fetchall()

    # Query to get the total number of genres
    cursor.execute(
        "SELECT COUNT(DISTINCT genre) as total_genres FROM uploadsong WHERE date <= ?",
        (current_date,),
    )
    total_genres = cursor.fetchone()[0]  # Access the count using index 0

    cursor.execute("SELECT COUNT(*) as total_filenames FROM uploadsong")
    total_filenames = cursor.fetchone()[0]  # Access the count using index 0

    # Query to get the count of distinct album_id entries
    cursor.execute(
        "SELECT COUNT(DISTINCT album_id) as total_albums FROM Albums",
    )
    total_albums = cursor.fetchone()[0]  # Access the count using index 0

    print(total_filenames, total_albums)

    print(total_genres)

    cursor.execute(
        "SELECT genre, date, COUNT(*) as genre_count FROM uploadsong WHERE date <= ? GROUP BY genre, date",
        (current_date,),
    )
    genre_day_counts = cursor.fetchall()
    print(genre_day_counts)

    genre_counts = {}
    for entry in genre_day_counts:
        genre = entry[0]
        count = entry[2]

        if genre not in genre_counts:
            genre_counts[genre] = count
        else:
            genre_counts[genre] += count

    for genre, count in genre_counts.items():
        print(f"{genre}: {count}")
    sorted_genre_counts = dict(sorted(genre_counts.items()))

    # Convert the dictionary into separate lists for chart rendering
    chart_categories = list(sorted_genre_counts.keys())
    chart_data = list(sorted_genre_counts.values())

    current_year = datetime.now().strftime("%Y")
    months = [str(i).zfill(2) for i in range(1, 13)]  # Months from '01' to '12'

    filename_counts = {}
    album_counts = {}

    for month in months:
        # Query to get the count of filenames for the current month
        cursor.execute(
            "SELECT COUNT(*) as filename_count FROM uploadsong WHERE strftime('%Y-%m', date) = ?",
            (f"{current_year}-{month}",),
        )
        filename_counts[month] = cursor.fetchone()[0]

        # Query to get the count of Album names for the current month
        cursor.execute(
            "SELECT COUNT(*) as album_count FROM Albums WHERE strftime('%Y-%m', Release_Date) = ?",
            (f"{current_year}-{month}",),
        )
        album_counts[month] = cursor.fetchone()[0]

    print("Counts of tracks for each month:")
    for month, count in filename_counts.items():
        print(f"{current_year}-{month}: {count}")

    print("\nCounts of Albums for each month:")
    for month, count in album_counts.items():
        print(f"{current_year}-{month}: {count}")

    today_date = datetime.now().strftime("%Y-%m-%d")

    # Query to get the top 10 ratings for today
    cursor.execute(
        """
        SELECT uploadsong_id
        FROM Likes
        WHERE strftime('%Y-%m-%d', Like_Date_Time) = ? 
        ORDER BY Rating DESC
        LIMIT 10
        """,
        (today_date,),
    )

    top_ratings_ids = cursor.fetchall()

    # Extract the uploadsong_id values from the result
    uploadsong_ids = [row[0] for row in top_ratings_ids]

    # Query to get the titles from the uploadsong table using the uploadsong_ids
    cursor.execute(
        """
        SELECT title
        FROM uploadsong
        WHERE uploadsong_id IN ({})
        """.format(
            ", ".join("?" for _ in uploadsong_ids)
        ),
        uploadsong_ids,
    )

    titles = cursor.fetchall()

    for i, title in enumerate(titles, start=1):
        print(f"{i}. {title[0]}")

    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM creator")
    creator_count = cursor.fetchone()[0]

    print(f"User Count: {user_count}")
    print(f"Creator Count: {creator_count}")

    return render_template(
        "admin.html",
        chart_categories=chart_categories,
        chart_data=chart_data,
        total_genres=total_genres,
        total_filenames=total_filenames,
        total_albums=total_albums,
    )


@app.route("/creator", methods=["GET", "POST"])
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


@app.route("/tracklist", methods=["GET", "POST"])
def tracklist():
    if request.method == "GET":
        cursor.execute("SELECT DISTINCT genre FROM uploadsong")
        genres = cursor.fetchall()
        genres = [genre[0] for genre in genres]
        print(genres)

        genre_songs = {}
        for genre in genres:
            cursor.execute("SELECT * FROM uploadsong WHERE genre = ?", (genre,))
            songs = cursor.fetchall()
            songs = [song for song in songs]
            print(songs)
            print("\n")
            genre_songs[genre] = songs

        print(genre_songs)
        return render_template("adminflag.html", genresnsongs=genre_songs)
    return render_template("adminflag.html")


@app.route("/flagunflag/<id>", methods=["GET", "POST"])
def flagunflag(id):
    if request.method == "GET":
        cursor.execute(
            "SELECT isFlagged FROM uploadsong WHERE uploadsong_id = ?", (id,)
        )
        isFlagged = cursor.fetchone()
        if isFlagged is not None:
            isFlagged = isFlagged[0]
            if isFlagged == 0:
                cursor.execute(
                    "UPDATE uploadsong SET isFlagged = 1 WHERE uploadsong_id = ?", (id,)
                )
                conn.commit()
                return redirect("/tracklist")
            else:
                cursor.execute(
                    "UPDATE uploadsong SET isFlagged = 0 WHERE uploadsong_id = ?", (id,)
                )
                conn.commit()
                return redirect("/tracklist")
        else:
            return redirect("/tracklist")
    return redirect("/tracklist")


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "GET":
        cursor.execute("DELETE FROM uploadsong WHERE uploadsong_id = ?", (id,))
        conn.commit()
        return redirect("/tracklist")
    return redirect("/tracklist")


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


# admin dash kiti genre aataparyant aale || no of filenames from uploasong || total albums from album_id Albums
# day wise eka genre madhe kiti songs aahet till that date or kahipn

# aajchya data time chya saglya entries retrieve eka track id nusar group by or order by tya track id sathi total rating

# date nusar  group by uploadsong table tya particular date sathi total number of tracks and albums

# creator dash
# creator_id = uploadsong table madhe jaun select uploadsong id je related aahe selected creator id sobat
# likes table madhe trackid


if __name__ == "__main__":
    app.run(debug=True)
