from flask import Flask, request, render_template
from datetime import datetime, timedelta
from models import db, Pressure  # , Result
from k_nearest import *
import os
import json
import random
import math

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

    back_left = data_json['back_left']
    back_right = data_json['back_right']
    back_bottom = data_json['back_bottom']
    back_score = generate_score([back_left, back_right, back_bottom])
    seat_left = data_json['seat_left']
    seat_right = data_json['seat_right']
    seat_rear = data_json['seat_rear']
    seat_score = generate_score([seat_left, seat_right, seat_rear])

    # TODO check that knn is initialized
    classification = make_prediction(knn, back_score, seat_score)
    feedback = ""
    if classification.lower() == "bad":
        feedback = make_advice(back_left, back_right, back_bottom,
                               seat_left, seat_right, seat_rear)

    p1 = Pressure(timestamp=datetime.now(), back_left=back_left, back_right=back_right,
                  back_bottom=back_bottom,
                  seat_left=seat_left, seat_right=seat_right,
                  seat_rear=seat_rear, back_score=back_score, seat_score=seat_score,
                  classification=classification,
                  feedback=feedback)

    db.session.add(p1)
    db.session.commit()

    return json.dumps(p1.serialize())


@application.route("/data/")
def data():
    # random fake data for testing
    # new_data = Pressure(timestamp=datetime.now(), back_left=random.randint(0, 1023),
    #                     back_right=random.randint(0, 1023), back_bottom=random.randint(0, 1023),
    #                     seat_left=random.randint(0, 1023), seat_right=random.randint(0, 1023),
    #                     seat_rear=random.randint(0, 1023), back_score=random.uniform(0, 50),
    #                     seat_score=random.uniform(0, 50),
    #                     classification=random.choice(["Good Posture", "Bad Posture"]),
    #                     feedback="")
    # db.session.add(new_data)
    # db.session.commit()

    num_minutes = int(request.args.get('minutes'))
    time_offset = datetime.now() - timedelta(minutes=num_minutes)

    data_list = db.session.query(Pressure).filter(Pressure.timestamp > time_offset) \
        .order_by(Pressure.timestamp.asc()).all()

    all_data = dict()

    length = len(data_list)

    avg_back_score, avg_seat_score = 0, 0
    avg_back_left, avg_back_right, avg_back_bottom = 0, 0, 0
    avg_seat_left, avg_seat_right, avg_seat_rear = 0, 0, 0

    labels = []

    back_score_data = []
    seat_score_data = []

    back_left_data = []
    back_right_data = []
    back_bottom_data = []
    seat_left_data = []
    seat_right_data = []
    seat_rear_data = []

    # if no data pass empty dict
    if length > 0:
        current_values = data_list[-1]

        all_data.update({"latest": current_values.serialize()})

        for element in data_list:
            avg_back_score += element.back_score / length
            avg_seat_score += element.seat_score / length

            avg_back_left += element.back_left / length
            avg_back_right += element.back_right / length
            avg_back_bottom += element.back_bottom / length
            avg_seat_left += element.seat_left / length
            avg_seat_right += element.seat_right / length
            avg_seat_rear += element.seat_rear / length

        average_values = Pressure(timestamp=datetime.now(), back_left=avg_back_left, back_right=avg_back_right,
                                  back_bottom=avg_back_bottom,
                                  seat_left=avg_seat_left, seat_right=avg_seat_right,
                                  seat_rear=avg_seat_rear, back_score=avg_back_score, seat_score=avg_seat_score,
                                  classification=make_prediction(knn, avg_back_score, avg_seat_score),
                                  feedback=make_advice(avg_back_left, avg_back_right, avg_back_bottom,
                                                       avg_seat_left, avg_seat_right, avg_seat_rear))
        all_data.update({"average": average_values.serialize()})

        decimation_factor = math.floor(math.sqrt(length))

        # populate chart with decimated data
        for j in range(0, length - decimation_factor + 1, decimation_factor):
            back_score_point, seat_score_point = 0, 0

            back_left_point, back_right_point, back_bottom_point = 0, 0, 0
            seat_left_point, seat_right_point, seat_rear_point = 0, 0, 0

            # TODO needs to be more consistent
            #  aka jump less, use same starting points when decFactor same?

            for k in range(0, decimation_factor):
                back_score_point += data_list[j + k].back_score
                seat_score_point += data_list[j + k].seat_score

                back_left_point += data_list[j + k].back_left
                back_right_point += data_list[j + k].back_right
                back_bottom_point += data_list[j + k].back_bottom
                seat_left_point += data_list[j + k].seat_left
                seat_right_point += data_list[j + k].seat_right
                seat_rear_point += data_list[j + k].seat_rear

            # TODO improve
            labels.append(data_list[j + math.floor(decimation_factor / 2)].time_string())

            back_score_data.append(back_score_point / decimation_factor)
            seat_score_data.append(seat_score_point / decimation_factor)

            back_left_data.append(back_left_point / decimation_factor)
            back_right_data.append(back_right_point / decimation_factor)
            back_bottom_data.append(back_bottom_point / decimation_factor)
            seat_left_data.append(seat_left_point / decimation_factor)
            seat_right_data.append(seat_right_point / decimation_factor)
            seat_rear_data.append(seat_rear_point / decimation_factor)

        all_data.update({"labels": labels,
                         "back_score_data": back_score_data,
                         "seat_score_data": seat_score_data,
                         "back_left_data": back_left_data,
                         "back_right_data": back_right_data,
                         "back_bottom_data": back_bottom_data,
                         "seat_left_data": seat_left_data,
                         "seat_right_data": seat_right_data,
                         "seat_rear_data": seat_rear_data})

    return json.dumps(all_data)


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
                      classification=random.choice(["Good Posture", "Bad Posture"]),
                      feedback="")
        db.session.add(p1)

    db.session.commit()

    print("Added bootstrap data")


knn = main()

if __name__ == "__main__":
    init_db()
    application.run(threaded=True)
