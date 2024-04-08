
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