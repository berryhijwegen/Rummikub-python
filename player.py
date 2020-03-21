import numpy as np

import helpers
import settings


class Player:
    def __init__(self, _id, table):
        """ Player initializer.

        Args:
            _id (:obj:`int`): Identifier of player.
            table (:obj:`Table`): Table the player is playing on.  

        """
        #: :obj:`int`: Identifier of player.
        self._id = _id

        #: ndarray of ndarray: 2D-array with stones currently on player's rack, where first element represents the number of the stone, the second elements represent the color of the stone.
        self.rack = np.empty((0, 2), dtype=np.int64)

        #:  :obj:`Table`: Reference to the table the player is playing on.
        self.table = table

        #: :obj:`int`: True if the first set of the player has been done, else False. Required to check score >= 30 rule in first set.
        self.first_set_done = False

    def addStones(self, stones):
        """ Add stones to rack.

        Args:
            stones (ndarray): 2D-array of stones to add to rack.

        """
        self.rack = np.append(self.rack, stones, axis=0)

    def try_set(self, stones):
        """ Try a set with the given stones, send it to the table.

        Args:
            stones (ndarray): 2D-array of stones to add to the table.

        Returns:
            :obj:`bool`: True if set was valid, else False. 

        """
        if (self.table.put_on_table(stones)):
            self.remove_from_rack(stones)
            print("set is done")
            return True
        print("set is invalid")
        return False

    def remove_from_rack(self, stones):
        """ Remove stones from rack.

        args:
            stones (ndarray): 2D-array of stones to remove from rack.

        """
        self.rack = helpers.remove_from_arr(self.rack, stones)

    def chose_stones(self):
        """ Do a set from the CLI. """
        next_set = np.empty((0, 2), dtype=np.int64)
        for i in range(self.rack.shape[0]):
            print(
                f"{f'{i}:':>3} {f'Number: {self.rack[i][0]} ':<12} Color: {settings.COLOR_MAPPING[self.rack[i][1]]}")

        input_ended = False
        while not input_ended:
            user_input = input(
                "Fill in a index to add to your set. Click on enter to end: ")
            if not user_input:
                input_ended = True
            else:
                index = int(user_input)
                next_set = np.append(next_set, [self.rack[index]], axis=0)

        self.try_set(next_set)
