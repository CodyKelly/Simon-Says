import pygame, random

pygame.mixer.init()

right = pygame.mixer.Sound('data/sfx/right.ogg')
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
        self.moves = simon.rounds+simon.addedRounds
        self.moveList = []
        for i in range(0, self.moves):
            self.moveList.append(random.randint(0,3))
        self.delayFrame = 0
        self.delay = 50
        self.currentMove = 0
        self.startDelay = 150
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
                if self.currentMove < self.moves:
                    self.simon.board.flash_tile(self.moveList[self.currentMove])
                    self.currentMove += 1
                else:
                    self.active = False
                    self.next_state.active = True
                    self.simon.moveList = self.moveList
                self.delayFrame = self.delay

class InputState(State):
    # This state allows the user to choose tiles and keeps track of the tiles picked.
    def __init__(self, simon):
        State.__init__(self, simon)
        self.delayFrames = 0
        self.delay = 250
        self.moveList = []
    def update(self, events):
        if not self.moveList == []:
            if self.delayFrames < self.delay:
                self.delayFrames += 1
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.activateTile(0)
                        if event.key == pygame.K_w:
                            self.activateTile(1)
                        if event.key == pygame.K_a:
                            self.activateTile(2)
                        if event.key == pygame.K_s:
                            self.activateTile(3)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        tile = self.simon.board.get_tile(mousePos)
                        self.activateTile(tile)
            else:
                self.active = False
                self.next_state.active = True
                self.simon.playerMoveList = self.moveList
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    tile = self.simon.board.get_tile(mousePos)
                    self.activateTile(tile)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.activateTile(0)
                    if event.key == pygame.K_w:
                        self.activateTile(1)
                    if event.key == pygame.K_a:
                        self.activateTile(2)
                    if event.key == pygame.K_s:
                        self.activateTile(3)
    def activateTile(self, tile):
        self.simon.board.flash_tile(tile)
        self.moveList.append(tile)
        self.delayFrames = 0

class ResultState(State):
    # this state compares the tiles Simon picked and the tiles the user picked
    # if the user was correct, it adds a round to the game. Otherwise the game is reset to three rounds.
    def __init__(self, simon):
        State.__init__(self, simon)
    def update(self, events):
        if self.simon.moveListsMatch():
            right.play()
            self.simon.board.flash()
            self.simon.addRound()
        else:
            wrong.play()
            self.simon.board.disable()
            self.simon.reset()

class Simon(object):
    # Keeps track of states and number of rounds.
    def __init__(self, board, rounds, addedRounds):
        self.board = board
        self.rounds = rounds
        self.addedRounds = addedRounds
        self.stateDict = [
            OutputState(self),
            InputState(self),
            ResultState(self)
        ]
        for i in range(0,len(self.stateDict)-1):
            self.stateDict[i].set_next_state(self.stateDict[i+1])
        self.stateDict[0].active = True
        self.moveList = []
        self.playerMoveList = []
    def update(self, events):
        for state in self.stateDict:
            if state.active:
                state.update(events)
    def moveListsMatch(self):
        return self.moveList == self.playerMoveList
    def reset(self):
        self.__init__(self.board, self.rounds, 0)
    def addRound(self):
        self.__init__(self.board, self.rounds, self.addedRounds + 1)
