
import requests
import json

def create_game(player_name):
    url = "http://localhost:8000/games"
    data = {"player_name": player_name}
    response = requests.post(url, json=data)
    return response.json()
def list_games():
    url = "http://localhost:8000/games"
    response = requests.get(url)
    
    # Verificar si la respuesta tiene el tipo de contenido correcto
    if response.headers.get('content-type') == 'application/json':
        return response.json()
    else:
        print("La respuesta del servidor no es JSON válido.")
        return []



def find_game_by_id(game_id):
    url = f"http://localhost:8000/games/{game_id}"
    response = requests.get(url)
    return response.json()

def find_game_by_name(player_name):
    games = list_games()
    for game in games:
        if game["player_name"] == player_name:
            return game
    return None

def update_attempts(game_id, guess):
    url = f"http://localhost:8000/games/{game_id}"
    data = {"guess": guess}
    response = requests.post(url, json=data)
    return response.json()

def delete_game(game_id):
    url = f"http://localhost:8000/games/{game_id}"
    response = requests.delete(url)
    return response.status_code == 200

# Ejemplos de uso
if __name__ == "__main__":
    # Crear una partida
    game = create_game("Jugador1")
    print("Partida creada:", game)

    # Listar partidas
    games = list_games()
    print("Listado de partidas:", games)

    # Buscar partida por ID
    game_id = 1
    game = find_game_by_id(game_id)
    print("Partida encontrada por ID:", game)

    # Buscar partida por nombre de jugador
    player_name = "Jugador1"
    game = find_game_by_name(player_name)
    print("Partida encontrada por nombre de jugador:", game)

    # Actualizar intentos
    game_id = 1
    guess = 50
    update_result = update_attempts(game_id, guess)
    print("Resultado de actualizar intentos:", update_result)

    # Eliminar partida
    game_id = 1
    delete_result = delete_game(game_id)
    if delete_result:
        print("Partida eliminada exitosamente")
    else:
        print("No se pudo eliminar la partida")



def list_games():
    url = "http://localhost:8000/games"
    response = requests.get(url)
    
    # Verificar si la respuesta tiene el tipo de contenido correcto
    if response.headers.get('content-type') == 'application/json':
        return response.json()
    else:
        print("La respuesta del servidor no es JSON válido.")
        return []
