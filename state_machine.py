class State():
    name = 'State'

    def __init__(self, state_machine) -> None:
        self._state_machine = state_machine
        self._next_state = ''

    def update(self):
        if self._next_state:
            return self._next_state

        return self.name

    def enter(self):
        self._next_state = ''
        print(self.name, 'ENTER')

    def exit(self):
        print(self.name, 'EXIT')

class StateMachine():
    def __init__(self) -> None:
        self.current_state_name = ''
        self.previous_state_name = ''
        self._states = {}
        return

    def update(self):
        if self.current_state_name not in self._states:
            return

        next_state = self._states[self.current_state_name].update()

        if self.current_state_name != next_state:
            self.change(next_state)
    
    def add(self, state):
        self._states[state.name] = state

    def change(self, state_name):
        if self.current_state_name in self._states:
            self._states[self.current_state_name].exit()

        self.previous_state_name = self.current_state_name
        self.current_state_name = state_name
        self._states[self.current_state_name].enter()

    def get_active_state(self):
        if self.current_state_name in self._states:
            return self._states[self.current_state_name]
    