import numpy as np
import helpers
class Table:
    def __init__(self):
        self.pot = np.empty((0,2), dtype=np.int64)
        self.stones = np.empty((0,2), dtype=np.int64)

    def fill_pot(self, stones):
        self.pot = np.append(self.pot, stones, axis=0)
    
    def pick_stones(self, number_of_stones):
        random_stones = self.pot[np.random.choice(
            self.pot.shape[0], number_of_stones, replace=False)]

        for random_stone in random_stones:
            self.pot = helpers.remove_from_arr(self.pot, random_stone)
            
        return random_stones

    def pick_stone(self):
        return self.pick_stones(1)[0]
    
    def put_on_table(self, stones):
        if self.row_is_valid(stones):
            self.add_to_table(stones)
            return True
        return False

    def add_to_table(self, stones):
        self.stones = np.append(self.stones, stones, axis=0)

    def row_is_valid(self, stones):
        return stones.shape[0] >= 3 and helpers.calculate_score(stones) >= 30 and (
            (helpers.all_equal(stones, index=0) and helpers.all_unique(stones, index=1)) or        # index 0 all the same, index 1 all diferent
            (helpers.is_consecutive(stones, index=0) and helpers.all_equal(stones, index=1))      # index 0 consecutive, index 1 all the same
        )