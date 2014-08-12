#Created by Cody Kelly, aka hoyohoyo9

import pygame, sys
from board import Board
from simon import Simon

pygame.init()

windowRect = pygame.Rect((0,0),(800, 800))

screen = pygame.display.set_mode(windowRect.size)

RED = (255,0,0)

clock = pygame.time.Clock()

caption = 'Simon Says'
pygame.display.set_caption(caption)

def run():

    #initialize everything
    board = Board(windowRect)
    simon = Simon(board, 3, 0)

    #game loop
    while True:
        clock.tick(60)
        screen.fill(RED)

        events = pygame.event.get()

        #gotta check for quit
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #update everything
        simon.update(events)
        board.update()

        #draw board
        board.draw(screen)

        pygame.display.update()
