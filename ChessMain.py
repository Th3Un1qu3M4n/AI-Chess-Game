# import pygame as pg
import pygame
import ChessEngine
import AI
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
pygame.init()

#
#
WIDTH = HEIGHT = 400
DIMENSION = 8 #8x8
SQ_SIZE = HEIGHT // DIMENSION
#
MAX_FPS = 15   # only from animation
#
IMAGES = {}
#
#
def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

#
# def main():
def main():
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # used to chk whether to regenrate the validMoves function again or not based on the move performed

    # load images before starting game
    load_images()

    # Run until the user asks to quit

    running = True
    doAnimate = False
    sqselected = ()
    playerClicks = []
    gameOver = False

    # chess_instruction()
    ROOT = tk.Tk()

    ROOT.withdraw()
    chess_instruction()
    while True:


        choice = simpledialog.askstring(title="Options",
                                               prompt="Choose Your Desired Option: \n1) Player vs AI \n2) AI vs AI \n3)Player vs Player")

        print(choice)
        if choice == '1':
            player1 = True
            player2 = False
            break
        elif choice == '2':
            player1 = False
            player2 = False
            break
        elif choice == '3':
            player1 = True
            player2 = True
            break
        else:
            print("invalid Choice")



    print("\nPlayer White Turn")
    while running:

        userTurn = (gs.whiteToMove and player1) or (not gs.whiteToMove and player2)
        # Did the user click the window close button?

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            #mouse click to select a piece
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver and userTurn:
                    location = pygame.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqselected == (row, col):
                        sqselected = ()
                        playerClicks = []
                    else:
                        sqselected = (row, col)
                        playerClicks.append(sqselected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board, player1, player2)
                        print(move.getChessNotation())
                        print("Possible moves: ")
                        for temp in validMoves:
                                print(temp.getChessNotation(), end=", ")

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                doAnimate = True
                                sqselected = ()
                                playerClicks = []

                        if not moveMade:
                            playerClicks = [sqselected]

            #using key 'Z' to undo a move and 'R' to reset Game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undoMove()
                    print("\nUndoing Move\n")
                    moveMade = True
                    doAnimate = False
                    gameOver = False

                if event.key == pygame.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqselected = ()
                    playerClicks = []
                    moveMade = False
                    doAnimate = False
                    gameOver = False

        #AI
        if not gameOver and not userTurn:
            AIMove = AI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = AI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            print("Ai Moved: ", AIMove.getChessNotation())
            moveMade = True
            doAnimate = True

        # Generating new possible moves after a move
        if moveMade:
            if doAnimate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()

            if len(gs.getValidMoves()) == 0:
                if gs.inCheck:
                    gs.checkMate = True
                else:
                    gs.staleMate = True

            if(gs.whiteToMove):
                print("\n\nPlayer White Turn")
            else:
                print("\n\nPlayer Black Turn")
            moveMade = False
            print("checkMate:", gs.checkMate)
            print("staleMate:", gs.staleMate)
            print("Available Moves: ", len(validMoves))

        # Draw Game State
        draw_game_state(screen, gs, validMoves, sqselected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Check Mate !! Black Wins")
            else:
                drawText(screen, "Check Mate !! White Wins")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stale Mate !! Match Draws")

        clock.tick(MAX_FPS)

        # Flip the display

        pygame.display.flip()

    # Done! Time to quit.

    pygame.quit()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):
            title = pygame.Surface((SQ_SIZE, SQ_SIZE))
            title.set_alpha(100) # range 0 -255
            title.fill(pygame.Color('blue'))
            screen.blit(title, (col*SQ_SIZE, row*SQ_SIZE))
            title.fill(pygame.Color('Yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(title, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def animateMove(move, screen, board, clock):
    global colors
    deltaR = move.endRow - move.startRow
    deltaC = move.endCol - move.startCol
    fps = 6
    frameCount = (abs(deltaR) + abs(deltaC)) * fps

    for frame in range(frameCount+1):
        frameRatio = frame/frameCount
        row, col = (move.startRow +deltaR*frameRatio, move.startCol + deltaC*frameRatio)
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSqr = pygame.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSqr)

        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSqr)

        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = pygame.font.SysFont("Century Gothic", 28, True, False)
    textObject = font.render(text, 0, pygame.Color('black'))
    textLocation = pygame.Rect( 0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

def draw_game_state(screen, gs, validMoves, sqSelected):

    # drawing simple squares
    draw_board(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)

    # draw pieces on top of board
    draw_pieces(screen, gs.board)

    # TOD: draw highlighting ang available moves
#
#
def draw_board(screen):
    global colors
    colors = [pygame.Color("#eeeed2"), pygame.Color("#769656")]
    # colors = [pygame.Color("white"), pygame.Color("grey")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def chess_instruction():
    r = Toplevel()
    r.title("Rules and Instructions")
    r.canvas_width = 800
    r.canvas_height = 800
    r1 = Canvas(r, bg="darkred", width=r.canvas_width, height=r.canvas_height)
    r1.pack()
    # r_img = PhotoImage(file="bg/rules.png")
    # r1.create_image(-100, 0, anchor=NW, image=r_img)
    r1.create_text(400, 70, fill="snow", font="Times 30 bold", text="Rules And Instructions")
    r1.create_text(80, 120, fill="snow", font="Times 20 bold", text="Instructions:")
    r1.create_text(150, 145, fill="snow", font="Calibri 10 bold", text="1: There are two players: Black & White")
    r1.create_text(269, 160, fill="snow", font="Calibri 10 bold",
                   text="2: The computer (AI) is given Black color by default meaning you have White pieces.")
    r1.create_text(180, 175, fill="snow", font="Calibri 10 bold",
                   text="3: The White player will always have the first turn.")
    r1.create_text(375, 190, fill="snow", font="Calibri 10 bold",
                   text="4: In order to move the piece, you will have to click the piece and then click the valid square you want to place that piece ")
    r1.create_text(42, 240, fill="snow", font="Times 20 bold", text="Rules:")
    r1.create_text(150, 265, fill="snow", font="Calibri 10 bold", text="1: There are 6 different pieces in chess:")
    r1.create_text(145, 280, fill="snow", font="Calibri 10 bold", text="a: Rook (worth 5 points)")
    r1.create_text(148, 295, fill="snow", font="Calibri 10 bold", text="b: Knight (worth 3 points)")
    r1.create_text(150, 310, fill="snow", font="Calibri 10 bold", text="c: Bishop (worth 3 points)")
    r1.create_text(150, 325, fill="snow", font="Calibri 10 bold", text="d: Queen (worth 10 points)")
    r1.create_text(158, 340, fill="snow", font="Calibri 10 bold", text="e: King (worth 1000 points)")
    r1.create_text(148, 355, fill="snow", font="Calibri 10 bold", text="f: Pawn (worth 1 points)")
    r1.create_text(80, 380, fill="snow", font="Calibri 10 bold", text="2: Basic Moves:")
    r1.create_text(430, 395, fill="snow", font="Calibri 10 bold",
                   text="A: Queen Moves: The Queen can move any number of squares in horizontal, vertical or diagonal direction as long as the path is not ")
    r1.create_text(180, 410, fill="snow", font="Calibri 10 bold", text="blocked by one of its own pieces.")
    r1.create_text(435, 425, fill="snow", font="Calibri 10 bold",
                   text="B: Rook Moves: The Rook can moveee any number of squares horizontally or vertically as long as the path is not blocked by one of its ")
    r1.create_text(120, 440, fill="snow", font="Calibri 10 bold", text="own pieces.")
    r1.create_text(370, 455, fill="snow", font="Calibri 10 bold",
                   text="C: Bishop Moves: The Bishop can move any number of squares diagonally as long as the path is not blocked by ")
    r1.create_text(148, 470, fill="snow", font="Calibri 10 bold", text="one of its own pieces.")
    r1.create_text(425, 485, fill="snow", font="Calibri 10 bold",
                   text="D: Knight Moves: The Knight can move in 'L-shape'. It can either move two squares horizontally and one vertically or two vertically")
    r1.create_text(337, 500, fill="snow", font="Calibri 10 bold",
                   text="and one horizontally. If its path is blocked by its own teammate, it can simply jump over it.")
    r1.create_text(330, 515, fill="snow", font="Calibri 10 bold",
                   text="E: King Moves: The King can move one square in any direction (horizontal, vertical or diagonal).")
    r1.create_text(373, 530, fill="snow", font="Calibri 10 bold",
                   text="F: Pawn Moves: The pawn can move only in forward direction. On the first move it can move two squares at a ")
    r1.create_text(395, 545, fill="snow", font="Calibri 10 bold",
                   text="time while one square at a time on the remaining moves. Furthermore, it cannmot aattack an opponents piece ")
    r1.create_text(340, 560, fill="snow", font="Calibri 10 bold",
                   text="in forward direction. It can only do that in upper diagonals (top-left and top-right) direction.")
    r1.create_text(355, 590, fill="snow", font="Calibri 10 bold",
                   text="3: Checkmate: Checkmate condition is achieved when King's every possible move is threathened by the opponents ")
    r1.create_text(160, 605, fill="snow", font="Calibri 10 bold", text="pieces. This leads to a victory.")
    r1.create_text(352, 630, fill="snow", font="Calibri 10 bold",
                   text="4: Stalemate: When the King is not in Check but there is no such move which won't lead to the King being in check.")
    r1.create_text(135, 645, fill="snow", font="Calibri 10 bold", text=" This leads to a draw.")
    r1.create_text(315, 670, fill="snow", font="Calibri 10 bold",
                   text="5: Illegal Moves: Such moves that lead you king in check. There aren't allowed in our implementation.")
    r1.create_text(383, 695, fill="snow", font="Calibri 10 bold",
                   text="6: Special Move (Castling): Each player can castle only once . In castling, the player moves his King two squares either to its left ")
    r1.create_text(410, 710, fill="snow", font="Calibri 10 bold",
                   text="or right toward one of his Rooks. At the same time, the Rook involved goes to the square on the other side of the King.")
    r1.create_text(368, 735, fill="snow", font="Calibri 10 bold",
                   text="7: Special Move (En-Passant): Each player can perform on the pawns. In en-passant, the player moves his pawn such that ")
    r1.create_text(410, 750, fill="snow", font="Calibri 10 bold",
                   text="it captures the opponents pawn that has moved two squares in its first move.")
    r1.create_text(356, 775, fill="snow", font="Calibri 10 bold",
                   text="8: Special Move (Pawn Promotion): Each player can perform on the pawns that have reached the last opposite row.")
    r1.create_text(410, 790, fill="snow", font="Calibri 10 bold",
                   text="The Pawn(P) can be promoted to either Queen(Q), Rook(R), Bishop(B), or Knight(N).")

    r1.update()

    return

if __name__ == '__main__':
    main()

