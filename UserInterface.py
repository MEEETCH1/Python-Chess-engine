import pygame as p
import BoardGeneration, Perft
import time

WIDTH = HEIGHT = 512
DIMENSION = 8           # dimension of chess board 8 by 8
SQ_SIZE = WIDTH//DIMENSION
MAX_FPS = 15            # for animation later
IMAGES = {}

def load_images():
    pieces = ["p", "r", "n", "b", "q", "k", "P", "R", "N", "B", "Q", "K", "F", "f"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + "w" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) if piece.isupper() else p.transform.scale(p.image.load("images/" + "b" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: now we can access an images by saying 'IMAGES["wp"]'

def GUI():
    whiteToMove = True
    running = True
    gameOver = False
    humanTurn = True
    moveMade = False  # flag variable for when a move is made
    animate = True
    sqSelected = ()
    playerClicks = []

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    bg = BoardGeneration.BoardGeneration()
    bg.initiateStandardChess()
    P = Perft.Pert()
    # start = time.perf_counter()
    # P.perftRoot(bg.WP,bg.WN,bg.WB,bg.WR,bg.WQ,bg.WK,bg.BP,bg.BN,bg.BB,bg.BR,bg.BQ,bg.BK,bg.EP,bg.CWK,bg.CWQ,bg.CBK,bg.CBQ,whiteToMove,0)
    # end = time.perf_counter()
    # print("Nodes: " + str(P.perftTotalMoveCounter))
    # print("That took: " + str(end - start) + " seconds")
    # print("Nodes per second: " + str(P.perftTotalMoveCounter // ((end-start))))

    validMoves = bg.getValidMoves(whiteToMove)
    # print(validMoves)

    load_images()
    drawGameState(screen, bg, validMoves, sqSelected, whiteToMove)

    while running == True:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # gets x and y position of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both first and 2nd clicks

                if len(playerClicks) == 2:  # after 2nd click
                    move = str(playerClicks[0][0]) + str(playerClicks[0][1]) + str(playerClicks[1][0]) + str(playerClicks[1][1])
                    possibleEP = bg.adjustMove(playerClicks[0][0],playerClicks[0][1],playerClicks[1][0],playerClicks[1][1],whiteToMove)
                    for i in range(0, len(validMoves), 4):
                        if move == validMoves[i:i+4]:
                            # print(move.getChessNotation())
                            # bg.updateEnPassant(move)
                            bg.makeMove(move)
                            bg.drawArray()
                            moveMade = True
                            animate = True
                            sqSelected = ()  # reset user clicks
                            playerClicks = []
                            break
                        elif possibleEP != "" and possibleEP == validMoves[i:i+4]:
                            bg.makeMove(possibleEP)
                            bg.drawArray()
                            moveMade = True
                            animate = True
                            sqSelected = ()  # reset user clicks
                            playerClicks = []
                            break
                    if not moveMade:
                        playerClicks = [sqSelected]
        if moveMade:
            moveMade = False
            whiteToMove = not whiteToMove
            validMoves = bg.getValidMoves(whiteToMove)

        drawGameState(screen, bg, validMoves, sqSelected, whiteToMove)

        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected, whiteToMove):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0].isupper() if whiteToMove else gs.board[r][c][0].islower(): # sqSelected is a piece that can be moved
            # Highlight selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)        # transparency value -> 0 = transparent; 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for i in range(0, len(validMoves), 4):
                move = validMoves[i:i+4]
                if int(move[0]) == r and int(move[1]) == c:
                    screen.blit(s, (int(move[3])*SQ_SIZE, int(move[2])*SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected, whiteToMove):
    drawBoard(screen)  # draw squares on board
    highlightSquares(screen, gs, validMoves, sqSelected, whiteToMove)

    # Note: for later, we can add in piece highlighting and move suggestions

    drawPieces(screen, gs.board)  # draw pieces on top of the squares

'''
Draw squares on board. in chess board, top left square always light 
'''

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != " ": # i.e if it's not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# if __name__ == "__main__":
#     main()
