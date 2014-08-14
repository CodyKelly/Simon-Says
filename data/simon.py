import pygame, random

pygame.mixer.init()

wrong = pygame.mixer.Sound('data/sfx/wrong.ogg')

class State(object):
    # base class for Simon's states. Holds the next state, whether the state is active or not, and Simon
    def __init__(self, simon):
        self.active = False
        self.simon = simon
    def set_next_state(self, state):
        self.next_state = state

class OutputState(State):
    # This state chooses and flashes random tiles and keeps track of the tiles picked.
    def __init__(self, simon):
        State.__init__(self, simon)
        simon.moveList.append(random.randint(0,3))
        self.delayFrame = 0
        self.delay = 30
        self.currentMove = 0
        self.startDelay = 100
        self.startDelayFrame = 0
    def set_next_state(self, state):
        self.next_state = state
    def update(self, events):
        if self.startDelayFrame < self.startDelay:
            self.startDelayFrame += 1
        else:
            if self.delayFrame > 0:
                self.delayFrame -= 1
            else:
                if self.currentMove < len(self.simon.moveList):
                    self.simon.board.flash_tile(self.simon.moveList[self.currentMove])
                    self.currentMove += 1
                else:
                    self.active = False
                    self.next_state.active = True
                self.delayFrame = self.delay

class InputState(State):
    # This state allows the user to choose tiles and keeps track of the tiles picked.
    def __init__(self, simon):
        State.__init__(self, simon)
        self.moveList = []
        self.activators = {pygame.K_q: 0,
                           pygame.K_w: 1,
                           pygame.K_a: 2,
                           pygame.K_s: 3}
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.activators:
                    self.activate_tile(self.activators[event.key])
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                tile = self.simon.board.get_tile(mousePos)
                self.activate_tile(tile)
    def activate_tile(self, tile):
        # Checks if tile activated is right and responds accordingly
        if tile == self.simon.moveList[len(self.moveList)]:
            self.simon.board.flash_tile(tile)
            self.moveList.append(tile)
            if len(self.simon.moveList) == len(self.moveList):
                self.simon.board.flash()
                self.simon.add_round()
        else:
            wrong.play()
            self.simon.board.disable()
            self.simon.reset()

class Simon(object):
    # Keeps track of states and number of rounds.
    def __init__(self, board, moveList):
        self.board = board
        self.moveList = moveList
        self.stateDict = [
            OutputState(self),
            InputState(self)
        ]
        for i in range(0,len(self.stateDict)-1):
            self.stateDict[i].set_next_state(self.stateDict[i+1])
        self.stateDict[0].active = True
        self.playerMoveList = []
    def update(self, events):
        for state in self.stateDict:
            if state.active:
                state.update(events)
    def moveListsMatch(self):
        return self.moveList == self.playerMoveList
    def reset(self):
        self.__init__(self.board, [])
    def add_round(self):
        self.__init__(self.board, self.moveList)
