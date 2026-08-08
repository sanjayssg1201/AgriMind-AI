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

from brain.task import Task

from algorithms.heuristics import Heuristic

from models.game_state import GameState


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

        for product, quantity in inventory.items():

            if quantity <= 0:
                continue

            price = state.market.price(product)

            if price <= 0:
                continue

            tasks.append(

                Task(
                    task_type="SELL",
                    target=product,
                    priority=50,
                    estimated_reward=(
                        quantity * price
                    ),
                    metadata={
                        "product": product,
                        "quantity": quantity,
                        "price": price,
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

        for row in farm.tiles:

            for tile in row:

                if not tile.is_empty:
                    continue

                for crop, quantity in (
                    state.current_player.inventory
                    .seeds.items()
                ):

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

                    # Only generate one planting task per tile
                    break

        return tasks

