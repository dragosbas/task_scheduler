from Inventory import Inventory
from Product import Product
from Recipie import Recipie
from Machine import Machine
from typing import List
from Task import Task
from Service import Service


class Factory:
    def __init__(self, service: Service, inventory: Inventory = Inventory()):
        self.service = service
        self.machines: List[Machine] = service.machines
        self.recipes: List[Recipie] = service.recipies
        self.inventory: Inventory = inventory if inventory is not None else Inventory()
        self.tasks: List[Task] = []

    def match_inventory(self, target_inventory: 'Inventory') -> bool:
        current_quantities = self.inventory.get_quantities()
        target_quantities = target_inventory.get_quantities()
        for product_name, desired_quantity in target_quantities.items():
            if desired_quantity > current_quantities.get(product_name, 0):
                return False
        return True

    def get_available_machines(self, at_time: int) -> List[Machine]:
        result: List[Machine] = []
        for machine in self.machines:
            task_at_time = [task for task in self.tasks if
                            task.selected_machine.name == machine.name and task.time < at_time < task.time + task.recipie.timer]
            if len(task_at_time) == 0:
                result.append(machine)
        return result

    def estimate_with_tasks(self, initial_inventory: Inventory, tasks: List[Task]) -> List[Product]:
        new_inventory = Inventory(initial_inventory.storage_list)

        sorted_tasks = sorted(tasks, key=lambda t: t.time)
        for task in sorted_tasks:
            new_inventory.pop(task.recipie.product.uuid)
            for ingredient in task.recipie.requirements:
                new_inventory.append(ingredient)

        return new_inventory.storage_list

    def create_schedule(self, current_inventory_requirements: Inventory) -> List[Task]:
        initial_inventory = Inventory(current_inventory_requirements.storage_list)
        tasks: List[Task] = []
        key_times = {0}

        while not self.match_inventory(current_inventory_requirements):
            analyzed_time = min(key_times)

            finished_tasks = [task for task in tasks if task.time + task.recipie.timer <= analyzed_time]

            products_required_at_analyzed_time = self.estimate_with_tasks(initial_inventory, finished_tasks)

            product_requirements = {}
            for tested_recipie in self.recipes:
                product_requirements[tested_recipie.product.name] = len(tested_recipie.requirements)

            products_required_at_analyzed_time = sorted(products_required_at_analyzed_time,
                                                        key=lambda p: product_requirements[p.name])

            for product in products_required_at_analyzed_time:
                for current_machine in self.machines:
                    if product.name in {acceptable_product.name for acceptable_product in
                                        current_machine.acceptable_products}:

                        current_tasks = [task for task in tasks if
                                         task.time <= analyzed_time < task.time + task.recipie.timer]

                        bookend_machines = [task.selected_machine.name for task in current_tasks]

                        if current_machine.name not in bookend_machines:

                            for turn_recipie in self.recipes:
                                if product.name == turn_recipie.product.name:

                                    new_recipie = self.service.create_recipie_for_product(turn_recipie.name, product)
                                    task = Task(current_machine, new_recipie, analyzed_time)
                                    tasks.append(task)

                                    for required_product in new_recipie.get_requirements():
                                        current_inventory_requirements.append(required_product)

                                    current_inventory_requirements.pop(new_recipie.get_product().uuid)
                                    key_times.add(analyzed_time + new_recipie.get_timer())
                                    break

            key_times.remove(analyzed_time)

        optimised_tasks = self.optimise_task(tasks)

        return optimised_tasks

    def validate_tasks(self, tasks: List[Task], inventory: Inventory = Inventory()) -> bool:
        try:
            self.estimate_with_tasks(inventory, tasks)
            return True
        except Exception:
            return False

    def optimise_task(self, tasks: List[Task]) -> List[Task]:
        total_time = max([task.time
                          + task.recipie.timer
                          for task in tasks]) + tasks[0].time

        result: List[Task] = []

        for task in tasks[::-1]:
            task.time = total_time - task.time - task.recipie.timer
            result.append(task)

        return result
