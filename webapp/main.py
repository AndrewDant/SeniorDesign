from flask import Flask, request, session, render_template, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if __name__ == "__main__":
    app.run(threaded=True)


@app.route("/")
def home():
    return render_template("index.html")
