#!/usr/bin/python2.7
# -*- coding: utf8 -*


from random import randint
import Tkinter

class minesweeper(Tkinter.Tk):
    """minesweeper class"""

    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):

        self.createValues()
        self.fillMineField()
        self.fillHints()
        self.playfield = Tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        self.createPlayfield()

    def createValues(self):
        self.CELLSIZE = 30
        self.sizeY = 10 # height
        self.sizeX = 10 # width
        self.nbMines = 10
        self.WIDTH = (10 * 2) + (self.sizeY * self.CELLSIZE)
        self.HEIGHT = (10 * 2) + (self.sizeX * self.CELLSIZE) 

        self.hints = [[0 for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.field = [[0 for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.cells = [[0 for x in range(self.sizeX)] for y in range(self.sizeY)]

    def fillMineField(self):

        minesLeftToPlace = self.nbMines

        while minesLeftToPlace > 0:
            randY, randX = randint(0, self.sizeY-1), randint(0, self.sizeX-1)
            currentCell = self.field[randY][randX]
            if currentCell == 1:
                pass
            else:
                self.field[randY][randX] = 1
                minesLeftToPlace = minesLeftToPlace - 1


    def fillHints(self):

        for y in range(self.sizeY):
            for x in range(self.sizeX):
                if self.field[y][x] == 1:
                    self.hints[y][x] = 'X'
                else:
                    mineCount = 0
                    if x > 0 and y > 0:
                        mineCount = mineCount + self.field[y-1][x-1]
                    if x > 0:
                        mineCount = mineCount + self.field[y][x-1]
                    if x > 0 and y < (self.sizeY-1):
                        mineCount = mineCount + self.field[y+1][x-1]
                    if y > 0:
                        mineCount = mineCount + self.field[y-1][x]
                    if y < (self.sizeY-1):
                        mineCount = mineCount + self.field[y+1][x]
                    if x < (self.sizeX-1) and y > 0:
                        mineCount = mineCount + self.field[y-1][x+1]
                    if x < (self.sizeX-1):
                        mineCount = mineCount + self.field[y][x+1]
                    if x < (self.sizeX-1) and y < (self.sizeY-1):
                        mineCount = mineCount + self.field[y+1][x+1]

                    self.hints[y][x] = mineCount


    def activateCell(self, event):
        cell = event.widget.find_closest(event.x, event.y)
        self.playfield.delete(cell)
        coords = self.getCoords(cell)
        cellValue = self.hints[coords[1]][coords[0]]
        if cellValue == "X":
            pass
            # Boum you're dead
        elif cellValue == 0:
            pass
            # reveal all open field
        else
            pass
            

    def placeFlag(self,event):
        cell = event.widget.find_closest(event.x, event.y)
        coords = self.playfield.coords(cell)
        self.playfield.create_text(coords[0] + 15, coords[1] + 15, text="M")


    def createPlayfield(self):

        spacer = (self.CELLSIZE / 2)

        for x in range(self.sizeY):
            for y in range(self.sizeX):
                posX = 10 + (self.CELLSIZE * x)
                posY = 10 + (self.CELLSIZE * y)
                self.playfield.create_text(posX + spacer, posY + spacer, text=self.hints[x][y])
                self.playfield.create_rectangle(posX, posY, posX + self.CELLSIZE, posY + self.CELLSIZE)
                self.cells[y][x] = self.playfield.create_rectangle(posX, posY, posX + self.CELLSIZE, posY + self.CELLSIZE, fill="white")
                self.playfield.tag_bind(self.cells[y][x], '<ButtonPress-1>', self.activateCell)
                self.playfield.tag_bind(self.cells[y][x], '<ButtonPress-3>', self.placeFlag)

        self.playfield.pack()

    def getCoords(self, cell):
        for x in range(self.sizeY):
            for y in range(self.sizeX):
                if self.cells[y][x] == cell[0]:
                    return [x, y]


if __name__ == "__main__":
    app = minesweeper(None)
    app.title('minesweeper')
    app.mainloop()        
