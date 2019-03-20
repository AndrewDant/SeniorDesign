from flask import Flask, request, render_template
from datetime import datetime, timedelta
from models import db, Pressure  # , Result
from k_nearest import *
import os
import json
import random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "post-chair.db"
)
# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

main()

if __name__ == "__main__":
    app.run(threaded=True)


@app.route("/")
def index():
    return render_template("index.j2")


@app.route("/input/", methods=["POST"])
def data_input():
    data_json = request.get_json()

    back_score = generate_score([data_json['back_left'], data_json['back_right'], data_json['back_bottom']])
    seat_score = generate_score([data_json['seat_left'], data_json['seat_right'], data_json['seat_rear']])

    # TODO real classification
    p1 = Pressure(timestamp=datetime.now(), back_left=data_json['back_left'], back_right=data_json['back_right'], back_bottom=data_json['back_bottom'],
                  seat_left=data_json['seat_left'], seat_right=data_json['seat_right'], seat_rear=data_json['seat_rear'], back_score=back_score, seat_score=seat_score,
                  classification="Good Posture")

    db.session.add(p1)
    db.session.commit()

    return json.dumps(p1.serialize())


@app.route("/data/")
def data():
    new_data = Pressure(timestamp=datetime.now(), back_left=random.uniform(1, 3.3),
                        back_right=random.uniform(1.8, 3.3), back_bottom=random.uniform(1.5, 3),
                        seat_left=random.uniform(0, 2.3), seat_right=random.uniform(0, 2),
                        seat_rear=random.uniform(1, 1.9), back_score=random.uniform(0, 50),
                        seat_score=random.uniform(0, 50),
                        classification="Good Posture")
    # db.session.add(new_data)
    # db.session.commit()

    num_minutes = int(request.args.get('minutes'))
    time_offset = datetime.now() - timedelta(minutes=num_minutes)

    data_list = db.session.query(Pressure).filter(Pressure.timestamp > time_offset) \
        .order_by(Pressure.timestamp.asc()).all()

    return json.dumps([d.serialize() for d in data_list])


@app.cli.command("initdb")
def init_db():
    db.drop_all()
    db.create_all()
    print("Initialized default DB")


@app.cli.command("bootstrap")
def bootstrap_data():
    db.drop_all()
    db.create_all()

    p1 = Pressure(timestamp=datetime.now(), back_left=1.1, back_right=2.2, back_bottom=.8,
                  seat_left=.5, seat_right=1, seat_rear=1.4, back_score=19, seat_score=10,
                  classification="Good Posture")
    db.session.add(p1)

    p2 = Pressure(timestamp=datetime.now(), back_left=1.4, back_right=1.0, back_bottom=1.8,
                  seat_left=2.1, seat_right=1.1, seat_rear=1.2, back_score=12, seat_score=15,
                  classification="Good Posture")
    db.session.add(p2)

    p3 = Pressure(timestamp=datetime.now(), back_left=3.1, back_right=1.9, back_bottom=2.8,
                  seat_left=2.3, seat_right=1.2, seat_rear=2, back_score=16, seat_score=30,
                  classification="Good Posture")
    db.session.add(p3)

    p4 = Pressure(timestamp=datetime.now(), back_left=1.9, back_right=2.3, back_bottom=1.5,
                  seat_left=1.5, seat_right=1, seat_rear=2.1, back_score=14, seat_score=40,
                  classification="Good Posture")
    db.session.add(p4)

    # r1 = Result(back_score=12, seat_score=10, classification="Good Posture", p_id=p1.p_id)
    # db.session.add(r1)

    db.session.commit()

    print("Added bootstrap data")
