from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from config.db import get_session
from crud.user import get_user_by_id
from services.match_service import fetch_and_save_matches, get_player_match_history

match_routes = Blueprint("matches", __name__)


@match_routes.route("/sync", methods=["POST"])
@jwt_required()
def sync_my_matches():
    """
    Sincroniza las partidas del usuario autenticado
    
    Body (opcional):
    {
        "count": 20  # cantidad de partidas a sincronizar (default: 20)
    }
    """
    with get_session() as db:
        try:
            app_user_id = get_jwt_identity()
            user = get_user_by_id(db, app_user_id)
            
            if not user or not user.puuid:
                return jsonify({
                    "code": 404,
                    "msg": "Usuario no tiene cuenta de LoL vinculada"
                }), 404
            
            # Obtener parámetros
            data = request.get_json() or {}
            count = data.get("count", 20)
            
            # Necesitamos el platform del usuario
            from backend.crud.player import get_player_by_puuid
            player = get_player_by_puuid(db, user.puuid)
            
            if not player:
                return jsonify({
                    "code": 404,
                    "msg": "Datos del jugador no encontrados"
                }), 404
            
            # Sincronizar partidas
            stats = fetch_and_save_matches(
                db=db,
                puuid=user.puuid,
                platform=player.platform,
                count=count
            )
            
            return jsonify({
                "code": 200,
                "msg": "Partidas sincronizadas",
                "stats": stats
            }), 200
            
        except Exception as e:
            return jsonify({
                "code": 500,
                "msg": "Error al sincronizar partidas",
                "detail": str(e)
            }), 500


@match_routes.route("/history", methods=["GET"])
@jwt_required()
def get_my_match_history():
    """
    Obtiene el historial de partidas del usuario autenticado desde la DB
    
    Query params:
    - limit: cantidad de partidas (default: 20)
    """
    with get_session() as db:
        try:
            app_user_id = get_jwt_identity()
            user = get_user_by_id(db, app_user_id)
            
            if not user or not user.puuid:
                return jsonify({
                    "code": 404,
                    "msg": "Usuario no tiene cuenta de LoL vinculada"
                }), 404
            
            limit = request.args.get("limit", 20, type=int)
            
            matches = get_player_match_history(db, user.puuid, limit)
            
            return jsonify({
                "code": 200,
                "data": matches
            }), 200
            
        except Exception as e:
            return jsonify({
                "code": 500,
                "msg": "Error al obtener historial",
                "detail": str(e)
            }), 500


@match_routes.route("/history/<puuid>", methods=["GET"])
def get_player_history(puuid: str):
    """
    Obtiene el historial de partidas de cualquier jugador por PUUID
    
    Query params:
    - limit: cantidad de partidas (default: 20)
    """
    with get_session() as db:
        try:
            limit = request.args.get("limit", 20, type=int)
            matches = get_player_match_history(db, puuid, limit)
            
            if not matches:
                return jsonify({
                    "code": 404,
                    "msg": "No se encontraron partidas para este jugador"
                }), 404
            
            return jsonify({
                "code": 200,
                "data": matches
            }), 200
            
        except Exception as e:
            return jsonify({
                "code": 500,
                "msg": "Error al obtener historial",
                "detail": str(e)
            }), 500