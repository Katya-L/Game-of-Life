import pygame
import sys
import numpy

HEIGHT = 100
WIDTH = 100
CELLSIZE = 5
FPS = 20

BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)

# BG = (244, 204, 112)
# BG_PAUSED = (236, 130, 66)
# CELL = (32, 148, 139)

BG = (154, 50, 205)
BG_PAUSED = (104, 34, 139)
CELL = (255, 215, 0)

BEGIN = frozenset([3])
STAY = frozenset([2, 3])
aliveList = set()
deadList = set()

but = 0
doMove = False
paused = True

field = numpy.array(numpy.zeros((HEIGHT, WIDTH)), dtype=numpy.int)
fieldBuffer = numpy.array(numpy.zeros((HEIGHT, WIDTH)), dtype=numpy.int)


def eventsProc():
    global doMove, but, paused
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            doMove = True
            if event.button == 1:
                but = 1
            elif event.button == 3:
                but = 3

        if event.type == pygame.MOUSEBUTTONUP:
            doMove = False

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION and doMove:
            xposs = event.pos[0] // CELLSIZE * CELLSIZE
            yposs = event.pos[1] // CELLSIZE * CELLSIZE

            if but == 1:
                field[int(yposs / CELLSIZE), int(xposs / CELLSIZE)] = 1
            elif but == 3:
                field[int(yposs / CELLSIZE), int(xposs / CELLSIZE)] = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:
                field.fill(0)

            if event.key == pygame.K_f and paused:
                step()


def draw():

    if paused:
        screen.fill(BG_PAUSED)
    else:
        screen.fill(BG)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if field[i][j]:
                pygame.draw.rect(screen, CELL, (j * CELLSIZE + 1, i * CELLSIZE + 1, CELLSIZE - 1, CELLSIZE - 1))

    pygame.display.update()


def norm(i, j):
    if i < 0:
        i += HEIGHT
    elif i >= HEIGHT:
        i -= HEIGHT

    if j < 0:
        j += WIDTH
    elif j >= WIDTH:
        j -= WIDTH

    return i, j


def getNeighbors(i, j):

    n = 0
    if field[norm(i - 1, j - 1)]:
        n += 1
    if field[norm(i, j - 1)]:
        n += 1
    if field[norm(i + 1, j - 1)]:
        n += 1
    if field[norm(i + 1, j)]:
        n += 1
    if field[norm(i + 1, j + 1)]:
        n += 1
    if field[norm(i, j + 1)]:
        n += 1
    if field[norm(i - 1, j + 1)]:
        n += 1
    if field[norm(i - 1, j)]:
        n += 1

    return n


def getDeadNeighbors(i, j):

    deadN = set()

    if not field[norm(i - 1, j - 1)]:
        deadN.add(norm(i - 1, j - 1))
    if not field[norm(i, j - 1)]:
        deadN.add(norm(i, j - 1))
    if not field[norm(i + 1, j - 1)]:
        deadN.add(norm(i + 1, j - 1))
    if not field[norm(i + 1, j)]:
        deadN.add(norm(i + 1, j))
    if not field[norm(i + 1, j + 1)]:
        deadN.add(norm(i + 1, j + 1))
    if not field[norm(i, j + 1)]:
        deadN.add(norm(i, j + 1))
    if not field[norm(i - 1, j + 1)]:
        deadN.add(norm(i - 1, j + 1))
    if not field[norm(i - 1, j)]:
        deadN.add(norm(i - 1, j))

    return deadN


def step():
    global field, deadList

    for i in range(HEIGHT):
        for j in range(WIDTH):

            if field[i][j]:
                aliveList.add((i, j))
                deadList = deadList.union(getDeadNeighbors(i, j))

    for cell in aliveList:

        i, j = cell[0], cell[1]
        n = getNeighbors(i, j)

        if n in STAY:
            fieldBuffer[i][j] = 1

    aliveList.clear()

    for cell in deadList:
        i, j = cell[0], cell[1]
        n = getNeighbors(i, j)

        if n in BEGIN:
            fieldBuffer[i][j] = 1

    deadList.clear()

    field = fieldBuffer.copy()
    fieldBuffer.fill(0)


pygame.init()
screen = pygame.display.set_mode((WIDTH * CELLSIZE, HEIGHT * CELLSIZE), pygame.DOUBLEBUF) # | pygame.OPENGL)
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

while True:

    eventsProc()
    draw()
    if not paused:
        step()
        clock.tick(FPS)
