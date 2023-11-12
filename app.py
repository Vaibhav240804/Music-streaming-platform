import sqlite3
from flask import Flask, jsonify, redirect, render_template, request

app = Flask(__name__)
app.static_folder = 'static'


# Route for displaying the user login page
@app.route("/loginuser")
def userlogin():
    return render_template("loginUser.html")

# Route for handling user registration
@app.route("/loginuser", methods=["POST"])
def register_user():
    # Extract form data
    name = request.form["name"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Connect to the database
    connection = sqlite3.connect("Music project.db")
    cursor = connection.cursor()

    # Prepare the SQL query
    query = "INSERT INTO MUSIC-PROJECT VALUES (?, ?, ?, ?)"

    # Insert user data into the database
    try:
        cursor.execute(query, (name, username, email, password))
        connection.commit()
    except sqlite3.IntegrityError:
        # Handle username uniqueness constraint
        print("Error: Username already exists")
        return jsonify({"error": "Username already exists"})

    # Close the connection
    connection.close()

    # Print a success message
    print("User registration successful.")

    # Redirect to login page after successful registration
    return redirect("/loginuser")


# Route for retrieving user information based on username

@app.route("/usercreatesalbum", methods=["GET","POST"])
def create_album():
    if request.method == "GET":
        return render_template("usercreatesalbum.html")
    else:
        return render_template("usercreatesalbum.html")

@app.route("/userfetchesalbum", methods=["GET","POST"])
def fetch_album():
    if request.method == "GET":
        return render_template("userfetchesalbum.html")
    else:
        return render_template("userfetchesalbum.html")

@app.route("/",methods=["GET"])
def lyrics():
    return render_template("home.html")

@app.route("/uploadsong",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        return render_template("uploadsong.html")
    else:
        return render_template("uploadsong.html")

@app.route("/creatorsdash",methods=["GET"])
def creatorsdash():
    return render_template("creatordash.html")

@app.route("/play",methods=["GET"])
def play():
    return render_template("lyricsnplay.html")

@app.route("/admin",methods=["GET"])
def admin():
    return render_template("admin.html")

@app.route("/creator",methods=["GET"])
def creator():
    return render_template("creator.html")

@app.route("/tracklist",methods=["GET"])
def tracklist():
    return render_template("adminflag.html")


@app.route("/getuser/loginuser", methods=["GET"])
def get_user(username):
    # Connect to the database
    connection = sqlite3.connect("Music project.db")
    cursor = connection.cursor()

    # Prepare the SQL query
    query = "SELECT * FROM MUSIC-PROJECT WHERE username = ?"

    # Fetch user information
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()

    # Close the connection
    connection.close()

    # Check if user data was found
    if user_data:
        # Return user data as JSON
        return jsonify({
            "name": user_data[0],
            "username": user_data[1],
            "email": user_data[2],
        })
    else:
        # Return error message if user not found
        return jsonify({"error": "User not found"})

# Route for displaying the admin login page
@app.route("/loginadmin")
def adminlogin():
    return render_template("loginAdmin.html")


@app.route("/home")
def homepage():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
