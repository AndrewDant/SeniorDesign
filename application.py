from flask import Flask, request, render_template
from datetime import datetime, timedelta
from models import db, Pressure  # , Result
from k_nearest import *
import os
import json
import random

application = Flask(__name__)

application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    application.root_path, "post-chair.db"
)
# Suppress deprecation warning
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(application)


@application.route("/")
def index():
    return render_template("index.j2")


@application.route("/input/", methods=["POST"])
def data_input():
    data_json = request.get_json()

    back_score = generate_score([data_json['back_left'], data_json['back_right'], data_json['back_bottom']])
    seat_score = generate_score([data_json['seat_left'], data_json['seat_right'], data_json['seat_rear']])

    # TODO real classification
    p1 = Pressure(timestamp=datetime.now(), back_left=data_json['back_left'], back_right=data_json['back_right'],
                  back_bottom=data_json['back_bottom'],
                  seat_left=data_json['seat_left'], seat_right=data_json['seat_right'],
                  seat_rear=data_json['seat_rear'], back_score=back_score, seat_score=seat_score,
                  classification="Good Posture")

    db.session.add(p1)
    db.session.commit()

    return json.dumps(p1.serialize())


@application.route("/data/")
def data():
    # new_data = Pressure(timestamp=datetime.now(), back_left=random.randint(0, 1023),
    #                     back_right=random.randint(0, 1023), back_bottom=random.randint(0, 1023),
    #                     seat_left=random.randint(0, 1023), seat_right=random.randint(0, 1023),
    #                     seat_rear=random.randint(0, 1023), back_score=random.uniform(0, 50),
    #                     seat_score=random.uniform(0, 50),
    #                     classification=random.choice(["Good Posture", "Bad Posture"]))
    # db.session.add(new_data)
    # db.session.commit()

    num_minutes = int(request.args.get('minutes'))
    time_offset = datetime.now() - timedelta(minutes=num_minutes)

    data_list = db.session.query(Pressure).filter(Pressure.timestamp > time_offset) \
        .order_by(Pressure.timestamp.asc()).all()

    return json.dumps([d.serialize() for d in data_list])


@application.cli.command("initdb")
def init_db():
    db.drop_all()
    db.create_all()
    print("Initialized default DB")


@application.cli.command("bootstrap")
def bootstrap_data():
    db.drop_all()
    db.create_all()

    for _ in range(0, 10):
        p1 = Pressure(timestamp=datetime.now(), back_left=random.randint(0, 1023),
                      back_right=random.randint(0, 1023), back_bottom=random.randint(0, 1023),
                      seat_left=random.randint(0, 1023), seat_right=random.randint(0, 1023),
                      seat_rear=random.randint(0, 1023), back_score=random.uniform(0, 50),
                      seat_score=random.uniform(0, 50),
                      classification=random.choice(["Good Posture", "Bad Posture"]))
        db.session.add(p1)

    db.session.commit()

    print("Added bootstrap data")


main()


if __name__ == "__main__":
    init_db()
    application.run(threaded=True)
