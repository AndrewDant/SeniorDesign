from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pressure(db.Model):
    # left/right based on sitting on the seat and facing forward
    p_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    back_left = db.Column(db.Float, nullable=False)
    back_right = db.Column(db.Float, nullable=False)
    back_bottom = db.Column(db.Float, nullable=False)
    seat_left = db.Column(db.Float, nullable=False)
    seat_right = db.Column(db.Float, nullable=False)
    seat_rear = db.Column(db.Float, nullable=False)

    # TODO separate Result model?
    # good scores are any in a certain range i.e. 0-30
    back_score = db.Column(db.Float, nullable=False)
    seat_score = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            'p_id': self.p_id,
            'timestamp': self.timestamp.strftime("%H:%M:%S"),
            'back_left': self.back_left,
            'back_right': self.back_right,
            'back_bottom': self.back_bottom,
            'seat_left': self.seat_left,
            'seat_right': self.seat_right,
            'seat_rear': self.seat_rear,

            # TODO separate Result model?
            'back_score': self.back_score,
            'seat_score': self.seat_score,
            'classification': self.classification
        }


# class Result(db.Model):
#     # good scores are any in a certain range i.e. 0-30
#     back_score = db.Column(db.Float, nullable=False)
#     seat_score = db.Column(db.Float, nullable=False)
#     classification = db.Column(db.String, nullable=False)
#     p_id = db.Column(db.Integer, db.ForeignKey('pressure.p_id'), primary_key=True)
#
#     data = db.relationship('Pressure', foreign_keys=[p_id], backref='dataset')
