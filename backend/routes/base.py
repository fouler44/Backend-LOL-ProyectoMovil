from flask import Blueprint, request, jsonify
base_routes = Blueprint("base", __name__)

@base_routes.route("/", methods=["GET"])
def landing():
    return jsonify({"message": "Inicio"})