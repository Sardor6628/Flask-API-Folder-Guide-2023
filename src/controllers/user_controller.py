from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime
import jwt
import os

users = Blueprint("users", __name__)


@users.route('/signup', methods=["POST"])
def handle_signup():
    try:
        data = request.json
        if "firstname" in data and "lastname" in data and "email" in data and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if not user:
                user_obj = User(
                    firstname=data["firstname"],
                    lastname=data["lastname"],
                    email=data["email"],
                    password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
                )
                db.session.add(user_obj)
                db.session.commit()

                payload = {
                    'iat': datetime.utcnow(),
                    'user_id': str(user_obj.id).replace('-', ""),
                    'firstname': user_obj.firstname,
                    'lastname': user_obj.lastname,
                    'email': user_obj.email,
                }
                token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                return Response(
                    response=json.dumps({'status': "success", "message": "User Sign up Successful", "token": token}),
                    status=201,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps({'status': "failed", "message": "User already exists kindly use sign in"}),
                    status=409,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({'status': "failed",
                                     "message": "User Parameters Firstname, Lastname, Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred - 1", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@users.route('/signin', methods=["POST"])
def handle_signin():
    try:
        data = request.json
        user = User.query.filter_by(email=data["email"]).first()
        check_validity = not user or not bcrypt.check_password_hash(user.password, data["password"])
        if check_validity:
            raise ValueError("Wrong login credentials!")
        if "email" in data and "password" in data:
            return Response(
                response=json.dumps({'status': "success", "message": "User Sign up Successful", "token": ""}),
                status=201,
                mimetype='application/json'
            )
        else:
            raise ValueError("Email or password is missing")
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred - 1", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@users.route('/usersAll', methods=["GET"])
def get_all_users():
    try:
        users = User.query.all()
        list_of_users = []
        for _user in users:
            payload = {
                "user_name": _user.firstname + " " + _user.lastname,
                "email": _user.email}
            list_of_users.append(payload)
        return Response(
                response=json.dumps(
                    {'status': "success","users": list_of_users}),
                status=200,
                mimetype='application/json')
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred - 1", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )
