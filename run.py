from websocket import create_app, socketio

app = create_app()

if __name__ == "__main__":
    print('Server On')
    socketio.run(app, host="0.0.0.0", port=5000)