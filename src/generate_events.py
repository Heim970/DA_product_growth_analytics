import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ---------------------------------------------
# Load Users & Menus
# ---------------------------------------------
users = pd.read_csv("./data/users.csv")
menus = pd.read_csv("./data/menus.csv")

# AB test group assignment
def assign_ab_group(users):
    groups = ["A", "B"]
    users["experiment_group"] = np.random.choice(groups, size=len(users))
    return users

users = assign_ab_group(users)


# ---------------------------------------------
# Menu Selection Logic (70/20/10)
# ---------------------------------------------
def choose_menu(user, menus):
    # 확률 기반 선택
    choice = random.choices(
        ["preferred", "discount", "random"],
        weights=[0.7, 0.2, 0.1]
    )[0]

    if choice == "preferred":
    # Preferred category 70%
        subset = menus[menus["category"] == user["preferred_category"]]
        return subset.sample(1).iloc[0]

    elif choice == "discount":
    # Discount menu 20%
        subset = menus[menus["discount_flag"] == 1]
        return subset.sample(1).iloc[0]

    else:
    # Random 10%
        return menus.sample(1).iloc[0]


# ---------------------------------------------
# Event probability functions
# ---------------------------------------------
def generate_session_events(user, date, session_idx, menus):
    events = []

    # Create session_id
    session_id = f"{user['user_id']}_{date.strftime('%Y%m%d')}_{session_idx}"

    # random time
    time_cursor = datetime.combine(date, datetime.min.time()) + timedelta(
        minutes=random.randint(0, 1380)
    )

    def add_event(event_type, menu=None):
        nonlocal time_cursor
        events.append({
            "timestamp": time_cursor,
            "user_id": user["user_id"],
            "session_id": session_id,
            "event_type": event_type,
            "menu_id": None if menu is None else menu["menu_id"],
            "price": None if menu is None else menu["price"],
            "category": None if menu is None else menu["category"],
            "experiment_group": user["experiment_group"],
            "device": user["device"],
            "channel": user["channel"],
        })

    # AppOpen
    add_event("AppOpen")

    # SearchMenu (70%)
    if random.random() < 0.7:
        time_cursor += timedelta(seconds=random.randint(5, 15))
        add_event("SearchMenu")

    # ViewMenu (1~4회)
    view_count = random.randint(1, 4)
    viewed_items = []

    for _ in range(view_count):
        menu = choose_menu(user, menus)
        viewed_items.append(menu)
        time_cursor += timedelta(seconds=random.randint(5, 15))
        add_event("ViewMenu", menu)

    # AddToCart (impulse_level 기반)
    if random.random() < user["impulse_level"]:
        chosen = random.choice(viewed_items)
        time_cursor += timedelta(seconds=random.randint(5, 15))
        add_event("AddToCart", chosen)

        # CheckoutStart (impulse 기반)
        if random.random() < min(1, user["impulse_level"] * 0.8):
            time_cursor += timedelta(seconds=random.randint(5, 15))
            add_event("CheckoutStart", chosen)

            # PaymentSuccess 결정 (CVR 모델)
            base_cvr = 0.15 + (user["impulse_level"] * 0.10)

            # 할인 메뉴 + B 그룹일 경우 CVR 강화
            if chosen["discount_flag"] == 1 and user["experiment_group"] == "B":
                base_cvr *= 1.20

            # 가격 민감도 반영
            base_cvr *= (1 - user["price_sensitivity"] * 0.2)

            if random.random() < base_cvr:
                time_cursor += timedelta(seconds=random.randint(5, 15))
                add_event("PaymentSuccess", chosen)

    return events


# ---------------------------------------------
# MAIN: iterate 365 days x 200 users
# ---------------------------------------------
all_events = []
start_date = datetime(2024, 12, 1)
num_days = 365

for _, user in users.iterrows():
    for d in range(num_days):
        date = start_date + timedelta(days=d)

        # 방문 확률: signup 초기일수 + return_prob 반영
        days_since_signup = (date - datetime.strptime(user["signup_date"], "%Y-%m-%d")).days
        early_boost = 0.15 if days_since_signup < 30 else 0
        visit_prob = min(0.05 + user["return_prob"] + early_boost, 0.9)

        if random.random() < visit_prob:
            # 세션 수 결정
            if user["impulse_level"] > 0.7:
                session_count = random.choice([1, 2])
            elif user["impulse_level"] > 0.3:
                session_count = 1
            else:
                session_count = random.choice([0, 1])
            
            for s in range(session_count):
                ev = generate_session_events(user, date, s+1, menus)
                all_events.extend(ev)

# ---------------------------------------------
# Save CSV
# ---------------------------------------------
events_df = pd.DataFrame(all_events)
events_df = events_df.sort_values(by="timestamp")

events_df.to_csv("./data/events.csv", index=False, encoding="utf-8")
print("Events.csv created!", len(events_df), "rows")