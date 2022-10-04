import math
import random

import pygame

from states.state import State
from gameplay.player import SpaceShip
from gameplay.enemy import EnemyType1
from gameplay.healthbar import HealthBar
from gameplay.explosion import Explosion
from states.gameover import GameOver
from states.pause import Pause

class BackGround:
    def __init__(self, img, width, height) -> None:
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(img, (self.width, self.height))
        self.buffer = 1
        self.scroll = 0
        self.tiles = math.ceil(height/ width) + self.buffer
        self.scroll_speed = 2

    
    def update(self):
        if self.scroll > self.height:
            self.scroll = 0
        self.scroll += self.scroll_speed


    def render(self, display):
        for tile in range(self.tiles):
            self.rect = self.image.get_rect(midbottom=(self.width/2, self.height - (tile * self.height) + self.scroll))
            display.blit(self.image, self.rect)

    
class GamePlay(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.background = BackGround(self.game.backgroud_img, self.game.screen_w, self.game.screen_h)
        self.player = SpaceShip(game)
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.healhbar = HealthBar(10, 10)
        self.timer = pygame.time.get_ticks()
        self.collision_dgm = 50
        self.gameover = False
        self.game.score.reset_score()
        self.play_music()


    def update(self, actions):
        self.background.update()
        self.player.update(actions)
        self.respawn_enemy()
        self.enemy_group.update()
        self.respawn_enemy_bullet()
        self.enemy_bullet_group.update()
        self.explosion_group.update()
        self.check_collisions()
        self.check_gameover()
        self.check_if_paused(actions)


    def render(self, display):
        self.background.render(display)
        self.player.render(display)
        self.enemy_group.draw(display)
        self.enemy_bullet_group.draw(display)
        self.healhbar.render(display)
        self.enemy_bullet_group.draw(display)
        self.explosion_group.draw(display)
        self.game.score.render(display)


    def respawn_enemy(self):
        current_timer = pygame.time.get_ticks()
        if current_timer - self.timer > random.randint(1000, 3000):
            new_enemy = EnemyType1(self.game.game_canvas, self.game.enemy_type1 ,self.game.bullet_spritesheet, self.game.screen_w, self.game.screen_h)
            self.enemy_group.add(new_enemy)
            self.timer = current_timer


    def respawn_enemy_bullet(self):
        for enemy in self.enemy_group:
            if enemy.current_time - enemy.last_shoot > enemy.cooldown:
                self.game.enemy_1_shoot_sfx.play()
                new_bullet = enemy.create_bullet()
                self.enemy_bullet_group.add(new_bullet)


    def create_exposion(self, rect):
        self.game.explosion_sfx.play()
        new_explosion = Explosion(self.game.exposion_spritesheet, rect, self.game.screen_w, self.game.screen_h)
        self.explosion_group.add(new_explosion)


    def check_if_paused(self, actions):
        if actions["enter"]:
            new_state = Pause(self.game)
            new_state.enter_state()


    def check_collisions(self):
        for enemy in self.enemy_group:
            if pygame.sprite.spritecollide(self.player, self.enemy_bullet_group, True):
                self.game.player_hit_sfx.play()
                self.healhbar.remaining -= enemy.damage

        for sprite in pygame.sprite.groupcollide(self.player.bullets, self.enemy_group, True, True):
            self.game.score.add(self.healhbar.remaining)
            self.create_exposion(sprite.rect)

        for sprite in pygame.sprite.spritecollide(self.player, self.enemy_group, True):
            self.healhbar.remaining -= enemy.damage + self.collision_dgm
            self.create_exposion(sprite.rect)

        self.healhbar.update()

    def check_gameover(self):
        if not self.gameover and self.healhbar.remaining <= 0:
            self.create_exposion(self.player.rect)
            self.gameover = True

        if self.gameover and len(self.explosion_group) == 0:
            self.stop_music()
            self.game.score.save_hi_score()
            new_record = self.game.score.has_new_record()
            self.play_xfs(new_record)
            new_state = GameOver(self.game, new_record)
            new_state.enter_state()
    
    def play_music(self):
        pygame.mixer.music.play(-1)
    

    def stop_music(self):
        pygame.mixer.music.stop()


    def play_xfs(self, new_record):
        if new_record:
                self.game.new_record_sfx.play()
        else:
            self.game.game_over_sfx.play()
