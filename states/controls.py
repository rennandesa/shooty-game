from states.state import State


class ControlsMenu(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.color = "white"
        self.controls = {
            "UP": "Up Arrow Key",
            "LEFT": "Left Arrow key",
            "RIGHT": "Right Arrow Key",
            "DOWN": "Down Arrow Key",
            "SHOOT": "Space",
            "PAUSE": "Enter"
        }

    
    def update(self, actions):
        if actions["enter"]:
            self.exit_state()


    def render(self, display):
        display.fill("black")
        self.game.draw_text(self.game.large_font, display, "GAME CONTROLS", self.color, self.game.screen_w/2, 200)
        for index, option in enumerate(self.controls.items()):
            self.game.draw_text(self.game.small_font, display, f"{option[0]} = {option[1]}", self.color, self.game.screen_w/2, 400 + (index * 40))
