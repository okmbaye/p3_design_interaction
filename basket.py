from typing import Union, Dict, Optional, List, Tuple

class Basket:
    """
    Class to represent a laundry_basket.

    Attributes:
        capacity[int]: How many items can fit in a laundry basket.
        count[int]: How many items are in the basket.
        bsk_type[str]: Is it a light or dark basket?
    """

    
    def __init__(self, bsk_type):
        self.capacity = 25
        self.count = 0
        self.bsk_type = bsk_type

    def increase_count(self):
        """
        Increase the count of a basket.

        Returns: None.
        """
        self.count += 1

    def is_full(self):
        """
        Check if the basket is full.

        Returns [bool]: True if full, false otherwise.
        """
        return self.count == self.capacity

    def get_count(self):
        """
        Get the basket count.

        Returns [int]: how many clothes are in the basket
        """
        return self.count

    def get_load_size(self):
        """
        Get the load size of the of what is currently in the basket.
        
        Returns [str]: the type of load "small", "med", "large".
        """
        if self.count < 12:
            return "small"
        if self.count < 20:
            return "med"
        return "large"

    def empty_basket(self):
        """
        empties the basket

        returns none
        """
        self.count = 0
        return
    
    def at_capacity(self):
        """
        Returns true if the basket is at capacity and false if not

        returns bool
        """
        return self.count >= self.capacity

    
