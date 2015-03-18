def printMineField(difficulty):
    #easy difficulty
    if (difficulty == 1):
        minefield = [[0] * 15 for i in xrange(15)]
        return minefield
        
    #medium difficulty
    if (difficulty == 2):
        minefield = [[0] * 50 for i in xrange(50)]
        return minefield

    #hard difficulty
    if (difficulty == 3):
        minefield = [[0] * 150 for i in xrange(150)]
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
