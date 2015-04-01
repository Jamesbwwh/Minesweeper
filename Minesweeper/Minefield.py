import random

def generate(difficulty):
    mineField = printMineField(difficulty)
    height = len(mineField)
    width = len(mineField[0])
    ranges = width * height
    mines = random.randint(ranges // 8, ranges // 7)
    # mines = 4; # comment or remove this line.  for testing only.
    print "Difficulty: ", difficulty, "Mines: ", mines, "Height: ", height, "Width: ", width

    ranges -= 1
    for mine in range(mines):
        while(True):
            placeMine = random.randint(0, ranges)
            x = placeMine // width
            y = placeMine % width
            if mineField[x][y] != 9:
                mineField[x][y] = 9
                if x - 1 >= 0: #Top
                    if y - 1 >= 0: #Top-Left
                        if mineField[x - 1][y - 1] != 9:
                            mineField[x - 1][y - 1] += 1
                    if mineField[x - 1][y] != 9:
                        mineField[x - 1][y] += 1
                    if y + 1 < width: #Top-Right
                        if mineField[x - 1][y + 1] != 9:
                            mineField[x - 1][y + 1] += 1
                if y - 1 >= 0: #Left
                    if mineField[x][y - 1] != 9:
                        mineField[x][y - 1] += 1
                if y + 1 < width: #Right
                    if mineField[x][y + 1] != 9:
                        mineField[x][y + 1] += 1
                if x + 1 < width: #Bottom
                    if y - 1 >= 0: #Bottom-Left
                        if mineField[x + 1][y - 1] != 9:
                            mineField[x + 1][y - 1] += 1
                    if mineField[x + 1][y] != 9:
                        mineField[x + 1][y] += 1
                    if y + 1 < width: #Bottom-Right
                        if mineField[x + 1][y + 1] != 9:
                            mineField[x + 1][y + 1] += 1
                break
    return mineField, mines

def printMineField(difficulty):
    #easy difficulty
    if (difficulty == 1):
        minefield = [[0] * 9 for i in xrange(9)]
        return minefield
        
    #medium difficulty
    if (difficulty == 2):
        minefield = [[0] * 16 for i in xrange(16)]
        return minefield

    #hard difficulty
    if (difficulty == 3):
        minefield = [[0] * 20 for i in xrange(20)]
        return minefield

    #Very hard difficulty
    if (difficulty == 4):
        minefield = [[0] * 25 for i in xrange(25)]
        return minefield

    #custom difficulty
    if (difficulty == 0):
        width = input("Enter the width : ")
        height = input("Enter the height : ")
        minefield = [[0] * width for i in xrange(height)]
        return minefield

def displayTestMineField(minemap, limiter):
    counter = 0
    #prints until reach k value specified as the limiter
    for i in range(len(minemap)):
        if (counter != limiter):
            print minemap[i]
            counter +=1

#displayTestMineField(printMineField(1), 2)
#for i in range(len(mineField)):
#    for j in range(len(mineField[i])):
#        print mineField[i][j],
#    print ""
