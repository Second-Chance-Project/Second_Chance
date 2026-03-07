import random
import pygame as pg

from src.constants import *
from src.states.minigames.minigame import Minigame, Timer


class Filler(Minigame):
    def __init__(self):
        instructions = "Click colors to expand your territory. Capture 50% of the board to win!"
        super().__init__(instructions)

        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        # Board settings
        self.rows = 7
        self.cols = 9
        self.tile_size = 40

        # Colors for the tiles
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
        self.computer_tiles = set()
        self.moves = 0

        # Tracks last color used by each player to avoid collisions
        self.player_last_color = -1
        self.computer_last_color = -1

        # Generate board and setup starting positions
        self.generate_board()
        self.create_color_buttons()

    def generate_board(self):
        """Creates a random colored grid and sets starting tiles."""
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(random.randint(0, len(self.colors)-1))
            self.board.append(row)

        # Player starts top-left
        self.player_tiles.add((0, 0))
        # Computer starts bottom-right
        self.computer_tiles.add((self.rows-1, self.cols-1))

    def create_color_buttons(self):
        """Creates clickable color buttons."""
        self.color_buttons = []
        for i in range(len(self.colors)):
            rect = pg.Rect(100 + i*60, SCREEN_HEIGHT-80, 50, 50)
            self.color_buttons.append(rect)

    def flood_fill(self, new_color, tiles):
        """Expands territory using flood fill for given tile set."""
        queue = list(tiles)
        while queue:
            r, c = queue.pop(0)
            neighbors = [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]
            for nr, nc in neighbors:
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if (nr, nc) not in tiles:
                        if self.board[nr][nc] == new_color:
                            tiles.add((nr, nc))
                            queue.append((nr, nc))

        # Update board color for all tiles
        for r, c in tiles:
            self.board[r][c] = new_color

        self.moves += 1

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.color_buttons):
                    if button.collidepoint(event.pos) and i != self.computer_last_color:
                        self.player_last_color = i
                        self.flood_fill(i, self.player_tiles)
                        # Computer takes a turn immediately after
                        self.computer_turn()

        # Check win/lose conditions
        total_tiles = self.rows * self.cols
        if len(self.player_tiles) > total_tiles // 2:
            self.won = True
        elif len(self.computer_tiles) > total_tiles // 2:
            self.won = False
        elif self.moves > 15:  # Optional move limit
            self.won = len(self.player_tiles) > len(self.computer_tiles)

    def computer_turn(self):
        """Computer chooses a random valid color to expand."""
        possible_colors = set()
        for r, c in self.computer_tiles:
            neighbors = [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]
            for nr, nc in neighbors:
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    color = self.board[nr][nc]
                    if color != self.computer_last_color and color != self.player_last_color:
                        possible_colors.add(color)
        if possible_colors:
            choice = random.choice(list(possible_colors))
            self.computer_last_color = choice
            self.flood_fill(choice, self.computer_tiles)

    def update(self, events):
        super().update(events)

    def draw(self):
        super().draw()  # Draw background + instructions if still showing
        self.draw_grid()
        self.draw_buttons()

    def draw_grid(self):
        """Draw the board and highlight territories."""
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.colors[self.board[r][c]]
                x = c * self.tile_size + 200
                y = r * self.tile_size + 120
                pg.draw.rect(self.screen, color, [x, y, self.tile_size, self.tile_size])

                # Draw border for player and computer
                if (r,c) in self.player_tiles:
                    pg.draw.rect(self.screen, (255,255,255), [x, y, self.tile_size, self.tile_size], 3)
                elif (r,c) in self.computer_tiles:
                    pg.draw.rect(self.screen, (0,0,0), [x, y, self.tile_size, self.tile_size], 3)

    def draw_buttons(self):
        for i, rect in enumerate(self.color_buttons):
            pg.draw.rect(self.screen, self.colors[i], rect)
        # Show moves only (optional)
        font = pg.font.Font('freesansbold.ttf', 24)
        text = font.render(f"Moves: {self.moves}", True, (255,255,255))
        self.screen.blit(text, (600, SCREEN_HEIGHT-70))
