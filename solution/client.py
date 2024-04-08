
import requests
import json

BASE_URL = 'http://localhost:8000'

def create_game(player_name):
    url = f'{BASE_URL}/games'
    data = {'player_name': player_name}
    response = requests.post(url, json=data)
    return response.json()

def list_games():
    url = f'{BASE_URL}/games'
    response = requests.get(url)
    return response.json()

def get_game_by_id(game_id):
    url = f'{BASE_URL}/games/{game_id}'
    response = requests.get(url)
    return response.json()

def get_game_by_player(player_name):
    games = list_games()
    for game in games:
        if game['player_name'] == player_name:
            return game
    return None

def update_attempts(game_id, attempts):
    url = f'{BASE_URL}/games/{game_id}'
    data = {'attempts': attempts}
    response = requests.put(url, json=data)
    return response.json()

def delete_game(game_id):
    url = f'{BASE_URL}/games/{game_id}'
    response = requests.delete(url)
    return response.status_code == 204


if __name__ == "__main__":
    # Crear una partida
    game = create_game("Julian")
    print("Partida creada:", game)

    # Listar todas las partidas
    games = list_games()
    print("Todas las partidas:", games)
    

    # Buscar una partida por su id
    game_id = game['id']
    game_by_id = get_game_by_id(game_id)
    print("Partida por id:", game_by_id)

    # Buscar una partida por el nombre del jugador
    player_name = "Jugador1"
    game_by_player = get_game_by_player(player_name)
    print("Partida por jugador:", game_by_player)

    # Actualizar los intentos de una partida
    game_id = game['id']
    updated_game = update_attempts(game_id, 5)
    print("Partida actualizada:", updated_game)

    # Envia un valor

    
    # Eliminar una partida
    deleted = delete_game(game_id)
    if deleted:
        print("Partida eliminada con éxito")
    else:
        print("Error al eliminar la partida")





