import chessEngine as ce
import pygame as pg
from pygame import mixer
import time
import os

# Initializing Board variables

height = width = 800
squareSize = 100
fpsMax = 15
imageList = {}
soundList = {}
padding = 30


# Loading images into a dictionary
def imageLoad():
    pieceList = ["wQ", "wK", "wB", "wN", "wR", "wP", "bQ", "bK", "bB", "bN", "bR", "bP"]
    for piece in pieceList:
        imageList[piece] = pg.transform.scale(
            pg.image.load("assets/pieces/" + piece + ".png"),
            (squareSize - padding, squareSize - padding),
        )


# Loading game Sounds into a Dictionary
def soundLoad():
    sounds = os.listdir("assets/sounds")
    for sound in sounds:
        soundList[sound.split(".")[0]] = pg.mixer.Sound("assets/sounds/" + sound)


def main():
    # pygame setup (from Documentation)
    pg.init()
    window = pg.display.set_mode((width, height))
    window.fill("white")
    clock = pg.time.Clock()
    imageLoad()
    soundLoad()
    running = True
    chessGame = ce.GameStatus()

    clickList = []
    lastSquare = ()

    pg.mixer.Sound.play(soundList["game-start"])
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.mixer.Sound.play(soundList["game-end"])
                time.sleep(0.25)

            elif event.type == pg.MOUSEBUTTONDOWN:
                click = pg.mouse.get_pos()  # click cordinates raw
                selColumn = click[0] // squareSize
                selRow = click[1] // squareSize

                if lastSquare == (selRow, selColumn):
                    clickList = []
                    lastSquare = ()
                else:
                    lastSquare = (selRow, selColumn)
                    clickList.append(lastSquare)

                    if len(clickList) == 2:
                        if chessGame.board[clickList[0][0]][clickList[0][1]] != "--":
                            move = ce.Move(clickList, chessGame)
                            chessGame.makeMove(move)
                            pg.mixer.Sound.play(soundList["move-self"])
                            lastSquare = ()
                            clickList = []
                        else:
                            lastSquare = ()
                            clickList = []

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:  # Undo when 'R' is pressed
                    chessGame.undoMove()

        initiateGame(window, chessGame)
        clock.tick(fpsMax)
        pg.display.flip()


def initiateGame(window, game):
    placeBoard(window)
    placePieces(window, game.board)


def placeBoard(window):

    colors = [(124, 76, 52), (81, 42, 42)]
    for row in range(8):
        for column in range(8):

            color = colors[((row + column) % 2)]
            pg.draw.rect(
                window,
                color,
                pg.Rect(column * squareSize, row * squareSize, squareSize, squareSize),
            )


def placePieces(window, board):
    for row in range(8):
        for column in range(8):
            pieceName = board[row][column]
            if pieceName != "--":
                pieceImage = imageList[pieceName]
                window.blit(
                    pieceImage,
                    pg.Rect(
                        column * squareSize + (padding / 2),
                        row * squareSize + (padding / 2),
                        squareSize,
                        squareSize,
                    ),
                )


if __name__ == "__main__":
    main()
