import pytest
from classes import Game, Player, Enemy, Hydra, DragonHydra
from classes import (
    NegativePowerError,
    NameError,
    NegativeHealthError)


def test_create_player():
    player = Player('Jurek Ogórek')
    assert player._name == "Jurek Ogórek"
    assert player._power == 5


def test_create_player_with_power():
    player = Player('Jurek Ogórek', 4)
    assert player._name == 'Jurek Ogórek'
    assert player._power == 4


def test_create_player_with_negative_power():
    with pytest.raises(NegativePowerError):
        Player('Jurek Ogórek', -1)


def test_introduce():
    player = Player('Jurek Ogórek', 3)
    assert player.info() == 'My name is Jurek Ogórek. I have 3 power points.'
    player = Player('Jurek Ogórek', 1)
    assert player.info() == 'My name is Jurek Ogórek. I have 1 power point.'


def test_intoduce_as_str():
    player = Player('Jurek Ogórek', 3)
    assert str(player) == player.info()
    player = Player('Jurek Ogórek', 1)
    assert str(player) == player.info()


def test_set_name():
    player = Player('Jurek Ogórek')
    assert player.get_name() == 'Jurek Ogórek'
    player.set_name('Karolina Malina')
    assert player.get_name() == 'Karolina Malina'


def test_set_name_empty():
    player = Player('Jurek Ogórek')
    with pytest.raises(NameError):
        player.set_name('')


def test_set_name_lowercase():
    player = Player('Jurek Ogórek')
    assert player.get_name() == 'Jurek Ogórek'
    player.set_name('karolina malina')
    assert player.get_name() == 'Karolina Malina'


def test_get_name():
    player = Player('Jurek Ogórek')
    assert player.get_name() == 'Jurek Ogórek'


def test_set_power():
    player = Player('Jurek Ogórek', 1)
    assert player.get_power() == 1
    player.set_power(2)
    assert player.get_power() == 2


def test_set_power_zero():
    player = Player('Jurek Ogórek', 1)
    assert player.get_power() == 1
    player.set_power(0)
    assert player.get_power() == 0


def test_set_power_negative():
    player = Player('Jurek Ogórek', 1)
    assert player.get_power() == 1
    with pytest.raises(NegativePowerError):
        player.set_power(-1)


def test_attack():
    player = Player('Jurek Ogórek')
    assert player.get_power() == 5
    orc = Enemy('Norbert Gierczak', 10)
    assert orc.get_health() == 10
    enemies = [orc]
    (target, damage, status) = player.attack(enemies)
    assert status is True
    assert target == orc
    assert player.get_power() == 4
    assert orc.get_health() < 10
    assert orc.get_health() == 10-damage


def test_attack_choice():
    player = Player('Jurek Ogórek')
    assert player.get_power() == 5
    orc1 = Enemy('Norbert Gierczak', 10)
    orc2 = Enemy("disstream", 20)
    base_health = {orc1: 10, orc2: 20}
    enemies = [orc1, orc2]
    (target, damage, status) = player.attack(enemies)
    assert status is True
    assert player.get_power() == 4
    assert target in enemies
    assert damage > 0
    assert target.get_health() < base_health[target]
    assert target.get_health() == base_health[target] - damage


def test_attack_choose_enemy(monkeypatch):
    player = Player('Jurek Ogórek')
    assert player.get_power() == 5
    orc1 = Enemy('Norbert Gierczak', 10)
    orc2 = Enemy("disstream", 20)
    enemies = [orc1, orc2]

    def get_orc(topory):
        return orc2
    monkeypatch.setattr('classes.choice', get_orc)
    (target, damage, status) = player.attack(enemies)
    assert damage > 0
    assert status is True
    assert player.get_power() == 4
    assert target == orc2
    assert orc1.get_health() == 10 or orc2.get_health() == 20 - damage


def test_attack_no_power():
    player = Player('Jurek Ogórek', 0)
    assert player.get_power() == 0
    orc = Enemy('Norbert Gierczak', 10)
    assert orc.get_health() == 10
    enemies = [orc]
    (target, damage, status) = player.attack(enemies)
    assert status is False
    assert damage == 0
    assert target is None
    assert player.get_power() == 0
    assert orc.get_health() == 10


def test_attack_power_eq_1():
    player = Player('Jurek Ogórek', 1)
    assert player.get_power() == 1
    orc = Enemy('Norbert Gierczak', 10)
    assert orc.get_health() == 10
    enemies = [orc]
    (target, damage, status) = player.attack(enemies)
    assert damage == 1
    assert target == orc
    assert status is True
    assert player.get_power() == 0
    assert orc.get_health() == 10 - damage


def test_attack_power(monkeypatch):
    player = Player('Jurek Ogórek')
    assert player.get_power() == 5
    orc = Enemy('Norbert Gierczak', 10)
    assert orc.get_health() == 10
    enemies = [orc]

    def power_2(topory, topor):
        return 2
    monkeypatch.setattr('classes.randint', power_2)
    (target, damage, status) = player.attack(enemies)
    assert status is True
    assert damage == 2
    assert target == orc
    assert player.get_power() == 4
    assert orc.get_health() == 10 - damage


