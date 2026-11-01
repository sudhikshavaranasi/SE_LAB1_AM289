
import pytest
from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status,
)


def test_reward_below_minimum():
    assert reward_points("paper", 3, False) == 0


def test_reward_at_minimum():
    assert reward_points("paper", 5, False) == 0


def test_reward_with_bonus():
    assert reward_points("paper", 5, True) == 6


def test_reward_plastic():
    assert reward_points("plastic", 5, False) == 12


def test_reward_metal():
    assert reward_points("metal", 4, False) == 24


def test_reward_large_weight():
    assert reward_points("paper", 26, False) == 210


def test_reward_large_metal():
    assert reward_points("metal", 23, False) == 378


def test_unknown_material():
    with pytest.raises(ValueError):
        reward_points("glass", 10, False)


def test_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -1, False)


def test_hazardous_collection_accepted():
    assert collection_accepted(5, 10, True) is True


def test_hazardous_collection_rejected():
    assert collection_accepted(6, 1, True) is False


def test_regular_collection_accepted():
    assert collection_accepted(50, 3, False) is True


def test_regular_collection_too_heavy():
    assert collection_accepted(51, 2, False) is False


def test_regular_collection_too_many_bags():
    assert collection_accepted(20, 4, False) is False


def test_slot_open():
    assert slot_status(20, True, False) == "open"


def test_slot_late():
    assert slot_status(10, False, False) == "open"


def test_slot_missed():
    assert slot_status(0, False, False) == "late"


def test_holiday_slot_open():
    assert slot_status(35, True, True) == "open"
