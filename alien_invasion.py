#Import Modules
import sys
import pygame 
from settings import Setting
from ship import Ship
from bullet import Bullet
from alien import Alien

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
        #Create self.ship attribute by making a ship object from Ship class
        self.ship = Ship(self)
        #Create the bullets attribute by making bullet object that behaves like a list
        self.bullets = pygame.sprite.Group()
        #Create aliens and alien fleet
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #Set background color RGB
        self.bg_color = self.settings.bg_color


    def run_game(self):
        #Start main loop for the game
        while True:
            self._check_events()
            self.ship._update()
            self._update_bullets()
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
        #If the key is the spacebar
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        #Respond to key releases
        #If the key is the right arrow
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        #If the key is the left arrow
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    #Helper method
    def _fire_bullet(self):
        #Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    #Helper method
    def _update_bullets(self):
        #Update position of bullets and get rid of old bullets
        self.bullets.update() #Update for each sprite in the group
        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    #Helper method
    def _update_screen(self):
        #Redraw screen during each pass through loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        #Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #Draw aliens
        self.aliens.draw(self.screen)
        #Make the most recently drawn screen visible, erases previous screen
        pygame.display.flip()
    
    #Helper method
    def _create_fleet(self):
        #Create the fleet of aliens
        #Make an alien
        alien = Alien(self)
        self.aliens.add(alien)


if __name__ == '__main__':
    #Make a game instance, and run the game
    #Runs game only if the file is called directly
    ai = AlienInvasion()
    ai.run_game()