def test_attack_set_power():
    player = Player('jurek Ogórek')
    assert player.get_power() == 5
    player.set_power(10)
    assert player.get_power() == 10


def test_enemy_create():
    enemy = Enemy('Orc', 50)
    assert enemy.get_name() == 'Orc'
    assert enemy.get_health() == 50


def test_enemy_create_negative_health():
    with pytest.raises(NegativeHealthError):
        Enemy('Orc', -10)


def test_enemy_create_without_name():
    with pytest.raises(NameError):
        Enemy('', 10)


def test_enemy_set_name():
    enemy = Enemy('orc', 50)
    assert enemy.get_name() == 'orc'
    enemy.set_name('dragon')
    assert enemy.get_name() == 'dragon'


def test_enemy_set_name_empty():
    enemy = Enemy('orc', 50)
    with pytest.raises(NameError):
        enemy.set_name('')


def test_enemy_set_health():
    enemy = Enemy('orc', 50)
    assert enemy.get_health() == 50
    enemy.set_health(60)
    assert enemy.get_health() == 60


def test_enemy_set_health_negative():
    enemy = Enemy('orc', 50)
    assert enemy.get_health() == 50
    enemy.set_health(-10)
    assert enemy.get_health() == 0


def test_enemy_description():
    enemy = Enemy('orc', 50)
    assert str(enemy) == 'This is orc. It has 50 health points left.'


def test_enemy_take_damage():
    enemy = Enemy('orc', 50)
    assert enemy.get_health() == 50
    assert enemy.take_damage(10) is True
    assert enemy.get_health() == 40


def test_enemy_take_damage_invalid():
    enemy = Enemy('orc', 50)
    with pytest.raises(ValueError):
        enemy.take_damage(-10)
    with pytest.raises(ValueError):
        enemy.take_damage(0)


def test_enemy_take_damage_below_zero():
    enemy = Enemy('orc', 10)
    assert enemy.get_health() == 10
    assert enemy.take_damage(20) is True
    assert enemy.get_health() == 0


def test_enemy_is_alive_true():
    enemy = Enemy('orc', 10)
    assert enemy.get_health() == 10
    assert enemy.is_alive()


def test_enemy_is_alive_false():
    enemy = Enemy('orc', 0)
    assert enemy.get_health() == 0
    assert not enemy.is_alive()


def test_hydra_create():
    hydra = Hydra('Norbert', health=100, heads=3)
    assert hydra.get_name() == 'Norbert'
    assert hydra.get_health() == 100
    assert hydra.get_heads() == 3
    assert hydra.get_base_health() == 100


def test_hydra_heads():
    hydra = Hydra('Norbert', health=200, heads=3)
    assert hydra.get_heads() == 3


def test_hydra_create_default_heads():
    hydra = Hydra('Norbert', health=200)
    assert hydra.get_heads() == 1


def test_hydra_description():
    hydra = Hydra('three-headed-hydra', health=100, heads=3)
    assert str(hydra) == 'This is three-headed-hydra. It has 100 health points left. It has 3 heads.'
    hydra = Hydra('one-headed-hydra', health=100, heads=1)
    assert str(hydra) == 'This is one-headed-hydra. It has 100 health points left. It has 1 head.'


def test_hydra_regenerate():
    hydra = Hydra('Norbert', 30, 3)
    hydra.take_damage(10)
    hydra.regenerate(5)
    assert hydra.get_health() == 25


def test_hydra_regenerate_max_health():
    hydra = Hydra('Norbert', 30, 3)
    hydra.take_damage(10)
    hydra.regenerate(15)
    assert hydra.get_health() == 30


def test_hydra_regenerate_health_above_base():
    hydra = Hydra('Norbert', 30, 3)
    assert hydra.get_base_health() == 30
    hydra.set_health(50)
    assert hydra.get_health() == 50
    hydra.take_damage(10)
    hydra.regenerate(5)
    assert hydra.get_health() == 40


def test_dragonHydra_take_damage_hit(monkeypatch: pytest.MonkeyPatch):
    def returnOne(f, t):
        return 1
    monkeypatch.setattr('classes.randint', returnOne)
    enemy = DragonHydra('three-headed-dragon', 40, 3)
    assert enemy.get_health() == 40
    assert enemy.take_damage(10) is True
    assert enemy.get_health() == 30


def test_dragonHydra_take_damage_miss(monkeypatch: pytest.MonkeyPatch):
    def returnZero(f, t):
        return 0
    monkeypatch.setattr('classes.randint', returnZero)
    enemy = DragonHydra('three-headed-dragon', 40, 3)
    assert enemy.get_health() == 40
    assert enemy.take_damage(10) is False
    assert enemy.get_health() == 40


def test_game_create():
    player = Player('Andrzej Duda', 1)
    enemies = [
        Hydra('h1', 10, 3),
        Enemy('Norbert Gierczak', 20)
    ]
    game = Game(player, enemies)
    assert game.player == player
    assert game.enemies == enemies


def test_game_create_default_enemies():
    player = Player('Andrzej Duda', 1)
    game = Game(player)
    assert game.player == player
    assert game.enemies == []
