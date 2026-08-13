"""
core/constants.py

Global constants and enumerations used throughout AgriMind AI.

This file should contain every fixed game constant so that
magic strings never appear elsewhere in the project.
"""

from enum import Enum

# ==========================================================
# Game Configuration
# ==========================================================

MAX_DAYS = 30
TURNS_PER_DAY = 24
TOTAL_TURNS = MAX_DAYS * TURNS_PER_DAY

DEFAULT_BOARD_SIZE = 10
QUADRANT_SIZE = 5

STARTING_MONEY = 3000
MAX_SHED_CAPACITY = 100
MAX_MARKET_ORDERS = 10


# ==========================================================
# Tile Types
# ==========================================================

class TileType(str, Enum):

    EMPTY = "EMPTY"

    LOCKED = "LOCKED"

    PLANT = "PLANT"

    WEED = "WEED"

    COOP = "COOP"

    PASTURE = "PASTURE"


# ==========================================================
# Crop Types
# ==========================================================

class CropType(str, Enum):

    WHEAT = "WHEAT"

    CARROT = "CARROT"

    TOMATO = "TOMATO"

    STRAWBERRY = "STRAWBERRY"

    MELON = "MELON"


# ==========================================================
# Animal Types
# ==========================================================

class AnimalType(str, Enum):

    GOOSE = "GOOSE"

    COW = "COW"

    SHEEP = "SHEEP"

ANIMAL_CONFIG = {
    "GOOSE": {
        "cost": 300,
        "first_yield_day": 4,
        "interval": 1,
        "product": "EGG",
    },
    "COW": {
        "cost": 400,
        "first_yield_day": 8,
        "interval": 2,
        "product": "MILK",
    },
    "SHEEP": {
        "cost": 500,
        "first_yield_day": 6,
        "interval": 3,
        "product": "WOOL",
    },
}


# ==========================================================
# Product Types
# ==========================================================

class ProductType(str, Enum):

    WHEAT = "WHEAT"

    CARROT = "CARROT"

    TOMATO = "TOMATO"

    STRAWBERRY = "STRAWBERRY"

    MELON = "MELON"

    EGG = "EGG"

    MILK = "MILK"

    WOOL = "WOOL"

    FERTILIZER = "FERTILIZER"


# ==========================================================
# Building Types
# ==========================================================

class BuildingType(str, Enum):

    COOP = "COOP"

    PASTURE = "PASTURE"


# ==========================================================
# Directions
# ==========================================================

class Direction(str, Enum):

    NORTH = "NORTH"

    SOUTH = "SOUTH"

    EAST = "EAST"

    WEST = "WEST"

    PASS = "PASS"


# ==========================================================
# Quadrants
# ==========================================================

class Quadrant(str, Enum):

    NW = "NW"

    NE = "NE"

    SW = "SW"

    SE = "SE"


# ==========================================================
# Unit Actions
# ==========================================================

class UnitAction(str, Enum):

    NORTH = "NORTH"

    SOUTH = "SOUTH"

    EAST = "EAST"

    WEST = "WEST"

    PASS = "PASS"

    PICKUP = "PICKUP"

    DROP = "DROP"

    PLANT = "PLANT"

    WATER = "WATER"

    HARVEST = "HARVEST"

    FERTILIZE = "FERTILIZE"

    PLACE = "PLACE"

    FEED = "FEED"

    CARE = "CARE"

    COLLECT_FERTILIZER = "COLLECT_FERTILIZER"

    BUILD_COOP = "BUILD_COOP"

    BUILD_PASTURE = "BUILD_PASTURE"

    DIG = "DIG"


# ==========================================================
# Market Actions
# ==========================================================

class MarketAction(str, Enum):

    BUY_SEED = "BUY_SEED"

    BUY_ANIMAL = "BUY_ANIMAL"

    BUY_PRODUCT = "BUY_PRODUCT"

    SELL = "SELL"

    HIRE = "HIRE"

    BUY_LAND = "BUY_LAND"


# ==========================================================
# Shop Types
# ==========================================================

class ShopType(str, Enum):

    BAKERY = "BAKERY"

    PIZZA_SHOP = "PIZZA_SHOP"

    BRUNCH_SPOT = "BRUNCH_SPOT"

    YARN_STORE = "YARN_STORE"

    ICE_CREAM_SHOP = "ICE_CREAM_SHOP"

    PET_CAFE = "PET_CAFE"

    SMOOTHIE_SHOP = "SMOOTHIE_SHOP"

    FARMERS_MARKET = "FARMERS_MARKET"


# ==========================================================
# AI Priorities
# ==========================================================

class Priority:

    CRITICAL = 100

    VERY_HIGH = 90

    HIGH = 75

    MEDIUM = 50

    LOW = 25

    VERY_LOW = 10

    NONE = 0


# ==========================================================
# AI Strategies
# ==========================================================

class StrategyType(str, Enum):

    OPENING = "OPENING"

    CROPS = "CROPS"

    LIVESTOCK = "LIVESTOCK"

    EXPANSION = "EXPANSION"

    MARKET = "MARKET"

    ENDGAME = "ENDGAME"


# ==========================================================
# Buyable Product Configuration
# ==========================================================

BUY_PRODUCT_CONFIG = {
    "WHEAT": {
        "max_useful_stock": 5,
        "daily_demand": 1,
    },

    "FERTILIZER": {
        "max_useful_stock": 5,
        "daily_demand": 1,
    },
}