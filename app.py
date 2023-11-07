from flask import Flask, jsonify, redirect, render_template, request

app = Flask(__name__)


# Route for displaying the user login page
@app.route("/loginuser")
def userlogin():
    return render_template("loginUser.html")


# Route for displaying the admin login page
@app.route("/loginadmin")
def adminlogin():
    return render_template("loginAdmin.html")


@app.route("/home")
def homepage():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
