import __main__
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        quit()
  #draw all our elements
  #update everything
  pygame.display.update()