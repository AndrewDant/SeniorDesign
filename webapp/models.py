from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pressure(db.Modelx):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    back_left = db.Column(db.Float, nullable=False)
    back_right = db.Column(db.Float, nullable=False)
    back_bottom = db.Column(db.Float, nullable=False)
    seat_left = db.Column(db.Float, nullable=False)
    seat_right = db.Column(db.Float, nullable=False)
    seat_rear = db.Column(db.Float, nullable=False)


class Result(db.Model):
    isGood = db.Column(db.Boolean, nullable=False)
    pressure_set = db.Column(db.Integer, db.ForeignKey('pressure.id'), nullable=False)

    data = db.relationship('Pressure', foreign_keys=[pressure_set], backref='dataset')
