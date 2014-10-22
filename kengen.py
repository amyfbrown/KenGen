# Amy Brown
#
# KenKen generator
#
# December 28, 2013 -

def oneOfEach(L):
    """ returns a list with only one of each of the components from the original list, L. removes duplicates """
    newL = []
    for i in range(len(L)):
        if L[i] not in newL:
            newL += [L[i]]
    return newL

def divUpToMax(cageprod, maxval):
        """ returns a list of the divisors up to the maximum value of the Latin Square """
        L = []
        for i in range(1,maxval+1):
            if cageprod%i == 0:
                L += [i]
        return L

def possSumValues(cagesum, numcells, maxval):
    """ returns a list of the possible sums for a cell """
    posvals = range(1,maxval + 1)
    posssums = []

    if numcells > 2:
        for i in posvals:
            prevsum = possSumValues(cagesum - i, numcells - 1, maxval)
            if len(prevsum) != 0:
                posssumi = []
                for k in range(len(prevsum)):
                    prevsum[k] += [i]
                    prevsum[k].sort()
                    posssumi += [prevsum[k]]
                posssums += posssumi
        return oneOfEach(posssums)

    elif numcells == 2:
        twosum = []
        for k in range(1,maxval+1):
            for l in range(k,maxval+1):
                if k+l == cagesum:
                    twosum += [[k,l]]
        return twosum

    else:
        print "WHUT?"
        return

def possProdValues(cageprod, numcells, maxval):
    """ returns a list of the possible products for a cell """
    posvals = divUpToMax(cageprod,maxval)
    possprods = []

    if numcells > 2:
        for i in posvals:
            prevprod = possProdValues(cageprod / i, numcells - 1, maxval)
            if len(prevprod) != 0:
                possprodi = []
                for k in range(len(prevprod)):
                    prevprod[k] += [i]
                    prevprod[k].sort()
                    possprodi += [prevprod[k]]
                possprods += possprodi
        return oneOfEach(possprods)

    elif numcells == 2:
        twoprod = []
        for k in range(1,maxval+1):
            for l in range(k,maxval+1):
                if k*l == cageprod:
                    twoprod += [[k,l]]
        return twoprod

    else:
        print "WHUT?"
        return


class Cage:
    """ scaffold for defining each individual cage in the KenKen. """

    def __init__(self, numcells, maxvalue, result, operation, location):
        """ the constructor """
        self.numcells = numcells                # the number of cells in the cage
        self.maxvalue = maxvalue                # the maximum number in any cell (the width/height of the cell)
        self.result = result                    # the sum, difference, product, or quotient of the cage
        self.operation = operation              # the operation on the cells in the cage ('+', '-', 'x', '/', ' ')
        self.location = location                # a list of the coordinates of the cells in the cage e.g. [[0,0],[0,1],[0,2]]
        self.location.sort()                    # this sorts the list first by row, then by column
        self.cagedata = [' ']*self.numcells     # this holds the numbers in the cells of the ordered coordinates in the cage

        if len(location) != numcells:
            print "ERROR; NUMCELLS DOES NOT MATCH LOCATION DATA"
            return

        # c = Cage(3,4,40,'x',[[0,0],[1,1],[0,1]])
        # c.location = [[0, 0], [0, 1], [1, 1]]
        # c.cagedata = [' ', ' ', ' ']





    def upperLeftMost(self):
        """  returns the coordinate of the upperleft-most cell in the cage where the operation and result will appear. """
        return min(self.location)

    def valueAt(self,coordinates):
        """ returns the number in the given cell """
        loc = self.location
        for i in range(len(loc)):
            if loc[i] == coordinates:
                return self.cagedata[i]

    def callCell(self,coordinates):
        """ returns all the information that is contained in a given cell of a cage. """
        result = self.result
        op = self.operation

        if coordinates == self.upperLeftMost():
            return [str(result),op,self.valueAt(coordinates)]
        else:
            return [' ',' ',self.valueAt(coordinates)]





    def isLinear(self):
        """ returns True if the cage is linear and False if it is not """
        loc = self.location
        num = self.numcells

        for i in range(num):
            if loc[i][0] != loc[0][0] and loc[i][1] != loc[0][1]:
                return False
        return True

    def divUpToMax(self):
        """ returns a list of the divisors up to the maximum value of the Latin Square """
        maxval = self.maxvalue
        result = self.result
        L = []
        for i in range(1,maxval+1):
            if result%i == 0:
                L += [i]
        return L

    def numDup(self):
        """ returns the number of duplicate numbers that can occur within a cage """
        numcells = self.numcells
        loc = self.location
        row = []
        col = []
        for i in range(numcells):
            row += [loc[i][0]]
            col += [loc[i][1]]
        rowdif = max(row) - min(row)
        coldif = max(col) - min(col)
        return min(rowdif,coldif) + 1



    def possCageValues(self):
        """ returns a list of the possible values the cells in the cage can take on; COMBINATIONS """
        op = self.operation
        maxval = self.maxvalue
        numcells = self.numcells
        result = self.result

        possval = []

        if op == ' ':
            self.cagedata = [str(result)]
            posval = [[result]]
            return posval

        elif op == '-':                         # numcells should be 2
            if numcells != 2:
                print "WHUT?"
            for i in range(1,maxval+1):
                for j in range(i+1,maxval+1):
                    if j-i == result:
                        possval += [[i,j]]
            return possval

        elif op == '/':                         # numcells should be 2
            if numcells != 2:
                print "WHUT?"
            for i in range(1,maxval+1):
                for j in range(i+1,maxval+1):
                    if j/i == result and j%i == 0:
                        possval += [[i,j]]
            return possval

        elif op == 'x':
            return possProdValues(result,numcells,maxval)

        elif op == '+':
            return possSumValues(result,numcells,maxval)






