import pygame
from npc import Npc

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Images/yelan.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (62, 150))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.flip(self.image, True, False)
        self.direction = "right"
        self.rect.x = x
        self.rect.y = y

        # Load and scale the walking animation frames
        self.player_walk_list = [f'Images/Animations/yelan_walk{i}.png' for i in range(12)]
        self.player_walk_list = [self.load_and_scale_image(image_path) for image_path in self.player_walk_list]

        self.player_walk_index = 0

        self.is_jumping = False
        self.jump_count = 0  # Number of jumps allowed

    def load_and_scale_image(self, image_path):
        original_image = pygame.image.load(image_path).convert_alpha()
        original_image = pygame.transform.scale(original_image, (90, 150))

        return original_image

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_a]:
            if self.direction == "right":
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction = "left"
            self.rect.x -= 5
        if keys[pygame.K_d]:
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction = "right"
            self.rect.x += 5
            
    def simulate_gravity(self):
        if not self.is_jumping and self.rect.bottom < 480:
            self.rect.y += 5
        if self.rect.bottom >= 480:
            self.rect.bottom = 480
            self.is_jumping = False
            self.jump_count = 2

    def interaction_check(self, npc):
        # Make sure characters interact only if they are close enough
        if self.rect.x - npc.rect.x <= 50 and self.rect.y - npc.rect.y <= 50:
            return True

    def player_animation(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d]:  # Check if the player is moving
            self.player_walk_index += 0.1  # Make the animation smoother
            frame_index = int(self.player_walk_index) % len(self.player_walk_list)
            self.image = self.player_walk_list[frame_index]

            # Update the direction attribute when moving
            if keys[pygame.K_a]:
                self.direction = "left"
            elif keys[pygame.K_d]:
                self.direction = "right"

            # Flip the image based on the direction
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            # Player is not moving, set to idle frame
            if self.direction == "left":
                self.image = pygame.transform.flip(self.player_walk_list[0], True, False)
            else:
                self.image = self.player_walk_list[0]

    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and (not self.is_jumping or (self.is_jumping and self.jump_count > 0)):
            self.is_jumping = True
            self.jump_count -= 1
        if self.is_jumping:
            self.rect.y -= 10
            if self.rect.y <= 200:
                self.is_jumping = False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def die(self):
        self.kill()

    def update(self):
        self.player_input()
        self.simulate_gravity()
        self.player_animation()
        self.jump()
        