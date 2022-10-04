
class Score:
    def __init__(self, game) -> None:
        self.game = game
        self.color = "white"
        self.score = 0
        self.load_hi_score()
        self.new_record = False
        

    def add(self, health):
        self.score += 500 + (health * 10)

    
    def reset_score(self):
        self.new_record = False
        self.score = 0


    def load_hi_score(self):
        self.hi_score = 0


    def save_hi_score(self):
        if self.score > self.hi_score:
            self.new_record = True
            self.hi_score = self.score

    
    def has_new_record(self):
        return self.new_record


    def render(self, display):
        self.game.draw_text(self.game.small_font, display, f"SCORE: {self.score:05}", self.color, 670, 20)
        self.game.draw_text(self.game.small_font, display, f"HI-SCORE: {self.hi_score:05}", self.color, 650, 50)