"""
remember to make one line before putting into shell

c0 = Cage(2,4,3,'-',[[0,0],[1,0]]); c1 = Cage(2,4,3,'+',[[0,1],[0,2]]);
c2 = Cage(3,4,36,'x',[[0,3],[1,2],[1,3]]); c3 = Cage(2,4,2,'/',[[1,1],[2,1]]);
c4 = Cage(3,4,8,'+',[[2,0],[3,0],[3,1]]); c5 = Cage(2,4,3,'-',[[2,2],[3,2]]);
c6 = Cage(2,4,1,'-',[[2,3],[3,3]]); LoC = [c0,c1,c2,c3,c4,c5,c6]; g = Grid(LoC); g
"""


class Grid:
    """ This is the grid on which the KenKen is represented. """

    def __init__(self,listOfCages):
        """ the constructor """

        self.LoC = listOfCages

        cage0 = self.LoC[0]
        for i in range(len(self.LoC)):
            c = self.LoC[i]
            if c.maxvalue != cage0.maxvalue:
                print "ERROR; CAGE MAXVALUES DO NOT MATCH"
                return
        self.size = cage0.maxvalue

        self.griddata = [[' ']*self.size for i in range(self.size)]





    def whichCage(self,coordinates):
        """ Given a grid and a set of coordinates, it will return which cage the coordinates are from. """
        LoC = self.LoC
        for i in range(len(LoC)):
            if coordinates in LoC[i].location:
                return i

    def callCell(self,coordinates):
        """ Given a grid with a number of cages and a set of coordinates, this returns the following list: [ result (if applicable), operation (if applicable), the number in the cell at the coordinates, the number of the cage it came from]. """
        LoC = self.LoC
        numcages = len(LoC)
        for i in range(numcages):
            if coordinates in LoC[i].location:
                return LoC[i].callCell(coordinates) + [self.whichCage(coordinates)]





    def maxLenResults(self):
        """ This takes in a grid and returns the longest length of the results of all the cages in the grid. """
        LoC = self.LoC

        L = []
        for i in range(len(LoC)):
            L += [len(str(LoC[i].result))]
        return L

    def __repr__(self):
        """ the reaper """
        LoC = self.LoC
        size = self.size
        res = self.maxLenResults()

        """
        for row in range(size):
            for col in range(size):
                cage = self.whichCage([row,col])
                self.griddata[row][col] = LoC[cage].valueAt([row,col])
        """

        # This helps determine repr proportions based on result lengths
        if max(res) <= 3:
            maxlen = 3
        else:
            maxlen = max(res)

        s = ''

        # top border
        s += ' '*(maxlen+1)
        for i in range(size):
            s += str(i)
            s += ' '*maxlen
        s += '\n'
        s += '  +'
        for i in range(size):
            s += '-'*maxlen
            s += '+'
        s += '\n'

        for row in range(size):

            # top 1/3 of each row featuring result, if any
            s += '  |'

            for col in range(size):

                L = self.callCell([row,col])        # [result, operation, number in cell, cage from which it came]
                if L[0] != ' ':
                    s += L[0]
                    s += ' '*(maxlen - res[L[3]])
                else:
                    s += ' '*maxlen

                # consecutive cells
                if self.whichCage([row,col]) == self.whichCage([row,col+1]):
                    s += ' '
                else:
                    s += '|'

            s += '\n'

            # middle 1/3 of each row featuring operation, if any
            s += str(row)
            s += ' |'

            for col in range(size):
                L = self.callCell([row,col])        # [result, operation, number in cell, cage from which it came]
                if L[1] != ' ':
                    s += L[1]
                    s += ' '*(maxlen - len(L[1]))
                else:
                    s += ' '*maxlen

                # consecutive cells
                if self.whichCage([row,col]) == self.whichCage([row,col+1]):
                    s += ' '
                else:
                    s += '|'

            s += '\n'

            # bottom 1/3 of each row featuring number, if any
            s += '  |'

            for col in range(size):
                L = self.callCell([row,col])        # [result, operation, number in cell, cage from which it came]
                if L[2] != ' ':
                    s += ' '*(maxlen - len(L[2]))
                    s += L[2]
                else:
                    s += ' '*maxlen

                # consecutive cells
                if self.whichCage([row,col]) == self.whichCage([row,col+1]):
                    s += ' '
                else:
                    s += '|'

            s += '\n'

            # border between rows
            s += '  +'
            for col in range(size):
                # consecutive cells
                if self.whichCage([row,col]) == self.whichCage([row+1,col]):
                    s += ' '*maxlen
                else:
                    s += '-'*maxlen
                s += '+'
            s += '\n'

        return s




    def checkSoFar(self):
        """ checks that the cells so far are correct """

    def checkComplete(self):
        """ checks that the puzzle is completed and all cells are correct """

    def solve(self):
        """ solves the KenKen in the given grid """





def latinsquare(size):
    """ produces a Latin Square of the given size """




def generate():
    """ generates a KenKen, although not necessarily one with a unique solution """

    #latin square
    #divide into cages
    #randomly select operation
    #fill in
    #make numbers disappear
