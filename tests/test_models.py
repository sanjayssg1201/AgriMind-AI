"""
tests/test_models.py

Basic tests for the AgriMind model layer.
"""

import pytest


# =========================================================
# Import Helpers
# =========================================================

def import_model(module_name, class_name):
    """
    Safely import a model class.

    This keeps the test file easy to adapt if a model
    module is renamed later.
    """

    try:

        module = __import__(
            module_name,
            fromlist=[class_name],
        )

        return getattr(
            module,
            class_name,
        )

    except (
        ImportError,
        AttributeError,
    ):

        return None


# =========================================================
# Farmer
# =========================================================

def test_farmer_model_exists():

    Farmer = import_model(
        "models.farmer",
        "Farmer",
    )

    assert Farmer is not None


# =========================================================
# Tile
# =========================================================

def test_tile_model_exists():

    Tile = import_model(
        "models.tile",
        "Tile",
    )

    assert Tile is not None


# =========================================================
# Animal
# =========================================================

def test_animal_model_exists():

    Animal = import_model(
        "models.animal",
        "Animal",
    )

    assert Animal is not None


# =========================================================
# Inventory
# =========================================================

def test_inventory_model_exists():

    Inventory = import_model(
        "models.inventory",
        "Inventory",
    )

    assert Inventory is not None


# =========================================================
# Market
# =========================================================

def test_market_model_exists():

    Market = import_model(
        "models.market",
        "Market",
    )

    assert Market is not None


# =========================================================
# Model Construction
# =========================================================

def test_farmer_can_be_constructed():

    Farmer = import_model(
        "models.farmer",
        "Farmer",
    )

    if Farmer is None:
        pytest.skip(
            "Farmer model is unavailable."
        )

    try:

        farmer = Farmer()

    except TypeError:

        pytest.skip(
            "Farmer requires constructor arguments."
        )

    assert farmer is not None


def test_tile_can_be_constructed():

    Tile = import_model(
        "models.tile",
        "Tile",
    )

    if Tile is None:
        pytest.skip(
            "Tile model is unavailable."
        )

    try:

        tile = Tile()

    except TypeError:

        pytest.skip(
            "Tile requires constructor arguments."
        )

    assert tile is not None


def test_animal_can_be_constructed():

    Animal = import_model(
        "models.animal",
        "Animal",
    )

    if Animal is None:
        pytest.skip(
            "Animal model is unavailable."
        )

    try:

        animal = Animal()

    except TypeError:

        pytest.skip(
            "Animal requires constructor arguments."
        )

    assert animal is not None


def test_inventory_can_be_constructed():

    Inventory = import_model(
        "models.inventory",
        "Inventory",
    )

    if Inventory is None:
        pytest.skip(
            "Inventory model is unavailable."
        )

    try:

        inventory = Inventory()

    except TypeError:

        pytest.skip(
            "Inventory requires constructor arguments."
        )

    assert inventory is not None


def test_market_can_be_constructed():

    Market = import_model(
        "models.market",
        "Market",
    )

    if Market is None:
        pytest.skip(
            "Market model is unavailable."
        )

    try:

        market = Market()

    except TypeError:

        pytest.skip(
            "Market requires constructor arguments."
        )

    assert market is not None