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
        #Makes game appear in full screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        #Create self.ship attribute by making a ship onject from Ship class
        self.ship = Ship(self)
        #Set background color RGB
        self.bg_color = self.settings.bg_color


    def run_game(self):
        #Start main loop for the game
        while True:
            self._check_events()
            self.ship._update()
            self._update_screen()

    #Helper method       
    def _check_events(self):
        #Watch for keyboard and mouse events
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                #Detects quit events and exits the game
                sys.exit()
            #If the player presses a key
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #If the player lefts up on a key
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    #Helper method
    def _check_keydown_events(self, event):
        #Respond to key presses
        #If the key is the right arrow
        #Can use elif because each event is connected to only one key
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        #If the key is the left arrow
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True     
        #If the key is Q
        elif event.key == pygame.K_q:
            sys.exit() 

    def _check_keyup_events(self, event):
        #Respond to key releases
        #If the key is the right arrow
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        #If the key is the left arrow
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    #Helper method
    def _update_screen(self):
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
