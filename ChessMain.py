# import pygame as pg
import pygame
import ChessEngine
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
    moveMade = False #used to chk whether to regenrate the validMoves function again or not based on the move performed

    # load images before starting game
    load_images()

    # Run until the user asks to quit

    running = True
    sqselected = ()
    playerClicks = []
    print("\nPlayer White Turn")
    while running:

        # Did the user click the window close button?

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            #mouse click to select a piece
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    print("Possible moves: ")
                    for temp in validMoves:
                            print(temp.getChessNotation(), end=", ")

                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqselected = ()
                            playerClicks = []

                    if not moveMade:
                        playerClicks = [sqselected]

            #using key 'Z' to undo a move
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undoMove()
                    print("\nUndoing Move\n")
                    moveMade = True

        # Generating new possible moves after a move
        if moveMade:
            validMoves = gs.getValidMoves()
            if(gs.whiteToMove):
                print("\n\nPlayer White Turn")
            else:
                print("\n\nPlayer Black Turn")
            moveMade = False
            print("checkMate:", gs.checkMate)
            print("staleMate:", gs.staleMate)

        # Draw Game State
        draw_game_state(screen, gs, validMoves, sqselected)
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


if __name__ == '__main__':
    main()

