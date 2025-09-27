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
        "message": "OK"
    }), code

@base_routes.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        code = 200
        return jsonify({
            "code": code,
            "message": "OK"
        }), code
    else:
        return redirect("/login")