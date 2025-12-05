import pandas as pd

# Load events
events = pd.read_csv("data/events.csv")

# Filter only PaymentSuccess events
purchases = events[events["event_type"] == "PaymentSuccess"].copy()
purchases["purchase_id"] = range(1, len(purchases) + 1)

# select final columns
purchases = purchases[
    [
        "purchase_id",
        "timestamp",
        "user_id",
        "menu_id",
        "price",
        "category",
        "experiment_group",
        "device",
        "channel"
    ]
]

purchases.to_csv("data/purchases.csv", index=False, encoding="utf-8-sig")

print("Purchases.csv created!", len(purchases), "rows")