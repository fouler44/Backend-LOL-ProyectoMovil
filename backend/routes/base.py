import datetime
from flask import Blueprint, request, jsonify, redirect

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

base_routes = Blueprint("base", __name__)

'''
  GET /
  GET /login
  POST /login
  GET /signup
  POST /signup
'''

@base_routes.route("/", methods=["GET"])
def landing():
    code = 200
    return jsonify({
        "code": code,
        "msg": "OK"
    }), code

@base_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        code = 400
        return jsonify({
            "code": code,
            "msg": "Username and password required"
        }), code
    
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(minutes=60))
    code = 200
    return jsonify(access_token=access_token)

@base_routes.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user = get_jwt_identity()
    code = 200
    return jsonify({
        "code": code,
        "msg": f"Logged in as {user}"
    }), code