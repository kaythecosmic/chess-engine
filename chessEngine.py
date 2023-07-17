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
            self.whiteToPlay = not self.whiteToPlay

    def getValidMoves(self):
        return self.getPossibleMOves()

    def getPossibleMOves(self):
        moves = []
        for row in range(8):
            for column in range(8):
                playerTurn = self.board[row][column][0]
                if (playerTurn == "w" and self.whiteToPlay) or (
                    playerTurn == "b" and not self.whiteToPlay
                ):
                    piece = self.board[row][column][1]

                    # Getting Different piece moves
                    if piece == "P":
                        self.getPawnMoves(row, column, moves)

                    # elif piece == "R":
                    #     self.getRookMoves(row, column, moves)

                    # elif piece == "N":
                    #     self.getKnightMoves(row, column, moves)

                    # elif piece == "B":
                    #     self.getBishopMoves(row, column, moves)

                    # elif piece == "K":
                    #     self.getKingMoves(row, column, moves)

                    # elif piece == "Q":
                    #     self.getQueenMoves(row, column, moves)

        return moves

    def getPawnMoves(self, row, column, moves):

        # White pawn Moves
        if self.whiteToPlay:
            if row == 6 and self.board[row - 1][column] == "--":
                moves.append(Move([(row, column), (row - 1, column)], self.board))

                if self.board[row - 2][column] == "--":

                    moves.append(Move([(row, column), (row - 2, column)], self.board))

            elif self.board[row - 1][column] == "--":
                moves.append(Move([(row, column), (row - 1, column)], self.board))

            if column != 7 and column != 0:

                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(
                        Move([(row, column), (row - 1, column - 1)], self.board)
                    )
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(
                        Move([(row, column), (row - 1, column + 1)], self.board)
                    )

            elif column == 0:
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(
                        Move([(row, column), (row - 1, column + 1)], self.board)
                    )

            elif column == 7:
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(
                        Move([(row, column), (row - 1, column - 1)], self.board)
                    )

        # Black pawn Moves
        else:
            if row == 1 and self.board[row + 1][column] == "--":
                moves.append(Move([(row, column), (row + 1, column)], self.board))

                if self.board[row + 2][column] == "--":
                    moves.append(Move([(row, column), (row + 2, column)], self.board))

            elif self.board[row + 1][column] == "--":
                moves.append(Move([(row, column), (row + 1, column)], self.board))

            if column != 7 and column != 0:
                if (
                    self.board[row + 1][column - 1][0] == "w"
                    or self.board[row + 1][column + 1][0] == "w"
                ):
                    moves.append(
                        Move([(row, column), (row + 1, column - 1)], self.board)
                    )
                    moves.append(
                        Move([(row, column), (row + 1, column + 1)], self.board)
                    )
            elif column == 0:
                if self.board[row + 1][column - 1][0] == "b":
                    moves.append(
                        Move([(row, column), (row + 1, column + 1)], self.board)
                    )

            elif column == 7:
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(
                        Move([(row, column), (row + 1, column - 1)], self.board)
                    )

    def getRookMoves(self, row, column, moves):
        pass


class Move:

    rowToRank = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    colToFile = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    def __init__(self, moveCordinates, gameBoard):
        self.start = moveCordinates[0]
        self.end = moveCordinates[1]
        self.pieceMoved = gameBoard[self.start[0]][self.start[1]]
        self.pieceCaptured = gameBoard[self.end[0]][self.end[1]]
        self.moveString = self.convertChessNotation()

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveString == other.moveString
        return False

    def convertChessNotation(self):
        endRank = self.rowToRank[self.end[0]]
        endFile = self.colToFile[self.end[1]]

        startRank = self.rowToRank[self.start[0]]
        startFile = self.colToFile[self.start[1]]

        pieceName = self.pieceMoved[1]

        notationString = (
            str(pieceName)
            + str(startFile)
            + str(startRank)
            + str(endFile)
            + str(endRank)
        )

        return notationString
