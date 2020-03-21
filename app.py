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
        rooms[room].add_player(username)
        join_room(room)
        emit('join_room', {'room': room})
    else:
        emit('error', {'error': f"Room {room} is not in rooms: " + str([_id for _id in rooms])})

@app.route('/')
def index():
    """Serve the index HTML"""
    return "Hello World"

@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    gm = Game(
        number_of_players = data['number_of_players']
    )
    room = gm.game_id
    rooms[room] = gm
    username = data['username']
    join(username, room)

@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    username = data['username']
    room = data['room']
    join(username, room)
       

if __name__ == '__main__':
    socketio.run(app, debug=True)