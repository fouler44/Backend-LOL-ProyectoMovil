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
            from crud.player import get_player_by_puuid
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
            
@match_routes.route("/<match_id>/details", methods=["GET"])
def get_match_details(match_id: str):
    with get_session() as db:
        try:
            from crud.match import get_match_by_id, get_participations_by_match
            
            match = get_match_by_id(db, match_id)
            if not match:
                return jsonify({"code": 404, "msg": "Partida no encontrada"}), 404
            
            participations = get_participations_by_match(db, match_id)
            
            # Separar por team_id
            team_100 = []  # Equipo azul
            team_200 = []  # Equipo rojo
            
            for part in participations:
                player_data = {
                    "puuid": part.puuid,
                    "game_name": part.game_name,
                    "tag": part.tag,
                    "champion_id": part.champion_id,
                    "kills": part.kills,
                    "deaths": part.deaths,
                    "assists": part.assists,
                    "kda": float(part.kda),
                    "kp": float(part.kp),
                    "total_damage": float(part.total_damage),
                    "damage_per_min": part.damage_per_min,
                    "lane": part.lane,
                    "champion_level": part.champion_level,
                    "items": part.item_slots,
                    "trinket": part.trinket,
                    "cs": part.total_minions,
                    "vision_score": part.vision_score,
                    "win": part.win,
                }
                
                if part.team_id == 100:
                    team_100.append(player_data)
                else:
                    team_200.append(player_data)
            
            return jsonify({
                "code": 200,
                "data": {
                    "match": {
                        "match_id": match.match_id,
                        "duration_seconds": match.duration_seconds,
                        "game_mode": match.game_mode,
                        "game_status": match.game_status,
                        "patch_version": match.patch_version,
                    },
                    "teams": {
                        "blue": team_100,
                        "red": team_200
                    }
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                "code": 500,
                "msg": "Error al obtener detalles",
                "detail": str(e)
            }), 500