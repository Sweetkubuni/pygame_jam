class State:
    def __init__(self, game) -> None:
        self.game = game
        self.previos_state = None

    def update(self):
        pass
    def render(self):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.previos_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()