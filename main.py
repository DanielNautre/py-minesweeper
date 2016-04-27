#!/usr/bin/python2.7
# -*- coding: utf8 -*

from random import randint
from Tkinter import *

WIDTH = 400
HEIGHT = 400

sizeY, sizeX = 10, 10
nbMines = 20

hints = [[0 for x in range(sizeX)] for y in range(sizeY)]
field = [[0 for x in range(sizeX)] for y in range(sizeY)]

print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in field]))
print "\n\n"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in hints]))

def fillMineField():

    minesLeftToPlace = nbMines

    while minesLeftToPlace > 0:
        randY, randX = randint(0, sizeY-1), randint(0, sizeX-1)
        currentCell = field[randY][randX]
        if currentCell == 1:
            pass
        else:
            field[randY][randX] = 1
            minesLeftToPlace = minesLeftToPlace - 1


def fillHints():

    for y in range(sizeY):
        for x in range(sizeX):
            if field[y][x] == 1:
                hints[y][x] = 'X'
            else:
                mineCount = 0
                if x > 0 and y > 0:
                    mineCount = mineCount + field[y-1][x-1]
                if x > 0:
                    mineCount = mineCount + field[y][x-1]
                if x > 0 and y < (sizeY-2):
                    mineCount = mineCount + field[y+1][x-1]
                if y > 0:
                    mineCount = mineCount + field[y-1][x]
                if y < (sizeY-2):
                    mineCount = mineCount + field[y+1][x]
                if x < (sizeX-2) and y > 0:
                    mineCount = mineCount + field[y-1][x+1]
                if x < (sizeX-2):
                    mineCount = mineCount + field[y][x+1]
                if x < (sizeX-2) and y < (sizeY-2):
                    mineCount = mineCount + field[y+1][x+1]

                hints[y][x] = mineCount


def createPlayfield():

    playfield = Canvas(window, width=WIDTH, height=HEIGHT)

    for x in range(sizeY):
        for y in range(sizeX):
            playfield.create_text(10 + (30 * x), 10 + (30 * y), text=hints[x][y])

    playfield.pack()





window = Tk()

fillMineField()
fillHints()
createPlayfield()

# Dirty way of displaying the matrices for debug

print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in field]))
print "\n\n"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in hints]))

window.mainloop()
