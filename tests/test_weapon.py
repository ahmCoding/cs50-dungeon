from game.core.weapon import Weapon


def test_get_damage():
    for d in range(1, 100):
        w1 = Weapon(damage=d)
        assert w1.get_damage() == d
