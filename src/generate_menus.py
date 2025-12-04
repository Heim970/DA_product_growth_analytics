import pandas as pd

menus = [
    (1, "Americano", "coffee", 2500, 0),
    (2, "Cafe Latte", "coffee", 3300, 0),
    (3, "Vanilla Latte", "coffee", 3800, 0),
    (4, "Caramel Macchiato", "coffee", 3800, 1),
    (5, "Dolce Latte", "coffee", 3900, 1),
    (6, "Hazelnut Latte", "coffee", 3600, 0),
    (7, "Chocolate Latte", "coffee", 3500, 0),
    (8, "Cold Brew", "coffee", 3500, 0),
    (9, "Cold Brew Latte", "coffee", 3900, 1),
    (10, "Brown Sugar Latte", "coffee", 4000, 1),

    (11, "Grape Ade", "beverage", 3500, 0),
    (12, "Grapefruit Ade", "beverage", 3500, 0),
    (13, "Lemon Ade", "beverage", 3300, 0),
    (14, "Mango Yogurt Smoothie", "beverage", 4200, 1),
    (15, "Strawberry Yogurt Smoothie", "beverage", 4200, 1),
    (16, "Chocolate Frappe", "beverage", 4300, 0),
    (17, "Mint Chocolate Frappe", "beverage", 4300, 1),
    (18, "Oreo Frappe", "beverage", 4300, 1),
    (19, "Matcha Latte", "beverage", 3800, 0),
    (20, "Brown Sugar Bubble Tea", "beverage", 3900, 1),

    (21, "Choco Chip Cookie", "dessert", 2000, 0),
    (22, "Brownie", "dessert", 2500, 0),
    (23, "Muffin", "dessert", 2800, 0),
    (24, "Scone", "dessert", 2800, 0),
    (25, "Chocolate Cake", "dessert", 4500, 1),
    (26, "Cheesecake", "dessert", 4500, 1),
    (27, "Tiramisu", "dessert", 4800, 1),
    (28, "Caramel Pudding", "dessert", 3000, 0),
    (29, "Butter Croissant", "dessert", 3200, 0),
    (30, "Banana Bread", "dessert", 3300, 0),
]

df = pd.DataFrame(menus, columns=["menu_id", "name", "category", "price", "discount_flag"])
df.to_csv("data/menus.csv", index=False, encoding="utf-8")
print("menus.csv saved!")
