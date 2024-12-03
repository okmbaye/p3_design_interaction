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

        # Curr_System init
        self.current_system = LSystem()

        # Initialize Pygame and Text Capabilities 
        pygame.init()
        pygame.font.get_init()

        # Set window title
        pygame.display.set_caption("Tide-Y Time")

        # Initialize display
        self.surface = pygame.display.set_mode((window + border,
                                                window - border))
        self.light_load = 0
        self.dark_load = 0   
        self.clock = pygame.time.Clock()
        self.event_loop()

    def draw_main_screen(self):
        """
        Draw the main program screen.
        """
        #Background
        self.surface.fill((237, 185, 204))

        # Draw the rectangle representing the compartment, folding board, and laundry baskets
        tide_rect = (45, 450, 135, 125)
        light_basket_rect = (198, 320, 150, 255)
        dark_basket_rect = (366, 320, 150, 255)
        folding_rect = (534, 450, 195, 125)

        pygame.draw.rect(self.surface, (219, 151, 176), tide_rect, 0, 10)
        pygame.draw.rect(self.surface, (219, 151, 176), light_basket_rect, 0, 10)
        pygame.draw.rect(self.surface, (219, 151, 176), dark_basket_rect, 0, 10)
        pygame.draw.rect(self.surface, (219, 151, 176), folding_rect, 0, 10)

        # Each basket has 5 levels of shading to visualize fullness
        lbask_level1 = (209, 332, 125, 61)
        lbask_level2 = (209, 379, 125, 61)
        lbask_level3 = (209, 420, 125, 61)
        lbask_level4 = (209, 471, 125, 61)
        lbask_level5 = (209, 522, 125, 41)
        lbask_levels = [lbask_level1, lbask_level2, lbask_level3, lbask_level4, lbask_level5][::-1]

        drbask_level1 = (377, 332, 125, 61)
        drbask_level2 = (377, 379, 125, 61)
        drbask_level3 = (377, 420, 125, 61)
        drbask_level4 = (377, 471, 125, 61)
        drbask_level5 = (377, 522, 125, 41)
        drbask_levels = [drbask_level1, drbask_level2, drbask_level3, drbask_level4, drbask_level5][::-1]

        # Get the level of laundry for each basket 
        lbask_height =  self.current_system.light_basket.get_count() // 5
        drbask_height = self.current_system.light_basket.get_count() // 5

        for level in range(5):
            # Draw how full the basket is
            if level < lbask_height:
                pygame.draw.rect(self.surface, (186, 110, 140), lbask_levels[level], 0, 5) 
            else:
                pygame.draw.rect(self.surface, (199, 135, 160), lbask_levels[level], 0, 5)

            # Draw how full the basket is
            if level < drbask_height:
                pygame.draw.rect(self.surface, (186, 110, 140), drbask_levels[level], 0, 5) 
            else:
                pygame.draw.rect(self.surface, (199, 135, 160), drbask_levels[level], 0, 5)

        # Draw bar for when you have to do your laundry based on combined compacity
        status_bar = (45, 200, 675, 45)
        inner_bar = (50, 205, 665, 35)
        capacity_marker_1 = (216, 205, 5, 35)
        capacity_marker_2 = (382, 205, 5, 35)
        capacity_marker_3 = (548, 205, 5, 35)

        pygame.draw.rect(self.surface, (219, 151, 176), status_bar, 0, 12)
        pygame.draw.rect(self.surface, (199, 135, 160), inner_bar, 0, 8)

        # Fill in levels based on total capacity
        capacity_level = (self.current_system.light_basket.get_count() + self.current_system.dark_basket.get_count() + 2) // 13
        cap_level_1 = (50, 205, 166, 35)
        cap_level_2 = (221, 205, 166, 35)
        cap_level_3 = (387, 205, 166, 35)
        cap_level_4 = (553, 205, 160, 35)
        cap_levels =[cap_level_1, cap_level_2, cap_level_3, cap_level_4]

        for level in range(4):
            if level < capacity_level:
                pygame.draw.rect(self.surface, (144, 153, 89), cap_levels[level], 0, 8)
            else:
                pygame.draw.rect(self.surface, (199, 135, 160), cap_levels[level], 0, 8)

        # Draw markers over top levels
        pygame.draw.rect(self.surface, (219, 151, 176), capacity_marker_1, 0, 0)
        pygame.draw.rect(self.surface, (219, 151, 176), capacity_marker_2, 0, 0)
        pygame.draw.rect(self.surface, (219, 151, 176), capacity_marker_3, 0, 0)

        # Draw accents for tide pod compartment and folding board
        accent1_tide_rect = (59, 475, 108, 77)
        pygame.draw.rect(self.surface, (199, 135, 160), accent1_tide_rect, 0, 4)

        accent1_activity_stat = (554, 475, 155, 75)
        if(self.current_system.timer.is_running):
            pygame.draw.rect(self.surface, (178, 186, 132), accent1_activity_stat, 0, 4)
        else:
            pygame.draw.rect(self.surface, (199, 135, 160), accent1_activity_stat, 0, 4)

        ###### Handling Text Objects ########

        # Title Text
        title_text = pygame.font.SysFont("Impact", 85)
        title_render = title_text.render("Tide-Y Time", True, (163, 100, 124))
        title_object = title_render.get_rect()
        title_object.center = 380 , 100
        self.surface.blit(title_render, title_object)

        # Basket Capacity Text
        lbasket_text = pygame.font.SysFont("Sans Serif", 20)
        lbasket_render = lbasket_text.render(f"LIGHT TOTAL: {self.current_system.light_basket.get_count()}/25", True, (163, 100, 124))
        lbasket_object = lbasket_render.get_rect()
        lbasket_object.center = 273, 595
        self.surface.blit(lbasket_render, lbasket_object)

        drbasket_text = pygame.font.SysFont("Sans Serif", 20)
        drbasket_render = drbasket_text.render(f"DARK TOTAL: {self.current_system.dark_basket.get_count()}/25", True, (163, 100, 124))
        drbasket_object = drbasket_render.get_rect()
        drbasket_object.center = 441, 595
        self.surface.blit(drbasket_render, drbasket_object)

        # Activity Text 
        active_text = pygame.font.SysFont("Impact", 25)

        if(self.current_system.timer.is_running):
            active_render = active_text.render("TIME RUNNING", True, (163, 100, 124))
        else:
            active_render = active_text.render("TIME OFF", True, (163, 100, 124))
        active_object = active_render.get_rect()
        active_object.center = 631, 512
        self.surface.blit(active_render, active_object)

        # Press Prompt Text
        press_text = pygame.font.SysFont("Sans Serif", 20)
        press_render = press_text.render("GET TIDE POD REC!", True, (163, 100, 124))
        press_object = press_render.get_rect()
        press_object.center = 112, 432
        self.surface.blit(press_render, press_object)

        # Capacity Text
        capacity_text = pygame.font.SysFont("Sans Serif", 20)
        capacity_render = press_text.render(f"TIDE-Y CHECK - %{(self.current_system.light_basket.get_count() + self.current_system.dark_basket.get_count()) // 50} Till You're at Capacity", True, (163, 100, 124))
        capacity_object = press_render.get_rect()
        capacity_object.center = 115, 185
        self.surface.blit(capacity_render, capacity_object)


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
                    lsys.get_timer().start_timer(lsys.get_light_basket())

            if (keys[DARK_BASKET_KEY] and dark_button_cooldown <= 0):
                lsys.get_dark_basket().increase_count()
                dark_button_cooldown = DARK_COOLDOWN

                if lsys.get_dark_basket().at_capacity() and not lsys.get_timer().is_running:
                    lsys.get_timer().start_timer(lsys.get_dark_basket())
            
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
    
