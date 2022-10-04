import pygame

class HealthBar:
    def __init__(self, pos_x, pos_y):
        self.full_health = 250
        self.remaining = 250
        self.image = pygame.Surface((self.full_health, 20))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.bar = pygame.draw.rect(self.image, "red", (0,0, self.full_health, 20))
        self.health = pygame.draw.rect(self.image, "green", (0,0, self.remaining, 20))
        

    def update(self):
        self.bar = pygame.draw.rect(self.image, "red", (0,0, self.full_health, 20))
        self.health = pygame.draw.rect(self.image, "green", (0,0, self.remaining, 20))

    def render(self, display):
        display.blit(self.image, self.rect)
