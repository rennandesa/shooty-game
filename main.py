#!/usr/bin/env python

from gameplay.game import Game

if __name__ == "__main__":
    game = Game()

    while game.running:
        game.game_loop()
    

 