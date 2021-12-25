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

        knightMoves = ((-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1))  # L shapes as in left_down2, left_up2, right_down2, right_up2, left2_down, left2_up, right2_down, right2_up
        if self.whiteToMove:
            print("white")
            allyColor = "w"
        else:
            print("black")
            allyColor = "b"

        for n_move in knightMoves:
            endRow = row + n_move[0]
            endCol = col + n_move[1]

            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    possibleMoves.append(Move((row, col), (endRow, endCol), self.board))




    def getBishopMoves(self, row, col, possibleMoves):

        bishopMoves = ((-1, -1), (1, -1), (-1, 1), (1, 1))  # left_down, right_down, left_up, right_up
        if self.whiteToMove:
            print("white")
            enemyColor = "b"
        else:
            print("black")
            enemyColor = "w"

        for b_moves in bishopMoves:
            for i in range(1, 8):
                endRow = row + b_moves[0] * i
                endCol = col + b_moves[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
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

    def getRookMoves(self, row, col, possibleMoves):

        rookMoves = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        if self.whiteToMove:
            print("white")
            enemyColor = "b"
        else:
            print("black")
            enemyColor = "w"

        for r_move in rookMoves:
            for i in range(1,8):
                endRow = row + r_move[0]*i
                endCol = col + r_move[1]*i
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

        self.getBishopMoves(row, col, possibleMoves)
        self.getRookMoves(row, col, possibleMoves)

    def getKingMoves(self, row, col, possibleMoves):

        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1))  # left_down, left, left_up, right_down, right_up, right, rifght_up, down, up
        if self.whiteToMove:
            print("white")
            allyColor = "w"
        else:
            print("black")
            allyColor = "b"

        for k_move in range(8):
            endRow = row + kingMoves[k_move][0]
            endCol = col + kingMoves[k_move][1]

            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    possibleMoves.append(Move((row, col), (endRow, endCol), self.board))





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