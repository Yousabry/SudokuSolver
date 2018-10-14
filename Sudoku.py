"""
Sudoku2.0
"""
def setup():
    grid = [
    [0,8,0,0,0,6,0,0,9],
    [4,0,0,0,0,1,5,0,0],
    [0,0,1,0,0,0,0,0,2],
    [0,0,0,4,7,0,8,0,0],
    [0,9,0,0,1,0,0,4,0],
    [0,0,3,0,9,5,0,0,0],
    [9,0,0,0,0,0,7,0,0],
    [0,0,2,5,0,0,0,0,3],
    [5,0,0,1,0,0,0,2,0]]
    updater(grid)
    printer(grid)
    main(grid)

def main(grid):
    while solvedcheck(grid) == False and mistakecheck(grid) == False:
        if str(grid) == str(solver(grid)):
            guesser(grid)
        else:
            main(solver(grid))

    if solvedcheck(grid) == True:
        printer(grid)
        print('This Sudoku is solved!')
        end()

    if mistakecheck(grid) == True:
        print('There is already a mistake in this Sudoku!')
        printer(grid)
        end()

def solvedcheck(grid):
    #Returns True if completed, otherwise returns False
    solved = True
    for row in grid:
        for b in row:
            if integercheck(b) == False:
                solved = False
    return solved

def integercheck(value):
    #Receives value and returns True(for int) or false for anything else
    return isinstance(value,int)

def mistakecheck(grid):
    mistake = False
    #Checking if number is repeated in same row or column
    for row in range(9):
        allboxes = []
        for b in range(9):
            if integercheck(grid[row][b]) == True:
                allboxes.append(grid[row][b])
        if repeatedfinder(allboxes) == True:
            mistake = True

    for b in range(9):
        allboxes = []
        for row in range(9):
            if integercheck(grid[row][b]) == True:
                allboxes.append(grid[row][b])

        if repeatedfinder(allboxes) == True:
            mistake = True

    #Checking if any box has no possibilities
    for row in range(9):
        for b in range(9):
            if integercheck(grid[row][b]) == False:
                if len(switchposs(grid[row][b])) < 1:
                    print('NO POSSIBLE SOLUTIONS FOR BOX: ',row,b)
                    mistake = True

    return mistake

def printer(grid):
    for row in range(9):
        print('')
        for b in range(9):
            if integercheck(grid[row][b]) == True:
                print(grid[row][b],end='   ')
            else:
                print(0,end='   ')
    print('\n\n')

def solver(grid):
    #STRATEGY OF ELIMINATION NUMBER 1 (PER INDIVIDUAL BOX)
    for row in range(9):
        for b in range(9):
            if integercheck(grid[row][b]) == False:
                if len(switchposs(grid[row][b])) == 1:
                    grid[row][b] = switchposs(grid[row][b])[0]
                    updater(grid)

    #STRATEGY OF ELIMINATION NUMBER 2 (PER 3x3 BOX)
    listofrang = [[0,1,2],[3,4,5],[6,7,8]]
    for rang in listofrang:
        for rang2 in listofrang:
            allboxsposs = []
            for row in rang:
                for b in rang2:
                    if integercheck(grid[row][b]) == False:
                        for possibility in switchposs(grid[row][b]):
                            allboxsposs.append(possibility)

            uniquelist = uniquefinder(allboxsposs)
            if len(uniquelist)>=1:
                for number in uniquelist:
                    for row in rang:
                        for y in rang2:
                            if integercheck(grid[row][y]) == False:
                                if number in switchposs(grid[row][y]):
                                    grid[row][y] = number
                                    updater(grid)

    #STRATEGY OF ELIMINATION NUMBER 3 (PER ROW)
    for row in range(9):
        allboxsposs = []
        for b in range(9):
            if integercheck(grid[row][b]) == False:
                for possibility in switchposs(grid[row][b]):
                    allboxsposs.append(possibility)

        uniquelist = uniquefinder(allboxsposs)
        if len(uniquelist)>=1:
            for ansfound in uniquelist:
                for b in range(9):
                    if integercheck(grid[row][b]) == False:
                            if ansfound in switchposs(grid[row][b]):
                                grid[row][b] = ansfound
                                updater(grid)

    #STRATEGY OF ELIMINATION NUMBER 4 (PER COLUMN)
    for b in range(9):
        allboxsposs = []
        for row in range(9):
            if integercheck(grid[row][b]) == False:
                for possibility in switchposs(grid[row][b]):
                    allboxsposs.append(possibility)

        uniquelist = uniquefinder(allboxsposs)
        if len(uniquelist)>=1:
            for ansfound in uniquelist:
                for row in range(9):
                    if integercheck(grid[row][b]) == False:
                            if ansfound in switchposs(grid[row][b]):
                                grid[row][b] = ansfound
                                updater(grid)

    return updater(grid)

