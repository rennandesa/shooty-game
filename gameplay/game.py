import os

import pygame

from states.title import Title
from gameplay.score import Score

SCREEN_WIDTH = 780
SCREEN_HEIGHT = 800
FPS = 60

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen_w = SCREEN_WIDTH
        self.screen_h = SCREEN_HEIGHT
        self.game_canvas = pygame.Surface((self.screen_w, self.screen_h))
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Shooty Game created in Pygame")
        self.clock = pygame.time.Clock()
        self.score = Score(self)
        self.actions = {
            "enter": False,
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False
        }
        self.running, self.playing = True, True
        self.state_stack = []
        self.load_assets()
        self.load_states()

    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.actions["enter"] = True
                if event.key == pygame.K_UP:
                    self.actions["up"] = True
                if event.key == pygame.K_DOWN:
                    self.actions["down"] = True
                if event.key == pygame.K_LEFT:
                    self.actions["left"] = True
                if event.key == pygame.K_RIGHT:
                    self.actions["right"] = True
                if event.key == pygame.K_SPACE:
                    self.actions["shoot"] = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.actions["enter"] = False
                if event.key == pygame.K_UP:
                    self.actions["up"] = False
                if event.key == pygame.K_DOWN:
                    self.actions["down"] = False
                if event.key == pygame.K_LEFT:
                    self.actions["left"] = False
                if event.key == pygame.K_RIGHT:
                    self.actions["right"] = False
                if event.key == pygame.K_SPACE:
                    self.actions["shoot"] = False
    
    
    def reset_keys(self):
        self.actions["enter"] = False
        self.actions["up"] = False
        self.actions["down"] = False
        self.actions["left"] = False
        self.actions["right"] = False
        self.actions["shoot"] = False
    

    def update(self):
        self.state_stack[-1].update(self.actions)


    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(self.game_canvas, (0, 0))
        pygame.display.flip()
    

    def game_loop(self):
        while self.playing:
            self.clock.tick(FPS)
            self.get_events()
            self.update()
            self.render()
    
    def quit(self):
        self.running = False
        self.playing = False


    def draw_text(self, font, surface, text, color, xcoord, ycoord):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (xcoord, ycoord)
        surface.blit(text_surface, text_rect)


    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.spritesheets_dir = os.path.join(self.assets_dir, "spritesheets")
        self.backgroud_dir = os.path.join(self.assets_dir, "backgrounds")
        self.music_dir = os.path.join(self.assets_dir, "sounds", "music")
        self.sfx_dir = os.path.join(self.assets_dir, "sounds", "sfx")
        self.font_dir =  os.path.join(self.assets_dir, "fonts")

        self.small_font = pygame.font.Font(os.path.join(self.font_dir, "m6x11.ttf"), 30)
        self.large_font = pygame.font.Font(os.path.join(self.font_dir, "m6x11.ttf"), 80)

        self.backgroud_img = pygame.image.load(os.path.join(self.backgroud_dir, "desert-background.png")).convert()
        self.player_spritesheet = pygame.image.load(os.path.join(self.spritesheets_dir, "ship.png")).convert_alpha()
        self.bullet_spritesheet = pygame.image.load(os.path.join(self.spritesheets_dir, "laser-bolts.png")).convert_alpha()
        self.enemy_type1 = pygame.image.load(os.path.join(self.spritesheets_dir, "enemy-small.png")).convert_alpha()
        self.exposion_spritesheet = pygame.image.load(os.path.join(self.spritesheets_dir, "explosion.png")).convert_alpha()

        self.loop_music = pygame.mixer.music.load(os.path.join(self.music_dir, "X.ogg"))
        self.explosion_sfx = pygame.mixer.Sound(os.path.join(self.sfx_dir, "explosion.mp3"))
        self.player_shoot_sfx = pygame.mixer.Sound(os.path.join(self.sfx_dir, "player_shoot.mp3"))
        self.player_hit_sfx = pygame.mixer.Sound(os.path.join(self.sfx_dir, "hit_01.mp3"))
        self.enemy_1_shoot_sfx = pygame.mixer.Sound(os.path.join(self.sfx_dir, "shoot_01.mp3"))
        self.new_record_sfx = pygame.mixer.Sound(os.path.join(self.sfx_dir, "jingle_Win_00.mp3"))
        self.game_over_sfx = pygame.mixer.Sound(os.path.join(self.sfx_dir, "jingle_Lose_00.mp3"))
        self.menu_nav_sfx = pygame.mixer.Sound(os.path.join(self.sfx_dir, "menu_Navigate_00.mp3"))


    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)
