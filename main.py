#!/usr/bin/python2.7
# -*- coding: utf8 -*


from random import randint
import Tkinter


CELLSIZE = 30
sizeY, sizeX = 10, 10
nbMines = 10
WIDTH = (10 * 2) + (sizeY * CELLSIZE)
HEIGHT = (10 * 2) + (sizeX * CELLSIZE)


hints = [[0 for x in range(sizeX)] for y in range(sizeY)]
field = [[0 for x in range(sizeX)] for y in range(sizeY)]
cell = [[0 for x in range(sizeX)] for y in range(sizeY)]


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
                if x > 0 and y < (sizeY-1):
                    mineCount = mineCount + field[y+1][x-1]
                if y > 0:
                    mineCount = mineCount + field[y-1][x]
                if y < (sizeY-1):
                    mineCount = mineCount + field[y+1][x]
                if x < (sizeX-1) and y > 0:
                    mineCount = mineCount + field[y-1][x+1]
                if x < (sizeX-1):
                    mineCount = mineCount + field[y][x+1]
                if x < (sizeX-1) and y < (sizeY-1):
                    mineCount = mineCount + field[y+1][x+1]

                hints[y][x] = mineCount


def activateCell(event):
    cell = event.widget.find_closest(event.x, event.y)
    playfield.delete(cell)


def placeFlag(event):
    cell = event.widget.find_closest(event.x, event.y) 
    coords =  playfield.coords(cell)
    playfield.create_text(coords[0] + 15, coords[1] + 15, text="M")

def createPlayfield():

    for x in range(sizeY):
        for y in range(sizeX):
            posX = 10 + (CELLSIZE * x)
            posY = 10 + (CELLSIZE * y)
            playfield.create_text(posX + 15, posY + 15, text=hints[x][y])
            playfield.create_rectangle(posX, posY, posX + CELLSIZE, posY + CELLSIZE)
            cell[y][x] = playfield.create_rectangle(posX, posY, posX + CELLSIZE, posY + CELLSIZE, fill="white")
            playfield.tag_bind(cell[y][x], '<ButtonPress-1>', activateCell)
            playfield.tag_bind(cell[y][x], '<ButtonPress-3>', placeFlag)

    playfield.pack()


window = Tkinter.Tk()

fillMineField()
fillHints()

playfield = Tkinter.Canvas(window, width=WIDTH, height=HEIGHT)

createPlayfield()

window.mainloop()
