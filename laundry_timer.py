import datetime
import time
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

    def start_timer(self, basket):
        """
        Start the laundry timer.

        """
        current_time = datetime.datetime.now()
        self.start_time = current_time
        self.is_running = True
        self.current_basket = basket

    def end_timer(self):
        """
        Stop the laundry timer.

        """
        self.is_running = False
        self.previous_time = self.get_time_difference()
        self.current_basket = None

    def get_statistic(self):
        """
        Get a string representation of the laundry performance.
        """
        if self.previous_time is None:
            return "This is your first time doing laundry!"

        percent_delta = 1 - (self.get_time_difference() / self.previous_time)
        if percent_delta > 0:
            return f"You were {int(percent_delta * 100 // 1)}% faster!"
        
        elif percent_delta < 0:
            return f"You were{int(percent_delta * -100 // 1)}% slower!"
        
        else:
            return f"You were as quick as last time!"
        
    def str_timer (self, time):
        """
        gets the string version of the time

        Inputs:
            time: (datetime.timedelta) time

        returns str of time
        """
        if time is None:
            return("No time")
        
        days = time.days
        hours, remainder = divmod(time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{days} days {hours} hours {minutes} minutes"
