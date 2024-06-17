from datetime import datetime
from models.request_table import RequestModel
from db import db 

class StatusModel(db.Model): 
    __tablename__ = 'statuses' 
    request_id = db.Column(db.Text, db.ForeignKey('requests.request_id'), primary_key=True) 
    status_code = db.Column(db.Text, nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

