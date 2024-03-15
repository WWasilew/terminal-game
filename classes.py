from random import randint


class NegativeLivesError(Exception):
    def __init__(self, lives):
        super().__init__('Life count cannot be negative')
        self.lives = lives


class NameError(Exception):
    pass


class NegativeHealthError(Exception):
    def __init__(self, health):
        super().__init__('Health cannot be negative')
        self.health = health


class InvalidHydraHeadError(Exception):
    def __init__(self, heads):
        super().__init__('Needs to have at least one head')
        self.head_count = heads


class Player:
    """
    Class Player. Contains attributes:
    :param name: player's name
    :type name: str

    :param: lives: player's lives, default = 0
    :type lives: int
    """
    def __init__(self, name, lives=1):
        """
        Creates instance of player.

        Raises ValueError if name is invalid or lives are negative
        """
        self._name = name
        lives = int(lives)
        if lives < 0:
            raise NegativeLivesError(lives)
        self._lives = lives

    def get_name(self):
        """
        Returns player's name.
        """
        return str(self._name)

    def set_name(self, new_name):
        """
        Sets player's name.

        Raises ValueError if there is not given any name.
        """
        if not new_name:
            raise NameError('Name cannot be empty')
        self._name = str(new_name).title()

    def get_lives(self):
        """
        Returns players's lives.
        """
        return self._lives

    def set_lives(self, new_lives):
        """
        Sets player's lives.
        """
        if new_lives < 0:
            raise NegativeLivesError(new_lives)
        self._lives = new_lives

    def info(self):
        """
        Returns basic desrition about player.
        """
        if self._lives == 1:
            lives = "life"
        else:
            lives = "lives"
        return f'My name is {self._name}. I have {self._lives} {lives} left.'

    def __str__(self):
        return self.info()


class Enemy:
    """
    Class Enemy. Contains attributes:
    :param name: enemy's name
    :type name: str

    :param: lives: enemy's lives
    :type health: int
    """

    def __init__(self, name, health):
        """
        Creates instance of Enemy.

        Raises ValueError if name is empty or health is negative.
        """
        if not name:
            raise NameError('Name cannot be empty')
        self._name = name
        health = int(health)
        if health < 0:
            raise NegativeHealthError(health)
        self._health = health

    def get_name(self):
        """
        Returns enemy's name.
        """
        return self._name

    def get_health(self):
        """
        Returns enemy's health points.
        """
        return self._health

    def set_name(self, new_name):
        """
        Sets enemy's name.

        Raises ValueError if there is not given any name
        """
        if not new_name:
            raise NameError('Name cannot be empty')
        self._name = new_name

    def set_health(self, new_health):
        """
        Sets enemy's health.
        """
        if new_health <= 0:
            self._health = 0
        else:
            self._health = new_health

    def __str__(self):
        name = self._name
        health = self._health
        return f'This is {name}. It has {health} health points left.'

    def take_damage(self, damage):
        """
        Reduces enemy's health.
        """
        damage = int(damage)
        if damage <= 0:
            raise ValueError('Damage has to be positive')
        self._health = max(0, self._health-damage)

    def is_alive(self):
        """
        Returns True if health is greater than zero.
        """
        return self._health > 0


class Hydra(Enemy):
    """
    Class Hydra. Contains attributes:
    :param name: enemy's name
    :type name: str

    :param lives: enemy's lives
    :type health: int

    :param heads: number of hydra's heads
    :type heads: int
    """

    def __init__(self, name, health, heads=1):
        """
        Creates instance of Hydra

        Raises ValueError if invalid number of heads are given
        """
        super().__init__(name, health)
        heads = int(heads)
        if heads < 1:
            raise InvalidHydraHeadError(heads)
        self._heads = heads
        self._base_health = health

    def get_heads(self):
        """
        Returns heads of Hydra.
        """
        return int(self._heads)

    def get_base_health(self):
        """
        Returns base health of hydra.
        """
        return int(self._base_health)

    def __str__(self):
        base = super().__str__()
        return f'{base} It has {self._heads} heads.'

    def regenerate(self, health_regen):
        """
        Changes value of health for hydra.
        """
        if health_regen < 0:
            raise ValueError("Cannot regenerate negative value")
        if health_regen == 0:
            return
        if self.get_health() >= self.get_base_health():
            return
        self._health = min(self._base_health, self._health + health_regen)


class DragonHydra(Hydra):
    def take_damage(self, damage):
        """
        DragonHydra has a chance to avoid taking damage.
        """
        if randint(0, 1):
            super().take_damage(damage)


class Game:
    def __init__(self, player, enemies=None):
        self.player = player
        if not enemies:
            self.enemies = []
        else:
            self.enemies = enemies
        self._result = None
