import pygame
from colors import Colors
from walls import create_wall_group
from pacman import PacMan
from food import create_grid
from grid import get_graph
from ghosts import Ghost
from heart import create_heart_group

# screen size
height = 440
width = 600

arrow_keys = [
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN,
]

# how many lifes does the player have
lifes = 3

# initial positions of all moving objects
pacman_init_pos = 13, 13
blinky_init_pos = 553, 13

# pygame initialization goes after this comment
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("PacMan")

# sprite + group initialization goes after this comment
all_sprites_group = pygame.sprite.RenderPlain()

player = PacMan(*pacman_init_pos, "./images/pacman", lifes)
pacman_group = pygame.sprite.RenderPlain()
pacman_group.add(player)
all_sprites_group.add(player)

blinky = Ghost(553, 13, "./images/ghosts", "blinky")
ghost_group = pygame.sprite.RenderPlain()
ghost_group.add(blinky)
all_sprites_group.add(blinky)

wall_group = create_wall_group(all_sprites_group)
food_group, nodes_grid = \
    create_grid(all_sprites_group, wall_group, pacman_group)

heart_group = create_heart_group(lifes, all_sprites_group)

graph = get_graph(nodes_grid)

running = True
while running:
    screen.fill(Colors.BLACK)
    pacman_group.draw(screen)
    wall_group.draw(screen)
    food_group.draw(screen)
    heart_group.draw(screen)
    ghost_group.draw(screen)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            # if X(close) button is pressed
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in arrow_keys:
                player.on_arrow_key_down(event.key)

    pygame.display.flip()
    player.update_position_and_velocity(
        wall_group, food_group, all_sprites_group)
    blinky.update_position_and_velocity(
        player.get_block_indices(), graph, nodes_grid)

    ghost_collide = pygame.sprite.spritecollide(player, ghost_group, False)
    if ghost_collide:
        player.on_ghost_collide(
            heart_group, pacman_init_pos,
            blinky_init_pos, blinky,
            all_sprites_group)
        if player.lifes == 0:
            running = False

    clock.tick(25)

pygame.quit()
