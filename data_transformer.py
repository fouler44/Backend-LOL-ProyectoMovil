def clean_str(val, max_len = 80):
    """Convierte a str, recorta espacios y limita longitud."""
    if val is None:
        return ""
    s = str(val).strip()
    if max_len and len(s) > max_len:
        return s[:max_len]
    return s

def coerce_int(val, default = 0):
    """Convierte a int si es posible, si no devuelve default."""
    try:
        return int(float(val))
    except Exception:
        return default

def coerce_bool(val, default = False):
    """Convierte a booleano con heurística simple."""
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        v = val.strip().lower()
        if v in ("true", "1", "yes", "y", "t"):
            return True
        if v in ("false", "0", "no", "n", "f"):
            return False
    if isinstance(val, (int, float)):
        return val != 0
    return default

def safe_get(d, *keys, default=None):
    """Acceso anidado seguro: safe_get(obj, 'a','b','c')."""
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def transform_match_data(match_data):
    """
    Recibe el JSON crudo de la Riot API para una partida y devuelve:
      - match_info: Dict con metadatos de la partida
      - participants_data: List[ (player_dict, champion_dict, participation_dict) ]

    Si faltan campos críticos, devuelve (None, []).
    """
    
    if not isinstance(match_data, dict):
        print("ERROR: match_data no es un dict")
        return None, []
    
    info = match_data.get("info") or {}
    meta = match_data.get("metadata") or {}
    
    # ↓ Transformar los datos de partida
    
    match_id = clean_str(meta.get("matchId"), max_len=50)
    if not match_id:
        print("matchId ausente en metadata")
        return None, []
    
    duration_seconds = coerce_int(info.get("gameDuration"), 0)
    if duration_seconds <= 0:
        start_ts = coerce_int(info.get("gameStartTimestamp"), 0)
        end_ts = coerce_int(info.get("gameEndTimestamp"), 0)
        
        if end_ts > start_ts > 0:
            duration_seconds = (end_ts - start_ts) // 1000 # ms -> s
        
    game_mode = clean_str(info.get("gameMode") or "UNKNOWN", max_len=50)
    patch_version = clean_str(info.get("gameVersion") or "UNKNOWN")
    
    match_info = {
        "match_id": match_id,
        "duration_seconds": duration_seconds,
        "game_mode": game_mode,
        "patch_version": patch_version
    }
    
    
    # A partir de aqui voy a transformar los participantes
    
    participants = info.get("participants") or []
    if not isinstance(participants, list) or not participants:
        print(f"Partida {match_id}: invalida")
        return match_info, []
    
    rows = []
    
    
    for i, participant in enumerate(participants, start=1):
        if not isinstance(participant, dict):
            print(f"Partida {match_id}: Participante {i} no es válido")
            continue
    
        #puuid
        puuid = clean_str(participant.get("puuid"), max_len=78)
        if not puuid:
            print(f"Partida {match_id}: participante {i} sin puuid")
        
        
        #summoner_name
        game_name = clean_str(participant.get("riotIdGameName"))
        tag = clean_str(participant.get("riotIdTagline"), max_len=6)
        if game_name and tag:
            summoner_name = f"{game_name}#{tag}"
        else:
            summoner_name = clean_str(participant.get("summonerName"), max_len=80)
            
        player_dict = {
            "puuid": puuid,
            "summoner_name": summoner_name
        }
        
        # Champion ---------
        
        champion_id = coerce_int(participant.get("championId"), 0)
        champion_name = clean_str(participant.get("championName"))
        
        champion_dict = {
            "champion_id": champion_id,
            "champion_name": champion_name
        }
        
        # Participation
        
        kills = coerce_int(participant.get("kills", 0))
        deaths = coerce_int(participant.get("deaths", 0))
        assists = coerce_int(participant.get("assists", 0))
        lane = clean_str(participant.get("lane") or participant.get("teamPosition") or "UNKNOWN", max_len=20)
        win = coerce_bool(participant.get("win"), False)
        
        participation_dict = {
            "match_id": match_id,
            "puuid": puuid,
            "champion_id": champion_id,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "lane": lane,
            "win": win
        }
        
        rows.append((player_dict, champion_dict, participation_dict))
        
    if not rows:
        print(f"Partida {match_id}: los participantes no fueron validos")
        
    return match_info, rows
