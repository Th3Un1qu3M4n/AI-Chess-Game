import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    if gs.whiteToMove:
        bestAlphaBetaMinMaxMove(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1)
    else:
        bestAlphaBetaMinMaxMove(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, -1)
    print(counter)
    return nextMove

def bestAlphaBetaMinMaxMove(gs, validMoves, depth, alpha, beta, turn):
    global nextMove
    if depth == 0:
        return turn * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -bestAlphaBetaMinMaxMove(gs, nextMoves, depth - 1, -beta, -alpha, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()

        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):

    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            if square[0] == 'b':
                score -= pieceScore[square[1]]
    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            if square[0] == 'b':
                score -= pieceScore[square[1]]

    return score