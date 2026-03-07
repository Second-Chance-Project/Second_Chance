import random
import pygame as pg

from src.constants import *
from src.states.minigames.minigame import Minigame


class Filler(Minigame):
    def __init__(self):
        instructions = "Click colors to expand your territory. Capture more territory than the computer to win!"
        super().__init__(instructions)

        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        # Smaller board
        self.rows = 7
        self.cols = 9
        self.tile_size = 50  # slightly bigger tiles

        # Colors
        self.colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255)
        ]

        # Board and territories
        self.board = []
        self.player_tiles = set()
        self.computer_tiles = set()

        # Track last chosen colors
        self.player_last_color = None
        self.computer_last_color = None

        self.moves = 0
        self.max_moves = 15

        self.generate_board()
        self.create_color_buttons()

    def generate_board(self):
        """Creates a random colored grid and sets starting positions."""
        self.board = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(random.randint(0, len(self.colors)-1))
            self.board.append(row)

        # Player top-left, computer bottom-right
        self.player_tiles = {(0, 0)}
        self.computer_tiles = {(self.rows-1, self.cols-1)}

    def create_color_buttons(self):
        """Creates clickable color buttons."""
        self.color_buttons = []
        for i in range(len(self.colors)):
            rect = pg.Rect(100 + i*60, SCREEN_HEIGHT-80, 50, 50)
            self.color_buttons.append(rect)

    def flood_fill(self, new_color, tiles):
        """Expands territory using flood fill."""
        queue = list(tiles)
        while queue:
            r, c = queue.pop(0)
            neighbors = [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]
            for nr, nc in neighbors:
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if (nr,nc) not in tiles and self.board[nr][nc] == new_color:
                        tiles.add((nr,nc))
                        queue.append((nr,nc))

        for r,c in tiles:
            self.board[r][c] = new_color

    def computer_move(self):
        """Simple AI: pick a random neighboring color not used by player this turn."""
        neighboring_colors = set()
        for r, c in self.computer_tiles:
            for dr, dc in [(0,1),(1,0),(-1,0),(0,-1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    color = self.board[nr][nc]
                    if color != self.player_last_color and (nr,nc) not in self.computer_tiles:
                        neighboring_colors.add(color)
        if neighboring_colors:
            choice = random.choice(list(neighboring_colors))
            self.flood_fill(choice, self.computer_tiles)
            self.computer_last_color = choice

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.color_buttons):
                    if button.collidepoint(event.pos):
                        if i != self.computer_last_color:  # cannot pick computer's last color
                            self.flood_fill(i, self.player_tiles)
                            self.player_last_color = i
                            self.computer_move()
                            self.moves += 1

        # End game conditions
        total_tiles = len(self.player_tiles) + len(self.computer_tiles)
        if total_tiles == self.rows * self.cols or self.moves >= self.max_moves:
            self.won = len(self.player_tiles) > len(self.computer_tiles)

    def update(self, events):
        super().update(events)

    def draw(self):
        super().draw()
        self.draw_grid()
        self.draw_buttons()

    def draw_grid(self):
        """Draw the board and territory borders."""
        # Draw tiles
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.colors[self.board[r][c]]
                x = c * self.tile_size + 200
                y = r * self.tile_size + 120
                pg.draw.rect(self.screen, color, [x, y, self.tile_size, self.tile_size])

        # Draw borders following the territory shape
        self.draw_territory_border(self.player_tiles, (255, 255, 255))
        self.draw_territory_border(self.computer_tiles, (50, 50, 50))

    def draw_territory_border(self, tiles, border_color):
        """Draws a border around the outer edges of a set of tiles."""
        for r, c in tiles:
            x = c * self.tile_size + 200
            y = r * self.tile_size + 120
            # Check neighbors
            top = (r-1, c) not in tiles
            bottom = (r+1, c) not in tiles
            left = (r, c-1) not in tiles
            right = (r, c+1) not in tiles
            if top:
                pg.draw.line(self.screen, border_color, (x, y), (x+self.tile_size, y), 3)
            if bottom:
                pg.draw.line(self.screen, border_color, (x, y+self.tile_size), (x+self.tile_size, y+self.tile_size), 3)
            if left:
                pg.draw.line(self.screen, border_color, (x, y), (x, y+self.tile_size), 3)
            if right:
                pg.draw.line(self.screen, border_color, (x+self.tile_size, y), (x+self.tile_size, y+self.tile_size), 3)

    def draw_buttons(self):
        for i, rect in enumerate(self.color_buttons):
            pg.draw.rect(self.screen, self.colors[i], rect)
        font = pg.font.Font('freesansbold.ttf', 24)
        text = font.render(f"Moves: {self.moves}", True, (255, 255, 255))
        self.screen.blit(text, (600, SCREEN_HEIGHT-70))
