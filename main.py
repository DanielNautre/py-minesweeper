#!/usr/bin/python2.7
# -*- coding: utf8 -*

from random import randint


sizex, sizey = 10, 10
nbmines = 10

hints = [[0 for x in range(sizex)] for y in range(sizey)]
field = [[0 for x in range(sizex)] for y in range(sizey)]


def fillMineField():

    mineslefttoplace = nbmines
    print mineslefttoplace

    while mineslefttoplace > 0:
        randx, randy = randint(0, 9), randint(0, 9)
        currentcell = field[randx][randy]
        if currentcell == 1:
            pass
        else:
            field[randx][randy] = 1
            mineslefttoplace = mineslefttoplace - 1

fillMineField()
