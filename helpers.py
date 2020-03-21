import numpy as np

def all_equal(np_arr, index=0):
    return np.all(np_arr[:,index] == np_arr[0][index])

def all_unique(np_arr, index=0):
    return np.unique(np_arr[:,index]).size == np_arr[:,index].size

def is_consecutive(np_arr, index=0):
    sorted_arr = np.sort(np_arr[:,index])
    return np.all(np.gradient(sorted_arr)==1)

def remove_from_arr(np_arr, stones_to_remove):
    for stone_to_remove in stones_to_remove:
        for i in range(len(np_arr)):
            stone = np_arr[i]
            if(np.array_equal(stone, stone_to_remove)):
                np_arr = np.delete(np_arr, i, axis=0)
                break
    
    return np_arr

def calculate_score(np_arr):
    return np.sum(np_arr[:,0])