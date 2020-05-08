import pygame
import numpy as np
import time


pygame.init()

width, height = 600, 600
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

#cells state: live = 1, dead = 0

gameState = np.zeros((nxC, nyC))

gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

#Execution control
pauseExect = False

while True:

  newGameState = np.copy(gameState)

  screen.fill(bg)
  time.sleep(0.1)

  #Register mouse and keyboard event
  ev = pygame.event.get()

  for event in ev:

      if event.type == pygame.KEYDOWN:
          pauseExect = not pauseExect

      if event.type == pygame.QUIT:
          running = False
          pygame.display.quit()

      mouseClick = pygame.mouse.get_pressed()

      if sum(mouseClick) > 0:
          posX, posY = pygame.mouse.get_pos()
          celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
          newGameState[celX, celY] = 1  



  for y in range(0, nxC):
     for x in range(0, nyC):

        if not pauseExect:

             # calculate the number of neighbor
             n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                       gameState[(x)   % nxC, (y-1) % nyC] + \
                       gameState[(x+1) % nxC, (y-1) % nyC] + \
                       gameState[(x-1) % nxC, (y)   % nyC] + \
                       gameState[(x+1) % nxC, (y)   % nyC] + \
                       gameState[(x-1) % nxC, (y+1) % nyC] + \
                       gameState[(x)   % nxC, (y+1) % nyC] + \
                       gameState[(x+1) % nxC, (y+1) % nyC]

             # Rule #1 : a dead cell with 3 life cell near, come alive again
             if gameState[x, y] == 0 and n_neigh == 3:
                      newGameState[x, y] = 1

          # Rule #2  : a live cell with < 2 or > 3 live cells, come dead again
             elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                      newGameState[x, y] = 0

        # Create cells polygon to draw
        poly = [((x) * dimCW, y * dimCH),
               ((x+1) * dimCW, y * dimCH),
               ((x+1) * dimCW, (y+1) * dimCH),
               ((x)   * dimCW, (y+1) * dimCH)]

        # Draw cell for each pair of x, y
        if newGameState[x, y] == 0:
              pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
        else:
              pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

  gameState = np.copy(newGameState)
  pygame.display.flip()
