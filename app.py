import sys, time
sys.path.append("./rummikub")
import threading

from flask import Flask, render_template, request, copy_current_request_context
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit, send

from rummikub.game import Game
from rummikub.settings import COLOR_MAPPING
from gevent import monkey
monkey.patch_all()

# initialize Flask
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = {}  # dict to track active rooms


def broadcast_users(room):
    emit('new_player', {
        'players': [player.username for player in rooms[room].players]
    },
        room=room
    )

def emit_enter_room(username, room):
    emit('join_room', {
                'room': room.game_id,
                'own_username': username,
                'players': [player.username for player in room.players],
                'max_players': room.max_players
        })

def is_full(game):
    return len(game.players) >= game.max_players


def join(username, room):
    if room in rooms:
        current_room = rooms[room]
        if (len(current_room.players) < current_room.max_players):

            current_room.add_player(request.sid, username)
            join_room(room)
            emit_enter_room(username, current_room)
            broadcast_users(room)

            # REMOVE AFTER TESTING FRONT END
            current_room.start()
            for player in current_room.players:
                emit('start', {
                    'message': 'game_started!',
                    'stones': [[stone[0], COLOR_MAPPING[stone[1]]] for stone in player.rack.tolist()],
                    'pot_size': current_room.table.pot.shape[0]
                }, room=player._id)

            if (len(current_room.players) == current_room.max_players):  
                @copy_current_request_context
                def countdown(game, sec):
                    countdown = sec
                    while is_full(game) and countdown > 0:
                        emit('countdown', {'seconds_left': countdown}, room=game.game_id)
                        socketio.sleep(1)
                        print(countdown)
                        countdown -= 1
                            
                    if not is_full(game):
                        emit('cancel_start', {'message': 'Game start is cancelled!'}, room=game.game_id)
                    if countdown == 0:
                        current_room.start()
                        for player in current_room.players:
                            emit('start', {
                                'message': 'game_started!',
                                'stones': [[stone[0], COLOR_MAPPING[stone[1]]] for stone in player.rack.tolist()],
                                'pot_size': current_room.table.pot.shape[0]
                            }, room=player._id)

                socketio.start_background_task(target=countdown, game=current_room, sec=10)

        else:
            emit('join_error', {
                 'error': f"Room {room} is full! ({len(current_room.players)}/{current_room.max_players})"})
    else:
        emit('join_error', {'error': f"Room {room} is not a room!"})


@app.route('/')
def index():
    """Serve the index HTML"""
    return "Hello World"


@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    if type(data['max_players']) == int or data['max_players'].isnumeric():
        max_players = int(data['max_players'])

        if max_players > 1 and max_players < 5:
            gm = Game(
                max_players=max_players
            )
            room = gm.game_id
            rooms[room] = gm
            username = data['username']
            join(username, room)
        else:
            emit('create_error', {
                 'error': f"Max players should be between two and four!"})
    else:
        emit('create_error', {'error': f"Max players should be an integer!"})


@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    username = data['username']
    room = int(data['room'])
    join(username, room)


@socketio.on('disconnect')
def on_disconnection():
    player = None
    player_room = 0
    for room in rooms:
        found_player = rooms[room].find_by_id(request.sid)
        if found_player:
            player = found_player
            player_room = room

    if player:
        print(f'player {player.username} removed!')
        rooms[player_room].remove_player(player)
        broadcast_users(player_room)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
