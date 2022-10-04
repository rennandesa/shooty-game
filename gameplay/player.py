import pygame

from gameplay.bullet import Bullet

SPRITE_SHEET_COLUMN = 5
SPRITE_SHEET_ROW = 2
SCALE = 3

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.canas = game.game_canvas
        self.canvas_width = game.screen_w
        self.canvas_height = game.screen_h
        self.bullet_spritesheet = game.bullet_spritesheet
        self.padding = 10
        self.spritesheet = game.player_spritesheet
        self.spritesheet_width = self.spritesheet.get_width() * SCALE
        self.spritesheet_height = self.spritesheet.get_height() * SCALE
        self.sprite_width = self.spritesheet_width / SPRITE_SHEET_COLUMN
        self.sprite_height = self.spritesheet_height / SPRITE_SHEET_ROW
        self.spritesheet = pygame.transform.scale(self.spritesheet, (self.spritesheet_width, self.spritesheet_height))
        self.frame_x = 2
        self.frame_y = 0
        self.speed = 10
        self.roll_speed = 0.2
        self.axis = 2
        self.last_timer = pygame.time.get_ticks()
        self.inverval = 300
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(midbottom=(self.canvas_width/2, self.canvas_height - self.padding))
        self.bullets = pygame.sprite.Group()
        self.cooldown = 300
        self.last_shoot = pygame.time.get_ticks()


    def update(self, actions):
        if actions["up"]:
            self.up()
        if actions["down"]:
            self.down()
        if actions["right"]:
            self.right()
        if actions["left"]:
            self.left()
        if actions["shoot"]:
            self.shoot()

        if not actions["left"] and not actions["right"]:
            self.roll_back()

        self.bullets.update()

    def render(self, display):
        self.image.blit(self.spritesheet, (0,0), self.get_frame_area())
        display.blit(self.image, self.rect)
        self.animate_turbine()
        self.bullets.draw(display)


    def get_frame_area(self):
        return self.sprite_width * self.frame_x, self.frame_y, self.sprite_width, self.sprite_height


    def roll_back(self):
        if self.frame_x > 2:
            self.rotate_left()
        if self.frame_x < 2:
            self.rotate_rigth()


    def animate_turbine(self):
        current_timer = pygame.time.get_ticks()
        if current_timer > self.last_timer + self.inverval:
            if self.frame_y == 0:
                self.frame_y = self.sprite_height
            elif self.frame_y == self.sprite_height:
                self.frame_y = 0
            self.last_timer = current_timer


    def rotate_rigth(self):
        if self.frame_x < 4:
            self.axis += self.roll_speed
            self.frame_x = int(self.axis)


    def rotate_left(self):
        if self.frame_x > 0:
            self.axis -= self.roll_speed
            self.frame_x = int(self.axis)


    def right(self):
        self.rotate_rigth()
        if self.rect.right < self.canvas_width:
            self.rect.right += self.speed


    def left(self):
        self.rotate_left()
        if self.rect.left > 0:
            self.rect.right -= self.speed


    def up(self):
        if self.rect.top > self.padding:
            self.rect.top -= self.speed


    def down(self):
        if self.rect.bottom < self.canvas_height - self.padding:
            self.rect.bottom += self.speed


    def shoot(self):
        current_timer = pygame.time.get_ticks()
        if current_timer > self.last_shoot + self.cooldown:
            self.game.player_shoot_sfx.play()
            projectil = Bullet(self.bullet_spritesheet)
            projectil.rect.midbottom = (self.rect.midtop)
            self.bullets.add(projectil)
            self.last_shoot = current_timer

