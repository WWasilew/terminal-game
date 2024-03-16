from classes import Game, Player, Enemy, Hydra, DragonHydra


def main():
    """
    Defining player's name and power of attack.

    Defining enemies.

    game.play(number of rounds)
    """
    player = Player('Adam Małysz', 102)
    enemies = [
        Enemy('Norbert Gierczak', 15),
        Hydra('Wonsz', 50, 1),
        DragonHydra('Wonsz rzeczny', 30, 3)
    ]
    game = Game(player, enemies)
    game.play(10)


if __name__ == "__main__":
    main()
