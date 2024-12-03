import datetime
from typing import Union, Dict, Optional, List, Tuple
from basket import Basket

class LTimer:
    """
    Class to represent a laundry_timer.

    Attributes:
        previous_time: time it took to finish the most recent load of laundry
        start_time: when the current load 
        current_basket: the laundry basket that is being unloaded, can be None.
        is_running[bool]: is the laundry basket full?
    """

    
    def __init__(self):
        self.previous_time = None
        self.start_time = None
        self.current_basket = None
        self.is_running = False

    def get_time_difference(self):
        """
        Get the difference between the start time and the current time.

        Returns: None.
        """
        current_time = datetime.datetime.now()
        return current_time - self.start_time

    def start_timer(self):
        """
        Start the laundry timer.

        """
        current_time = datetime.datetime.now()
        self.start_time = current_time
        self.is_running = True

    def end_timer(self):
        """
        Stop the laundry timer.

        """
        self.is_running = False
        self.previous_time = self.get_time_difference
         
        

    def get_statistic(self):
        """
        Get a string representation of the laundry performance.
        """
        return f"The time it took to run the last load was {self.previous_time}"

    

