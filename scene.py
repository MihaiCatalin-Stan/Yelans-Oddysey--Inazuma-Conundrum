import pygame

class Scene():
    def __init__(self, player, screen, npc=None):
        self.player = player
        self.npc = npc
        self.screen = screen
        self.background = None  # Initialize background in derived classes

    def display(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

        if self.npc:
            self.npc.draw(self.screen)
            self.npc.update()

        self.player.draw(self.screen)
        self.player.update()

        pygame.display.flip()

    def talk_npc(self):
        pass

    def transition(self):
        # check player position and transition accordingly
        pass

    def get_npc(self):
        return self.npc if self.npc is not None else None
    
    def get_player(self):
        return self.player

    def update(self):
        self.display()
        self.talk_npc()
        self.transition()
        self.get_npc()
        
