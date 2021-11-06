import pygame
import sys
from random import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = int(SCREEN_WIDTH / 150)
EMPTY_TILE_COLOR = (25,25,25)
SAND_COLOR = (243,238,73)

UPDATEEVENT, t1 = pygame.USEREVENT + 1, 20 # create an event type that will get triggered every 500 ms

class FallingSand:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.tiles = []
        self.mouse_is_down = False

    def main_loop(self):
        self.init_tiles()
        pygame.time.set_timer(UPDATEEVENT, t1)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_is_down = True
                    self.handle_mouse_click(pygame.mouse.get_pos())

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_is_down = False

                # triggered every 500 ms
                if event.type == UPDATEEVENT:
                    self.update_tiles()

            if self.mouse_is_down:
                self.handle_mouse_click(pygame.mouse.get_pos())

            self.draw_tiles()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]: # escape to quit the game
                break

            pygame.display.update()

        pygame.quit()

    def init_tiles(self):
        """
        initialize all tiles to empty
        """
        tiles_across = int(SCREEN_WIDTH / TILE_SIZE)
        tiles_down = int(SCREEN_HEIGHT / TILE_SIZE)

        for i in range(tiles_down):
            row = []
            for j in range(tiles_across):
                row.append(EMPTY_TILE_COLOR)
            
            self.tiles.append(row)

    def draw_tiles(self):
        """
        draw tiles to the screen
        """
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                pygame.draw.rect(
                    self.screen,
                    self.tiles[i][j],
                    (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                )

    def update_tiles(self):
        """
        - If the tile below a sand tile is empty, move down
        - If it is already on the bottom of the screen don't move any more.
        - If the cell below a sand tile contains sand, but the space to the left or right of
          the already populated cell is empty, go there. If both left and right are free, choose
          one randomly.
        """
        # update from the bottom up
        for i in range(len(self.tiles) - 1, 0, -1):
            for j in range(len(self.tiles[i]) - 1, 0, -1):
                # don't update anything on the bottom row
                if i < len(self.tiles) - 1:
                    # case when cell below is empty
                    if self.tiles[i][j] == SAND_COLOR and self.tiles[i + 1][j] == EMPTY_TILE_COLOR:
                        self.tiles[i][j] = EMPTY_TILE_COLOR
                        self.tiles[i + 1][j] = SAND_COLOR

                    # case when tile below is sand and left and right are both empty
                    if self.tiles[i][j] == SAND_COLOR and self.tiles[i + 1][j - 1] == EMPTY_TILE_COLOR and self.tiles[i + 1][j + 1] == EMPTY_TILE_COLOR:
                        new_x_pos = j - 1 if random() >= 0.5 else j + 1 # randomly decide to move left or right
                        self.tiles[i][j] = EMPTY_TILE_COLOR
                        self.tiles[i + 1][new_x_pos] = SAND_COLOR

                    # case when only left is empty
                    if self.tiles[i][j] == SAND_COLOR and self.tiles[i + 1][j - 1] == EMPTY_TILE_COLOR:
                        self.tiles[i][j] = EMPTY_TILE_COLOR
                        self.tiles[i + 1][j - 1] = SAND_COLOR

                    # case when only right is empty
                    if self.tiles[i][j] == SAND_COLOR and self.tiles[i + 1][j + 1] == EMPTY_TILE_COLOR:
                        self.tiles[i][j] = EMPTY_TILE_COLOR
                        self.tiles[i + 1][j + 1] = SAND_COLOR

    def handle_mouse_click(self, pos):
        """
        Determine which tile the mouse clicked. If the tile is empty, fill it with sand,
        else leave it alone.

        Args:
            pos (tuple): x and y position of mouse click
        """
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                if pos[0] >= j * TILE_SIZE and pos[0] < j * TILE_SIZE + TILE_SIZE \
                    and pos[1] >= i * TILE_SIZE and pos[1] < i * TILE_SIZE + TILE_SIZE:
                    self.tiles[i][j] = SAND_COLOR

if __name__ == '__main__':
    fs = FallingSand()
    fs.main_loop()
    sys.exit()