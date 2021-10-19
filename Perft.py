import Moves, BoardGeneration
M = Moves.Moves()
bg = BoardGeneration.BoardGeneration()

class Pert:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # cool way to reverse a dictionary

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self):
        self.perftTotalMoveCounter = 0
        self.perftMoveCounter = 0
        self.perftMaxDepth = 2
    def getChessNotation(self, move):
        # can add more to this function to make it real chess notation
        return self.getRankFile(int(move[0]), int(move[1])) + self.getRankFile(int(move[2]), int(move[3]))
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    def perftRoot(self, WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ, whiteToMove,depth):
        if whiteToMove:
            Moves = M.PossibleMovesW(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP, CWK, CWQ)
        else:
            Moves = M.PossibleMovesB(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP, CBK, CBQ)
        i = 0
        for i in range(0, len(Moves), 4):
            move = Moves[i:i + 4]
            WPt = M.makeMove(WP, move, 'P')
            WNt = M.makeMove(WN, move, 'N')
            WBt = M.makeMove(WB, move, 'B')
            WRt = M.makeMove(WR, move, 'R')
            WQt = M.makeMove(WQ, move, 'Q')
            WKt = M.makeMove(WK, move, 'K')

            BPt = M.makeMove(BP, move, 'p')
            BNt = M.makeMove(BN, move, 'n')
            BBt = M.makeMove(BB, move, 'b')
            BRt = M.makeMove(BR, move, 'r')
            BQt = M.makeMove(BQ, move, 'q')
            BKt = M.makeMove(BK, move, 'k')

            EPt = M.makeMoveEP(WP | BP, move)

            WRt = M.makeMoveCastle(WRt, WK | BK, move, 'R')
            BRt = M.makeMoveCastle(BRt, WK | BK, move, 'R')

            CWKt = CWK
            CWQt = CWQ
            CBKt = CBK
            CBQt = CBQ

            if move[3].isnumeric():
                start = int(move[0]) * 8 + int(move[1])
                if ((1 << start) & WK) != 0:
                    CWKt = False; CWQt = False
                elif ((1 << start) & BK) != 0:
                    CBKt = False; CBQt = False
                elif ((1 << start) & WR & (1 << M.CASTLE_ROOKS[0])) != 0:
                    CWKt = False
                elif ((1 << start) & WR & (1 << M.CASTLE_ROOKS[1])) != 0:
                    CWQt = False
                elif ((1 << start) & BR & (1 << M.CASTLE_ROOKS[2])) != 0:
                    CBKt = False
                elif ((1 << start) & BR & 1) != 0:
                    CBQt = False

            if ((WKt & M.unsafeForWhite(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt)) == 0 and whiteToMove) | \
                ((BKt & M.unsafeForBlack(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt)) == 0 and not whiteToMove):
                self.perft(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt, EPt, CWKt, CWQt, CBKt,
                      CBQt, not whiteToMove, depth + 1)
                print(self.getChessNotation(move) + " " + str(self.perftMoveCounter))
                self.perftTotalMoveCounter += self.perftMoveCounter
                self.perftMoveCounter = 0
    def perft(self, WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ, whiteToMove,depth):
        if depth < self.perftMaxDepth:
            moves = ""
            if whiteToMove:
                Moves = M.PossibleMovesW(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP, CWK, CWQ)
            else:
                Moves = M.PossibleMovesB(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP, CBK, CBQ)

            i = 0
            for i in range(0, len(Moves), 4):
                move = Moves[i:i + 4]
                WPt = M.makeMove(WP, move, 'P')
                WNt = M.makeMove(WN, move, 'N')
                WBt = M.makeMove(WB, move, 'B')
                WRt = M.makeMove(WR, move, 'R')
                WQt = M.makeMove(WQ, move, 'Q')
                WKt = M.makeMove(WK, move, 'K')

                BPt = M.makeMove(BP, move, 'p')
                BNt = M.makeMove(BN, move, 'n')
                BBt = M.makeMove(BB, move, 'b')
                BRt = M.makeMove(BR, move, 'r')
                BQt = M.makeMove(BQ, move, 'q')
                BKt = M.makeMove(BK, move, 'k')

                EPt = M.makeMoveEP(WP | BP, move)

                WRt = M.makeMoveCastle(WRt, WK | BK, move, 'R')
                BRt = M.makeMoveCastle(BRt, WK | BK, move, 'R')

                CWKt = CWK
                CWQt = CWQ
                CBKt = CBK
                CBQt = CBQ

                if move[3].isnumeric():
                    start = int(move[0]) * 8 + int(move[1])

                    if ((1 << start) & WK) != 0: CWKt=False; CWQt=False
                    elif ((1 << start) & BK) != 0: CBKt= False; CBQt= False
                    elif ((1 << start) & WR & (1 << 63)) != 0: CWKt= False
                    elif ((1 << start) & WR & (1 << 56)) != 0: CWQt=False
                    elif ((1 << start) & BR & (1 << 7)) != 0: CBKt= False
                    elif ((1 << start) & BR & 1) != 0: CBQt = False

                if ((WKt & M.unsafeForWhite(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt,BKt)) == 0 and whiteToMove) or \
                        ((BKt & M.unsafeForBlack(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt,BKt)) == 0 and  (not whiteToMove)):
                    if depth + 1 == self.perftMaxDepth:
                        self.perftMoveCounter += 1
                    self.perft(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt, EPt, CWKt, CWQt, CBKt, CBQt, (not whiteToMove), depth + 1)







