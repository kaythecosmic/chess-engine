import chessEngine as ce
import pygame as pg
import numpy as np

# Initializing Board variables

height = width = 800
squareSize = 100
fpsMax = 15
imageList = {}
padding = 30


# Loading images into a dictionary


def imageLoad():
    pieceList = ["wQ", "wK", "wB", "wN", "wR", "wP", "bQ", "bK", "bB", "bN", "bR", "bP"]
    for piece in pieceList:
        imageList[piece] = pg.transform.scale(
            pg.image.load("assets/pieces/" + piece + ".png"),
            (squareSize - padding, squareSize - padding),
        )


def main():
    # pygame setup (from Documentation)
    pg.init()
    window = pg.display.set_mode((width, height))
    window.fill("white")
    clock = pg.time.Clock()
    imageLoad()
    running = True
    chessGame = ce.GameStatus()

    clickList = []
    lastSquare = ()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                click = pg.mouse.get_pos()  # click cordinates raw
                selColumn = click[0] // squareSize
                selRow = click[1] // squareSize

                print(selColumn, selRow)

                if lastSquare == (selRow, selColumn):
                    clickList = []
                    lastSquare = ()
                else:
                    lastSquare = (selRow, selColumn)
                    clickList.append(lastSquare)

                    if len(clickList) == 2:
                        move = ce.Move(clickList, chessGame)
                        chessGame.makeMove(move)
                        lastSquare = ()
                        clickList = []

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
