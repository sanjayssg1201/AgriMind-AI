"""
brain/task_generator.py

Generates intelligent tasks from the current GameState.

Pipeline:
GameState
    ↓
Generate Tasks
    ↓
Filter Tasks
    ↓
Scheduler
"""

from typer.cli import state

from brain.task import Task

from algorithms.heuristics import Heuristic

from models.game_state import GameState

from core.constants import ANIMAL_CONFIG


class TaskGenerator:
    """
    Generates tasks from the current game state.
    """

    MAX_TASKS = 25

    URGENT_PRIORITY = 90

    IMPORTANT_PRIORITY = 60

    LOW_PRIORITY = 30

    def __init__(self):

        pass

    # =====================================================
    # Public API
    # =====================================================

    def generate(
        self,
        state: GameState,
    ) -> list[Task]:

        tasks = []

        # -----------------------------------------------
        # Crops
        # -----------------------------------------------

        tasks.extend(
            self._crop_tasks(state)
        )

        # -----------------------------------------------
        # Animals
        # -----------------------------------------------

        tasks.extend(
            self._animal_tasks(state)
        )

        # -----------------------------------------------
        # Market
        # -----------------------------------------------

        tasks.extend(
            self._market_tasks(state)
        )
        tasks.extend(
            self._buy_seed_tasks(state)
)

        # -----------------------------------------------
        # Expansion
        # -----------------------------------------------

        tasks.extend(
            self._expansion_tasks(state)
        )

        # -----------------------------------------------
        # Hiring
        # -----------------------------------------------

        tasks.extend(
            self._hire_tasks(state)
        )

        # -----------------------------------------------
        # Planting
        # -----------------------------------------------

        tasks.extend(
            self._planting_tasks(state)
        )

        return self._filter_tasks(tasks)

    # =====================================================
    # Task Filter
    # =====================================================

    def _filter_tasks(
        self,
        tasks: list[Task],
    ) -> list[Task]:

        if not tasks:
            return []

        tasks.sort(

            key=lambda task: (

                task.priority,

                task.expected_profit,

                task.estimated_reward,

            ),

            reverse=True,

        )

        urgent = [

            task

            for task in tasks

            if task.priority >= self.URGENT_PRIORITY

        ]

        important = [

            task

            for task in tasks

            if (

                self.IMPORTANT_PRIORITY

                <= task.priority

                < self.URGENT_PRIORITY

            )

        ]

        low = [

            task

            for task in tasks

            if task.priority < self.IMPORTANT_PRIORITY

        ]

        filtered = []

        filtered.extend(urgent)

        remaining = self.MAX_TASKS - len(filtered)

        if remaining > 0:

            filtered.extend(
                important[:remaining]
            )

        remaining = self.MAX_TASKS - len(filtered)

        if remaining > 0:

            filtered.extend(
                low[:remaining]
            )

        return filtered

    # =====================================================
    # Crop Tasks
    # =====================================================

    def _crop_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        raise NotImplementedError

    # =====================================================
    # Animal Tasks
    # =====================================================

    def _animal_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        raise NotImplementedError

    # =====================================================
    # Market Tasks
    # =====================================================

    def _market_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        raise NotImplementedError

    # =====================================================
    # Expansion Tasks
    # =====================================================

    def _expansion_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        raise NotImplementedError

    # =====================================================
    # Hiring Tasks
    # =====================================================

    def _hire_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        raise NotImplementedError

    # =====================================================
    # Planting Tasks
    # =====================================================

    def _planting_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        raise NotImplementedError
    # =====================================================
    # Crop Tasks
    # =====================================================

    def _crop_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        tasks = []

        farm = state.current_player.farm

        for row in farm.tiles:

            for tile in row:

                if not tile.is_plant:
                    continue

                crop = tile.crop

                # ----------------------------
                # Harvest
                # ----------------------------

                if crop.can_harvest:

                    tasks.append(

                        Task(
                            task_type="HARVEST",
                            target=tile,
                            priority=100,
                            estimated_reward=(
                                crop.yield_units * 120
                            ),
                            metadata={
                                "crop": crop.name,
                            },
                        )

                    )

                    continue

                # ----------------------------
                # Emergency Water
                # ----------------------------

                if crop.is_dying:

                    tasks.append(

                        Task(
                            task_type="WATER",
                            target=tile,
                            priority=95,
                            estimated_reward=40,
                            metadata={
                                "crop": crop.name,
                                "emergency": True,
                            },
                        )

                    )

                    continue

                # ----------------------------
                # Normal Water
                # ----------------------------

                if crop.needs_water:

                    tasks.append(

                        Task(
                            task_type="WATER",
                            target=tile,
                            priority=70,
                            estimated_reward=20,
                            metadata={
                                "crop": crop.name,
                            },
                        )

                    )

                # ----------------------------
                # Fertilize
                # ----------------------------

                if (
                    not crop.is_fertilized
                    and crop.remaining_life > 2
                    and state.has_item("FERTILIZER")
                ):

                    tasks.append(

                        Task(
                            task_type="FERTILIZE",
                            target=tile,
                            priority=55,
                            estimated_reward=30,
                            estimated_cost=5,
                            metadata={
                                "crop": crop.name,
                            },
                        )

                    )

        return tasks

    # =====================================================
    # Animal Tasks
    # =====================================================

    def _animal_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        tasks = []

        farm = state.current_player.farm

        for row in farm.tiles:

            for tile in row:

                if not tile.has_animal:
                    continue

                animal = tile.animal

                # ----------------------------
                # Emergency Feed
                # ----------------------------

                if animal.is_starving:

                    tasks.append(

                        Task(
                            task_type="FEED",
                            target=tile,
                            priority=100,
                            estimated_reward=50,
                            metadata={
                                "animal": animal.name,
                                "emergency": True,
                            },
                        )

                    )

                    continue

                # ----------------------------
                # Feed
                # ----------------------------

                if animal.needs_feed:

                    tasks.append(

                        Task(
                            task_type="FEED",
                            target=tile,
                            priority=80,
                            estimated_reward=25,
                            metadata={
                                "animal": animal.name,
                            },
                        )

                    )

                # ----------------------------
                # Care
                # ----------------------------

                if animal.needs_care:

                    tasks.append(

                        Task(
                            task_type="CARE",
                            target=tile,
                            priority=65,
                            estimated_reward=20,
                            metadata={
                                "animal": animal.name,
                            },
                        )

                    )

                # ----------------------------
                # Collect Product
                # ----------------------------

                if animal.has_product:

                    tasks.append(

                        Task(
                            task_type="COLLECT",
                            target=tile,
                            priority=90,
                            estimated_reward=(
                                animal.yield_units * 150
                            ),
                            metadata={
                                "animal": animal.name,
                            },
                        )

                    )

                # ----------------------------
                # Collect Fertilizer
                # ----------------------------

                if animal.can_collect_fertilizer:

                    tasks.append(

                        Task(
                            task_type="COLLECT_FERTILIZER",
                            target=tile,
                            priority=60,
                            estimated_reward=15,
                            metadata={
                                "animal": animal.name,
                            },
                        )

                    )

        # =================================================
        # Buy Animal
        # =================================================

        farm = state.current_player.farm

        animal_structures = {
            "GOOSE": "COOP",
            "COW": "PASTURE",
            "SHEEP": "PASTURE",
        }

        for animal, config in ANIMAL_CONFIG.items():

            cost = config["cost"]

            if state.money < cost:
                continue

            product = config["product"]

            price = state.market.price(product)

            if price <= 0:
                continue

            # determine if there's an empty coop/pasture for this animal
            has_empty_structure = any(
                (
                    tile.is_coop
                    if animal_structures[animal] == "COOP"
                    else tile.is_pasture
                )
                and not tile.has_animal
                for row in farm.tiles
                for tile in row
            )

            if not has_empty_structure:
                continue

            tasks.append(
                Task(
                    task_type="BUY_ANIMAL",
                    target=animal,
                    priority=35,
                    estimated_reward=0,
                    estimated_cost=cost,
                    metadata={
                        "animal": animal,
                        "cost": cost,
                        "product": product,
                        "price": price,
                    },
                )
            )

        # =================================================
        # Place Purchased Animals
        # =================================================

        animal_structures = {
            "GOOSE": "COOP",
            "COW": "PASTURE",
            "SHEEP": "PASTURE",
        }

        inventory = state.current_player.inventory.shed

        for animal, structure in animal_structures.items():

            if inventory.get(animal, 0) <= 0:
                continue

            for row in farm.tiles:

                for tile in row:

                    is_matching_structure = (
                        tile.is_coop
                        if structure == "COOP"
                        else tile.is_pasture
                    )

                    if not is_matching_structure:
                        continue

                    if tile.has_animal:
                        continue

                    tasks.append(
                        Task(
                            task_type="PLACE",
                            target=tile,
                            priority=95,
                            estimated_reward=40,
                            estimated_cost=0,
                            metadata={
                                "animal": animal,
                                "structure": structure,
                            },
                        )
                    )

        return tasks

    # =====================================================
    # Market Tasks
    # =====================================================

    def _market_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        tasks = []

        inventory = state.current_player.inventory.shed

        # =====================================================
        # SELL
        # =====================================================

        for product, quantity in inventory.items():

            if quantity <= 0:
                continue

            # Do not create SELL tasks for things that are
            # not actually sellable market products.
            if product == "FERTILIZER":
                continue

            price = state.market.price(product)

            if price <= 0:
                continue

            tasks.append(
                Task(
                    task_type="SELL",
                    target=product,
                    priority=50,
                    metadata={
                        "quantity": 1,
                        "price": price,
                        "inventory": quantity,
                    },
                )
            )

        # =====================================================
        # BUY SEED
        # =====================================================

        tasks.extend(
            self._buy_seed_tasks(state)
        )

        # =====================================================
        # BUY PRODUCT
        # =====================================================

        tasks.extend(
            self._buy_product_tasks(state)
        )

        return tasks

    # =====================================================
    # Buy Seed Tasks
    # =====================================================

    def _buy_seed_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        tasks = []

        # No reason to buy seeds if there is
        # nowhere to plant them.
        if state.empty_tiles <= 0:
            return tasks

        # Keep enough cash for basic operations.
        reserve = 300

        if state.money <= reserve:
            return tasks

        # Kaggriculture seed costs.
        seed_costs = {
            "WHEAT": 10,
            "CARROT": 20,
            "TOMATO": 50,
            "STRAWBERRY": 100,
            "MELON": 80,
        }

        for crop, cost in seed_costs.items():
            price = state.market.price(crop)

            if price <= 0:
                continue

            current_seeds = state.seeds(crop)

            # Already have enough seeds for the currently
            # available planting capacity.
            if current_seeds >= state.empty_tiles:
                continue

            if state.money < reserve + cost:
                continue

            tasks.append(
                Task(
                    task_type="BUY_SEED",
                    target=crop,
                    priority=35,
                    estimated_reward=0,
                    estimated_cost=cost,
                    metadata={
                        "crop": crop,
                        "quantity": 1,
                        "cost": cost,
                    },
                )
            )

        return tasks


    # =====================================================
    # Expansion Tasks
    # =====================================================

    def _expansion_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        if not state.expansion_available:
            return []

        farm = state.current_player.farm

        if farm.empty_tiles > 6:
            return []

        if state.money < 2000:
            return []

        return [

            Task(
                task_type="EXPAND",
                priority=55,
                estimated_reward=500,
                estimated_cost=2000,
            )

        ]


    # =====================================================
    # Hiring Tasks
    # =====================================================

    def _hire_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        if state.money < 1200:
            return []

        farm = state.current_player.farm

        if farm.farmhand_count >= 5:
            return []

        if farm.crop_tiles + farm.animal_tiles < 8:
            return []

        return [

            Task(
                task_type="HIRE",
                priority=45,
                estimated_reward=300,
                estimated_cost=1000,
            )

        ]

    # =====================================================
    # Planting Tasks
    # =====================================================

    def _planting_tasks(
        self,
        state: GameState,
    ) -> list[Task]:

        tasks = []

        farm = state.current_player.farm
        seeds = state.current_player.inventory.seeds

        for row in farm.tiles:

            for tile in row:

                if not tile.is_empty:
                    continue

                for crop, quantity in seeds.items():

                    if quantity <= 0:
                        continue

                    tasks.append(
                        Task(
                            task_type="PLANT",
                            target=tile,
                            priority=40,
                            estimated_reward=120,
                            estimated_cost=10,
                            metadata={
                                "crop": crop,
                            },
                        )
                    )

        return tasks


