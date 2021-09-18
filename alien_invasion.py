#Import Modules
import sys
import pygame 
from settings import Setting
from ship import Ship

#Game Class
class AlienInvasion:
    #Initialize game and create resources
    def __init__(self):
        pygame.init()
        #Creat instance of setting and assign it to settings attribute
        self.settings = Setting()
        #Create display window by assigning a suface to self.screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        #Create self.ship attribute by making a ship onject from Ship class
        self.ship = Ship(self)
        #Set background color RGB
        self.bg_color = (230, 230, 230)

    def run_game(self):
        #Start main loop for the game
        while True:
            #Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Detects quit events and exits the game
                    sys.exit()
            

            #Redraw screen during each pass through loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            #Make the most recently drawn screen visible, erases previous screen
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game
    #Runs game only if the file is called directly
    ai = AlienInvasion()
    ai.run_game()
