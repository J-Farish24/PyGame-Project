import pygame
#Create ship class
class Ship:

    def __init__(self, ai_game):
        #Gives access to all game resources defined in Alien Invasion
        #Initialize ship and set starting position
        self.screen = ai_game.screen
        #Create ship setting to use in _update()
        self.settings = ai_game.settings
        #Access screen's rect attribute
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        #Store a decimal value for te ship's horizontal position
        self.x = float(self.rect.x)
        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #Movement flag
        self.moving_right = False
        self.moving_left = False


    def _update(self):
        #Update the ship's position based on the movement flag
        #Two ifs because if an elif was used, right key would have priority
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        #Update rect object from self.x, only integer portion stored
        self.rect.x = self.x


    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image, self.rect)