from chess import UserInterface, BoardGeneration
from game import Game

g = Game(BoardGeneration.BoardGeneration())

def main():
    #UserInterface.GUI()

    g.playing = True
    while g.playing == True:
        g.game_loop()



if __name__ == "__main__":
    main()
