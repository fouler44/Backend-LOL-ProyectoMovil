import datetime
from flask import Blueprint, request, jsonify, redirect

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask_bcrypt import Bcrypt

from config.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from models.user import AppUser

from crud.user import update_user_puuid

bcrypt = Bcrypt()

user_routes = Blueprint("user", __name__)

@user_routes.route("/", methods=["GET"])
@jwt_required()
def get_authenticated_user():
    username = get_jwt_identity()
    conn = SessionLocal()
    user = conn.scalars(select(AppUser).filter_by(username=username)).first()
    if not user:
        code = 404
        return jsonify({
            "code": code,
            "msg": "El usuario proporcionado no existe"
        }), code
    
    code = 200
    return jsonify({
        "code": code,
        "user": user.data()
    })

@user_routes.route("/create", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        code = 400
        return jsonify({
            "code": code,
            "msg": "Username and password required"
        }), code

    conn = SessionLocal()
    user = conn.scalars(select(AppUser).filter_by(username=username)).first()
    if user:
        code = 409
        return jsonify({
            "code": code,
            "msg": f"El usuario {username} ya existe"
        }), code
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = AppUser(username=username, hashed_password=hashed_password)
    conn.add(new_user)
    conn.commit()
    conn.close()

    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(minutes=60))

    code = 200
    return jsonify({
        "code": code,
        "msg": f"User {username} created",
        "access_token": access_token
    }), code

@user_routes.route("/edit/pwd", methods=["PUT", "PATCH"])
@jwt_required()
def change_pwd():
    data = request.get_json()
    username = get_jwt_identity()
    current_pwd = data.get("password")
    new_pwd = data.get("new_password")
    if not current_pwd or not new_pwd:
        code = 400
        return jsonify({
            "code": code,
            "msg": "Se requieren los parametros 'password' y 'new_password'"
        }), code

    conn = SessionLocal()
    user = conn.scalars(select(AppUser).filter_by(username=username)).first()
    if not user:
        code = 404
        return jsonify({
            "code": code,
            "msg": "El usuario proporcionado no existe"
        }), code
    
    user_data = user.data()
    if not bcrypt.check_password_hash(user_data["hashed_password"], current_pwd):
        code = 401
        return jsonify({
            "code": code,
            "msg": "Credenciales incorrectas"
        }), code
    
    user.hashed_password = bcrypt.generate_password_hash(new_pwd).decode("utf-8")
    conn.commit()
    conn.close()

    code = 200
    return jsonify({
        "code": code,
        "msg": f"Contraseña del usuario {username} actualizada"
    })

@user_routes.route("/edit/puuid", methods=["PUT", "PATCH"])
@jwt_required()
def change_puuid():
    data = request.get_json()
    username = get_jwt_identity()
    puuid = data.get("puuid")
    if not puuid:
        code = 400
        return jsonify({
            "code": code,
            "msg": "Se requiere el parámetro 'puuid'"
        }), code

    conn = SessionLocal()
    user = conn.scalars(select(AppUser).filter_by(username=username)).first()
    if not user:
        code = 404
        return jsonify({
            "code": code,
            "msg": "El usuario proporcionado no existe"
        }), code
    
    update_user_puuid(conn, user.data()["user_id"], puuid)
    conn.commit()
    conn.close()

    code = 200
    return jsonify({
        "code": code,
        "msg": f"PUUID del usuario {username} actualizada: {puuid}"
    })

@user_routes.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    data = request.get_json()
    username = get_jwt_identity()
    password = data.get("password")
    if not password:
        code = 400
        return jsonify({
            "code": code,
            "msg": "Se requiere el parámetro 'password'"
        }), code

    conn = SessionLocal()
    user = conn.scalars(select(AppUser).filter_by(username=username)).first()
    if not user:
        code = 404
        return jsonify({
            "code": code,
            "msg": "El usuario proporcionado no existe"
        }), code
    
    user_data = user.data()
    if not bcrypt.check_password_hash(user_data["hashed_password"], password):
        code = 401
        return jsonify({
            "code": code,
            "msg": "Credenciales incorrectas"
        }), code
    
    conn.delete(user)
    conn.commit()
    conn.close()

    code = 200
    return jsonify({
        "code": code,
        "msg": f"Usuario {username} eliminado"
    })