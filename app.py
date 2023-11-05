from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def userlogin():
  return render_template("loginUser.html")

if __name__ == "__main__":
  app.run()