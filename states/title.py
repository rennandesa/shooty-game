from states.state import State
from states.gameplay import GamePlay
from states.controls import ControlsMenu

class Title(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.menu_options = {
            0: "play",
            1: "controls",
            2: "quit",
        }
        self.index = 0
        self.cursor = "->"
        self.line_spacing = 80
        self.cursor_pos_y = self.game.screen_h/2 - 50
        self.left_margin = 210
        self.color = "white"
        self.pressed_button = False
    

    def update(self, actions):
        if actions["enter"]:
            if self.menu_options[self.index] == "play":
                new_state = GamePlay(self.game)
                new_state.enter_state()
            elif self.menu_options[self.index] == "controls":
                new_state = ControlsMenu(self.game)
                new_state.enter_state()
            elif self.menu_options[self.index] == "quit":
                self.game.quit()

        self.update_cursor(actions)


    def render(self, display):
        display.fill("black")
        for index, menu_option in self.menu_options.items():
            self.game.draw_text(self.game.large_font, display, menu_option.upper(), self.color, self.game.screen_w/2, self.cursor_pos_y + ( index * self.line_spacing ))

        self.game.draw_text(self.game.large_font, display, self.cursor, self.color, self.left_margin, self.cursor_y)


    def update_cursor(self, actions):
        if not self.pressed_button:
            if actions["down"]:
                self.play_sfx()
                self.pressed_button = True
                self.index = (self.index + 1) % len(self.menu_options)
            elif actions["up"]:
                self.play_sfx()
                self.pressed_button = True
                self.index = (self.index - 1) % len(self.menu_options)
        
        if not actions["down"] and not actions["up"]:
            self.pressed_button = False

        self.cursor_y = self.cursor_pos_y + (self.index * self.line_spacing)
    
    def play_sfx(self):
        self.game.menu_nav_sfx.play()
