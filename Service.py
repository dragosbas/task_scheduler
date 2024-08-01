from Product import Product
from Recipie import Recipie
from Machine import Machine
from typing import List, Dict


class Service:
    def __init__(self, name: str = "default"):
        self.name = name
        self.products: List[Product] = []
        self.machines: List[Machine] = []
        self.recipies: List[Recipie] = []
        self.standard_products: Dict[str, Product] = {}

    def define_product(self, name: str) -> Product:
        new_product = Product(name)
        self.standard_products[name] = new_product
        return new_product

    def create_product(self, name: str) -> Product:
        mock_product = self.standard_products[name]
        new_product = Product(mock_product.name)
        self.products.append(new_product)
        return new_product

    def count_products(self) -> Dict[str, int]:
        result = {}
        for current_product in self.products:
            result[current_product.name] = result.get(current_product.name, 0) + 1
        return result

    def define_recipie(self, name: str, desired_product: Product, timer: float,
                       requirements: List[Product] = None) -> Recipie:
        new_recipie = Recipie(name, desired_product, timer, requirements)
        self.recipies.append(new_recipie)
        return new_recipie

    def create_recipie_for_product(self, name, desired_product: Product) -> Recipie:
        template_recipies = [template_recipie for template_recipie in self.recipies if
                             template_recipie.product.name == desired_product.name]
        if len(template_recipies) == 0:
            raise ValueError(f"No recipie found for {name}")
        template_recipie = template_recipies[0]

        new_recipie = Recipie(name, desired_product, template_recipie.get_timer(),
                              [self.create_product(product.name) for product in template_recipie.get_requirements()])

        self.recipies.append(new_recipie)
        return new_recipie

    def create_machine(self, name, acceptable_products: List[Product]) -> Machine:
        new_machine = Machine(name, acceptable_products)
        self.machines.append(new_machine)
        return new_machine

    def __repr__(self) -> str:
        return f"Service(name={self.name}, machines={self.machines}, recipies={self.recipies})"
