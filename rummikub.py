import settings
"""
- 106 stones; 2x 1-13, red, yellow, blue, black + two jokers
- 2, 3 or 4 players
- every player starts with 14 stones

Points:
- first set should be have points >=30.
- Every next set doesn't have a minimum score. Stones can be attached to existing rows, stones can be moved if all rows stay valid
- Points are measured by the number on the stone

Valid rows:
- At least 3 Consecutive numbers of the same color.
- Jokers can be used everywhere; they count for the same number as they represent

- If no valid row can be made; the user picks up a stone from the pot.

Play ends if:
- One of the players placed al his stones on the table
- Pot is empty; if so, the player with the least points on its rack wins.
"""

import numpy as np
from player import Player
from table import Table

class Rummikub:
    def __init__(self):
        self.table = Table()

        self.NUMBERS = np.arange(1, settings.HIGHEST_NUMBER + 1)

        self.STONES_PER_PLAYER = settings.STONES_PER_PLAYER

        """ 0 = red, 1 = yellow, 2 = blue, 3 = black """
        self.COLORS = np.arange(settings.NUMBER_OF_COLORS)

        self.players = [Player(_id, self.table) for _id in range(1, settings.NUMBER_OF_PLAYERS+1)]

        combinations = np.array(np.meshgrid(
            self.NUMBERS, self.COLORS)).T.reshape(-1, 2)
        all_stones = np.vstack((combinations, combinations))
        jokers = [[99, 99], [99, 99]]

        self.table.fill_pot(np.append(all_stones, jokers, axis=0))

    def start(self):
        for player in self.players:
            player.addStones(self.table.pick_stones(settings.STONES_PER_PLAYER))
   
    def __str__(self):
        userStones = '\n    '.join([f"Player {player._id}: {player.stones.shape[0]} stones " for player in self.players])
        return f"""Pot: {self.table.pot.shape[0]} stones
Players:
    { userStones }
"""
    
    def __repr__(self):
        return self.__str__()
        