"""
Points:
- Stones can be attached to existing rows, stones can be moved if all rows stay valid

Valid rows:
- Jokers can be used everywhere; they count for the same number as they represent
- If no valid row can be made; the user picks up a stone from the pot.

Play ends if:
- One of the players placed all his stones on the table
- Pot is empty; if so, the player with the least points on its rack wins.
"""

import numpy as np

from player import Player
from table import Table
import settings


class Rummikub:
    def __init__(self):
        """ Rummikub Game initializer. """

        #: :obj:`Table`: Table where the game takes place.
        self.table = Table()

        #: :obj:`list` of :obj:`Player`: Players that are in the game.
        self.players = [Player(_id, self.table)
                        for _id in range(1, settings.NUMBER_OF_PLAYERS+1)]

    def start(self):
        """ Starts the game by filling the pot and giving every player a defined amount of stones. """
        for player in self.players:
            player.addStones(self.table.pick_stones(
                settings.STONES_PER_PLAYER))

    def prepare_table(self):
        """ Fills the pot attached to the :obj:`Table` with all cards. (106 stones; 2x 1-13, red, yellow, blue, black + two jokers) """
        NUMBERS = np.arange(1, settings.HIGHEST_NUMBER + 1)
        COLORS = np.arange(settings.NUMBER_OF_COLORS)

        combinations = np.array(np.meshgrid(
            NUMBERS, COLORS)).T.reshape(-1, 2)

        all_stones = np.vstack((combinations, combinations))
        jokers = [[99, 99], [99, 99]]

        self.table.add_to_pot(np.append(all_stones, jokers, axis=0))

    def __str__(self):
        """ String which represents :obj:``Rummikub` object when converted to :obj:`str`. """
        userStones = '\n    '.join(
            [f"Player {player._id}: {player.stones.shape[0]} stones " for player in self.players])
        return f"Pot: {self.table.pot.shape[0]} stones" \
            "Players:" + userStones

    def __repr__(self):
        """ String which represents :obj:``Rummikub` object when printed out on CLI. """
        return self.__str__()
