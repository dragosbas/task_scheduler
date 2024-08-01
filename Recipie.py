from typing import List, Optional
from BaseClass import BaseClass
from Product import Product


class Recipie(BaseClass):
    def __init__(self, name: str, base_product: Product, timer: float, requirements: Optional[List['Product']] = None):
        super().__init__()
        self.name = name
        self.product: Product = base_product
        self.product_name: str = base_product.get_name()
        self.timer: float = timer
        self.requirements: List[Product] = requirements if requirements is not None else []

    def get_name(self) -> str:
        return self.name

    def get_product(self) -> Product:
        return self.product

    def get_requirements(self) -> List[Product]:
        return self.requirements

    def get_timer(self) -> float:
        return self.timer

    def __repr__(self) -> str:
        return f"Recipie(name = {self.name}, product={self.product}, requirements=[{self.requirements}])"