import os
import requests

from flask import Blueprint, request, jsonify, redirect

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

player_routes = Blueprint("players", __name__)

@player_routes.route("/", methods=["GET"])
def landing():
    code = 200
    return jsonify({
        "code": code,
        "msg": "OK"
    }), code

@player_routes.route("/<puuid>", methods=["GET"])
def get_by_puuid(puuid):
    key = os.getenv("RIOT_API_KEY")
    req = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={key}")
    if(req.status_code != 200):
        code = 404
        return jsonify({
            "code": code,
            "msg": "Account not found"
        }), code
    
    code = 200
    return jsonify({
        "code": code,
        "data": req.json()
    }), code

@player_routes.route("/<user>/<tag>", methods=["GET"])
def get_by_usertag(user, tag):
    key = os.getenv("RIOT_API_KEY")
    req = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user}/{tag}?api_key={key}")
    if(req.status_code != 200):
        code = 404
        return jsonify({
            "code": code,
            "msg": "Account not found"
        }), code
    
    code = 200
    return jsonify({
        "code": code,
        "data": req.json()
    }), code