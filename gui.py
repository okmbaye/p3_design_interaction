import os
import sys

import pygame # pylint: disable=wrong-import-position
import math
from typing import List, Tuple, Union, Dict, Optional

from basket import Basket
from laundry_timer import LTimer
from laundry_system import LSystem

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

LIGHT_BASKET_KEY = pygame.K_LEFT
LIGHT_RESET_KEY =  pygame.K_DOWN
DARK_BASKET_KEY = pygame.K_RIGHT
DARK_RESET_KEY = pygame.K_UP
TIDEPOD_KEY = pygame.K_SPACE

LIGHT_COOLDOWN = 10
DARK_COOLDOWN = 10

WAIT_TIDEPOD_TIME = 1000
WAIT_STAT_TIME = 1000


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


    def draw_laundry_stat(self, ltimer: LTimer) -> None:
        """
        When the user resets the laundry timer show their performance.
        """
        font = pygame.font.Font(None, 60)
        text_color = (70, 130, 180)
        rect_color = (70, 70, 70)

        #create the text and center it on screen
        laundry_stat_txt = font.render(ltimer.get_statistic(), True, text_color)
        txt_rect = laundry_stat_txt.get_rect()
        txt_rect.center = (self.surface.get_width() // 2, self.surface.get_height() // 2)

        text_width, text_height = laundry_stat_txt.get_size()

        #create the rectangle that sits behind the text
        rect_width = text_width + self.border
        rect_height = text_height + self.border
        rect = pygame.Rect(0, 0, rect_width, rect_height)
        rect.center = (self.surface.get_width() // 2, self.surface.get_height() // 2)

        #draw the rectangle and text to screen
        pygame.draw.rect(self.surface, rect_color ,(rect))
        self.surface.blit(laundry_stat_txt, txt_rect)

    # Event loop to continuously draw board based on user interactions
    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
        lsys = LSystem()
        dark_button_cooldown = 0
        light_button_cooldown = 0
    
        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Handle the 5 sensor events here 
            # (select light or dark load, increment light or dark basket, reset load)
            light_button_cooldown -= 1
            dark_button_cooldown -= 1

            keys = pygame.key.get_pressed()
            if (keys[LIGHT_BASKET_KEY] and light_button_cooldown <= 0):
                lsys.get_light_basket().increase_count()
                light_button_cooldown = LIGHT_COOLDOWN

                if lsys.get_light_basket().at_capacity() and not lsys.get_timer().is_running:
                    lsys.get_timer().start_timer()

            if (keys[DARK_BASKET_KEY] and dark_button_cooldown <= 0):
                lsys.get_dark_basket().increase_count()
                dark_button_cooldown = DARK_COOLDOWN

                if lsys.get_dark_basket().at_capacity() and not lsys.get_timer().is_running:
                    lsys.get_timer().start_timer()
            
            if (keys[TIDEPOD_KEY]):
                self.draw_tide_pod_rect()
                pygame.display.update()
                pygame.time.wait(WAIT_TIDEPOD_TIME)
            
            if (keys[DARK_RESET_KEY]):
                lsys.get_dark_basket().empty_basket()

                if (lsys.get_timer().is_running) and not lsys.get_light_basket().at_capacity():

                    self.draw_laundry_stat()
                    lsys.get_timer().end_timer()

                    pygame.display.update()
                    pygame.time.wait(WAIT_STAT_TIME)

            if (keys[LIGHT_RESET_KEY]):
                lsys.get_light_basket().empty_basket()

                if (lsys.get_timer().is_running) and not lsys.get_dark_basket().at_capacity():

                    self.draw_laundry_stat()
                    lsys.get_timer().end_timer()

                    pygame.display.update()
                    pygame.time.wait(WAIT_STAT_TIME)
            
            self.draw_main_screen()
            pygame.display.update()
            self.clock.tick(5)
                

if __name__ == "__main__":
    LaundryGui()
    
