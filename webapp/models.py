from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pressure(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    back_left = db.Column(db.Float, nullable=False)
    back_right = db.Column(db.Float, nullable=False)
    back_bottom = db.Column(db.Float, nullable=False)
    seat_left = db.Column(db.Float, nullable=False)
    seat_right = db.Column(db.Float, nullable=False)
    seat_rear = db.Column(db.Float, nullable=False)


class Result(db.Model):
    # good scores are any in a certain range i.e. 0-30
    back_score = db.Column(db.Float, nullable=False)
    seat_score = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String, nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey('pressure.id'), primary_key=True)

    data = db.relationship('Pressure', foreign_keys=[p_id], backref='dataset')
