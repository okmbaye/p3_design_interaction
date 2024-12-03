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
            pass

        def is_full(self):
            """
            Check if the basket is full.

            Returns [bool]: True if full, false otherwise.
            """
            pass

        def get_count(self):
            """
            Get the basket count.
    
            Returns [int]: how many clothes are in the basket
            """
            pass

        def get_load_size(self):
            """
            Get the load size of the of what is currently in the basket.
            
            Returns [str]: the type of load "small", "med", "large".
            """
            pass

    
