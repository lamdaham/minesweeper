"""Gameboard where...
-1: mine
 f: flagged empty spot
 F: flagged mine
0-5: number of surrounding mines
None: uncovered spot
"""

import random

def myprint(array):
    print("  0 1 2 3 4 5 6 7 8")
    n = 0
    for li in array:
        row = str(n) + " "
        n += 1
        for elem in li:
            if elem == None:
                row += "?"
            elif elem == "f":
                row += "F"
            elif elem == -1:
                row += "M" if MODE=="admin" else "?"
            else:
                row += str(elem)
            row += " "
        print(row)

def create_board(width, height):
    gameboard = []
    for i in range(height):
        gameboard.append([None]*width)
    return gameboard
    
def bury_mines(gameboard, n, x, y):
    minenum = 0
    while minenum < n:
        mine_row = random.randint(0, (len(gameboard)-1))
        mine_column = random.randint(0, (len(gameboard)-1))
        CurrentRow = gameboard[mine_row]
        if not CurrentRow[mine_column] == -1:
            CurrentRow[mine_column] = -1
            minenum += 1
            checkleft = 0 < x 
            checkup = 0 < y 
            checkright = x < len(gameboard[0]) - 1
            checkdown = y < len(gameboard) - 1
            if gameboard[y][x] == -1:
                gameboard[y][x] = None
                minenum -= 1
            if checkleft and checkdown and gameboard[y+1][x-1] == -1 or checkleft and checkdown and gameboard[y+1][x-1] == "F":
                gameboard[y+1][x-1] = None
                minenum -= 1
            if checkleft and gameboard[y][x-1] == -1 or checkleft and gameboard[y][x-1] == "F":
                gameboard[y][x-1] = None
                minenum -=1
            if checkup and checkleft and gameboard[y-1][x-1] == -1 or checkup and checkleft and gameboard[y-1][x-1] == "F":
                gameboard[y-1][x-1] = None
                minenum -=1
            if checkdown and gameboard[y+1][x] == -1 or checkdown and gameboard[y+1][x] == "F":
                gameboard[y+1][x] = None
                minenum -=1
            if checkup and gameboard[y-1][x] == -1 or checkup and gameboard[y-1][x] == "F":
                gameboard[y-1][x] = None
                minenum -=1
            if checkup and checkright and gameboard[y-1][x+1] == -1 or checkup and checkright and gameboard[y-1][x+1] == "F":
                gameboard[y-1][x+1] = None
                minenum -=1
            if checkright and gameboard[y][x+1] == -1 or checkright and gameboard[y][x+1] == "F":
                gameboard[y][x+1] = None
                minenum -= 1
            if checkdown and checkright and gameboard[y+1][x+1] == -1 or checkdown and checkright and gameboard[y+1][x+1] == "F":
                gameboard[y+1][x+1] = None
                minenum -= 1

def get_mine_count(gameboard, x, y):
    minecount = 0
    checkleft = 0 < x 
    checkup = 0 < y 
    checkright = x < len(gameboard[0]) - 1
    checkdown = y < len(gameboard) - 1
    if checkleft and checkdown and gameboard[y+1][x-1] == -1 or checkleft and checkdown and gameboard[y+1][x-1] == "F":
        minecount +=1
    if checkleft and gameboard[y][x-1] == -1 or checkleft and gameboard[y][x-1] == "F":
        minecount +=1
    if checkup and checkleft and gameboard[y-1][x-1] == -1 or checkup and checkleft and gameboard[y-1][x-1] == "F":
        minecount +=1
    if checkdown and gameboard[y+1][x] == -1 or checkdown and gameboard[y+1][x] == "F":
        minecount +=1
    if checkup and gameboard[y-1][x] == -1 or checkup and gameboard[y-1][x] == "F":
        minecount +=1
    if checkup and checkright and gameboard[y-1][x+1] == -1 or checkup and checkright and gameboard[y-1][x+1] == "F":
        minecount +=1
    if checkright and gameboard[y][x+1] == -1 or checkright and gameboard[y][x+1] == "F":
        minecount +=1
    if checkdown and checkright and gameboard[y+1][x+1] == -1 or checkdown and checkright and gameboard[y+1][x+1] == "F":
        minecount +=1
    return minecount

def uncover_board(gameboard, x, y):
    if gameboard [y][x] == None:
        if get_mine_count(gameboard, x, y) == 0:
            checkleft = 0 < x 
            checkup = 0 < y 
            checkright = x < len(gameboard[0]) - 1
            checkdown = y < len(gameboard) - 1
            gameboard[y][x] = 0
            if checkleft and checkdown:
                uncover_board(gameboard, x-1, y+1)
            if checkleft:
                uncover_board(gameboard, x-1, y)
            if checkup and checkleft:
                uncover_board(gameboard, x-1, y-1)
            if checkdown:
                uncover_board(gameboard, x, y+1)
            if checkup:
                uncover_board(gameboard, x, y-1)
            if checkup and checkright:
                uncover_board(gameboard, x+1, y-1)
            if checkright:
                uncover_board(gameboard, x+1, y)
            if checkdown and checkright:
                uncover_board(gameboard, x+1, y+1)
        else:
            gameboard[y][x] = get_mine_count(gameboard, x, y)
           
class Game:
    def __init__(self):
        self.gameboard = create_board(9, 9)
        self.flagged_mines = 0
        self.unflagged_mines = []
        self.original = {}
        self.gameover = False
        self.first_uncover = True
    def Flag(self, x, y):
        if self.gameboard[y][x] != "f" and self.gameboard[y][x] != "F":
            self.original[(x,y)] = self.gameboard[y][x]
            if self.gameboard[y][x] == -1:
                self.gameboard[y][x] = "F"
                self.flagged_mines += 1
            else:
                self.gameboard[y][x] = "f"
        else:
            self.unflagged_mines.append(y)
            self.gameboard[y][x] = self.original[(x,y)]
        myprint(self.gameboard)
    def uncover(self, x, y):
        Cell = self.gameboard[y][x]
        if Cell == -1:
            print("game over")
            return True
        else:
            uncover_board(self.gameboard, x, y)
            myprint(self.gameboard)
            return False
    
    def run(self):
        while not self.gameover:
            x = int(input("X of Spot: "))
            y = int(input("Y of Spot: "))
            choice = input("uncover or flag: ")
            if choice == "uncover":
                if self.first_uncover:
                    bury_mines(self.gameboard, 10, x, y)
                    self.first_uncover = False
                self.gameover = self.uncover(x, y)
            else:
                self.Flag(x, y)
            
            if self.flagged_mines == 10:
                print("yay")
                self.gameover = True

MODE = input("Mode: ")
game = Game()
game.run()