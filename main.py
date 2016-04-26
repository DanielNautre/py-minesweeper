#!/usr/bin/python2.7
# -*- coding: utf8 -*

from random import randint
from Tkinter import *

WIDTH = 400
HEIGHT = 400

sizeRow, sizeCol = 10, 10
nbMines = 10

hints = [[0 for x in range(sizeRow)] for y in range(sizeCol)]
field = [[0 for x in range(sizeRow)] for y in range(sizeCol)]


def fillMineField():

    minesLeftToPlace = nbMines

    while minesLeftToPlace > 0:
        randRow, randCol = randint(0, 9), randint(0, 9)
        currentCell = field[randRow][randCol]
        if currentCell == 1:
            pass
        else:
            field[randRow][randCol] = 1
            minesLeftToPlace = minesLeftToPlace - 1


def fillHints():

    for x in range(sizeRow):
        for y in range(sizeCol):
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

def createPlayfield():

    playfield = Canvas(window, width=WIDTH, height=HEIGHT)

    for x in range(sizeRow):
        for y in range(sizeCol):
            playfield.create_text(10 + (30 * x), 10 + (30 * y), text=hints[x][y])

    playfield.pack()


# Dirty way of displaying the matrices for debug

print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in field]))
print "\n\n"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in hints]))


window = Tk()

fillMineField()
fillHints()
createPlayfield()

window.mainloop()
