import random
import pygame as pg

from src.constants import *
from src.states.minigames.minigame import Minigame


class Filler(Minigame):
    """Filler minigame: expand your territory and beat the computer."""

    def __init__(self):
        instructions = "Click colors to expand your territory. Capture 50% of the board to win!"
        super().__init__(instructions)  # Pass instructions to base class

        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.rows = 7
        self.cols = 9
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
        self.computer_tiles = set()
        self.moves = 0

        self.generate_board()
        self.create_color_buttons()

    def generate_board(self):
        """Creates a random colored grid and sets starting positions."""
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
        """Creates clickable color buttons at the bottom of the screen."""
        self.color_buttons = []
        for i in range(len(self.colors)):
            rect = pg.Rect(100 + i*60, SCREEN_HEIGHT-80, 50, 50)
            self.color_buttons.append(rect)

    def flood_fill(self, tiles, new_color):
        """Expands territory using flood fill."""
        queue = list(tiles)
        expanded = set(tiles)  # Copy so we can add new tiles
        while queue:
            r, c = queue.pop(0)
            for nr, nc in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if (nr,nc) not in expanded:
                        if self.board[nr][nc] == new_color:
                            expanded.add((nr,nc))
                            queue.append((nr,nc))
        for r,c in expanded:
            self.board[r][c] = new_color
        return expanded

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.color_buttons):
                    if button.collidepoint(event.pos):
                        # Prevent player from choosing computer's current color
                        comp_color = self.board[next(iter(self.computer_tiles))[0]][next(iter(self.computer_tiles))[1]]
                        if i == comp_color:
                            break
                        self.player_tiles = self.flood_fill(self.player_tiles, i)
                        self.moves += 1
                        # Computer move
                        self.computer_move()
                        self.check_win()

    def computer_move(self):
        """Simple AI: choose a random valid color adjacent to its territory."""
        comp_color = self.board[next(iter(self.computer_tiles))[0]][next(iter(self.computer_tiles))[1]]
        possible_colors = set()
        for r,c in self.computer_tiles:
            for nr, nc in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    color = self.board[nr][nc]
                    if color != comp_color and (nr,nc) not in self.computer_tiles and color != self.board[next(iter(self.player_tiles))[0]][next(iter(self.player_tiles))[1]]:
                        possible_colors.add(color)
        if possible_colors:
            choice = random.choice(list(possible_colors))
            self.computer_tiles = self.flood_fill(self.computer_tiles, choice)

    def check_win(self):
        """Check if either player or computer has won."""
        total_tiles = self.rows*self.cols
        if len(self.player_tiles) > total_tiles//2:
            self.won = True
        elif len(self.computer_tiles) >= total_tiles//2 or self.moves >= 15:
            self.won = False

    def update(self, events):
        super().update(events)

    def draw(self):
        """Draw grid, territories, and buttons."""
        self.screen.fill((0,0,0))
        self.draw_grid()
        self.draw_buttons()

    def draw_grid(self):
        """Draw tiles and border for territories."""
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.colors[self.board[r][c]]
                x = c*self.tile_size + 200
                y = r*self.tile_size + 120
                pg.draw.rect(self.screen, color, [x,y,self.tile_size,self.tile_size])

        # Draw border around player territory
        for r,c in self.player_tiles:
            x = c*self.tile_size + 200
            y = r*self.tile_size + 120
            pg.draw.rect(self.screen, (255,255,255), [x,y,self.tile_size,self.tile_size], 3)

        # Draw border around computer territory
        for r,c in self.computer_tiles:
            x = c*self.tile_size + 200
            y = r*self.tile_size + 120
            pg.draw.rect(self.screen, (0,0,0), [x,y,self.tile_size,self.tile_size], 3)

    def draw_buttons(self):
        """Draw color selection buttons and moves counter."""
        for i, rect in enumerate(self.color_buttons):
            pg.draw.rect(self.screen, self.colors[i], rect)

        font = pg.font.Font('freesansbold.ttf', 24)
        text = font.render(f"Moves: {self.moves}", True, (255,255,255))
        self.screen.blit(text, (600, SCREEN_HEIGHT-70))