def updater(grid):
    for row in range(9):
        for b in range(9):
            if integercheck(grid[row][b]) == False:
                #Have to add both lists and return a set to keep the values that are added manually
                #Cannot add set and list so must concatenate manually
                newlist = list(grid[row][b])
                for f in switchposs(possibilities(grid,row,b)):
                    newlist.append(f)
                grid[row][b] = []
                for item in set(newlist):
                    grid[row][b].append(item)
            if grid[row][b] == 0:
                grid[row][b] = switchposs(possibilities(grid,row,b))
    return grid

def switchposs(list):
    #Receives list of either isposs or notposs and returns the opposite
    switchposs = [1,2,3,4,5,6,7,8,9]
    if integercheck(list) == True:
        list = [list]
    for item in list:
        switchposs.remove(item)
    return switchposs

def guesser(grid):
    printer(grid)
    print('Running guesser')

    for a in range(9):
        for b in range(9):
            if integercheck(grid[a][b]) == False:
                options = switchposs(grid[a][b])
                found = False
                for option in options:
                    if found == False:
                        grid[a][b] = option #Setting the square to the first option
                        attempt = trial(updater(grid))
                        if attempt == True:
                            end()
                        if attempt == False:
                            print('Location {}{} cannot be {}'.format(a,b,grid[a]))
                            options.remove(option)
                            grid[a][b].remove(option)
                        if len(options) == 1:
                            grid[a][b] = options[0]


def trial(grid):
        while solvedcheck(grid) == False and mistakecheck(grid) == False:
            if str(grid) == str(solver(grid)):
                print("This one doesnt solve it!")
                return None
            else:
                trial(solver(grid))
        if solvedcheck(grid) == True:
            print('This Sudoku is solved!')
            printer(grid)
            end()
        if mistakecheck(grid) == True:
            return False

def repeatedfinder(list):
    #Returns True if there is any repetition in a list
    if len(list) == len(set(list)):
        repeated = False
    else:
        repeated = True

    return repeated

def uniquefinder(list):
    #Returns list of unique (Only seen once) items
    unique = []
    for item in list:
        counter = 0
        for b in list:
            if item == b:
                counter += 1
        if counter == 1:
            unique.append(item)
    return unique

def possibilities(grid,a,b):
    #This function receives the grid and the location of a box, returns all possible numbers for that box
    allposs = [1,2,3,4,5,6,7,8,9]
    #Othersquares is a list of unusable numbers (already found in other squares)
    othersquares = []
    square1 = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    square2 = [[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]
    square3 = [[0,6],[0,7],[0,8],[1,6],[1,7],[1,8],[2,6],[2,7],[2,8]]
    square4 = [[3,0],[3,1],[3,2],[4,0],[4,1],[4,2],[5,0],[5,1],[5,2]]
    square5 = [[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]]
    square6 = [[3,6],[3,7],[3,8],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8]]
    square7 = [[6,0],[6,1],[6,2],[7,0],[7,1],[7,2],[8,0],[8,1],[8,2]]
    square8 = [[6,3],[6,4],[6,5],[7,3],[7,4],[7,5],[8,3],[8,4],[8,5]]
    square9 = [[6,6],[6,7],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]]
    allsquares = [square1,square2,square3,square4,square5,square6,square7,square8,square9]

    #Adding the values of the other boxes in the 3x3 to the 'othersquares' list
    location = [a,b]
    for square in allsquares:
        if location in square:
            for box in square:
                if integercheck(grid[box[0]][box[1]]) == True:
                    othersquares.append(grid[box[0]][box[1]])
    #Rows
    for y in range(9):
        if integercheck(grid[a][y]) == True:
            othersquares.append(grid[a][y])

    #Columns
    for x in range(9):
        if integercheck(grid[x][b]) == True:
            othersquares.append(grid[x][b])

    #Need to return a list for solver function
    finallist = []
    for poss in (set(allposs)-set(othersquares)):
        finallist.append(poss)

    return sorted(finallist)

def end():
    print('This is the end of the program')
    exit()

setup()
