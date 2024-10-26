from flask import Blueprint

main = Blueprint("main", __name__)

@main.route("/")
def index():
   return {"status": "Servidor WebSocket esta funcionando!"}, 200