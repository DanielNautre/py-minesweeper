#!/usr/bin/python2.7
# -*- coding: utf8 -*


from random import randint
import Tkinter


class minesweeper(Tkinter.Tk):
    """minesweeper class"""

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.createValues()
        self.createInterface()

    def startGame(self):
        # make sure there is no existing mines in the field
        for row in range(self.nbRow):
            for col in range(self.nbCol):
                self.field[row][col] = 0

        # reset victory condition counter
        self.uncoveredCells = 0

        self.statusBar.config(text="")

        self.fillMineField()
        self.fillHints()

        if hasattr(self, 'playfield'):
            self.playfield.destroy()

        self.createPlayfield()

    def createInterface(self):
        """ Create the basic interface of the game """

        startBtn = Tkinter.Button(self, text="Start", command=self.startGame)
        self.statusBar = Tkinter.Label(self, text="", bd=1, relief=Tkinter.SUNKEN, anchor=Tkinter.W)
        self.statusBar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
        startBtn.pack()

    def createValues(self):
        """Generates the values used in the game """

        self.CELLSIZE = 32 + 2  # take width of the borders into account
        self.nbRow = 10  # height of the grid (Y): aka nb of Rows
        self.nbCol = 10  # width of the grid (X): aka nb of Cols
        self.nbMines = 15
        self.openCells = (self.nbCol * self.nbRow) - self.nbMines

        # Defines the height and width of the window based upon
        # the grid size and the cell size
        self.WIDTH = (10 * 2) + (self.nbRow * self.CELLSIZE)
        self.HEIGHT = (10 * 2) + (self.nbCol * self.CELLSIZE)

        # creates the various 2d arrays that will be used in teh game
        self.hints = [[0 for col in range(self.nbCol)] for row in range(self.nbRow)]
        self.field = [[0 for col in range(self.nbCol)] for row in range(self.nbRow)]
        self.cells = [[0 for col in range(self.nbCol)] for row in range(self.nbRow)]

    def loadImages(self):
        self.mineImg = Tkinter.PhotoImage(file="img/mine_placeholder.gif")
        self.flagImg = Tkinter.PhotoImage(file="img/flag_placeholder.gif")
        # self.boumImg = Tkinter.PhotoImage(file="img/boum_placeholder.gif")

    def fillMineField(self):
        """ This function randomoly generates n number of mines in the field"""
        minesLeftToPlace = self.nbMines

        print "A"

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
        """ This function fills the hints array with the correct hint
        depending on the field array """

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

    def getCellValue(self, row, col):
        return self.hints[row][col]

    def uncoverCell(self, row, col):
        """ uncover the cell sepcified by its coords
        and act depending on its content"""

        cellId = self.cells[row][col]
        if cellId == "O":
            return
        self.cells[row][col] = "O"
        self.playfield.delete(cellId)

        if "X" == self.getCellValue(row, col):
            self.statusBar.config(text="You're dead")
            return
            # Boum you're dead
        else:
            self.uncoveredCells = self.uncoveredCells + 1

            if self.uncoveredCells == self.openCells:
                self.statusBar.config(text="You Won")
                return
                # You won

            if 0 == self.getCellValue(row, col):
                # this recursively opens all adjacents empty cells
                if col > 0:
                    if row > 0:
                        self.uncoverCell(row-1, col-1)
                    if row < (self.nbRow-1):
                        self.uncoverCell(row+1, col-1)
                    self.uncoverCell(row, col-1)

                if col < (self.nbCol-1):
                    if row > 0:
                        self.uncoverCell(row-1, col+1)
                    if row < (self.nbRow-1):
                        self.uncoverCell(row+1, col+1)
                    self.uncoverCell(row, col+1)

                if row > 0:
                    self.uncoverCell(row-1, col)
                if row < (self.nbRow-1):
                    self.uncoverCell(row+1, col)

    def activateCell(self, event):
        """this function reacts to the player "stepping" on a cell
        depending on the presence or not of a mine"""

        cell = event.widget.find_closest(event.x, event.y)
        coords = self.getCoords(cell)

        self.uncoverCell(coords[0], coords[1])

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

        # block player from placing a flag or clicking on the cell
        self.playfield.tag_unbind(cell, "<ButtonPress-1>")
        self.playfield.tag_unbind(cell, "<ButtonPress-3>")

        spacer = (self.CELLSIZE / 2)
        coords = self.playfield.coords(cell)
        flag = self.playfield.create_image(coords[0] + spacer, coords[1] + spacer, image=self.flagImg)
        self.playfield.tag_bind(flag, '<ButtonPress-3>', self.removeFlag)

    def createPlayfield(self):
        """ This function creates the canvas for the playfield
        and populate it with thegrid, the hints and the buttons. """

        spacer = (self.CELLSIZE / 2)

        self.playfield = Tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        self.playfield.pack()

        self.loadImages()

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

                if self.hints[row][col] == "X":
                    self.playfield.create_image(posX + spacer, posY + spacer, image=self.mineImg)
                elif self.hints[row][col] != 0:
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
