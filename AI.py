import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    if gs.whiteToMove:
        turn = 1
    else:
        turn = -1

    maxScore = -CHECKMATE
    bestMove = None

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getvalidMoves()
        for opponentMove in opponentMoves:
            gs.makeMove(opponentMove)
            if gs.checkMate:
                score = -CHECKMATE
            elif gs.staleMate:
                score = STALEMATE
            else:
                score = -turn * scoreMaterial(gs.board)

            if score > maxScore:
                maxScore = score
                bestMove = playerMove
            gs.undoMove()

        gs.undoMove()

    return bestMove

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            if square[0] == 'b':
                score -= pieceScore[square[1]]

    return score