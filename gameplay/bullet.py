import pygame

SCALE = 2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.spritesheet_width = self.spritesheet.get_width() * SCALE
        self.spritesheet_height = self.spritesheet.get_height() * SCALE
        self.spritesheet = pygame.transform.scale(self.spritesheet, (self.spritesheet_width, self.spritesheet_height))
        self.sprite_width = self.spritesheet_width/2
        self.sprite_height = self.spritesheet_height/2
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.frame_x = 0
        self.speed = 10
        self.last_animation = pygame.time.get_ticks()
        self.animation_delay = 100
    
    def update(self):
        current_timer = pygame.time.get_ticks()
        if current_timer > self.last_animation + self.animation_delay:
            if self.frame_x == 0:
                self.frame_x = self.sprite_width
            else:
                self.frame_x = 0
            self.last_animation = current_timer

        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
    
        self.image.fill("black")
        self.image.blit(self.spritesheet, (0,0), (self.frame_x,self.sprite_width, self.sprite_width, self.sprite_height))
