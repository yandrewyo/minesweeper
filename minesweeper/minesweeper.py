from graphics import *;
from random import *
import numpy as np

window = GraphWin("Window", 500, 600)
window.setBackground("white")
grid = []
mines = []
numbers = []
flag = False
playing = True
flags = []

flagBtn = Rectangle(Point(400, 25), Point(500, 50))
flagBtn.draw(window)
flagTxt = Text(flagBtn.getCenter(), "Digging")
flagTxt.setFill("red")
flagTxt.draw(window)

for i in range(100, 600, 50):
    grid.append([])
    for j in range(0, 500, 50):
        grid[int((i-100)/50)].append(Rectangle(Point(j, i), Point(j+50, i+50)))
        grid[int((i-100)/50)][int(j/50)].draw(window)

for i in range(len(grid)):
    flags.append([])
    for j in grid[i]:
        flags[i].append(False)

def start(point):
    if point:
        for i in grid:
            for j in i:
                boxX1 = j.getP1().getX()
                boxY1 = j.getP1().getY()
                boxX2 = j.getP2().getX()
                boxY2 = j.getP2().getY()
                clickX = point.getX()
                clickY = point.getY()
                if boxX1 < clickX and clickX < boxX2 and boxY1 < clickY and clickY < boxY2:
                    j.setFill("blue")
                    createMines((grid.index(i), i.index(j)))
    global started
    started = True

def createMines(start):
    x = start[0] #i
    y = start[1] #j
    possibleMineLocations = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i <= x-2 or i >= x+2 or j <= y-2 or j >= y+2:
                possibleMineLocations.append(grid[i][j])
    for i in range(15):
        mines.append(possibleMineLocations.pop(randint(0, len(possibleMineLocations)-1)))
        #mines[i].setFill("red")
    createNumbers(mines,start)

def createNumbers(mines, start):
    global numbers
    copy = np.array(grid)
    copy = np.pad(copy, 1)
    for i in range(1,len(copy)-1):
        for j in range(1,len(copy[i])-1):
            if copy[i][j] not in mines:
                count = 0
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if copy[k][l] in mines:
                            count += 1
                num = Text(copy[i][j].getCenter(), str(count))
                numbers.append(num)
                #num.draw(window)
            else:
                num = Text(copy[i][j].getCenter(), "-1")
                numbers.append(num)
                #num.draw(window)
    numbers = np.pad(np.array(numbers).reshape(10,10),1,'constant',constant_values=(Text(Point(0,0), "1")))
    idk(numbers, [start], [], [])

def idk(numbers, points, opened, opened_index):
    new_points = points.copy()
    test = []
    for i in range(len(numbers)):
        test.append([])
        for j in range(len(numbers[i])):
            test[i].append(numbers[i][j].getText())
    for i in points:
        adjacent = []
        #adjacent.append((i[0]-1,i[1]))
        #adjacent.append((i[0],i[1]-1))
        #adjacent.append((i[0]+1,i[1]))
        #adjacent.append((i[0],i[1]+1))
        for j in range(i[0]-1, i[0]+2):
            for k in range(i[1]-1, i[1]+2):
                adjacent.append((j,k))
        for j in adjacent:
            if j not in points:
                if test[j[0]+1][j[1]+1] == '0':
                    new_points.append(j)
                    grid[j[0]][j[1]].setFill("blue")
                    opened_index.append((j[0],j[1]))
                    opened.append(grid[j[0]][j[1]])
    if len(new_points) == len(points):
        for i in range(len(opened_index)):
            for j in range(opened_index[i][0]-1, opened_index[i][0]+2):
                for k in range(opened_index[i][1]-1, opened_index[i][1]+2):
                    if 0 <= j and j < len(grid) and 0 <= k and k < len(grid):
                        if grid[j][k] not in opened:
                            try:
                                if numbers[j+1][k+1].getText() != "0":
                                    numbers[j+1][k+1].draw(window)
                                grid[j][k].setFill("blue")
                            except:
                                "nothing"
        return new_points
    else:
        return idk(numbers, new_points, opened, opened_index)

def placeFlag(box):
    if not flags[box[0]][box[1]]:
        flags[box[0]][box[1]] = True
        grid[box[0]][box[1]].setFill("green")
    else:
        flags[box[0]][box[1]] = False
        grid[box[0]][box[1]].setFill("white")

def click(point):
    box = False
    global flag
    global flagTxt
    if point:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                boxX1 = grid[i][j].getP1().getX()
                boxY1 = grid[i][j].getP1().getY()
                boxX2 = grid[i][j].getP2().getX()
                boxY2 = grid[i][j].getP2().getY()
                clickX = point.getX()
                clickY = point.getY()
                if boxX1 < clickX and clickX < boxX2 and boxY1 < clickY and clickY < boxY2:
                    if not flag:
                        box = True
                        if grid[i][j] in mines:
                            if not flags[i][j]:
                                for k in mines:
                                    k.setFill("red")
                                    global playing
                                    playing = False
                        else:
                            if numbers[i+1][j+1].getText() == "0":
                                idk(numbers, [(i,j)],[], [])
                                numbers[i+1][j+1].undraw()
                            else:
                                try:
                                    numbers[i+1][j+1].draw(window)
                                    grid[i][j].setFill("blue")
                                except:
                                    "nothing"
                    else:
                        placeFlag((i,j))
                        flag = False
                        flagTxt.setText("Digging")
        if not box:
            boxX1 = flagBtn.getP1().getX()
            boxY1 = flagBtn.getP1().getY()
            boxX2 = flagBtn.getP2().getX()
            boxY2 = flagBtn.getP2().getY()
            clickX = point.getX()
            clickY = point.getY()
            if boxX1 < clickX and clickX < boxX2 and boxY1 < clickY and clickY < boxY2:
                flag = True
                flagTxt.setText("Placing/Removing Flag")

started = False
while playing:
    if not started:
        start(window.getMouse())
    else:
        click(window.getMouse())
