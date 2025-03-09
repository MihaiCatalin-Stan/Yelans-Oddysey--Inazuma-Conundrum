import pygame

class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, dialogue_image, dialogue_path, scale_x, scale_y):
        super().__init__()
        self.image = pygame.image.load(picture).convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale_x, scale_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.npc_image = dialogue_image
        self.dialogue_path = dialogue_path

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def talk(self):
        pass
    
    def die(self):
        self.kill()

    def update(self):
        pass