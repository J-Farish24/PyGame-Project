#Import Modules
import sys
from time import sleep

import pygame 

from settings import Setting
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

#Game Class
class AlienInvasion:
    #Initialize game and create resources
    def __init__(self):
        #Initializes background settings Pygame needs to work properly
        pygame.init()

        #Creat instance of setting and assign it to settings attribute
        self.settings = Setting()

        #Create display window by assigning a suface to self.screen
        #Creates an object called a surface where a game element can be displayed
        #Not full screen
        '''self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))'''
        #Fullscreen mode
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #Updates settings after the screen is created
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #Set screen name
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistics
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #Create self.ship attribute by making a ship object from Ship class
        self.ship = Ship(self)

        #Create the bullets attribute by making bullet object that behaves like a list
        self.bullets = pygame.sprite.Group()

        #Create aliens and alien fleet
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Make the play button
        self.play_button = Button(self, "Play")

        #Set background color RGB
        self.bg_color = self.settings.bg_color


    def run_game(self):
        #Start main loop for the game
        while True:
            self._check_events()

            #If player has ships left
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets() #Calls update for each sprite in a group
                self._update_aliens()
            
            self._update_screen()


    #Helper method       
    def _check_events(self):
        #Watch for keyboard and mouse events
        #Mange events separately from other aspects of the game
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                #Detects quit events and exits the game
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            #If the player presses a key
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            #If the player lefts up on a key
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    #Helper method
    def _check_play_button(self, mouse_pos):
        #Start a new game when the Player clicks Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            #Get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #Hide the mouse cursor
            pygame.mouse.set_visible(False)

    #Helper method
    def _check_keydown_events(self, event):
        #Respond to key presses
        #If the key is the right arrow
        #Can use elif because each event is connected to only one key
        #If the key is the right arrow
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
        #Creates if there are less bullets than the maximum number of bullets
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    #Helper method
    def _update_bullets(self):
        #Update position of bullets and get rid of old bullets
        self.bullets.update() #Update for each sprite in the group

        #Get rid of bullets that have disappeared off the top of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        #Check for any bullets that have hit aliens and gets rid of the bullet and alien
        self._check_bullet_alien_collisons()

    #Helper Method
    def _check_bullet_alien_collisons(self):
        collisions = pygame.sprite.groupcollide(
        self.bullets, self.aliens, True, True)
        #Increase players score 
        if collisions:
            for aliens in collisions.values():
                #Collisions is a dictionary with lists as the values
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        #If there are no more aliens
        if not self.aliens:
            #Destory existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #Increase level
            self.stats.level +=1
            self.sb.prep_level()

    #Helper method
    def _update_aliens(self):
        #Update positions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()
        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Look for any aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    #Helper method
    def _update_screen(self):
        #Redraw screen during each pass through loop
        self.screen.fill(self.settings.bg_color)

        #Draw ship at current location
        self.ship.blitme()

        #Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #Draw aliens
        self.aliens.draw(self.screen)

        #Draw the score information
        self.sb.show_score()

        #Draw the play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button() 

        #Make the most recently drawn screen visible, erases previous screen
        pygame.display.flip()
    
    #Helper method
    def _create_fleet(self):
        #Create the fleet of aliens
        #Make an alien and find number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        #Leaving two alien lengths on the margins of the screen
        available_space_x = self.settings.screen_width - (2 * alien_width)
        #Spacing between each alien is equal to one alien width (one alien width between aliens)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine number of rows that can fit on the screen (alien already on top row of screen and two alien lengths above ship)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        #One alien length between aliens
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #Create an alien and place it in the row
                self._create_alien(alien_number, row_number)

    #Helper Method
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    #Helper Method
    def _check_fleet_edges(self):
        #Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    #Helper Method
    def _change_fleet_direction(self):
        #Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    #Helper Method
    def _ship_hit(self):
        #Respond to the ship being hit by an alien
        if self.stats.ships_left > 0:
            #Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #Get rid of remaining bullets and aliens
            self.aliens.empty()
            self.bullets.empty()
            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            #Make mouse visible when game ends
            pygame.mouse.set_visible(True)
    
    #Helper Method
    def _check_aliens_bottom(self):
        #Check if amy aliens have reached the bottom of the screen 
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as the ship getting hit
                self._ship_hit()
                break

if __name__ == '__main__':
    #Make a game instance, and run the game
    #Runs game only if the file is called directly
    ai = AlienInvasion()
    ai.run_game()
