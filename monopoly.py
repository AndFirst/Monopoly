'''
This file init game.
'''


if __name__ == '__main__':
    from modules.game import Game
    from modules.interface import Interface
    from modules.gameplay import Gameplay
    game = Game()
    interface = Interface(game)
    monopoly = Gameplay(interface, game)
    monopoly.main()
