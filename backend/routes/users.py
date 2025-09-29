from flask import Blueprint, request, jsonify, redirect

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask_bcrypt import Bcrypt

user_routes = Blueprint("users", __name__)

@user_routes.route("/", methods=["GET"])
def landing():
    code = 200
    return jsonify({
        "code": code,
        "msg": "OK"
    }), code