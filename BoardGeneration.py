import Moves

M = Moves.Moves()

class BoardGeneration():

    def __init__(self):

        self.board = [[]]

        self.WP = 0
        self.WN = 0
        self.WB = 0
        self.WR = 0
        self.WQ = 0
        self.WK = 0
        self.BP = 0
        self.BN = 0
        self.BB = 0
        self.BR = 0
        self.BQ = 0
        self.BK = 0
        self.WF = 0
        self.BF = 0
        self.EP = 0

        self.CWK = 1
        self.CWQ = 1
        self.CBK = 1
        self.CBQ = 1


        self.EMPTY = 0

        # self.boards = [self.WP, self.WN, self.WB, self.WR, self.WQ, self.WQ, self.WK, self.BP, self.BN, self.BB, self.BR, self.BQ, self.BQ, self.BK]

        # self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
        #                       'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.pieceBitBoards = {'P': self.WP, 'N': self.WN, 'B': self.WB, 'R': self.WR, 'Q': self.WQ, 'K': self.WK, 'F': self.WF,
                               'p': self.WP, 'n': self.WN, 'b': self.WB, 'r': self.WR, 'q': self.WQ, 'k': self.WK, 'f': self.BF,
                               ' ': self.EMPTY}
    def initiateStandardChess(self):

        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]]

        self.arrayToBitboards()
    def initiateChess960(self):
        pass
    def initiateFishChess(self):

        self.board = [
            ["f", "f", "f", "f", "k", "f", "f", "f"],
            ["f", "f", "f", "f", "f", "f", "f", "f"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["F", "F", "F", "F", "F", "F", "F", "F"],
            ["F", "F", "F", "F", "K", "F", "F", "F"]]

        self.arrayToBitboards()
    def adjustMove(self, sr, sc, er, ec, whiteToMove): # startrow, startcol, endrow, endcol
        possibleEP = ""
        move = str(sr)+str(sc)+str(er)+str(ec)
        if (abs(er-sr) == 1 and abs(ec-sc)==1):
            if whiteToMove:
                possibleEP = str(sc) + str(ec) + 'WE'
            else:
                possibleEP = str(sc) + str(ec) + 'BE'

        return possibleEP
    # def updateEnPassant(self,move):
    #     self.EP = M.makeMoveEP(self.WP|self.BP,move)
    def getValidMoves(self,whiteToMove):
        if whiteToMove:
            validMoves = M.PossibleMovesW(self.WP,self.WN,self.WB,self.WR,self.WQ,self.WK,self.BP,self.BN,self.BB,self.BR,self.BQ,self.BK, self.EP, self.CWK, self.CWQ)
        else:
            validMoves = M.PossibleMovesB(self.WP,self.WN,self.WB,self.WR,self.WQ,self.WK,self.BP,self.BN,self.BB,self.BR,self.BQ,self.BK, self.EP, self.CBK, self.CBQ)
        return validMoves
    def makeMove(self, move):

        self.WP = M.makeMove(self.WP, move, 'P')
        self.WN = M.makeMove(self.WN, move, 'N')
        self.WB = M.makeMove(self.WB, move, 'B')
        self.WR = M.makeMove(self.WR, move, 'R')
        self.WQ = M.makeMove(self.WQ, move, 'Q')
        self.WK = M.makeMove(self.WK, move, 'K')

        self.BP = M.makeMove(self.BP, move, 'p')
        self.BN = M.makeMove(self.BN, move, 'n')
        self.BB = M.makeMove(self.BB, move, 'b')
        self.BR = M.makeMove(self.BR, move, 'r')
        self.BQ = M.makeMove(self.BQ, move, 'q')
        self.BK = M.makeMove(self.BK, move, 'k')
        self.EP = M.makeMoveEP(self.WP | self.BP, move)


    def arrayToBitboards(self):
        i = 0
        for i in range(64):
            piece = self.board[int(i/8)][i%8]
            Binary = "0000000000000000000000000000000000000000000000000000000000000000"
            Binary = Binary[i:63] + "1" + Binary[0:i]
            self.pieceBitBoards[piece] += int(Binary, 2)

        self.WP = self.pieceBitBoards['P']
        self.WN = self.pieceBitBoards['N']
        self.WB = self.pieceBitBoards['B']
        self.WR = self.pieceBitBoards['R']
        self.WQ = self.pieceBitBoards['Q']
        self.WK = self.pieceBitBoards['K']
        self.WF = self.pieceBitBoards['F']

        self.BP = self.pieceBitBoards['p']
        self.BN = self.pieceBitBoards['n']
        self.BB = self.pieceBitBoards['b']
        self.BR = self.pieceBitBoards['r']
        self.BQ = self.pieceBitBoards['q']
        self.BK = self.pieceBitBoards['k']
        self.BF = self.pieceBitBoards['f']

        self.drawArray()
    def convertStringToBitboard(self, Binary):
        return int(Binary, 2)
    def drawArray(self):
        chessBoard = [[" "] * 8 for i in range(8)]

        i = 0
        for i in range(64):
            if self.WP >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "P"
            if self.WN >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "N"
            if self.WB >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "B"
            if self.WR >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "R"
            if self.WQ >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "Q"
            if self.WK >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "K"
            if self.BP >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "p"
            if self.BN >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "n"
            if self.BB >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "b"
            if self.BR >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "r"
            if self.BQ >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "q"
            if self.BK >> i & 1 == 1: chessBoard[int(i/8)][i % 8] = "k"

            if self.WF >> i & 1 == 1: chessBoard[int(i / 8)][i % 8] = "F"
            if self.BF >> i & 1 == 1: chessBoard[int(i / 8)][i % 8] = "f"

            self.board = chessBoard

        # print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #                  for row in chessBoard]))












