import random

import pygame

SCALE = 3

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, spritesheet, w_height) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.screen_height = w_height
        self.spritesheet = spritesheet
        self.spritesheet_width = self.spritesheet.get_width() * SCALE
        self.spritesheet_height = self.spritesheet.get_height() * SCALE
        self.spritesheet = pygame.transform.scale(self.spritesheet, (self.spritesheet_width, self.spritesheet_height))
        self.sprite_width = self.spritesheet_width/2
        self.sprite_height = self.spritesheet_height/2
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=(200,200))
        self.frame_x = 0
        self.speed = 10
    

    def update(self):
        self.image.fill("black")
        self.image.blit(self.spritesheet, (0,0), (self.frame_x,0, self.sprite_width, self.sprite_height))
            
        self.rect.y += self.speed

        if self.rect.top > self.screen_height:
            self.kill()


class EnemyType1(pygame.sprite.Sprite):
    def __init__(self, screen, enemy_spritesheet, bullet_spritesheet,  s_width, s_hight) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_width = s_width
        self.screen_height = s_hight
        self.spritesheet = enemy_spritesheet
        self.bullet_spritesheet = bullet_spritesheet
        self.spritesheet_width = self.spritesheet.get_width() * SCALE
        self.spritesheet_height = self.spritesheet.get_height() * SCALE
        self.spritesheet = pygame.transform.scale(self.spritesheet, (self.spritesheet_width, self.spritesheet_height))
        self.sprite_width = self.spritesheet_width/2
        self.sprite_height = self.spritesheet_height
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_colorkey("black")
        self.frame_x = 0
        self.move_speed = 1
        self.side_speed = 3
        self.cooldown = 1000
        self.moviment_counter = 0
        self.moviment_range = 100
        self.animation_delay = 300
        self.last_animation = pygame.time.get_ticks()
        self.last_shoot = pygame.time.get_ticks()
        self.start_pos = random.randint(0, self.screen_width - self.moviment_range * 2.5)
        self.rect = self.image.get_rect(center=(self.start_pos, 0))
        self.damage = 50
    
    
    def update(self):
        self.change_frame()
        self.movement()

        self.image.fill("black")
        self.image.blit(self.spritesheet, (0,0), (self.frame_x,0, self.sprite_width, self.sprite_height))
        
        self.auto_destroy()
        
        
    def change_frame(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time -self.last_animation > self.animation_delay:
            if self.frame_x == 0:
                self.frame_x = self.sprite_width
            else:
                self.frame_x = 0
            self.last_animation = self.current_time
    

    def movement(self):
        self.rect.y += self.move_speed
        
        if abs(self.moviment_counter) >= self.moviment_range:
            self.moviment_counter = 0
            self.side_speed*= -1

        if self.moviment_counter <= self.moviment_range:
            self.rect.x += self.side_speed
            self.moviment_counter += 1


    def create_bullet(self) -> EnemyBullet:
        bullet = EnemyBullet(self.bullet_spritesheet, self.screen_height)
        bullet.rect.midtop = (self.rect.center)
        self.last_shoot = self.current_time
        return bullet
    

    def auto_destroy(self):
        if self.rect.top > self.screen_height:
            self.kill()
