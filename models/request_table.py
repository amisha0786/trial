from datetime import datetime

from db import db 

class RequestModel(db.Model):
    __tablename__ = "requests"

    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    asl_name = db.Column(db.Text, nullable=False)
    emr_version = db.Column(db.Text, nullable=False)
    max_size = db.Column(db.Float, nullable=False)
    min_size = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    approval_status = db.Column(db.Boolean , default = False )
    scaling_type = db.Column(db.Text , nullable=False)

    # def as_dict(self):
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}



