import pygame
from colors import Colors


# sprite representing thin blue walls
class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        # create the rectangular image of the wall
        self.image = pygame.Surface((width, height))
        self.image.fill(Colors.BLUE)

        # set the coordinates of the rectangle
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


def create_wall_group(all_sprites_group):
    """
    Creates the walls, adds them to the all_sprites_group
    and returns their group
    """
    wall_group = pygame.sprite.RenderPlain()

    # parameters of all walls
    walls = [
        (7, 7, 6, 386),
        (587, 7, 6, 386),
        (7, 7, 586, 6),
        (7, 387, 586, 6),
        (47, 47, 6, 126),
        (47, 227, 6, 126),
        (547, 47, 6, 126),
        (547, 227, 6, 126),
        (87, 47, 126, 6),
        (247, 47, 106, 6),
        (387, 47, 126, 6),
        (87, 127, 126, 6),
        (247, 127, 106, 6),
        (387, 127, 126, 6),
        (87, 267, 126, 6),
        (247, 267, 106, 6),
        (387, 267, 126, 6),
        (87, 347, 126, 6),
        (247, 347, 106, 6),
        (387, 347, 126, 6),
        (47, 87, 246, 6),
        (327, 87, 226, 6),
        (47, 307, 226, 6),
        (307, 307, 246, 6),
        (47, 167, 126, 6),
        (427, 167, 126, 6),
        (47, 227, 126, 6),
        (427, 227, 126, 6),
        (207, 167, 6, 66),
        (387, 167, 6, 66),
        (247, 167, 106, 6),
        (247, 227, 106, 6)
    ]

    for item in walls:
        wall = Wall(*item)
        wall_group.add(wall)
        all_sprites_group.add(wall)

    return wall_group
