import numpy as np

import helpers, settings

class Player:
    def __init__(self, _id, table):
        self._id = _id
        self.rack = np.empty((0,2), dtype=np.int64)
        self.table = table
        self.first_set_done = False
    
    def addStones(self, stones):
        self.rack = np.append(self.rack, stones, axis=0)

    def request_set(self, stones):
        if (self.table.put_on_table(stones)):
            self.remove_from_rack(stones)
            print("set is done")
            return True
        print("set is invalid")
        return False
    def remove_from_rack(self, stones):
        self.rack = helpers.remove_from_arr(self.rack, stones)

    def chose_stones(self):
        next_set = np.empty((0,2), dtype=np.int64)
        for i in range(self.rack.shape[0]):
            print(f"{f'{i}:':>3} {f'Number: {self.rack[i][0]} ':<12} Color: {settings.COLOR_MAPPING[self.rack[i][1]]}")

        input_ended = False
        while not input_ended:
            user_input = input("Fill in a index to add to your set. Click on enter to end: ")
            if not user_input:
                input_ended = True
            else:
                index = int(user_input)
                next_set = np.append(next_set, [self.rack[index]], axis=0)

        self.request_set(next_set)