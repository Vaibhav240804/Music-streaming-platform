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
# def check_if_exists(field, value):
#     query = f"SELECT COUNT(*) FROM user WHERE {field} = {value}"
#     cursor.execute(query, (value,))
#     result = cursor.fetchone()
#     count = result[0]
#     return count


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
                return render_template("loginuser.html")
            else:
                if not data:
                    cursor.execute(
                        "INSERT INTO user (name, username, email, password) VALUES (?,?,?,?)",
                        (name, username, email, password),
                    )
                    conn.commit()
                    conn.close()
                    return render_template("loginuser.html")
        # # Check if username or email already exists
        # username_exists = check_if_exists("username", username)
        # email_exists = check_if_exists("email", email)

        # if username_exists > 0:
        #     print("Username already exists")
        #     return render_template(
        #         "loginUser.html", error_message="Username already exists"
        #     )
        # elif email_exists > 0:
        #     print("Email already exists")
        #     return render_template(
        #         "loginUser.html", error_message="Email already exists"
        #     )
        # else:
        #     try:
        #         # Insert user data into the database using a parameterized query
        #         query = "INSERT INTO user (name, username, email, password) VALUES (%s, %s, %s, %s)"
        #         cursor.execute(query, (name, username, email, password))
        #         conn.commit()

        #         print("User registered successfully")
        #         return redirect("/")
        #     except Exception as e:
        #         print(f"Error registering user: {e}")
        #         return render_template(
        #             "loginUser.html", error_message="Error registering user"
        # )
    elif request.method == "GET":
        return render_template("loginUser.html")


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


# @app.route("/getuser/loginuser", methods=["GET"])
# def get_user(username):
#     # Connect to the database
#     connection = sqlite3.connect("Music project.db")
#     cursor = connection.cursor()

#     # Prepare the SQL query
#     query = "SELECT * FROM MUSIC-PROJECT WHERE username = ?"

#     # Fetch user information
#     cursor.execute(query, (username,))
#     user_data = cursor.fetchone()

#     # Close the connection
#     connection.close()

#     # Check if user data was found
#     if user_data:
#         # Return user data as JSON
#         return jsonify({
#             "name": user_data[0],
#             "username": user_data[1],
#             "email": user_data[2],
#         })
#     else:
#         # Return error message if user not found
#         return jsonify({"error": "User not found"})


# Route for displaying the admin login page
@app.route("/loginadmin")
def adminlogin():
    return render_template("loginAdmin.html")


@app.route("/home")
def homepage():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
