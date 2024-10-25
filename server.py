import socketio
import eventlet
from flask import Flask

app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@app.route('/')
def index():
    return "Servidor WebSocket está funcionando!"

@sio.event
def connect(sid, environ):
    print(f"Cliente conectado: {sid}")

@sio.event
def joinRoom(sid, room):
    sio.enter_room(sid, room)
    print(f"Cliente {sid} entrou na sala {room}")

@sio.event
def moveMouse(sid, data):
    room = data.get('room')
    x = data.get('x')
    y = data.get('y')
    print(f"Movimento do mouse para X: {x}, Y: {y} na sala {room}")

    sio.emit("mouseMoved", {'x': x, 'y': y}, room=room, skip_sid=sid)

@sio.event
def click(sid, room):
    print(f"Clique do mouse recebido na sala: {room}")

    sio.emit("mouseClicked", room=room, skip_sid=sid)

@sio.event
def disconnect(sid):
    print(f"Cliente desconectado: {sid}")

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
