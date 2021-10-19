# import numpy as np

def reverse(x):
    x = ((x & 0x5555555555555555) << 1) | ((x & 0xAAAAAAAAAAAAAAAA) >> 1)
    x = ((x & 0x3333333333333333) << 2) | ((x & 0xCCCCCCCCCCCCCCCC) >> 2)
    x = ((x & 0x0F0F0F0F0F0F0F0F) << 4) | ((x & 0xF0F0F0F0F0F0F0F0) >> 4)
    x = ((x & 0x00FF00FF00FF00FF) << 8) | ((x & 0xFF00FF00FF00FF00) >> 8)
    x = ((x & 0x0000FFFF0000FFFF) << 16) | ((x & 0xFFFF0000FFFF0000) >> 16)
    x = ((x & 0xFFFFFFFF) << 32) | ((x & 0xFFFFFFFF00000000) >> 32)

    return x
def numberOfTrailingZeros(v):
    return (v & -v).bit_length() - 1

class Moves():
    def __init__(self):

        self.FILE_A = 9259542123273814144
        self.FILE_H = 72340172838076673
        self.FILE_AB = 13889313184910721216
        self.FILE_GH = 217020518514230019
        self.RANK_1 = 18374686479671623680
        self.RANK_4 = 1095216660480
        self.RANK_5 = 4278190080
        self.RANK_8 = 255
        self.CENTRE = 103481868288
        self.EXTENDED_CENTRE = 66229406269440
        self.KING_SPAN = 460039
        self.KNIGHT_SPAN = 43234889994
        self.NOT_MY_PIECES = 0
        self.MY_PIECES = 0
        self.OCCUPIED = 257
        self.EMPTY = 0
        self.CASTLE_ROOKS= [63, 56, 7, 0]
        self.RankMasks8 =  [0xFF, 0xFF00, 0xFF0000, 0xFF000000, 0xFF00000000, 0xFF0000000000, 0xFF000000000000,0xFF00000000000000]  # from rank1 torank8
        self.FileMasks8 = [ 0x101010101010101, 0x202020202020202, 0x404040404040404, 0x808080808080808,
                            0x1010101010101010, 0x2020202020202020, 0x4040404040404040, 0x8080808080808080]
        # from fileA toFileH
        self.DiagonalMasks8 = [0x1, 0x102, 0x10204, 0x1020408, 0x102040810, 0x10204081020, 0x1020408102040,
                               0x102040810204080, 0x204081020408000, 0x408102040800000, 0x810204080000000,
                               0x1020408000000000, 0x2040800000000000, 0x4080000000000000, 0x8000000000000000]
        # from top left to bottom right

        self.AntiDiagonalMasks8 = [0x80, 0x8040, 0x804020, 0x80402010, 0x8040201008, 0x804020100804, 0x80402010080402,
                      0x8040201008040201, 0x4020100804020100, 0x2010080402010000, 0x1008040201000000,
                      0x804020100000000, 0x402010000000000, 0x201000000000000, 0x100000000000000]
        # from top right to bottom left
    def makeMove(self, board, move, type):
        if move[3].isnumeric(): # regular move
            start = int(move[0])*8 + int(move[1])
            end = int(move[2])*8 + int(move[3])
            if ((board >> start)&1)==1:
                board &=~ (1<<start)
                board |= (1<<end)
            else:
                board &=~ (1 << end)
        elif move[3] == 'P':
            start = 0; end = 0
            if move[2].isupper():
                start = numberOfTrailingZeros(self.FileMasks8[int(move[0])] & self.RankMasks8[6])
                end = numberOfTrailingZeros(self.FileMasks8[int(move[1])] & self.RankMasks8[7])
            else:
                start = numberOfTrailingZeros(self.FileMasks8[int(move[0])] & self.RankMasks8[1])
                end = numberOfTrailingZeros(self.FileMasks8[int(move[1])] & self.RankMasks8[0])
            if type == move[2]:
                board |= (1 << end)
            else:
                board &= ~(1 << start)
                board &= ~(1 << end)
        elif move[3] == 'E' and (type == 'P' or type == 'p'):
            start = 0; end = 0
            if move[2] == 'W':
                start = numberOfTrailingZeros(self.FileMasks8[int(move[0])] & self.RankMasks8[3])
                end = numberOfTrailingZeros(self.FileMasks8[int(move[1])] & self.RankMasks8[2])
                board &= ~(self.FileMasks8[int(move[1])] & self.RankMasks8[3])
            else:
                start = numberOfTrailingZeros(self.FileMasks8[int(move[0])] & self.RankMasks8[4])
                end = numberOfTrailingZeros(self.FileMasks8[int(move[1])] & self.RankMasks8[5])
                board &= ~(self.FileMasks8[int(move[1])] & self.RankMasks8[4])
            if ((board>>start)&1)==1:
                board&=~(1<<start)
                board|=(1<<end)
            else:
                print("ERROR: Invalid move type")
        return board

    def makeMoveCastle(self, rookBoard, kingBoard, move, type):
        start = int(move[0]*8) + int(move[1])
        if ((kingBoard >> start) == 1) & ((move == "0402") | (move == "0406") | (move == "7472") | (move == "7476")):
            if type == 'R':
                if move == "7472":
                    rookBoard &=~ (1 << self.CASTLE_ROOKS[1])
                    rookBoard |= (1 << (self.CASTLE_ROOKS[1]+3))
                else:
                    rookBoard &= ~ (1 << self.CASTLE_ROOKS[0])
                    rookBoard |= (1 << (self.CASTLE_ROOKS[0] - 2))
            else:
                if move == "0402":
                    rookBoard &= ~ (1 << self.CASTLE_ROOKS[3])
                    rookBoard |= (1 << (self.CASTLE_ROOKS[3] + 3))
                else:
                    rookBoard &= ~ (1 << self.CASTLE_ROOKS[2])
                    rookBoard |= (1 << (self.CASTLE_ROOKS[2] - 2))

        return rookBoard
    def makeMoveEP(self, board, move):
        if move[3].isnumeric():
            start = int(move[0])*8 + int(move[1])
            if abs(int(move[0])-int(move[2])) == 2: # and ((board >> start) & 1) == 1:
                return self.FileMasks8[int(move[1])]
        return 0
    def HorizontalAndVerticalMoves(self, s):

        binaryS = 1 << s
        # return (self.OCCUPIED - 2 * binaryS) ^ reverse(reverse(self.OCCUPIED) - 2 * reverse(binaryS))
        possibilitiesHorizontal = (self.OCCUPIED - 2 * binaryS) ^ reverse(reverse(self.OCCUPIED) - 2 * reverse(binaryS))
        possibilitiesVertical = ((self.OCCUPIED & self.FileMasks8[s % 8]) - (2 * binaryS)) ^ reverse(reverse(self.OCCUPIED & self.FileMasks8[s % 8]) - (2 * reverse(binaryS)))
        return (possibilitiesHorizontal & self.RankMasks8[int(s/8)]) | (possibilitiesVertical & self.FileMasks8[s % 8])
    def DiagonalAndAntiDiagonalMoves(self, s):
        binaryS = 1 << s
        # return (self.OCCUPIED - 2 * binaryS) ^ reverse(reverse(self.OCCUPIED) - 2 * reverse(binaryS))
        possibilitiesDiagonal = ((self.OCCUPIED & self.DiagonalMasks8[int(s / 8) + (s % 8)]) - (2 * binaryS)) ^ reverse(reverse(self.OCCUPIED & self.DiagonalMasks8[int(s / 8) + (s % 8)]) - (2 * reverse(binaryS)))
        possibilitiesAntiDiagonal = ((self.OCCUPIED & self.AntiDiagonalMasks8[int(s / 8) + 7 - (s % 8)]) - (2 * binaryS)) ^ reverse(reverse(self.OCCUPIED & self.AntiDiagonalMasks8[int(s / 8) + 7 - (s % 8)]) - (2 * reverse(binaryS)))
        return (possibilitiesDiagonal & self.DiagonalMasks8[int(s / 8) + (s % 8)]) | (possibilitiesAntiDiagonal & self.AntiDiagonalMasks8[int(s / 8) + 7 - (s % 8)])
    def PossibleMovesW(self, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP, CWK, CWQ):
        self.NOT_MY_PIECES = ~(WP | WN | WB | WR | WQ | WK | BK)  # added BK to avoid illegal capture
        self.MY_PIECES = WP | WN | WB | WR | WQ  # omitted WK to avoid illegal capture
        self.OCCUPIED = WP | WN | WB | WR | WQ | WK | BP | BN | BB | BR | BQ | BK
        self.EMPTY=~self.OCCUPIED
        List = self.PossibleWP(WP, BP, EP) + \
               self.PossibleN(WN) + \
               self.PossibleB(WB) + \
               self.PossibleR(WR) + \
               self.PossibleQ(WQ) + \
               self.PossibleK(WK) + \
               self.PossibleCW(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, CWK, CWQ)
        return List
    def PossibleMovesB(self, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP, CBK, CBQ):
        self.NOT_MY_PIECES = ~(BP | BN | BB | BR | BQ | BK | WK)  # added WK to avoid illegal capture
        self.MY_PIECES = BP | BN | BB | BR | BQ  # omitted BK to avoid illegal capture
        self.OCCUPIED = WP | WN | WB | WR | WQ | WK | BP | BN | BB | BR | BQ | BK
        self.EMPTY = ~self.OCCUPIED
        List = self.PossibleBP(BP, WP, EP) + \
               self.PossibleN(BN) + \
               self.PossibleB(BB) + \
               self.PossibleR(BR) + \
               self.PossibleQ(BQ) + \
               self.PossibleK(BK) + \
               self.PossibleCB(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, CBK, CBQ);
        return List
    def PossibleWP(self, WP, BP, EP):
        list = ""
        PAWN_MOVES = (WP>>7) & self.NOT_MY_PIECES & self.OCCUPIED &~ self.RANK_8 &~ self.FILE_A # capture right
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 + 1)) + str(index % 8 - 1) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (WP >> 9) & self.NOT_MY_PIECES & self.OCCUPIED &~ self.RANK_8 &~ self.FILE_H # capture left
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 + 1)) + str(index % 8 + 1) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (WP >> 8) & self.EMPTY &~ self.RANK_8 # move 1 forward
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 + 1)) + str(index % 8) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (WP >> 16) & self.EMPTY & (self.EMPTY >> 8) & self.RANK_4 # move 2 forward
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 + 2)) + str(index % 8) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
    #     y1, y2, Promotion Type, "P"
        PAWN_MOVES = (WP >> 7) & self.NOT_MY_PIECES & self.OCCUPIED & self.RANK_8 & ~ self.FILE_A # pawn promotion by capture right
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 - 1) + str(index % 8) + "QP" + str(index % 8 - 1) + str(index % 8) + "RP" + str(index % 8 - 1) + str(index % 8) + "BP" + str(index % 8 - 1) + str(index % 8) + "NP"
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (WP >> 9) & self.NOT_MY_PIECES & self.OCCUPIED & self.RANK_8 & ~self.FILE_H # pawn promotion capture left
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 + 1) + str(index % 8) + "QP" + str(index % 8 + 1) + str(index % 8) + "RP" + str(index % 8 + 1) + str(index % 8) + "BP" + str(index % 8 + 1) + str(index % 8) + "NP"
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (WP >> 8) & self.EMPTY & self.RANK_8 # pawn promotion move 1 forward
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8) + str(index % 8) + "QP" + str(index % 8) + str(index % 8) + "RP" + str(index % 8) + str(index % 8) + "BP" + str(index % 8) + str(index % 8) + "NP"
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        # en passant right
        possibility = (WP << 1) & BP & self.RANK_5 & ~ self.FILE_A & EP # shows the piece to remove not the destination
        if possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 - 1) + str(index % 8) + "WE"

        possibility = (WP >> 1) & BP & self.RANK_5 & ~ self.FILE_H & EP # shows the piece to remove not the destination
        if possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 + 1) + str(index % 8) + "WE"
        return list
    def PossibleBP(self, BP, WP, EP):
        list = ""
        PAWN_MOVES = (BP<<7) & self.NOT_MY_PIECES & self.OCCUPIED &~ self.RANK_1 &~ self.FILE_H # capture right
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 - 1)) + str(index % 8 + 1) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (BP << 9) & self.NOT_MY_PIECES & self.OCCUPIED &~ self.RANK_1 &~ self.FILE_A # capture left
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 - 1)) + str(index % 8 - 1) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (BP << 8) & self.EMPTY &~ self.RANK_1 # move 1 forward
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 - 1)) + str(index % 8) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (BP << 16) & self.EMPTY & (self.EMPTY << 8) & self.RANK_5 # move 2 forward
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(int(index / 8 - 2)) + str(index % 8) + str(int(index / 8)) + str(index % 8)
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

    #     y1, y2, Promotion Type, "P"
        PAWN_MOVES = (BP << 7) & self.NOT_MY_PIECES & self.OCCUPIED & self.RANK_1 & ~ self.FILE_H # pawn promotion by capture right
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 + 1) + str(index % 8) + "qP" + str(index % 8 + 1) + str(index % 8) + "rP" + str(index % 8 + 1) + str(index % 8) + "bP" + str(index % 8 + 1) + str(index % 8) + "nP"
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (BP << 9) & self.NOT_MY_PIECES & self.OCCUPIED & self.RANK_1 & ~self.FILE_A # pawn promotion capture left
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 - 1) + str(index % 8) + "qP" + str(index % 8 - 1) + str(index % 8) + "rP" + str(index % 8 - 1) + str(index % 8) + "bP" + str(index % 8 - 1) + str(index % 8) + "nP"
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)

        PAWN_MOVES = (BP << 8) & self.EMPTY & self.RANK_1 # pawn promotion move 1 forward
        possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        while possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8) + str(index % 8) + "qP" + str(index % 8) + str(index % 8) + "rP" + str(index % 8) + str(index % 8) + "bP" + str(index % 8) + str(index % 8) + "nP"
            PAWN_MOVES &= ~possibility
            possibility = PAWN_MOVES & ~(PAWN_MOVES - 1)
        # en passant right
        possibility = (BP >> 1) & WP & self.RANK_4 & ~ self.FILE_H & EP # shows the piece to remove not the destination
        if possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 + 1) + str(index % 8) + "BE"

        possibility = (BP << 1) & WP & self.RANK_4 & ~ self.FILE_A & EP # shows the piece to remove not the destination
        if possibility != 0:
            index = numberOfTrailingZeros(possibility)
            list += "" + str(index % 8 - 1) + str(index % 8) + "BE"
        return list
    def PossibleN(self, N):
        list = ""
        i = N &~(N-1)
        possibility = 0
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            if (iLocation > 18):
                possibility = self.KNIGHT_SPAN << (iLocation-18)
            else:
                possibility = self.KNIGHT_SPAN >> (18-iLocation)

            if (iLocation%8 < 4):
                possibility &= ~self.FILE_AB & self.NOT_MY_PIECES
            else:
                possibility &= ~self.FILE_GH & self.NOT_MY_PIECES

            j = possibility &~ (possibility-1)
            while j !=0:
                index = numberOfTrailingZeros(j)
                if index < 64:
                    list += "" + str(int(iLocation / 8)) + str(iLocation % 8) + str(int(index / 8)) + str(index % 8)
                    possibility &= ~j
                    j = possibility & ~(possibility - 1)
                else:
                    break


            N &= ~i
            i = N & ~(N - 1)

        return list
    def PossibleB(self, B):
        list = ""
        i = B&~(B-1)
        possibility = 0
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            possibility = self.DiagonalAndAntiDiagonalMoves(iLocation) & self.NOT_MY_PIECES
            j = possibility &~ (possibility-1)
            while j != 0:
                index = numberOfTrailingZeros(j)
                list += "" + str(int(iLocation / 8)) + str(iLocation % 8) + str(int(index / 8)) + str(index % 8)
                possibility &= ~j
                j = possibility & ~(possibility - 1)

            B &= ~i
            i = B & ~(B - 1)
        return list
    def PossibleR(self, R):
        list = ""
        i = R&~(R-1)
        possibility = 0
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            possibility = self.HorizontalAndVerticalMoves(iLocation) & self.NOT_MY_PIECES
            j = possibility &~ (possibility-1)
            while j != 0:
                index = numberOfTrailingZeros(j)
                list += "" + str(int(iLocation / 8)) + str(iLocation % 8) + str(int(index / 8)) + str(index % 8)
                possibility &= ~j
                j = possibility & ~(possibility - 1)

            R &= ~i
            i = R & ~(R - 1)
        return list
    def PossibleQ(self, Q):
        list = ""
        i = Q&~(Q-1)
        possibility = 0
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            possibility = (self.HorizontalAndVerticalMoves(iLocation) | self.DiagonalAndAntiDiagonalMoves(iLocation)) & self.NOT_MY_PIECES
            j = possibility &~ (possibility-1)
            while j != 0:
                index = numberOfTrailingZeros(j)
                list += "" + str(int(iLocation / 8)) + str(iLocation % 8) + str(int(index / 8)) + str(index % 8)
                possibility &= ~j
                j = possibility & ~(possibility - 1)

            Q &= ~i
            i = Q & ~(Q - 1)
        return list
    def PossibleK(self, K):
        list = ""
        iLocation = numberOfTrailingZeros(K)
        possibility = 0
        if iLocation > 9:
            possibility = self.KING_SPAN << (iLocation-9)
        else:
            possibility = self.KING_SPAN >> (9 - iLocation)

        if iLocation%8 < 4:
            possibility &= ~self.FILE_AB & self.NOT_MY_PIECES

        else:
            possibility &= ~self.FILE_GH & self.NOT_MY_PIECES

        j = possibility & ~ (possibility - 1)
        while j != 0:
            index = numberOfTrailingZeros(j)
            if index < 64:
                list += "" + str(int(iLocation / 8)) + str(iLocation % 8) + str(int(index / 8)) + str(index % 8)
                possibility &= ~j
                j = possibility & ~(possibility - 1)
            else:
                break
        return list
    def PossibleCW(self, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, CWK, CWQ):
        list = ""
        UNSAFE = self.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK)
        if UNSAFE & WK == 0:
            if CWK & ((1 << self.CASTLE_ROOKS[0]) & WR)!=0:
                if (self.OCCUPIED | UNSAFE) & ((1 << 61) | (1 << 62)) == 0:
                    list += "7476"
            if CWQ & (((1 << self.CASTLE_ROOKS[1]) & WR) != 0):
                if ((self.OCCUPIED | (UNSAFE & ~(1 << 57))) & ((1 << 57) | (1 << 58) | (1 << 59))) == 0:
                    list += "7472"
        return list
    def PossibleCB(self, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, CBK, CBQ):
        list = ""
        UNSAFE = self.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK)
        if UNSAFE & BK == 0:
            if CBK & ((1 << self.CASTLE_ROOKS[2]) & BR) != 0:
                if (self.OCCUPIED | UNSAFE) & ((1 << 5) | (1 << 6)) == 0:
                    list += "0406"
            if CBQ & (((1 << self.CASTLE_ROOKS[3]) & BR) != 0):
                if ((self.OCCUPIED | (UNSAFE & ~(1 << 1))) & ((1 << 1) | (1 << 2) | (1 << 3))) == 0:
                    list += "0402"
        return list
    def unsafeForWhite(self, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK):
        unsafe = 0
        self.OCCUPIED=WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK
        # pawn
        unsafe = (BP<<7)&~ self.FILE_H # pawn capture right
        unsafe |= (BP<<9)&~ self.FILE_A # pawn capture left
        possibility = 0
        # knight
        i = BN & ~(BN - 1)
        while i != 0:
            iLocation= numberOfTrailingZeros(i)
            if iLocation > 18:
                possibility = self.KNIGHT_SPAN << (iLocation - 18)
            else:
                possibility = self.KNIGHT_SPAN >> (18 - iLocation)
            if iLocation % 8 < 4:
                possibility &= ~ self.FILE_AB
            else:
                possibility &= ~ self.FILE_GH

            unsafe |= possibility
            BN&=~i
            i=BN&~(BN-1)
        # bishop/queen
        QB = BQ | BB
        i = QB & ~(QB - 1)
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            possibility = self.DiagonalAndAntiDiagonalMoves(iLocation)
            unsafe |= possibility
            QB &= ~i
            i = QB & ~(QB - 1)
        # rook/queen
        QR = BQ|BR
        i = QR&~(QR-1)
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            possibility = self.HorizontalAndVerticalMoves(iLocation)
            unsafe |= possibility
            QR &= ~ i
            i = QR &~ (QR-1)
        # king
        iLocation = numberOfTrailingZeros(BK)
        if iLocation > 9:

            possibility = self.KING_SPAN<<(iLocation-9)
        else:
            possibility = self.KING_SPAN>>(9-iLocation)

        if iLocation%8<4:

            possibility &=~ self.FILE_AB
        else:
            possibility &=~ self.FILE_GH

        unsafe |= possibility

        return unsafe
    def unsafeForBlack(self, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK):
        unsafe = 0
        self.OCCUPIED = WP | WN | WB | WR | WQ | WK | BP | BN | BB | BR | BQ | BK
        # pawn
        unsafe = (WP >> 7) & ~ self.FILE_A  # pawn capture right
        unsafe |= (WP >> 9) & ~ self.FILE_H  # pawn capture left
        possibility = 0
        # knight
        i = WN & ~(WN - 1)
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            if iLocation > 18:
                possibility = self.KNIGHT_SPAN << (iLocation - 18)
            else:
                possibility = self.KNIGHT_SPAN >> (18 - iLocation)
            if iLocation % 8 < 4:
                possibility &= ~ self.FILE_AB
            else:
                possibility &= ~ self.FILE_GH

            unsafe |= possibility
            WN &= ~i
            i = WN & ~(WN - 1)
        # bishop/queen
        QB = WQ | WB
        i = QB & ~(QB - 1)
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            possibility = self.DiagonalAndAntiDiagonalMoves(iLocation)
            unsafe |= possibility
            QB &= ~i
            i = QB & ~(QB - 1)
        # rook/queen
        QR = WQ | WR
        i = QR & ~(QR - 1)
        while i != 0:
            iLocation = numberOfTrailingZeros(i)
            possibility = self.HorizontalAndVerticalMoves(iLocation)
            unsafe |= possibility
            QR &= ~ i
            i = QR & ~ (QR - 1)
        # king
        iLocation = numberOfTrailingZeros(WK)
        if iLocation > 9:

            possibility = self.KING_SPAN << (iLocation - 9)
        else:
            possibility = self.KING_SPAN >> (9 - iLocation)

        if iLocation % 8 < 4:

            possibility &= ~ self.FILE_AB
        else:
            possibility &= ~ self.FILE_GH

        unsafe |= possibility

        return unsafe











