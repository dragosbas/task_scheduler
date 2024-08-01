
from BaseClass import BaseClass


class Product(BaseClass):
    def __init__(self, type: str):
        super().__init__()
        self.name: str = type

    def get_name(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Product(type={self.name} uuid = {self.get_uuid()})"
