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
        self.createPlayfield()

    def createValues(self):
        """Generates the values used in the game """

        self.CELLSIZE = 30
        self.nbRow = 10 # height of the grid (Y): aka nb of Rows
        self.nbCol = 10 # width of the grid (X): aka nb of Cols
        self.nbMines = 10

        # Defines the height and width of the window based upon 
        # the grid size and the cell size
        self.WIDTH = (10 * 2) + (self.nbRow * self.CELLSIZE)
        self.HEIGHT = (10 * 2) + (self.nbCol * self.CELLSIZE) 

        #creates the various 2d arrays that will be used in teh game
        self.hints = [[0 for col in range(self.nbCol)] for row in range(self.nbRow)]
        self.field = [[0 for col in range(self.nbCol)] for row in range(self.nbRow)]
        self.cells = [[0 for col in range(self.nbCol)] for row in range(self.nbRow)]

    def fillMineField(self):
        """ This function randomoly generates n number of mines in the field"""
        minesLeftToPlace = self.nbMines

        while minesLeftToPlace > 0:
            randRow = randint(0, self.nbRow-1)
            randCol = randint(0, self.nbCol-1)
            currentCell = self.field[randRow][randCol]
            if currentCell == 1:
                pass
            else:
                self.field[randRow][randCol] = 1
                minesLeftToPlace = minesLeftToPlace - 1


    def fillHints(self):
        """ This function fills the hints array with the correct hint depending on the field array """

        for row in range(self.nbRow):
            for col in range(self.nbCol):

                # if there is a mine, show a "X" symbol
                if self.field[row][col] == 1:
                    self.hints[row][col] = 'X'
                else:
                    mineCount = 0
                    if col > 0 and row > 0:
                        mineCount = mineCount + self.field[row-1][col-1]
                    if col > 0:
                        mineCount = mineCount + self.field[row][col-1]
                    if col > 0 and row < (self.nbRow-1):
                        mineCount = mineCount + self.field[row+1][col-1]
                    if row > 0:
                        mineCount = mineCount + self.field[row-1][col]
                    if row < (self.nbRow-1):
                        mineCount = mineCount + self.field[row+1][col]
                    if col < (self.nbCol-1) and row > 0:
                        mineCount = mineCount + self.field[row-1][col+1]
                    if col < (self.nbCol-1):
                        mineCount = mineCount + self.field[row][col+1]
                    if col < (self.nbCol-1) and row < (self.nbRow-1):
                        mineCount = mineCount + self.field[row+1][col+1]

                    self.hints[row][col] = mineCount


    def activateCell(self, event):
        """this function reacts to the player "stepping" on a cell depeding on the presence or not of a mine"""

        cell = event.widget.find_closest(event.x, event.y)
        self.playfield.delete(cell)
        coords = self.getCoords(cell)
        cellValue = self.hints[coords[0]][coords[1]]
        if cellValue == "X":
            pass
            # Boum you're dead
        elif cellValue == 0:
            pass
            # reveal all open field in the vicinity
        else:
            pass

            
    def removeFlag(self, event):
        """ remove the flag that was right clicked """

        flag = event.widget.find_closest(event.x, event.y)
        self.playfield.delete(flag)

        # rebind the cell to placeFlag and activateCell
        cell = event.widget.find_closest(event.x, event.y)
        self.playfield.tag_bind(cell, '<ButtonPress-3>', self.placeFlag)       
        self.playfield.tag_bind(cell, '<ButtonPress-1>', self.activateCell)


    def placeFlag(self, event):
        """ if a cell is right clicked, place a flag 
        and block the cell from being activated"""

        cell = event.widget.find_closest(event.x, event.y)
        print cell

        #block player from placing a flag or clicking on the cell
        self.playfield.tag_unbind(cell, "<ButtonPress-1>")
        self.playfield.tag_unbind(cell, "<ButtonPress-3>")

        coords = self.playfield.coords(cell)
        flag = self.playfield.create_text(coords[0] + 15, coords[1] + 15, text="M")
        self.playfield.tag_bind(flag, '<ButtonPress-3>', self.removeFlag)



    def createPlayfield(self):
        """ This function creates the canvas for the playfield and populate it with thegrid, the hints and the buttons. """

        spacer = (self.CELLSIZE / 2)
        self.playfield = Tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT)

        for row in range(self.nbRow):
            for col in range(self.nbCol):
                
                # start position for the cells
                posX = 10 + (self.CELLSIZE * col)
                posY = 10 + (self.CELLSIZE * row)

                # end position for the cells
                posXbis = posX + self.CELLSIZE
                posYbis = posY + self.CELLSIZE
                
                # position grid
                self.playfield.create_rectangle(posX, posY, posXbis, posYbis)

                # position hints
                self.playfield.create_text(posX + spacer, posY + spacer, text=self.hints[row][col])
                
                # position "buttons"
                self.cells[row][col] = self.playfield.create_rectangle(posX, posY, posXbis, posYbis, fill="white")
                

                # bind mouse clicks on the playfield
                self.playfield.tag_bind(self.cells[row][col], '<ButtonPress-1>', self.activateCell)
                self.playfield.tag_bind(self.cells[row][col], '<ButtonPress-3>', self.placeFlag)

        self.playfield.pack()


    def getCoords(self, cell):
        """ Using the cell Tkinter id, find out it's X and Y value"""
        for row in range(self.nbRow):
            for col in range(self.nbCol):
                if self.cells[row][col] == cell[0]:
                    return [row, col]


if __name__ == "__main__":
    app = minesweeper(None)
    app.title('minesweeper')
    app.mainloop()        
