from random import randint, choice


class NegativePowerError(Exception):
    def __init__(self, power):
        super().__init__('Power value cannot be negative')
        self.power = power


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

    :param power: player's power, default = 5
    :type power: int
    """
    def __init__(self, name, power=5):
        """
        Creates instance of player.

        Raises ValueError if name is invalid or power value is negative
        """
        self._name = name
        power = int(power)
        if power < 0:
            raise NegativePowerError(power)
        self._power = power

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

    def get_power(self):
        """
        Returns players's power.
        """
        return self._power

    def set_power(self, new_power):
        """
        Sets player's power.
        """
        if new_power < 0:
            raise NegativePowerError(new_power)
        self._power = new_power

    def attack(self, enemies):
        """
        Chooses enemy from list of enemies.
        Calculates damage.
        Apply damage.
        """
        if self.get_power() == 0 or not enemies:
            return (None, 0, False)
        enemy = choice(enemies)
        damage = randint(1, self.get_power())
        took_damage = enemy.take_damage(damage)
        self.set_power(self.get_power()-1)
        return (enemy, damage, took_damage)

    def info(self):
        """
        Returns basic desrition about player.
        """
        if self._power == 1:
            power = "point"
        else:
            power = "points"
        return f'My name is {self._name}. I have {self._power} power {power}.'

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
        return True

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
        if self._heads == 1:
            singular = "head"
        else:
            singular = "heads"
        return f'{base} It has {self._heads} {singular}.'

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
            return super().take_damage(damage)
        return False


class Game:
    def __init__(self, player, enemies=None):
        self.player = player
        if not enemies:
            self.enemies = []
        else:
            self.enemies = enemies
        self._result = None

    def play(self, rounds):
        print('Starting the game!')
        print(self.player.__str__())
        print('My enemies: ')
        for all_enemies in self.enemies:
            print(all_enemies.__str__())
        for round in range(1, rounds+1):
            print(f'ROUND {round}:')
            print(f'Enemies remaining: {len(self.enemies)}')
            for enemies_left in self.enemies:
                print(f'{enemies_left.get_name()}, it has {enemies_left.get_health()} health left.')
            target, damage, status = self.player.attack(self.enemies)
            if target:
                if status:
                    print(f'ATTACK: {target.get_name()} took {damage} damage.')
                    if not target.is_alive():
                        print(f'{target.get_name()} died.')
                        self.enemies.remove(target)
                else:
                    print(f'{target.get_name()} did not take dmg.')
            else:
                break
        if self.enemies:
            self._result = True
            print('You lost the game!')
        else:
            self._result = False
            print('You won the game! No enemies left!')
