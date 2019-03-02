from flask import Flask, request, session, render_template, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Pressure
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "post-chair.db"
)
# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

if __name__ == "__main__":
    app.run(threaded=True)


@app.route("/")
def home():
    return render_template("index.j2")


@app.cli.command("initdb")
def init_db():
    db.drop_all()
    db.create_all()
    print("Initialized default DB")


@app.cli.command("bootstrap")
def bootstrap_data():
    db.drop_all()
    db.create_all()

    p1 = Pressure(timestamp=datetime.now(), back_left=1.1, back_right=1.1, back_bottom=.8,
                  seat_left=2.1, seat_right=2.1, seat_rear=2.1)
    db.session.add(p1)

    r1 = Result(back_score=12, seat_score=10, p_id=p1.p_id)

    db.session.commit()

    print("Added bootstrap data")
