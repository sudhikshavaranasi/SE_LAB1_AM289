
import pytest
from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status,
)


@pytest.mark.parametrize(
    "material,weight,bonus,expected",
    [
        ("paper", 4, False, 0),
        ("paper", 5, False, 0),
        ("paper", 5, True, 6),
        ("plastic", 2, False, 0),
        ("plastic", 2, True, 0),
        ("plastic", 3, True, 6),
        ("metal", 2, True, 0),
        ("metal", 3, True, 12),
        ("metal", 4, False, 24),
        ("paper", 26, False, 210),
        ("metal", 23, False, 378),
    ],
)
def test_reward_branches(material, weight, bonus, expected):
    assert reward_points(material, weight, bonus) == expected


def test_invalid_material():
    with pytest.raises(ValueError):
        reward_points("glass", 5, False)


def test_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -1, False)


@pytest.mark.parametrize(
    "weight,bags,hazardous,expected",
    [
        (5, 5, True, True),
        (6, 1, True, False),
        (50, 3, False, True),
        (51, 1, False, False),
        (20, 3, False, True),
        (20, 4, False, False),
    ],
)
def test_collection_branches(weight, bags, hazardous, expected):
    assert collection_accepted(weight, bags, hazardous) is expected


@pytest.mark.parametrize(
    "minutes,morning,holiday,expected",
    [
        (20, True, False, "open"),
        (19, True, False, "late"),
        (5, True, False, "late"),
        (10, False, False, "open"),
        (9, False, False, "late"),
        (0, False, False, "late"),
        (35, True, True, "open"),
        (34, True, True, "late"),
        (20, False, True, "late"),
        (19, False, True, "late"),
        (4, False, True, "missed"),
    ],
)
def test_slot_status_branches(minutes, morning, holiday, expected):
    assert slot_status(minutes, morning, holiday) == expected
