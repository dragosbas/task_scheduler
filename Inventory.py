from Product import Product
from typing import List, Dict
import uuid


class Inventory:
    def __init__(self, initial_products: List[Product] = None):
        self.storage = {}
        self.storage_list: List[Product] = []

        for initial_product in initial_products if initial_products is not None else []:
            self.append(initial_product)

    def get_quantities(self) -> Dict[str, int]:
        result = {}

        for product_name, storage_products in self.storage.items():
            result[product_name] = len(storage_products)

        return result

    def __repr__(self) -> str:
        return f"Inventory(storage={self.storage})"

    def append(self, initial_product) -> None:
        self.storage_list.append(initial_product)

        if initial_product.name not in self.storage.keys():
            self.storage[initial_product.name] = [initial_product]
        else:
            self.storage[initial_product.name].append(initial_product)

    def pop(self, product_uuid: uuid) -> Product:
        found_product = [product for product in self.storage_list if product.uuid == product_uuid]
        if len(found_product) == 0:
            raise ValueError(f"No such product in inventory : {product_uuid}")
        the_product = found_product[0]
        self.storage_list = [product for product in self.storage_list if product.uuid != product_uuid]

        for name, entities in self.storage.items():
            found_entities = [entity for entity in entities if entity.get_uuid() == product_uuid]
            if len(found_entities) > 0:
                entities.remove(found_entities[0])
                return found_entities[0]

        return the_product