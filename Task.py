from BaseClass import BaseClass
from Machine import Machine
from Recipie import Recipie


class Task(BaseClass):
    def __init__(self, selected_machine: Machine, selected_recipie: Recipie, start_time: int):
        super().__init__()
        self.selected_machine = selected_machine
        self.recipie = selected_recipie
        self.time = start_time

    def __repr__(self) -> str:
        return (f"Task=(start_time={self.time}), products={self.recipie.product}, machine={self.selected_machine}, "
                f"selected_recipie={self.recipie}")