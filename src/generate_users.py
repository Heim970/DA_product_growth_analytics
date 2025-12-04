import pandas as pd
import numpy as np
import random
import itertools
from datetime import datetime, timedelta

# ==============================
# 1) user_id 생성 (AAA, AAB ...)
# ==============================
def generate_user_ids(n=200):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    combos = itertools.product(letters, repeat=3)
    ids = [''.join(c) for c in combos]
    return ids[:n]

# ==============================
# 2) signup_date 생성
# ==============================
def random_date(start, end):
    delta = end - start
    offset = random.randint(0, delta.days)
    return start + timedelta(days=offset)

# ==============================
# 3) Users.csv 생성 함수
# ==============================
def generate_users_csv(n_users=200, filepath="users.csv"):

    user_ids = generate_user_ids(n_users)

    start_date = datetime(2024, 12, 1)
    end_date = datetime(2025, 11, 30)

    devices = ["iOS", "Android"]
    device_probs = [0.4, 0.6]

    channels = ["organic", "ad", "push", "social"]
    channel_probs = [0.55, 0.25, 0.10, 0.10]

    categories = ["coffee", "beverage", "dessert"]
    category_probs = [0.6, 0.25, 0.15]

    rows = []
    for uid in user_ids:

        signup = random_date(start_date, end_date)

        row = {
            "user_id": uid,
            "signup_date": signup.strftime("%Y-%m-%d"),
            "device": random.choices(devices, device_probs)[0],
            "channel": random.choices(channels, channel_probs)[0],
            "price_sensitivity": np.round(np.random.uniform(0, 1), 3),
            "impulse_level": np.round(np.random.uniform(0, 1), 3),
            "return_prob": np.round(np.random.uniform(0.1, 0.5), 3),
            "preferred_category": random.choices(categories, category_probs)[0]
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)
    print(f"Users.csv 생성 완료! -> {filepath}")

# 실행
if __name__ == "__main__":
    generate_users_csv()
