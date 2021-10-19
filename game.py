import pygame as p

class Game():
    def __init__(self, bg):
        self.bg = bg
        self.bg.initiateStandardChess()
        #self.perft = perft

        p.init()

        self.running, self.playing = True, False
        self.whiteToMove = True
        self.WIDTH, self.HEIGHT = 512, 512
        self.DIMENSION = 8  # dimension of chess board 8 by 8
        self.SQ_SIZE = self.WIDTH // self.DIMENSION
        self.MAX_FPS = 15  # for animation later
        self.gameOver = False
        self.humanTurn = True
        self.moveMade = False  # flag variable for when a move is made
        self.animate = True
        self.sqSelected = ()
        self.playerClicks = []
        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = p.time.Clock()
        self.screen.fill(p.Color("white"))
        self.SQ_SIZE = self.WIDTH // self.DIMENSION
        self.location = ()
        self.IMAGES = {}
        self.load_images()

        self.validMoves = self.bg.getValidMoves(self.whiteToMove)

        # bg.



    def load_images(self):
        pieces = ["p", "r", "n", "b", "q", "k", "P", "R", "N", "B", "Q", "K", "F", "f"]
        for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(p.image.load("images/" + "w" + piece + ".png"),
                                              (self.SQ_SIZE, self.SQ_SIZE)) if piece.isupper() else p.transform.scale(
                p.image.load("images/" + "b" + piece + ".png"), (self.SQ_SIZE, self.SQ_SIZE))
        # Note: now we can access an images by saying 'IMAGES["wp"]'

    def game_loop(self):
        while self.playing:
            self.check_events()

    def check_events(self):
        for e in p.event.get():
            if e.type == p.QUIT:
                self.running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                self.location = p.mouse.get_pos()  # gets x and y position of mouse
                col = self.location[0] // self.SQ_SIZE
                row = self.location[1] // self.SQ_SIZE
                if self.sqSelected == (row, col):  # user clicked the same square twice
                    self.sqSelected = ()  # deselect
                    self.playerClicks = []  # clear player clicks
                else:
                    self.sqSelected = (row, col)
                    self.playerClicks.append(self.sqSelected)  # append for both first and 2nd clicks

                if len(self.playerClicks) == 2:  # after 2nd click
                    move = str(self.playerClicks[0][0]) + str(self.playerClicks[0][1]) + str(self.playerClicks[1][0]) + str(self.playerClicks[1][1])
                    possibleEP = self.bg.adjustMove(self.playerClicks[0][0], self.playerClicks[0][1], self.playerClicks[1][0], self.playerClicks[1][1], self.whiteToMove)
                    for i in range(0, len(self.validMoves), 4):
                        if move == self.validMoves[i:i + 4]:
                            self.bg.makeMove(move)
                            self.bg.drawArray()
                            self.moveMade = True
                            self.animate = True
                            self.sqSelected = ()  # reset user clicks
                            self.playerClicks = []
                            break
                        elif possibleEP != "" and possibleEP == self.validMoves[i:i + 4]:
                            self.bg.makeMove(possibleEP)
                            self.bg.drawArray()
                            self.moveMade = True
                            self.animate = True
                            self.sqSelected = ()  # reset user clicks
                            self.playerClicks = []
                            break
                    if not self.moveMade:
                        self.playerClicks = [self.sqSelected]
        if self.moveMade:
            self.moveMade = False
            self.whiteToMove = not self.whiteToMove
            self.validMoves = self.bg.getValidMoves(self.whiteToMove)

        self.drawGameState()
        self.clock.tick(self.MAX_FPS)
        p.display.flip()

    def highlightSquares(self):
        if self.sqSelected != ():
            r, c = self.sqSelected
            if self.bg.board[r][c][0].isupper() if self.whiteToMove else self.bg.board[r][c][0].islower():  # sqSelected is a piece that can be moved
                # Highlight selected square
                s = p.Surface((self.SQ_SIZE, self.SQ_SIZE))
                s.set_alpha(100)  # transparency value -> 0 = transparent; 255 -> opaque
                s.fill(p.Color('blue'))
                self.screen.blit(s, (c * self.SQ_SIZE, r * self.SQ_SIZE))
                # highlight moves from that square
                s.fill(p.Color('yellow'))
                for i in range(0, len(self.validMoves), 4):
                    move = self.validMoves[i:i + 4]
                    if int(move[0]) == r and int(move[1]) == c:
                        self.screen.blit(s, (int(move[3]) * self.SQ_SIZE, int(move[2]) * self.SQ_SIZE))

    def drawGameState(self):
        self.drawBoard()  # draw squares on board
        self.highlightSquares()

        # Note: for later, we can add in piece highlighting and move suggestions

        self.drawPieces()  # draw pieces on top of the squares

    def drawBoard(self):
        global colors
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                color = colors[((r + c) % 2)]
                p.draw.rect(self.screen, color, p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawPieces(self):
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = self.bg.board[r][c]
                if piece != " ":  # i.e if it's not an empty square
                    self.screen.blit(self.IMAGES[piece], p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def reset_keys(self):
        self.gameOver = False
        self.humanTurn = True
        self.moveMade = False  # flag variable for when a move is made
        self.whiteToMove = True