# =====================================================
# Buy Product Tasks
# =====================================================

def _buy_product_tasks(
    self,
    state: GameState,
) -> list[Task]:

    tasks = []

    BUYABLE_PRODUCTS = {
        "WHEAT",
        "FERTILIZER",
    }

    inventory = state.current_player.inventory

    # --------------------------------------------------
    # Basic constraints
    # --------------------------------------------------

    # Cannot buy anything without shed space.
    if inventory.is_full:
        return tasks

    # Keep emergency cash available.
    reserve = 300

    available_cash = max(
        0,
        state.money - reserve,
    )

    if available_cash <= 0:
        return tasks

    # --------------------------------------------------
    # Evaluate each genuinely buyable product
    # --------------------------------------------------

    for product in BUYABLE_PRODUCTS:

        current_price = state.market.price(product)

        if current_price <= 0:
            continue

        # --------------------------------------------------
        # Inventory constraint
        # --------------------------------------------------

        current_stock = inventory.item_count(product)

        config = BUY_PRODUCT_CONFIG.get(product)

        if config is None:
            continue

        max_useful_stock = config["max_useful_stock"]

        if current_stock >= max_useful_stock:
            continue

        # --------------------------------------------------
        # Actual need
        # --------------------------------------------------

        daily_demand = config["daily_demand"]

        days_remaining = max(
            0,
            state.turns_remaining // 24,
        )

        required_stock = min(
            max_useful_stock,
            max(
                0,
                days_remaining * daily_demand,
            ),
        )

        needed_quantity = (
            required_stock - current_stock
        )

        if needed_quantity <= 0:
            continue

        # Only consider one unit at a time.
        quantity = 1

        # --------------------------------------------------
        # Cash constraint
        # --------------------------------------------------

        if current_price > available_cash:
            continue

        # --------------------------------------------------
        # Downstream value
        # --------------------------------------------------
        downstream_value = self.economy.downstream_value(
            state,
            product,
        )

        if downstream_value <= 0:
            continue

        expected_profit = (
            downstream_value - current_price
        )

        if expected_profit <= 0:
            continue

        margin = (
            expected_profit / current_price
        )

        if margin < 0.10:
            continue
        # --------------------------------------------------
        # Do not buy simply because price is low.
        #
        # Buying must have positive downstream utility.
        # --------------------------------------------------

        expected_profit = (
            expected_value - current_price
        )

        minimum_margin = (
            config["min_profit_margin"]
        )

        minimum_required_value = (
            current_price
            * (1 + minimum_margin)
        )

        if expected_value < minimum_required_value:
            continue

        if expected_profit <= 0:
            continue

        # --------------------------------------------------
        # Create candidate
        # --------------------------------------------------

        tasks.append(
            Task(
                task_type="BUY_PRODUCT",
                target=product,
                priority=expected_profit,
                estimated_reward=expected_value,
                estimated_cost=current_price,
                metadata={
                    "product": product,
                    "quantity": quantity,
                    "price": current_price,
                    "current_stock": current_stock,
                    "needed_quantity": needed_quantity,
                    "downstream_value": downstream_value,
                    "expected_profit": expected_profit,
                },
            )
        )

    return tasks