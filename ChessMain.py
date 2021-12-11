import pygame as pg
import ChessEngine


WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15 # only from animation

IMAGES = {}

def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))