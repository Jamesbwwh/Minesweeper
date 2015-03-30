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
