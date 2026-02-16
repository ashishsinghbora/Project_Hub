import pygame
from src.environment import Environment

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ML Car Physics Simulation")

clock = pygame.time.Clock()

env = Environment(WIDTH, HEIGHT)

running = True
while running:
    clock.tick(60)

    accelerate = 0
    steer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        accelerate = 1
    if keys[pygame.K_DOWN]:
        accelerate = -1
    if keys[pygame.K_LEFT]:
        steer = -1
    if keys[pygame.K_RIGHT]:
        steer = 1

    env.update(accelerate, steer)

    if env.done:
        print("Collision detected. Resetting...")
        env.reset()

    env.draw(screen)
    pygame.display.flip()

pygame.quit()
