# import uuid
# from flask import request
# from flask.views import MethodView
# from flask_smorest import Blueprint, abort

# from db import db
# from sqlalchemy.exc import SQLAlchemyError
# #from models import request_entry 

# blp = Blueprint("Requests", __name__, description="Operations on request_table")
# from models.request_table import RequestModel
# from models.status_table import StatusModel


# @blp.route("/request/<string:request_id>")
# class Request_values(MethodView):
#     def get(self , request_id):
#         try:
#             status_table[request_id] = "retrieved"

#             return request_table[request_id]
        
#         # item = ItemModel.query.get_or_404(item_id)
#         # return item
#         except KeyError:
#             abort(404, message="Request not found.")  


#     def delete(self,request_id):
#         try:
#             del request_table[request_id]
#             status_table[request_id] = "deleted"
#             return {"message": "Request deleted successfully."}, 200
#         except KeyError:
#             abort(404, message="Request not found.")

#     def put(self , request_id):
#         request_data = request.get_json()
#         required_fields = ["user_name", "user_id", "asl_name", "scaling_type", "start_date", "end_date", "max_size", "min_size", "emr_version"]

#         if not all(field in request_data for field in required_fields):
#             abort(400, message="Bad request. Ensure all values are included in the JSON payload.")

#         if request_id in request_table:
#             # Update the existing request
#             request_table[request_id].update(request_data)
#             status_table[request_id] = "updated"
#             return request_table[request_id]
#         else:
#             # Create a new request with the given ID
#             request_generated = {**request_data, "request_id": request_id}
#             request_table[request_id] = request_generated
#             status_table[request_id] = "created"
#             return request_generated, 201

# @blp.route("/list/asl/<string:asl_name>")
# class Request_asl_list (MethodView):
#     def get(self , asl_name):
#         return_list = [value for value in request_table.values() if value.get("asl_name") == asl_name]
#         if not return_list:
#             abort(404, message="Request not found.")
#         for req in return_list:
#             status_table[req["request_id"]] = "retrieved"
#         return return_list



# @blp.route("/list/user/<string:user_id>")
# class Request_user_request_list (MethodView):
#     def get(self , user_id):
#         return_list = [value for value in request_table.values() if value.get("user_id") == user_id]
#         if not return_list:
#             abort(404, message="Request not found.")
#         for req in return_list:
#             status_table[req["request_id"]] = "retrieved"
#         return return_list


# @blp.route("/requests")
# class Get_all_request(MethodView):
#     def get(self):
#         return request_table  


# @blp.route("/create")
# class Create_request(MethodView) :
#     def post(self  ):
#         request_values = request.get_json()
#         request_data = RequestModel(** request_values)
       
#         try:
#              # status_table[request_id] = "created"
#             db.session.add(request_data)
#             db.session.commit()
#         except SQLAlchemyError:
#             abort(500, message="An error occurred while inserting the item.")

       
       
       


import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from sqlalchemy.exc import SQLAlchemyError
from models.request_table import RequestModel
from models.status_table import StatusModel

blp = Blueprint("Requests", __name__, description="Operations on request_table")

@blp.route("/request/<string:request_id>")
class RequestValues(MethodView):
    def get(self, request_id):
        request_item = RequestModel.query.get(request_id)
        if not request_item:
            abort(404, message="Request not found.")
        
        status = StatusModel.query.get(request_id)
        if not status:
            status = StatusModel(request_id=request_id, status_code="retrieved")
            db.session.add(status)
        else:
            status.status_code = "retrieved"
        db.session.commit()

        return request_item.as_dict()

    def delete(self, request_id):
        request_item = RequestModel.query.get(request_id)
        if not request_item:
            abort(404, message="Request not found.")
        
        db.session.delete(request_item)
        
        status = StatusModel.query.get(request_id)
        if status:
            status.status_code = "deleted"
        else:
            status = StatusModel(request_id=request_id, status_code="deleted")
            db.session.add(status)
        
        db.session.commit()
        return {"message": "Request deleted successfully."}, 200

    def put(self, request_id):
        request_data = request.get_json()
        required_fields = ["user_name", "user_id", "asl_name", "scaling_type", "start_date", "end_date", "max_size", "min_size", "emr_version"]

        if not all(field in request_data for field in required_fields):
            abort(400, message="Bad request. Ensure all values are included in the JSON payload.")

        request_item = RequestModel.query.get(request_id)
        if request_item:
            # Update the existing request
            for key, value in request_data.items():
                setattr(request_item, key, value)
            status = StatusModel.query.get(request_id)
            if not status:
                status = StatusModel(request_id=request_id, status_code="updated")
                db.session.add(status)
            else:
                status.status_code = "updated"
            db.session.commit()
            return request_item.as_dict()
        else:
            # Create a new request with the given ID
            request_generated = RequestModel(id=request_id, **request_data)
            db.session.add(request_generated)
            status_generated = StatusModel(request_id=request_id, status_code="created")
            db.session.add(status_generated)
            db.session.commit()
            return request_generated.as_dict(), 201

@blp.route("/list/asl/<string:asl_name>")
class RequestAslList(MethodView):
    def get(self, asl_name):
        requests = RequestModel.query.filter_by(asl_name=asl_name).all()
        if not requests:
            abort(404, message="Request not found.")
        for request_item in requests:
            status = StatusModel.query.get(request_item.id)
            if not status:
                status = StatusModel(request_id=request_item.id, status_code="retrieved")
                db.session.add(status)
            else:
                status.status_code = "retrieved"
        db.session.commit()
        return [request_item.as_dict() for request_item in requests]

@blp.route("/list/user/<string:user_id>")
class RequestUserRequestList(MethodView):
    def get(self, user_id):
        requests = RequestModel.query.filter_by(user_id=user_id).all()
        if not requests:
            abort(404, message="Request not found.")
        for request_item in requests:
            status = StatusModel.query.get(request_item.id)
            if not status:
                status = StatusModel(request_id=request_item.id, status_code="retrieved")
                db.session.add(status)
            else:
                status.status_code = "retrieved"
        db.session.commit()
        return [request_item.as_dict() for request_item in requests]

@blp.route("/requests")
class GetAllRequests(MethodView):
    def get(self):
        requests = RequestModel.query.all()
        return [request.as_dict() for request in requests]

@blp.route("/create")
class CreateRequest(MethodView):
    def post(self):
        request_values = request.get_json()
        request_id = uuid.uuid4().hex
        request_data = RequestModel(id=request_id, **request_values)
        status_data = StatusModel(request_id=request_id, status_code="created")
        
        try:
            db.session.add(request_data)
            db.session.add(status_data)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while inserting the item.")
        
        return request_data.as_dict(), 201
