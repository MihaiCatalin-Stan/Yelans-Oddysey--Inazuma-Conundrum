import pygame

class NpcInCombat(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, attack, scale_x, scale_y):
        super().__init__()
        self.image = pygame.image.load(picture).convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale_x, scale_y))
        self.rect = self.image.get_rect()
        self.max_health = 100
        self.remaining_health = self.max_health
        self.rect.x = x
        self.rect.y = y
        self.attack = attack

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def talk(self):
        pass
    
    def die(self):
        self.kill()

    def take_damage(self, damage):
        self.remaining_health -= damage

    def get_rect(self):
        return self.rect

    def update(self):
        pass
