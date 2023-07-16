import os
import numpy as np


class GameStatus:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.whiteToPlay = True
        self.moveHistory = []
        
    def makeMove(self, move):
        self.board[move.start[0]][move.start[1]] = "--"
        self.board[move.end[0]][move.end[1]] = move.pieceMoved
        self.moveHistory.append(move)
        self.whiteToPlay = not self.whiteToPlay
        # print(self.moveHistory)
        
    def undoMove(self):
        if len(self.moveHistory) != 0:
            move = self.moveHistory.pop()
            self.board[move.start[0]][move.start[1]] = move.pieceMoved
            self.board[move.end[0]][move.end[1]] = move.pieceCaptured
        


class Move:

    rowToRank = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    colToFile = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    def __init__(self, moveCordinates, gameStatus):
        self.start = moveCordinates[0]
        self.end = moveCordinates[1]

        self.pieceMoved = gameStatus.board[self.start[0]][self.start[1]]
        self.pieceCaptured = gameStatus.board[self.end[0]][self.end[1]]
        self.moveString = self.convertChessNotation()

    def convertChessNotation(self):

        endRank = self.rowToRank[self.end[0]]
        endFile = self.colToFile[self.end[1]]

        startRank = self.rowToRank[self.start[0]]
        startFile = self.colToFile[self.start[1]]

        pieceName = self.pieceMoved[1]

        if self.pieceCaptured == "--":
            notationString = (
                str(pieceName)
                + str(startFile)
                + str(startRank)
                + str(endFile)
                + str(endRank)
            )
        else:
            notationString = (
                str(pieceName)
                + str(startFile)
                + str(startRank)
                + "x"
                + str(endFile)
                + str(endRank)
            )

        return notationString
