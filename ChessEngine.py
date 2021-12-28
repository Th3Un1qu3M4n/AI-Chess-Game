import tkinter as tk
from tkinter import simpledialog

class GameState():
    def __init__(self):

        # board
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
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.possibleMoveFunctions = {'P': self.getPawnMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves,
                                      'R': self.getRookMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.enpassantPossible = ()  # the square for enpassant possible
        self.checkMate = False
        self.staleMate = False

        self.inCheck = False
        self.pins = []
        self.checks = []

        self.currentCastlingRights = CastleRights(True, True, True, True)
        # self.castleRightsLog = [self.currentCastlingRights]
        # Deep Copy Rights object
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

    # Simple Chess Moves:

    def makeMove(self, move):

        self.board[move.startRow][move.startCol] = "--"

        self.board[move.endRow][move.endCol] = move.pieceMoved

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)


        # For Pawn Promotion:
        if move.isPawnPromotion:
            if move.AIPlaying:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + move.AIPromotionKey
            else:
                ROOT = tk.Tk()

                ROOT.withdraw()
                # the input dialog

                while True:
                    promotedPiece = simpledialog.askstring(title="Test",
                                                      prompt="Promote Pawn(P) to Queen(Q), Rook(R), Bishop(B), or Knight(N):")

                    print(promotedPiece)
                    promotion = ['Q', 'R', 'B', 'N']
                    if promotedPiece in promotion:
                        self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
                        break
                    else:
                        print("invalid Promotion")


        # Update Enpassant Variable only if Pawn Moves Two Squares:
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)  # Taking Average to get the square in the middle of the 2 square move
            # print("\n en possant\n", move.pieceMoved)
        else:
            self.enpassantPossible = ()

        # For Enpassant Move:
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        # For Castle Move:
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # King side Castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else :  # Queen Side Castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        # Updating Castle Rights on Each Move:
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))
        # for log in self.castleRightsLog:
        #     print(log.wks, log.bks, log.wqs, log.bqs)
        # print("\n\n")

    def undoMove(self):

        if len(self.moveLog) != 0:

            move = self.moveLog.pop()

            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switching the turn
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # Undo Enpassant Move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'  # Making The Ending square blank as the pawn captured was not in that square
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            # Undo the captured
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo Castle Rights
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # undo Castle Move
            if move.isCastleMove:
                print("Is castle Move")
                if move.endCol - move.startCol == 2:  # King side Castle
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    # print(move.endRow, move.endCol + 1, " from ", move.endRow, move.endCol -1)
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # Queen Side Castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

            self.checkMate = False
            self.staleMate = False

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False
        if move.pieceCaptured == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False



    # every possible move that a piece can make without the concern of other pieces
    def getAllPossibleMoves(self):

        possibleMoves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.possibleMoveFunctions[piece](row, col, possibleMoves)

        return possibleMoves

    def getValidMoves(self):

        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
            allyColor = 'w'
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
            allyColor = 'b'

        if self.inCheck:
            # print("\n incheck: ", self.inCheck, "\n")
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[0] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
            # print("King At ", kingRow, kingCol)
            # print(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
            self.getCastleMoves(kingRow, kingCol, moves, allyColor)

        return moves


    def squareUnderAttack(self, row, col):
        # switch to opponent
        self.whiteToMove = not self.whiteToMove

        oppMoves = self.getAllPossibleMoves()

        # switch back to current player
        self.whiteToMove = not self.whiteToMove


        for move in oppMoves:
            # square under attack
            if move.endRow == row and move.endCol == col:
                return True

        return False

    def getPawnMoves(self, row, col, possibleMoves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # for white pieces
        if self.whiteToMove:

            # move up 1 or 2 squres
            if self.board[row - 1][col] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    possibleMoves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--":
                        possibleMoves.append(Move((row, col), (row - 2, col), self.board))

            # move diagonals
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        possibleMoves.append(Move((row, col), (row - 1, col - 1), self.board))
                if (row-1, col-1) == self.enpassantPossible:
                    possibleMoves.append(Move((row, col), (row - 1, col - 1), self.board, isEnpassantMove=True))

            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        possibleMoves.append(Move((row, col), (row - 1, col + 1), self.board))
                if (row-1, col+1) == self.enpassantPossible:
                    possibleMoves.append(Move((row, col), (row - 1, col + 1), self.board, isEnpassantMove=True))

        # for black pieces

        else:

            # move up 1 or 2 squres
            if self.board[row + 1][col] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    possibleMoves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--":
                        possibleMoves.append(Move((row, col), (row + 2, col), self.board))

            # move diagonals
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        possibleMoves.append(Move((row, col), (row + 1, col - 1), self.board))
                if (row + 1, col - 1) == self.enpassantPossible:
                    possibleMoves.append(Move((row, col), (row + 1, col - 1), self.board, isEnpassantMove=True))

            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        possibleMoves.append(Move((row, col), (row + 1, col + 1), self.board))
                if (row + 1, col + 1) == self.enpassantPossible:
                    possibleMoves.append(Move((row, col), (row + 1, col + 1), self.board, isEnpassantMove=True))

    def getKnightMoves(self, row, col, possibleMoves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1))  # L shapes as in left_down2, left_up2, right_down2, right_up2, left2_down, left2_up, right2_down, right2_up
        if self.whiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"

        for n_move in knightMoves:
            endRow = row + n_move[0]
            endCol = col + n_move[1]

            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        possibleMoves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, possibleMoves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        bishopMoves = ((-1, -1), (1, -1), (-1, 1), (1, 1))  # left_down, right_down, left_up, right_up
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"

        for b_moves in bishopMoves:
            for i in range(1, 8):
                endRow = row + b_moves[0] * i
                endCol = col + b_moves[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == b_moves or pinDirection == (-b_moves[0], -b_moves[1]):
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
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        rookMoves = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"

        for r_move in rookMoves:
            for i in range(1, 8):
                endRow = row + r_move[0] * i
                endCol = col + r_move[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == r_move or pinDirection == ( -r_move[0], -r_move[1]):
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

        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)

        # kingMoves = ((-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1),(0, 1))  # left_down, left, left_up, right_down, right_up, right, rifght_up, down, up
        if self.whiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"

        for k_move in range(8):
            # endRow = row + kingMoves[k_move][0]
            # endCol = col + kingMoves[k_move][1]

            endRow = row + rowMoves[k_move]
            endCol = col + colMoves[k_move]

            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:

                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                        # print("black King changed to ", self.blackKingLocation)
                        # print(rowMoves[k_move], colMoves[k_move])

                    inCheck, pins, checks = self. checkForPinsAndChecks()

                    if not inCheck:
                        possibleMoves.append(Move((row, col), (endRow, endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)
                        # print("black King changed BACK to ", self.blackKingLocation)

    def getCastleMoves(self, row, col, moves, allyColor):
        if self.squareUnderAttack(row, col):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingCastleMoves(row, col, moves, allyColor)

        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQeenCastleMoves(row, col, moves, allyColor)

    def getKingCastleMoves(self, row, col, moves, allyColor):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if (not self.squareUnderAttack(row, col+1)) and (not self.squareUnderAttack(row, col+2)):
                moves.append(Move((row, col), (row, col+2), self.board, isCastleMove=True))

    def getQeenCastleMoves(self, row, col, moves, allyColor):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if (not self.squareUnderAttack(row, col - 1)) and (not self.squareUnderAttack(row, col - 2)):
                moves.append(Move((row, col), (row, col -2), self.board, isCastleMove=True))


    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            allyColor = 'w'
            enemyColor = 'b'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            allyColor = 'b'
            enemyColor = 'w'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        # directions = ((-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1))
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # print("Black King location", self.blackKingLocation)
                        # print(startRow, startCol," enemy found in direction ", d[0], d[1], enemyColor, type, endRow, endCol, i, j)
                        # print((i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))))
                        # if enemy piece found near King
                        if ( 0<= j <=3  and type == 'R') or \
                            ( 4 <= j <=7 and type == 'B') or \
                            (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5) )) or \
                            (type == 'Q') or \
                            (i==1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True  # if enemy directly in range of King
                                # print("king in check by: ", enemyColor, type, endRow, endCol)
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)  # if ally piece in between king and enemy
                                break
                        else:
                            break  # if no enemy found the respective direction that poses threat
                else:
                    break

        #  Special Case for Knight Moves
        knightMoves = ((-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self. wqs = wqs
        self.bqs = bqs



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

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False, AIPromotionKey = 'Q', AIPlaying = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        #For AI:
        self.AIPromotionKey = AIPromotionKey
        self.AIPlaying = AIPlaying

        # For Pawn Promotion:
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True

        # For Enpassant Move:
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            if self.pieceMoved == 'wP':
                self.pieceCaptured = 'bP'
            else:
                self.pieceCaptured = 'wP'

        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
