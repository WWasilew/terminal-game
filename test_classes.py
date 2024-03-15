import pytest
from classes import Game, Player, Enemy, Hydra, DragonHydra
from classes import (
    NegativeLivesError,
    NameError,
    NegativeHealthError)


def test_create_player():
    player = Player('Jurek Ogórek')
    assert player._name == "Jurek Ogórek"
    assert player._lives == 1


def test_create_player_with_lives():
    player = Player('Jurek Ogórek', 4)
    assert player._name == 'Jurek Ogórek'
    assert player._lives == 4


def test_create_player_with_negative_lives():
    with pytest.raises(NegativeLivesError):
        Player('Jurek Ogórek', -1)


def test_introduce():
    player = Player('Jurek Ogórek', 3)
    assert player.info() == 'My name is Jurek Ogórek. I have 3 lives left.'
    player = Player('Jurek Ogórek', 1)
    assert player.info() == 'My name is Jurek Ogórek. I have 1 life left.'


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


def test_set_lives():
    player = Player('Jurek Ogórek', 1)
    assert player.get_lives() == 1
    player.set_lives(2)
    assert player.get_lives() == 2


def test_set_lives_zero():
    player = Player('Jurek Ogórek', 1)
    assert player.get_lives() == 1
    player.set_lives(0)
    assert player.get_lives() == 0


def test_set_lives_negative():
    player = Player('Jurek Ogórek', 1)
    assert player.get_lives() == 1
    with pytest.raises(NegativeLivesError):
        player.set_lives(-1)


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
    enemy.take_damage(10)
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
    enemy.take_damage(20)
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
    enemy.take_damage(10)
    assert enemy.get_health() == 30


def test_dragonHydra_take_damage_miss(monkeypatch: pytest.MonkeyPatch):
    def returnZero(f, t):
        return 0
    monkeypatch.setattr('classes.randint', returnZero)
    enemy = DragonHydra('three-headed-dragon', 40, 3)
    assert enemy.get_health() == 40
    enemy.take_damage(10)
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
