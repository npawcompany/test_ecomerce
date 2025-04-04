from typing import List, Optional

class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    def get_price(self) -> float:
        return self.price

class RegularProduct(Product):
    def __init__(self, id: int, name: str, price: float, discount: float = 0):
        super().__init__(id, name, price)
        self.discount = discount

    def get_price(self) -> float:
        return self.price * (1 - self.discount / 100)

class ProductGroup(Product):
    def __init__(self, id: int, name: str, products: List[Product], discount: float = 0):
        super().__init__(id, name, 0)
        self.products = products
        self.discount = discount

    def calculate_price(self, strategy) -> float:
        return strategy.calculate_price(self.products)

class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.subcategories: List[Category] = []
        self.products: List[Product] = []

    def add_subcategory(self, category: 'Category'):
        self.subcategories.append(category)

    def add_product(self, product: Product):
        self.products.append(product)

    def get_all_products(self) -> List[Product]:
        all_products = self.products[:]
        for subcategory in self.subcategories:
            all_products.extend(subcategory.get_all_products())
        return all_products

class DiscountStrategy:
    def __init__(self, discount_percentage: float):
        self.discount_percentage = discount_percentage

    def calculate_price(self, products: List[Product]) -> float:
        total_price = sum(product.get_price() for product in products)
        return total_price * (1 - self.discount_percentage / 100)

class FreeProductStrategy:
    def __init__(self, every_nth: int):
        self.every_nth = every_nth

    def calculate_price(self, products: List[Product]) -> float:
        sorted_products = sorted(products, key=lambda x: x.get_price())
        total_price = 0
        for i, product in enumerate(sorted_products):
            if (i + 1) % self.every_nth != 0:
                total_price += product.get_price()
        return total_price

if __name__ == "__main__":
    product1 = RegularProduct(1, "Товар 1", 100, discount=10)
    product2 = RegularProduct(2, "Товар 2", 200)
    product3 = RegularProduct(3, "Товар 3", 150)

    product_group = ProductGroup(4, "Группа товаров", [product1, product2, product3])

    electronics = Category(1, "Электроника")
    electronics.add_product(product1)
    electronics.add_product(product2)

    mobiles = Category(2, "Мобильные телефоны")
    mobiles.add_product(product3)
    electronics.add_subcategory(mobiles)

    all_products = electronics.get_all_products()
    print("Все продукты в категории 'Электроника':")
    for product in all_products:
        print(f"  {product.name}: {product.get_price()}")

    discount_strategy = DiscountStrategy(10)
    group_price_with_discount = product_group.calculate_price(discount_strategy)
    print(f"Цена группы товаров со скидкой: {group_price_with_discount}")

    free_product_strategy = FreeProductStrategy(2)
    group_price_with_free_product = product_group.calculate_price(free_product_strategy)
    print(f"Цена группы товаров с бесплатным продуктом: {group_price_with_free_product}")
