#!/usr/bin/python2.7
# -*- coding: utf8 -*

from random import randint


sizex, sizey = 10, 10
nbMines = 10

hints = [[0 for x in range(sizex)] for y in range(sizey)]
field = [[0 for x in range(sizex)] for y in range(sizey)]


def fillMineField():

    minesLeftToPlace = nbMines

    while minesLeftToPlace > 0:
        randx, randy = randint(0, 9), randint(0, 9)
        currentCell = field[randx][randy]
        if currentCell == 1:
            pass
        else:
            field[randx][randy] = 1
            minesLeftToPlace = minesLeftToPlace - 1


def fillHints():

    for x in range(0, 10):
        for y in range(0, 10):
            if field[x][y] == 1:
                hints[x][y] = 'X'
            else:
                mineCount = 0
                if x > 0 and y > 0:
                    mineCount = mineCount + field[x-1][y-1]
                if x > 0:
                    mineCount = mineCount + field[x-1][y]
                if x > 0 and y < 9:
                    mineCount = mineCount + field[x-1][y+1]
                if y > 0:
                    mineCount = mineCount + field[x][y-1]
                if y < 9:
                    mineCount = mineCount + field[x][y+1]
                if x < 9 and y > 0:
                    mineCount = mineCount + field[x+1][y-1]
                if x < 9:
                    mineCount = mineCount + field[x+1][y]
                if x < 9 and y < 9:
                    mineCount = mineCount + field[x+1][y+1]

                hints[x][y] = mineCount


fillMineField()
fillHints()


# Dirty way of displaying the matrices for debug

print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in field]))
print "\n\n"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in hints]))
