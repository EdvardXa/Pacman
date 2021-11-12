import pygame
import os
from grid import a_star_search


class Ghost(pygame.sprite.Sprite):

    def __init__(self, x, y, image_dir, name, speed=4):
        pygame.sprite.Sprite.__init__(self)

        path = os.path.join(image_dir, (name + '.png'))
        self.image = pygame.image.load(path)

        # set the coordinates
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.x = x
        self.y = y

        # set the velocity dictionary
        self.velocities = {
            'l': (-speed, 0),  # left
            'r': (speed, 0),  # right
            'u': (0, -speed),  # up
            'd': (0, speed)  # down
        }

        # the direction, will be determined later
        self.direction = None

    def update_position_and_velocity(self, pacmans_block, graph, grid):
        """
        Updates the position according to the
        current velocity direction of the ghost.
        If it is in the center of a block, determines a new shortest path to
        pacman and changes its direction to there
        """
        if self.direction is None or ((self.rect.top + 7) % 20 == 0
                                      and (self.rect.left + 7) % 20 == 0):
            i = (self.rect.top + 7) // 20
            j = (self.rect.left + 7) // 20
            self.direction = a_star_search(graph, (i, j), pacmans_block, grid)

        v = self.velocities[self.direction]
        self._add_to_coordinates(v)

    def _add_to_coordinates(self, v):
        self.x += v[0]
        self.y += v[1]
        self.rect.top = self.y
        self.rect.left = self.x
