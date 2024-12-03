from typing import Union, Dict, Optional, List, Tuple
from basket import Basket
from laundry_timer import LTimer

class LSystem:
    """
    Class to represent a laundry_system.

    Attributes:
        light_basket: the light basket
        dark_basket: the dark basket
        timer: the laundry timer
        load_type: if color of the load of laundry being run, can be none
    """

    
    def __init__(self):
        self.light_basket = Basket("light")
        self.dark_basket = Basket("dark")
        self.timer = LTimer()
        self.load_type = None

    def get_light_basket(self):
        """
        Get the light basket.

        """
        return self.light_basket

    def get_dark_basket(self):
        """
        Get the dark basket.

        """
        return self.dark_basket

    def get_timer(self):
        """
        Get the laundry timer.

        """
        return self.timer


    


