class GameState():
    def __init__(self):

        #board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.whiteToMove = True
        self.moveLog=[]
        self.possibleMoveFunctions = {'P': self.getPawnMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'R': self.getRookMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

    # Simple Chess Moves:

    def makeMove(self, move):

        self.board[move.startRow][move.startCol] = "--"

        self.board[move.endRow][move.endCol] = move.pieceMoved

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):

        if len(self.moveLog) != 0:

            move = self.moveLog.pop()

            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switching the turn

    #every possible move that a piece can make without the concern of other pieces
    def getAllPossibleMoves(self):

        possibleMoves = []

        for row in range (len(self.board)):
            for col in range (len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.possibleMoveFunctions[piece](row, col, possibleMoves)

        return possibleMoves


    def getValidMoves(self):

        return self.getAllPossibleMoves()

    def getPawnMoves(self, row, col, possibleMoves):
        # for white pieces

        if self.whiteToMove:

            # move up 1 or 2 squres
            if self.board[row-1][col] == "--":
                possibleMoves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == "--":
                    possibleMoves.append(Move((row, col), (row-2, col), self.board))

            # move diagonals
            if col-1>=0:
                if self.board[row-1][col-1][0] == 'b':
                    possibleMoves.append(Move((row, col), (row-1, col-1), self.board))
            if col+1 <=7:
                if self.board[row-1][col+1][0] == 'b':
                    possibleMoves.append(Move((row, col), (row-1, col+1), self.board))

        # for black pieces

        else:

            # move up 1 or 2 squres
            if self.board[row+1][col] == "--":
                possibleMoves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == "--":
                    possibleMoves.append(Move((row, col), (row+2, col), self.board))

            # move diagonals
            if col-1>=0:
                if self.board[row+1][col-1][0] == 'w':
                    possibleMoves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1<=7:
                if self.board[row+1][col+1][0] == 'w':
                    possibleMoves.append(Move((row, col), (row+1, col+1), self.board))



    def getKnightMoves(self, row, col, possibleMoves):
        # for white pieces
        pass


    def getBishopMoves(self, row, col, possibleMoves):
        pass

    def getRookMoves(self, row, col, possibleMoves):
        # for white pieces

        moveDirections = ((-1,0), (0,-1), (1,0), (0,1)) #up, left, down, right
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'

        for direction in moveDirections:
            for i in range(1,8):
                endRow = row + direction[0]*i
                endCol = col + direction[0]*i
                if 0<=endRow<=7 and 0<=endCol<=7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        possibleMoves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        possibleMoves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, row, col, possibleMoves):
        pass

    def getKingMoves(self, row, col, possibleMoves):
        pass





class Move():

    ranksToRows = {"1": 7,
                   "2": 6,
                   "3": 5,
                   "4": 4,
                   "5": 3,
                   "6": 2,
                   "7": 1,
                   "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]