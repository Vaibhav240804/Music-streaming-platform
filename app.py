from flask import Flask, render_template

app = Flask(__name__)


@app.route("/loginuser")
def userlogin():
    return render_template("loginUser.html")


@app.route("/loginadmin")
def adminlogin():
    return render_template("loginAdmin.html")

@app.route("/home")
def homepage():
    return render_template("home.html")


if __name__ == "__main__":
    app.run()
