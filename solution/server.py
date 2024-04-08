
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class NumberGuessGame:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.games = {}
        return cls._instance

    def create_game(self, player_name):
        game_id = len(self.games) + 1
        number_to_guess = random.randint(1, 100)
        game_data = {
            "id": game_id,
            "number_to_guess": number_to_guess,
            "attempts": 0,
            "guesses": [],
            "player_name": player_name
        }
        self.games[game_id] = game_data
        return game_data

    def guess_number(self, game_id, guess):
        game = self.games.get(game_id)
        if game:
            game["attempts"] += 1
            game["guesses"].append(guess)
            if guess == game["number_to_guess"]:
                return "¡Felicidades! Has adivinado el número.", True
            elif guess < game["number_to_guess"]:
                return "El número es mayor.", False
            else:
                return "El número es menor.", False
        else:
            return "Juego no encontrado.", False

class NumberGuessRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.game_instance = NumberGuessGame()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/games":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            player_name = data.get("player_name")
            game = self.game_instance.create_game(player_name)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game).encode("utf-8"))
        elif self.path.startswith("/games/"):
            game_id = int(self.path.split("/")[2])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            guess = int(json.loads(post_data.decode("utf-8"))["guess"])
            response, game_over = self.game_instance.guess_number(game_id, guess)
            response_data = {"message": response, "game_over": game_over}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, NumberGuessRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
    
    
    
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class NumberGuessRequestHandler(BaseHTTPRequestHandler):
    # Resto del código del servidor...

    def do_GET(self):
        if self.path == "/games":
            games_data = self.game_instance.games.values()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(list(games_data)).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()





from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class NumberGuessGame:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.games = {}
        return cls._instance

    def create_game(self, player_name):
        game_id = len(self.games) + 1
        number_to_guess = random.randint(1, 100)
        game_data = {
            "id": game_id,
            "number_to_guess": number_to_guess,
            "attempts": 0,
            "guesses": [],
            "player_name": player_name
        }
        self.games[game_id] = game_data
        return game_data

    def get_game(self, game_id):
        return self.games.get(game_id)

    def update_game(self, game_id, new_data):
        if game_id in self.games:
            self.games[game_id].update(new_data)
            return True
        else:
            return False

    def delete_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]
            return True
        else:
            return False

class NumberGuessRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.game_instance = NumberGuessGame()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/games":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            player_name = data.get("player_name")
            game = self.game_instance.create_game(player_name)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path.startswith("/games/"):
            game_id = int(self.path.split("/")[2])
            game = self.game_instance.get_game(game_id)
            if game:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(game).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith("/games/"):
            game_id = int(self.path.split("/")[2])
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode("utf-8"))
            if self.game_instance.update_game(game_id, data):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Game updated successfully"}).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/games/"):
            game_id = int(self.path.split("/")[2])
            if self.game_instance.delete_game(game_id):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Game deleted successfully"}).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, NumberGuessRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
