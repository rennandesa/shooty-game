from states.state import State

class GameOver(State):
    def __init__(self, game, new_record) -> None:
        super().__init__(game)
        self.new_record = new_record
        self.color = "white"

    
    def update(self, actions):
        if actions["enter"]:
            self.exit_state()
            self.prev_state.exit_state()
            

    def render(self, display):
        display.fill("black")
        self.game.draw_text(self.game.large_font, display, "GAME OVER", self.color, self.game.screen_w/2, self.game.screen_h/2)
        self.game.draw_text(self.game.small_font, display, "-PRESS ENTER TO RETURN TO MAIN MENU-", self.color, self.game.screen_w/2, self.game.screen_h/2 + 100)
        if self.new_record:
            self.game.draw_text(self.game.large_font, display, f"!!! NEW RECORD !!!", self.color, self.game.screen_w/2, self.game.screen_h/2 + 200)
            self.game.draw_text(self.game.small_font, display, f"{self.game.score.score} POINTS", self.color, self.game.screen_w/2, self.game.screen_h/2 + 260)

