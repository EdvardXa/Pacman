import pygame
from colors import Colors


class Food(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((4, 4))

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        pygame.draw.ellipse(self.image, Colors.YELLOW, self.image.get_rect())


def create_grid(all_sprite_group, walls, pacman):
    """
    Creates the grid of food block and the 20x30 grid as a list of list, where
    the value is zero if there is a wall at that block, 1 otherwise
    """
    food_sprite_group = pygame.sprite.RenderPlain()
    nodes_grid = [[] for _ in range(20)]
    for i in range(30):
        for j in range(20):
            x = i * 20 + 8
            y = j * 20 + 8
            block = Food(x, y)

            wall_collide = pygame.sprite.spritecollide(block, walls, False)
            pacman_collide = pygame.sprite.spritecollide(block, pacman, False)
            if wall_collide:
                nodes_grid[j].append(0)
            else:
                nodes_grid[j].append(1)
            if wall_collide or pacman_collide:
                continue
            all_sprite_group.add(block)
            food_sprite_group.add(block)

    return food_sprite_group, nodes_grid
