from flask import request
from flask_socketio import emit, join_room

from .extensions import socketio

# SOCKETIO EVENTS
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado:", request.sid)
    emit('connect', {'message': 'Conectado ao servidor WebSocket!'})

@socketio.on('joinRoom')
def handle_join_room(data):
    room = data.get('room')
    
    if not room:
        emit('error', {'message': 'Sala não especificada!'})
        return

    join_room(room)
    print(f"Cliente {request.sid} entrou na sala: {room}")
    emit('roomJoined', {'room': room}, to=room)

@socketio.on('moveMouse')
def handle_mouse_move(data):
    room = data.get('room')
    x = data.get('x')
    y = data.get('y')

    if room and x is not None and y is not None:
        print(f"Movimento do mouse: X={x}, Y={y} na sala {room}")
        emit('mouseMoved', {'x': x, 'y': y}, to=room)
    else:
        emit('error', {'message': 'Dados de movimento do mouse inválidos ou nulos!'})

@socketio.on('click')
def handle_click(data):
    room = data.get('room')
    
    if room:
        print(f"Clique recebido na sala: {room}")
        emit('mouseClicked', {}, to=room)
    else:
        emit('error', {'message': 'Sala não especificada!'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado:", request.sid) 