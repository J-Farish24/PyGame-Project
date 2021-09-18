import pygame
#Create ship class
class Ship:

    def __init__(self, ai_game):
        #Gives access to all game resources defined in Alien Invasion
        #Initialize ship and set starting position
        self.screen = ai_game.screen
        #Access screen's rect attribute
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image, self.rect)