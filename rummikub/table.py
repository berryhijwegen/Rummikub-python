import numpy as np
import helpers


class Table:
    def __init__(self):
        #: ndarray: 2D-array of stones in the pot.
        self.pot = np.empty((0, 2), dtype=np.int64)

        #: ndarray: 2D-array of stones on the table.
        self.stones = np.empty((0, 2), dtype=np.int64)

    def add_to_pot(self, stones):
        """ Add stones to the pot

        Args:
            stones (ndarray): 2D-array of stones to add to pot.

        """
        self.pot = np.append(self.pot, stones, axis=0)

    def pick_stones(self, number_of_stones):
        """ Pick random stones from the pot and remove from pot.

        Args:
            number_of_stones (:obj:`int`): Number of stones to get from the pot.

        Returns:
            ndarray: 2D-array of stones retrieved from the pot
        
        Note:
            Picked stones are directly removed from the pot.

        """
        random_stones = self.pot[np.random.choice(
            self.pot.shape[0], number_of_stones, replace=False)]

        self.pot = helpers.remove_from_arr(self.pot, random_stones)

        return random_stones

    def pick_stone(self):
        """ Pick one random stone from the pot and remove from pot.

        Returns:
            ndarray: 2D-array of the stone picked from the pot.
        
        Note:
            Picked stone is directly removed from the pot.

        """

        return self.pick_stones(1)[0]

    def put_on_table(self, stones):
        """ Try to put a row of stones on the table.

        Args:
            stones (ndarray): 2D-array of stones to put on the table.
        
        Returns:
            :obj:`bool`: True if row was valid and was put on table, else False.

        """
        if self.row_is_valid(stones):
            self.add_to_table(stones)
            return True
        return False

    def add_to_table(self, stones):
        self.stones = np.append(self.stones, stones, axis=0)

    def row_is_valid(self, stones, first_set=False):
        """ Checks if a given row of stones is valid according to defined rules:
        - (if first_set=True) first set should have points >=30, and
        - At least 3 consecutive numbers of the same color, or
        - At least 3 equal numbers of all different colors.

        Args:
            stones (ndarray): 2D-array to check if its valid according to described rules.
            first_set (:obj:`bool`): True if the player didn't do a valid set yet, else False.

        Returns:
            :obj:`bool`: True if row is valid, else false.

        """
        rules_valid = stones.shape[0] >= 3 and (
            # column 0 all the same, column 1 all different
            (helpers.all_equal(stones, column=0) and helpers.all_unique(stones, column=1)) or

            # column 0 consecutive, column 1 all the same
            (helpers.is_consecutive(stones, column=0) and helpers.all_equal(
                stones, column=1))
        )

        return rules_valid and (not first_set or helpers.calculate_score(stones) >= 30)
