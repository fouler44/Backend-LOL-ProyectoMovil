import requests
import time
from config import RIOT_API_KEY

TIMEOUT = 10

def get_match_by_puuid(puuid, region="americas", count=20):
    """
    Obtiene una lista de IDs de partidas de un invocador.

    Args:
        puuid (str): El identificador único del invocador.
        region (str): La región para la API de partidas (por ejemplo, 'americas').
        count (int): El número de IDs de partidas a obtener.

    Returns:
        list: Una lista de strings con los IDs de las partidas.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    params = {"count": count}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()  # Lanza un error si la petición falla
        match_ids = response.json()
        print(f"Obtenidos {len(match_ids)} IDs de partidas para el PUUID: {puuid}")
        return match_ids
    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP: {err}")
    except Exception as err:
        print(f"Error inesperado: {err}")
    return []


def get_match_data(match_id, region="americas"):
    """
    Obtiene los datos detallados de una partida específica.

    Args:
        match_id (str): El ID de la partida.
        region (str): La región de la API de partidas.

    Returns:
        dict: Un diccionario con los datos detallados de la partida.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        match_data = response.json()
        print(f"Obtenidos datos para la partida: {match_id}")
        return match_data
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429: 
            print("Límite de peticiones excedido. Esperando 10 segundos...")
            time.sleep(10) 
        print(f"Error HTTP: {err}")
    except Exception as err:
        print(f"Error inesperado: {err}")
    return {}
