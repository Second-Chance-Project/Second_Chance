import random
import pygame as pg

from src.constants import *
from src.states.minigames.minigame import Minigame


class Filler(Minigame):

    def __init__(self):
        instructions = "Click colors to expand your territory. Capture 50% of the board to win!"
        super().__init__(instructions)

        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.rows = 10
        self.cols = 10
        self.tile_size = 40

        self.colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255)
        ]

        self.board = []
        self.player_tiles = set()
        self.moves = 0

        self.generate_board()
        self.create_color_buttons()

    def generate_board(self):
        """Creates a random colored grid."""

        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(random.randint(0, len(self.colors)-1))
            self.board.append(row)

        self.player_tiles.add((0, 0))

    def create_color_buttons(self):
        """Creates clickable color buttons."""

        self.color_buttons = []

        for i in range(len(self.colors)):
            rect = pg.Rect(100 + i*60, SCREEN_HEIGHT-80, 50, 50)
            self.color_buttons.append(rect)

    def flood_fill(self, new_color):
        """Expands territory using flood fill."""

        queue = list(self.player_tiles)

        while queue:
            r, c = queue.pop(0)

            neighbors = [
                (r+1,c),
                (r-1,c),
                (r,c+1),
                (r,c-1)
            ]

            for nr, nc in neighbors:

                if 0 <= nr < self.rows and 0 <= nc < self.cols:

                    if (nr,nc) not in self.player_tiles:

                        if self.board[nr][nc] == new_color:
                            self.player_tiles.add((nr,nc))
                            queue.append((nr,nc))

        for r,c in self.player_tiles:
            self.board[r][c] = new_color

        self.moves += 1

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:

            if event.type == pg.MOUSEBUTTONDOWN:

                for i, button in enumerate(self.color_buttons):

                    if button.collidepoint(event.pos):
                        self.flood_fill(i)

        if len(self.player_tiles) > (self.rows*self.cols)//2:
            self.won = True

        if self.moves > 15:
            self.won = False

    def update(self, events):
        super().update(events)

    def draw(self):
        super().draw()

        self.draw_grid()
        self.draw_buttons()

    def draw_grid(self):

        for r in range(self.rows):
            for c in range(self.cols):

                color = self.colors[self.board[r][c]]

                x = c*self.tile_size + 200
                y = r*self.tile_size + 120

                pg.draw.rect(self.screen, color, [x,y,self.tile_size-2,self.tile_size-2])

                if (r,c) in self.player_tiles:
                    pg.draw.rect(self.screen, (255,255,255), [x,y,self.tile_size-2,self.tile_size-2], 3)

    def draw_buttons(self):

        for i, rect in enumerate(self.color_buttons):

            pg.draw.rect(self.screen, self.colors[i], rect)

        font = pg.font.Font('freesansbold.ttf', 24)
        text = font.render(f"Moves: {self.moves}", True, (255,255,255))
        self.screen.blit(text, (600, SCREEN_HEIGHT-70))
