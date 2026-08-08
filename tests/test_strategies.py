"""
tests/test_strategies.py

Tests for the AgriMind strategy layer.
"""

from strategies.balanced_strategy import BalancedStrategy
from strategies.crop_strategy import CropStrategy
from strategies.livestock_strategy import LivestockStrategy
from strategies.aggressive_strategy import AggressiveStrategy


# =========================================================
# Helpers
# =========================================================

class FakeFarm:
    """
    Minimal farm object for strategy tests.
    """

    def __init__(
        self,
        money=1000,
        crop_tiles=5,
        animal_tiles=3,
        empty_tiles=5,
        farmhand_count=1,
        unlocked_quadrants=None,
    ):

        self.money = money

        self.crop_tiles = crop_tiles

        self.animal_tiles = animal_tiles

        self.empty_tiles = empty_tiles

        self.farmhand_count = farmhand_count

        self.unlocked_quadrants = (
            unlocked_quadrants
            if unlocked_quadrants is not None
            else []
        )


class FakePlayer:

    def __init__(
        self,
        farm,
    ):

        self.farm = farm


class FakeState:

    def __init__(
        self,
        farm=None,
        money=None,
        expansion_available=True,
    ):

        if farm is None:

            farm = FakeFarm()

        if money is not None:

            farm.money = money

        self.current_player = FakePlayer(
            farm
        )

        self.money = farm.money

        self.expansion_available = (
            expansion_available
        )


# =========================================================
# Balanced Strategy
# =========================================================

def test_balanced_strategy_exists():

    strategy = BalancedStrategy()

    assert strategy.name == "BALANCED"


def test_balanced_strategy_score():

    strategy = BalancedStrategy()

    state = FakeState()

    score = strategy.score(
        state
    )

    assert isinstance(
        score,
        float,
    )


def test_balanced_task_bonus():

    strategy = BalancedStrategy()

    assert (
        strategy.task_bonus("HARVEST")
        > 0
    )


def test_balanced_description():

    strategy = BalancedStrategy()

    description = strategy.description()

    assert isinstance(
        description,
        str,
    )

    assert len(description) > 0


# =========================================================
# Crop Strategy
# =========================================================

def test_crop_strategy_exists():

    strategy = CropStrategy()

    assert strategy.name == "CROP"


def test_crop_strategy_score():

    strategy = CropStrategy()

    state = FakeState(
        farm=FakeFarm(
            crop_tiles=10,
            animal_tiles=1,
        )
    )

    score = strategy.score(
        state
    )

    assert isinstance(
        score,
        float,
    )


def test_crop_strategy_prefers_harvest():

    strategy = CropStrategy()

    assert (
        strategy.task_bonus("HARVEST")
        >
        strategy.task_bonus("BUY_ANIMAL")
    )


def test_crop_strategy_description():

    strategy = CropStrategy()

    assert isinstance(
        strategy.description(),
        str,
    )


# =========================================================
# Livestock Strategy
# =========================================================

def test_livestock_strategy_exists():

    strategy = LivestockStrategy()

    assert strategy.name == "LIVESTOCK"


def test_livestock_strategy_score():

    strategy = LivestockStrategy()

    state = FakeState(
        farm=FakeFarm(
            crop_tiles=1,
            animal_tiles=10,
        )
    )

    score = strategy.score(
        state
    )

    assert isinstance(
        score,
        float,
    )


def test_livestock_strategy_prefers_animals():

    strategy = LivestockStrategy()

    assert (
        strategy.task_bonus("FEED")
        >
        strategy.task_bonus("PLANT")
    )


def test_livestock_description():

    strategy = LivestockStrategy()

    assert isinstance(
        strategy.description(),
        str,
    )


# =========================================================
# Aggressive Strategy
# =========================================================

def test_aggressive_strategy_exists():

    strategy = AggressiveStrategy()

    assert strategy.name == "AGGRESSIVE"


def test_aggressive_strategy_score():

    strategy = AggressiveStrategy()

    state = FakeState(
        money=3000
    )

    score = strategy.score(
        state
    )

    assert isinstance(
        score,
        float,
    )


def test_aggressive_strategy_prefers_expansion():

    strategy = AggressiveStrategy()

    assert (
        strategy.task_bonus("EXPAND")
        >
        strategy.task_bonus("WATER")
    )


def test_aggressive_description():

    strategy = AggressiveStrategy()

    assert isinstance(
        strategy.description(),
        str,
    )


# =========================================================
# Strategy Comparison
# =========================================================

def test_strategies_are_independent():

    balanced = BalancedStrategy()

    crop = CropStrategy()

    livestock = LivestockStrategy()

    aggressive = AggressiveStrategy()

    assert balanced is not crop

    assert crop is not livestock

    assert livestock is not aggressive


def test_strategy_names_are_unique():

    names = {

        BalancedStrategy().name,

        CropStrategy().name,

        LivestockStrategy().name,

        AggressiveStrategy().name,

    }

    assert len(names) == 4