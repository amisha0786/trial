# import uuid
# from flask import request
# from flask.views import MethodView
# from flask_smorest import Blueprint, abort

# from db import request_table
# from db import status_table
# from sqlalchemy.exc import SQLAlchemyError

# blp = Blueprint("Status", __name__, description="Operations on status")


# @blp.route("/status/<string:request_id>")
# def get(request_id):
#     try:
#         return {"request_id": request_id, "status": status_table[request_id]} , 200
#     except KeyError:
#         abort(404, message="Request not found.")


# @blp.route("/status")
# def get():
#     return status_table       



import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models.status_table import StatusModel
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Status", __name__, description="Operations on status")

@blp.route("/status/<string:request_id>")
class StatusResource(MethodView):
    def get(self, request_id):
        status = StatusModel.query.get(request_id)
        if not status:
            abort(404, message="Request not found.")
        return {"request_id": request_id, "status": status.status_code}, 200

@blp.route("/status")
class StatusListResource(MethodView):
    def get(self):
        statuses = StatusModel.query.all()
        return [status.as_dict() for status in statuses]

# Register the blueprint in your main application file
# from app import app
# app.register_blueprint(blp, url_prefix='/api')