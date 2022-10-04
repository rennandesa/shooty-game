class State:
    def __init__(self, game) -> None:
        self.game = game
        self.prev_state = None
    

    def update(self, actions):
        pass


    def render(self, display):
        pass


    def enter_state(self):
        self.game.reset_keys()
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)


    def exit_state(self):
        self.game.reset_keys()
        self.game.state_stack.pop()
