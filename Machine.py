from BaseClass import BaseClass
from Product import Product
from typing import List


class Machine(BaseClass):
    def __init__(self, name: str, acceptable_products: List[Product]):
        super().__init__()
        self.name: str = name
        self.acceptable_products: List[Product] = acceptable_products

    def check_if_acceptable_product(self, product: Product) -> bool:
        return product.name in [inventory.name for inventory in self.acceptable_products]

    def __repr__(self) -> str:
        return f"Machine(machine_id={self.name}, acceptable_products={self.acceptable_products})"

