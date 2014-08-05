import pygame

pygame.mixer.init()

sound1 = pygame.mixer.Sound('data/sfx/1.ogg')
sound2 = pygame.mixer.Sound('data/sfx/2.ogg')
sound3 = pygame.mixer.Sound('data/sfx/3.ogg')
sound4 = pygame.mixer.Sound('data/sfx/4.ogg')

class Tile(object):
    def __init__(self, pos, size, color, sound):
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.flashFrames = 0
        self.flashDuration = 60
        self.disableFrames = 0
        self.disableDuration = 70
        self.sound = sound
    def update(self):
        # if flashing, reduce flash frames
        if self.flashFrames > 0:
            self.flashFrames -= 1
        if self.disableFrames > 0:
            self.disableFrames -= 1
    def draw(self, screen):
        if self.disableFrames == 0:
            if self.flashFrames > 0:
                # if flashing, display bright-colored square
                brightColor = [(num+255)/2 for num in self.color]
                pygame.draw.rect(screen, brightColor, self.rect, 0)
            else:
                # else, display dull-colored square
                pygame.draw.rect(screen, self.color, self.rect, 0)
    def flash(self):
        # increase flash frames to flash duration to fully light tile for duration
        self.flashFrames = self.flashDuration
    def disable(self):
        self.disableFrames = self.disableDuration

class Board(object):
    def __init__(self, windowRect):
        red = (255,0,0)
        blue = (0,0,255)
        yellow = (255,255,0)
        green = (0,255,0)
        halfWindowSize = (windowRect.width/2, windowRect.height/2)
        r = windowRect
        self.tiles = [
            Tile((r.topleft[0],r.topleft[1]), halfWindowSize, red, sound1),
            Tile((r.midtop[0], r.midtop[1]), halfWindowSize, blue, sound2),
            Tile((r.midleft[0], r.midleft[1]), halfWindowSize, yellow, sound3),
            Tile((r.center[0], r.center[1]), halfWindowSize, green, sound4)
        ]
        self.frames = 0
        self.duration = 50
    def update(self):
        for tile in self.tiles:
            tile.update()
    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)
    def flash_tile(self, tileNum):
        self.tiles[tileNum].flash()
        self.tiles[tileNum].sound.play()
    def get_tile(self, mousePos):
        for tileNum in range(0,len(self.tiles)):
            if self.tiles[tileNum].rect.collidepoint(mousePos):
                return tileNum
    def flash(self):
        for tile in self.tiles:
            tile.flash()
    def disable(self):
        for tile in self.tiles:
            tile.disable()