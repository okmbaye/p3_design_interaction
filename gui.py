import os
import sys

import pygame # pylint: disable=wrong-import-position
import math
from typing import List, Tuple, Union, Dict, Optional

from basket import Basket
from laundry_timer import LTimer
from laundry_system import LSystem

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class LaundryGui:
    """
    Class to represent a laundry program.
    """
    window : int
    border : int
    surface : pygame.surface.Surface
    clock : pygame.time.Clock

    def __init__(self,  window: int = 700, border: int = 50):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
        """
        
        # Initialize gui settings
        self.window = window
        self.border = border  

        # Initialize Pygame and Text Capabilities 
        pygame.init()
        pygame.font.get_init()

        # Set window title
        pygame.display.set_caption("Laundry Race")

        # Initialize display
        self.surface = pygame.display.set_mode((window + border,
                                                window + border))   
        self.clock = pygame.time.Clock()
        self.event_loop()


    def draw_main_screen(self):
        """
        Draw the main program screen.
        """
        # Background
        self.surface.fill((120, 120, 120))
    
        
    def draw_tide_pod_rect(self) -> None:
        """
        When the user selects a load draw the recommended amount of tide pods to use.
        """
        pass


    def draw_laundry_stat(self) -> None:
        """
        When the user resets the laundry timer show their performance.
        """
        pass


    # Event loop to continuously draw board based on user interactions
    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
    
        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle the 5 sensor events here 
                # (select light or dark load, increment light or dark basket, reset load)

            else:
                self.draw_main_screen()
                pygame.display.update()
                self.clock.tick(5)
                

if __name__ == "__main__":
    LaundryGui()
    
