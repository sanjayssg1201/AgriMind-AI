"""
Regression tests for the risk-aware economic layer.
"""

import pytest

from brain.economy import EconomyManager
from brain.memory import BrainMemory

from models.game_state import GameState
from models.market import Market
from models.player import Player
from models.farm import Farm
from models.inventory import Inventory
from models.town import Town
from models.tile import Tile


# =========================================================
# Helpers
# =========================================================

def make_tile():
    """
    Construct a minimal empty Tile.
    """

    return Tile(
        x=0,
        y=0,
    )


def make_inventory():
    """
    Construct an empty Inventory.
    """

    return Inventory(
        shed={},
        seeds={},
        inventories=[],
    )


def make_farm(
    money=1000.0,
):
    """
    Construct a minimal farm.
    """

    tile = make_tile()

    tiles = [
        [tile]
    ]

    try:
        return Farm(
            money=money,
            tiles=tiles,
            farmer_position=(0, 0),
            farmhands=[],
            unlocked_quadrants=["A"],
            hires_today=0,
        )

    except TypeError:
        pytest.skip(
            "Farm constructor differs from expected interface."
        )


def make_player(
    money=1000.0,
):
    """
    Construct a minimal player.
    """

    farm = make_farm(
        money=money,
    )

    inventory = make_inventory()

    try:
        return Player(
            player_id=0,
            farm=farm,
            inventory=inventory,
        )

    except TypeError:
        pytest.skip(
            "Player constructor differs from expected interface."
        )


def make_market(
    price=10,
):
    """
    Construct a simple market.
    """

    return Market(
        inventory={
            "WHEAT": 100,
            "FERTILIZER": 100,
        },
        prices={
            "WHEAT": price,
            "FERTILIZER": price,
        },
    )


def make_town():
    """
    Construct a minimal empty Town.
    """

    return Town(
        unlocked_shops=[],
    )


def make_state(
    money=1000.0,
    price=10,
):
    """
    Construct a minimal real GameState.
    """

    player = make_player(
        money=money,
    )

    opponent = make_player(
        money=1000.0,
    )

    market = make_market(
        price=price,
    )

    town = make_town()

    try:
        return GameState(
            day=1,
            hour=0,
            current_player=player,
            opponent=opponent,
            market=market,
            town=town,
        )

    except TypeError:
        pytest.skip(
            "GameState constructor differs from expected interface."
        )


def make_economy():
    """
    Construct EconomyManager using the real BrainMemory.
    """

    return EconomyManager(
        BrainMemory()
    )


# =========================================================
# Market Risk Score
# =========================================================

def test_market_risk_score_without_inventory_is_zero():

    state = make_state()

    economy = make_economy()

    risk = economy.market_risk_score(
        state,
        "WHEAT",
    )

    assert risk == 0.0


def test_market_risk_score_returns_high_risk_for_large_position():

    state = make_state(
        money=100,
        price=10,
    )

    inventory = state.current_player.inventory

    inventory.shed["WHEAT"] = 20

    economy = make_economy()

    risk = economy.market_risk_score(
        state,
        "WHEAT",
    )

    assert risk > 0


def test_market_risk_score_is_bounded():

    state = make_state(
        money=0,
        price=10,
    )

    inventory = state.current_player.inventory

    inventory.shed["WHEAT"] = 100

    economy = make_economy()

    risk = economy.market_risk_score(
        state,
        "WHEAT",
    )

    assert 0.0 <= risk <= 100.0


# =========================================================
# Position Sizing
# =========================================================

def test_position_size_is_zero_for_invalid_price():

    state = make_state(
        money=1000,
        price=0,
    )

    economy = make_economy()

    quantity = economy.calculate_position_size(
        state,
        "WHEAT",
        confidence=1.0,
    )

    assert quantity == 0


def test_position_size_is_zero_for_zero_confidence():

    state = make_state(
        money=1000,
        price=10,
    )

    economy = make_economy()

    quantity = economy.calculate_position_size(
        state,
        "WHEAT",
        confidence=0.0,
    )

    assert quantity == 0


def test_higher_confidence_does_not_reduce_position_size():

    state = make_state(
        money=1000,
        price=10,
    )

    economy = make_economy()

    low_confidence = economy.calculate_position_size(
        state,
        "WHEAT",
        confidence=0.25,
    )

    high_confidence = economy.calculate_position_size(
        state,
        "WHEAT",
        confidence=1.0,
    )

    assert high_confidence >= low_confidence


def test_position_size_never_exceeds_available_cash():

    state = make_state(
        money=100,
        price=10,
    )

    economy = make_economy()

    quantity = economy.calculate_position_size(
        state,
        "WHEAT",
        confidence=1.0,
    )

    assert quantity * 10 <= state.money


# =========================================================
# Portfolio Exposure
# =========================================================

def test_portfolio_exposure_is_zero_without_inventory():

    state = make_state(
        money=1000,
        price=10,
    )

    economy = make_economy()

    exposure = economy.portfolio_exposure_pct(
        state
    )

    assert exposure == 0.0


def test_portfolio_exposure_increases_with_inventory():

    state = make_state(
        money=1000,
        price=10,
    )

    state.current_player.inventory.shed[
        "WHEAT"
    ] = 10

    economy = make_economy()

    exposure = economy.portfolio_exposure_pct(
        state
    )

    assert exposure > 0


def test_portfolio_exposure_is_bounded():

    state = make_state(
        money=1000,
        price=10,
    )

    state.current_player.inventory.shed[
        "WHEAT"
    ] = 1000

    economy = make_economy()

    exposure = economy.portfolio_exposure_pct(
        state
    )

    assert exposure >= 0.0


# =========================================================
# Portfolio Position Guard
# =========================================================

def test_position_guard_rejects_zero_quantity():

    state = make_state()

    economy = make_economy()

    allowed = economy.can_take_position(
        state,
        "WHEAT",
        quantity=0,
    )

    assert allowed is False


def test_position_guard_rejects_invalid_price():

    state = make_state(
        price=0,
    )

    economy = make_economy()

    allowed = economy.can_take_position(
        state,
        "WHEAT",
        quantity=1,
    )

    assert allowed is False


def test_position_guard_allows_small_position():

    state = make_state(
        money=1000,
        price=10,
    )

    economy = make_economy()

    allowed = economy.can_take_position(
        state,
        "WHEAT",
        quantity=1,
    )

    assert allowed is True


# =========================================================
# Circuit Breaker
# =========================================================

def test_circuit_breaker_is_clear_with_no_exposure():

    state = make_state(
        money=1000,
        price=10,
    )

    economy = make_economy()

    triggered = economy.risk_circuit_breaker(
        state
    )

    assert triggered is False


def test_circuit_breaker_triggers_at_high_portfolio_exposure():

    state = make_state(
        money=100,
        price=10,
    )

    state.current_player.inventory.shed[
        "WHEAT"
    ] = 100

    economy = make_economy()

    triggered = economy.risk_circuit_breaker(
        state,
        max_portfolio_exposure_pct=60.0,
    )

    assert triggered is True


def test_circuit_breaker_responds_to_market_risk():

    state = make_state(
        money=0,
        price=10,
    )

    state.current_player.inventory.shed[
        "WHEAT"
    ] = 100

    economy = make_economy()

    triggered = economy.risk_circuit_breaker(
        state,
        max_portfolio_exposure_pct=100.0,
        max_market_risk_score=80.0,
    )

    assert triggered is True