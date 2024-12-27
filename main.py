import pygame
import random
import math
from boid import Boid

# Setup
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Main loop
boids = [Boid(random.randint(100, 700), random.randint(100, 500)) for _ in range(50)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))

    for boid in boids:
        boid.flock(boids)
        boid.update()
        boid.edges()
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
