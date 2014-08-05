import pygame, random

pygame.mixer.init()

right = pygame.mixer.Sound('data/sfx/right.ogg')
wrong = pygame.mixer.Sound('data/sfx/wrong.ogg')

class State(object):
    def __init__(self):
        self.active = False
    def set_next_state(self, state):
        self.next_state = state

class OutputState(State):
    def __init__(self, rounds):
        State.__init__(self)
        self.moves = rounds
        self.moveList = []
        for i in range(0, self.moves):
            self.moveList.append(random.randint(0,3))
        self.delayFrame = 0
        self.delay = 50
        self.currentmove = 0
        self.startDelay = 150
        self.startDelayFrame = 0
    def set_next_state(self, state):
        self.next_state = state
    def update(self, events, simon):
        if self.startDelayFrame < self.startDelay:
            self.startDelayFrame += 1
        else:
            if self.delayFrame > 0:
                self.delayFrame -= 1
            else:
                if self.currentmove < self.moves:
                    simon.board.flash_tile(self.moveList[self.currentmove])
                    self.currentmove += 1
                else:
                    self.active = False
                    self.next_state.active = True
                    simon.moveList = self.moveList
                self.delayFrame = self.delay

class InputState(State):
    def __init__(self):
        State.__init__(self)
        self.delayFrames = 0
        self.delay = 250
        self.moveList = []
    def update(self, events, simon):
        if not self.moveList == []:
            if self.delayFrames < self.delay:
                self.delayFrames += 1
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            simon.board.flash_tile(0)
                            self.moveList.append(0)
                            self.delayFrames = 0
                        if event.key == pygame.K_w:
                            simon.board.flash_tile(1)
                            self.moveList.append(1)
                            self.delayFrames = 0
                        if event.key == pygame.K_a:
                            simon.board.flash_tile(2)
                            self.moveList.append(2)
                            self.delayFrames = 0
                        if event.key == pygame.K_s:
                            simon.board.flash_tile(3)
                            self.moveList.append(3)
                            self.delayFrames = 0
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        tile = simon.board.get_tile(mousePos)
                        simon.board.flash_tile(tile)
                        self.moveList.append(tile)
                        self.delayFrames = 0
            else:
                self.active = False
                self.next_state.active = True
                simon.playerMoveList = self.moveList
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    tile = simon.board.get_tile(mousePos)
                    simon.board.flash_tile(tile)
                    self.moveList.append(tile)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        simon.board.flash_tile(0)
                        self.moveList.append(0)
                        self.delayFrames = 0
                    if event.key == pygame.K_w:
                        simon.board.flash_tile(1)
                        self.moveList.append(1)
                        self.delayFrames = 0
                    if event.key == pygame.K_a:
                        simon.board.flash_tile(2)
                        self.moveList.append(2)
                        self.delayFrames = 0
                    if event.key == pygame.K_s:
                        simon.board.flash_tile(3)
                        self.moveList.append(3)
                        self.delayFrames = 0

class ResultState(State):
    def __init__(self):
        State.__init__(self)
    def update(self, events, simon):
        if simon.moveListsMatch():
            right.play()
            simon.board.flash()
            simon.addRound()
        else:
            wrong.play()
            simon.board.disable()
            simon.reset()

class Simon(object):
    def __init__(self, board, rounds, addedRounds):
        self.board = board
        self.rounds = rounds
        self.addedRounds = addedRounds
        self.stateDict = [
            OutputState(self.rounds+self.addedRounds),
            InputState(),
            ResultState()
        ]
        for i in range(0,len(self.stateDict)-1):
            self.stateDict[i].set_next_state(self.stateDict[i+1])
        self.stateDict[0].active = True
        self.moveList = []
        self.playerMoveList = []
    def update(self, events):
        for state in self.stateDict:
            if state.active:
                state.update(events, self)
    def moveListsMatch(self):
        return self.moveList == self.playerMoveList
    def reset(self):
        self.__init__(self.board, self.rounds, 0)
    def addRound(self):
        self.__init__(self.board, self.rounds, self.addedRounds + 1)
