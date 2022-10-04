import pygame

SCALE = 4

class Explosion(pygame.sprite.Sprite):
    def __init__(self,spritesheet, rect, s_width, s_hight) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.screen_width = s_width
        self.screen_height = s_hight
        self.spritesheet = spritesheet
        self.spritesheet_width = self.spritesheet.get_width() * SCALE
        self.spritesheet_height = self.spritesheet.get_height() * SCALE
        self.spritesheet = pygame.transform.scale(self.spritesheet, (self.spritesheet_width, self.spritesheet_height))
        self.sprite_width = self.spritesheet_width/5
        self.sprite_height = self.spritesheet_height
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_colorkey("black")
        self.rect = rect
        self.frame_x = 0
        self.animation = 0
        self.animation_speed = 50
        self.last_timer = pygame.time.get_ticks()


    def update(self) -> None:
        current_timer = pygame.time.get_ticks()
        if current_timer - self.last_timer > self.animation_speed:
            self.image.fill("black")
            self.image.blit(self.spritesheet, (0,0), (self.frame_x,0, self.sprite_width, self.sprite_height))
            
            self.frame_x += self.sprite_width
            self.last_timer = current_timer
            self.animation += 1
            if self.animation > 5:
                self.kill()