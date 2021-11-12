import pygame
import os


class PacMan(pygame.sprite.Sprite):

    def __init__(self, x, y, image_dir, lifes, speed=5):
        pygame.sprite.Sprite.__init__(self)

        dirs = ['r', 'l', 'u', 'd']
        self.images = {
            x: pygame.image.load(os.path.join(image_dir, x+'.png')).
            convert() for x in dirs
        }
        self.image = self.images['r']

        # set the coordinates
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.x = x
        self.y = y

        self.lifes = lifes

        # set the velocity dictionary
        self.velocities = {
            's': (0, 0),  # stopped
            'l': (-speed, 0),  # left
            'r': (speed, 0),  # right
            'u': (0, -speed),  # up
            'd': (0, speed)  # down
        }

        # defining the velocity direction
        self.direction = 's'  # stopped initially
        # if next_direction is not None,
        # will change direction whenever possible
        self.next_direction = None

    def update_position_and_velocity(self, walls, foods, all_sprites):
        """
        Updates the position according to the
        current velocity direction of the player.
        If there is a collision with the walls, reverts the changes
        """
        changed = False
        prev_dir = self.direction
        if self.next_direction is not None and (self.rect.top + 7) % 20 == 0 \
                and (self.rect.left + 7) % 20 == 0:
            changed = True
            self._change_direction()

        v = self.velocities[self.direction]
        self._add_to_coordinates(v)

        wall_collide = pygame.sprite.spritecollide(self, walls, False)

        if wall_collide:
            self._add_to_coordinates((-v[0], -v[1]))
            if changed:
                self.next_direction = prev_dir
                self._change_direction()
                self.update_position_and_velocity(walls, foods, all_sprites)
            else:
                self.direction = 's'

        food_collide = pygame.sprite.spritecollide(self, foods, False)
        if len(food_collide) > 0:
            foods.remove(food_collide[0])
            all_sprites.remove(food_collide[0])

    def on_ghost_collide(
            self, hearts, init_pos,
            blinky_init_pos, blinky, all_sprites):
        self.lifes -= 1
        all_sprites.remove(hearts.sprites()[-1])
        hearts.remove(hearts.sprites()[-1])

        self._set_coordinate_to(self, init_pos)
        self._set_coordinate_to(blinky, blinky_init_pos)

    def on_arrow_key_down(self, key):
        if key == pygame.K_LEFT:
            self._set_next_direction('l')
        elif key == pygame.K_RIGHT:
            self._set_next_direction('r')
        elif key == pygame.K_UP:
            self._set_next_direction('u')
        elif key == pygame.K_DOWN:
            self._set_next_direction('d')

    def get_block_indices(self):
        """
        :return: (i, j) indicating the closest grid block of the player
        """
        x_center = self.x + 17
        y_center = self.y + 17
        return y_center // 20, x_center // 20

    def _set_next_direction(self, direction):
        """
        :param direction: 'l', 'r', 'u', 'd' or 's'(stopped)
        """
        if direction in self.velocities.keys():
            self.next_direction = direction
        else:
            raise ValueError("invalid direction is passed")

    def _change_direction(self):
        self.direction = self.next_direction
        self.next_direction = None
        if self.direction != 's':
            self.image = self.images[self.direction]

    def _add_to_coordinates(self, v):
        self.x += v[0]
        self.y += v[1]
        self.rect.top = self.y
        self.rect.left = self.x

    @staticmethod
    def _set_coordinate_to(sprite, position):
        sprite.x = position[0]
        sprite.y = position[1]
        sprite.rect.top = sprite.y
        sprite.rect.left = sprite.x
