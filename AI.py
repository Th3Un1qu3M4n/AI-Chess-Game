import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    if gs.whiteToMove:
        turn = 1
    else:
        turn = -1

    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        if gs.checkMate:
            opponentMaxScore = CHECKMATE
        elif gs.staleMate:
            opponentMaxScore = STALEMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = -turn * CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turn * scoreMaterial(gs.board)

                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()

        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()

    return bestPlayerMove

def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    if gs.whiteToMove:
        bestMinMaxMove(gs, validMoves, DEPTH, 1)
    else:
        bestMinMaxMove(gs, validMoves, DEPTH, -1)
    return nextMove

def bestMinMaxMove(gs, validMoves, depth, turn):
    global nextMove
    if depth == 0:
        return turn * scoreMaterial(gs.board)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -bestMinMaxMove(gs, nextMoves, depth - 1, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


# def bestMinMaxMove(gs, validMoves, depth, whiteToMove):
#     global nextMove
#     if depth == 0:
#         return scoreMaterial(gs.board)
#
#     if whiteToMove:
#         maxScore = -CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = bestMinMaxMove(gs, nextMoves, depth - 1, False)
#             if score > maxScore:
#                 maxScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return maxScore
#     else:
#         minScore = CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = bestMinMaxMove(gs, nextMoves, depth - 1, True)
#             if score < minScore:
#                 minScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return minScore
#

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