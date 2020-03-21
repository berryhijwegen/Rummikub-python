from rummikub import Rummikub
import numpy as np

if __name__ == "__main__":
    rummikub = Rummikub()
    rummikub.start()

    player_0 = rummikub.players[0]
    player_0.chose_stones()