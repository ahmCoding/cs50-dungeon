import pytest


@pytest.fixture
def game_map():
    my_map = [
        ["#", "#", "#", "#", "#"],
        ["#", ".", ".", ".", "#"],
        ["#", ".", ">", ".", "#"],
        ["#", ".", ".", ".", "#"],
        ["#", "#", "#", "#", "#"],
    ]

    print(my_map)


def test_move_to_right_wall():
    pass
