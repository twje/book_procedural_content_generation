class NullState:
    def exit(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def render(self):
        pass


class StateMachine:
    def __init__(self):
        self.states = {}
        self.state = NullState()

    def set_state(self, name):
        self.state = self.states[name]

    def add_state(self, name, state):
        self.state.exit()
        self.states[name] = state
        self.state.start()

    def update(self):
        self.state.update()

    def render(self):
        self.state.render()
