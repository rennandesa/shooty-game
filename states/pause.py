import pygame

from states.state import State

class Pause(State):
    def __init__(self, game) -> None:
        self.pause_music()
        super().__init__(game)
        self.color = "white"

    
    def update(self, actions):
        if actions["enter"]:
            self.unpause_music()
            self.exit_state()


    def render(self, display):
        self.game.draw_text(self.game.small_font, display, "PAUSED", self.color, self.game.screen_w/2, self.game.screen_h/2)


    def pause_music(self):
        pygame.mixer.music.pause()

    
    def unpause_music(self):
        pygame.mixer.music.unpause()
