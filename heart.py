import pygame


# the life hearts displayed in the bottom of the screen
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/heart.png")

        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y
        self.x = x
        self.y = y


def create_heart_group(lifes, all_sprites):
    heart_group = pygame.sprite.RenderPlain()

    for i in range(lifes):
        x = 540 - i * 40
        y = 400
        heart = Heart(x, y)
        heart_group.add(heart)
        all_sprites.add(heart)

    return heart_group
