#Track statistics for Alien invasion
class GameStats:
    def __init__(self, ai_game):
        #Initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()
        #Start Alien Invasion in an inactive state
        self.game_active = False

    #Initialize statistics that change during the game
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit