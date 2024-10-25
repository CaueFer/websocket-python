from flask import Flask, request
from flask_socketio import SocketIO, join_room, emit
from gevent import monkey

# Necessário para que o SocketIO funcione de forma assíncrona com Flask
monkey.patch_all()

# Configuração inicial do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuração do SocketIO com gevent
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# ROUTES
@app.route('/')
def index():
    return "Servidor WebSocket está funcionando!"



# SOCKETIO EVENTS
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado:", request.sid)
    emit('connect', {'message': 'Conectado ao servidor WebSocket!'})

@socketio.on('joinRoom')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    print(f"Cliente {request.sid} entrou na sala: {room}")
    emit('roomJoined', {'room': room}, to=room)

@socketio.on('moveMouse')
def handle_mouse_move(data):
    room = data['room']
    x, y = data['x'], data['y']
    print(f"Movimento do mouse: X={x}, Y={y} na sala {room}")
    emit('mouseMoved', {'x': x, 'y': y}, to=room)

@socketio.on('click')
def handle_click(data):
    room = data['room']
    print(f"Clique recebido na sala: {room}")
    emit('mouseClicked', {}, to=room)

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado:", request.sid)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
