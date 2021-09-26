import pygame 
from pygame.sprite import Sprite
#A class to represent a single alien in the fleet
class Alien(Sprite):
    def __init__(self, ai_game):
        #Intialize the alien and set its starting position
        super().__init__()
        self.screen = ai_game.screen
        #load alien image and set ret attributes
        self.image = pygame.image.load('alien.bmp')
        self.rect = self.image.get_rect()
        #Start each new a;oem mear the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #Store the alien's exact horizontal position
        self.x = float(self.rect.x)