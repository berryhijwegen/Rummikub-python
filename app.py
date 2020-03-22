import sys
sys.path.append("./rummikub")

from flask import Flask, render_template
from flask_cors import CORS

from flask_socketio import SocketIO, join_room, emit, send
from rummikub.game import Game
# initialize Flask
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = {} # dict to track active rooms

def join(username, room):
    if room in rooms:
        current_room = rooms[room]
        if (len(current_room.players) < current_room.max_players):
            current_room.add_player(username)
            join_room(room)
            
            emit('join_room', {'room': current_room.game_id, 'players': [player.username for player in current_room.players], 'max_players': current_room.max_players})
        else:
            emit('join_error', {'error': f"Room {room} is full! ({len(current_room.players)}/{current_room.max_players})"})
    else:
        emit('join_error', {'error': f"Room {room} is not a room!"})

@app.route('/')
def index():
    """Serve the index HTML"""
    return "Hello World"

@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    gm = Game(
        max_players = int(data['max_players'])
    )
    room = gm.game_id
    rooms[room] = gm
    username = data['username']
    join(username, room)

@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    username = data['username']
    room = int(data['room'])
    join(username, room)
    emit('new_player', {'players': [player.username for player in rooms[room].players]}, room=room)
       

if __name__ == '__main__':
    socketio.run(app, debug=True)