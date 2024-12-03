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
        self.light_load = 0
        self.dark_load = 0   
        self.clock = pygame.time.Clock()
        self.event_loop()
        


    def draw_main_screen(self):
        """
        Draw the main program screen.
        """
        #Background
        self.surface.fill((120, 120, 120))
    
        
    def draw_tide_pod_rect(self, curr_system: LSystem) -> None:
        """
        When the user selects a load draw the recommended amount of tide pods to use.
        """
        light_count = curr_system.get_light_basket().get_count()
        dark_count = curr_system.get_dark_basket().get_count()

        total_items = light_count + dark_count
        
        recommended_pods = max(1, math.ceil(total_items / 10))
        font = pygame.font.Font(None, 36)

        recommendation_text = font.render(f"Recommended Tide Pods: {recommended_pods}", True, (255, 255, 255))
        
        text_width, text_height = recommendation_text.get_size()
        rect_x = self.border
        rect_y = self.window - self.border - text_height - 10
        rect_width = text_width + 20
        rect_height = text_height + 10

        pygame.draw.rect(self.surface, (50, 50, 50), (rect_x, rect_y, rect_width, rect_height))
        self.surface.blit(recommendation_text, (rect_x + 10, rect_y + 5))


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
    
