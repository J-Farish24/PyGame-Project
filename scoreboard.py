import pygame.font
from pygame.sprite import Group, Sprite
from ship import Ship
class Scoreboard:
    def __init__(self, ai_game):
        #Initialize score keeping attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        #Font settings for scoring information
        self.text_color  = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        #Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        #Turn the score into a rendered image
        rounded_score = round(self.stats.score, -1) #Negative number will cause to round to 10, 100, 1000 place, etc.
        score_str = "{:,}".format(rounded_score) #Tells python to insert commas into numbers when converting a numercial value to a string
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)
        #Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        #Turn the high score into a rendered image
        high_score = round(self.stats.high_score,-1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, 
            self.text_color, self.settings.bg_color)
        #Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top
    
    def prep_level(self):
        #Turn the level into a rendered image
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
        self.text_color, self.settings.bg_color)
        #position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        #Make level 10 pixels beneath score
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        #Show how many ships are left
        #Create empty group
        self.ships = Group()
        #Runs once for each ship a player has left
        for ship_number in range(self.stats.ships_left):
            #Create ship and set x-coordinate  so ships appear next to each other with
            #a 10-pixel margin on the left side of the group of ships
            ship =Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            #Sets ships y-coordinate 10 pixels down the screen
            ship.rect.y = 10
            #Add ship to group of ships
            self.ships.add(ship)

    def show_score(self):
        #Draw scores, levels, and ships to the screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #Draws each ship in a group
        self.ships.draw(self.screen)

    def check_high_score(self):
        #Check to see if there's a new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()