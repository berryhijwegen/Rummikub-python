import numpy as np

def all_equal(np_arr, column=0):
    """ Checks if all elements are equal in the defined column

    Args:
        np_arr (ndarray): NumPy array to check equality for.
        column (int): Column in defined np_arr to check equality for.

    Returns:
        bool: True if all elements in column are equal, else False.

    """
    return np.all(np_arr[:,column] == np_arr[0][column])

def all_unique(np_arr, column=0):
    """ Checks if all elements are unique in the defined column

    Args:
        np_arr (ndarray): NumPy array to check if all elements are unique.
        column (int): Column in defined np_arr to check if all elements are unique.

    Returns:
        bool: True if all elements in column are unique, else False.

    """
    return np.unique(np_arr[:,column]).size == np_arr[:,column].size

def is_consecutive(np_arr, column=0):
    """ Checks if all elements are consecutivity in the defined column

    Args:
        np_arr (ndarray): NumPy array to check consecutivity for.
        column (int): Column in defined np_arr to check consecutivity for.

    Returns:
        bool: True if all elements in column are consecutive, else False.

    """
    sorted_arr = np.sort(np_arr[:,column])
    return np.all(np.gradient(sorted_arr)==1)

def remove_from_arr(np_arr, elements):
    """ Remove given elements from given NumPy array.
    
    Args:
        np_arr (ndarray): NumPy array to check remove given elements from.
        elements (ndarray/int): Elements to remove from given NumPy array.

    Returns:
        bool: New NumPy array with given elements removed. 
        
    Note: 
        Only removes the first found element for each given element.

    """
    for element_to_remove in elements:
        for i in range(len(np_arr)):
            element = np_arr[i]
            if(np.array_equal(element, element_to_remove)):
                np_arr = np.delete(np_arr, i, axis=0)
                break
    
    return np_arr

def calculate_score(np_arr):
    """ Calculates the Rummikub score for given NumPy array.

    Args:
        np_arr (ndarray): 2D-NumPy array to check remove given elements from.
        elements (ndarray/int): Elements to remove from given NumPy array.

    Returns:
        int: Sum of given array.
    
    """
    return np.sum(np_arr[:,0])