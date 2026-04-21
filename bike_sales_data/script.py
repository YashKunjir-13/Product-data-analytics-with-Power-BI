import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

n_rows = 10000

cust_id = np.random.randint(1000000, 9999999, n_rows)
sales_id = cust_id.copy()
product_code = np.random.randint(10000, 99999, n_rows)

himalayan_variants = {
    'Himalayan 450': datetime(2023, 11, 24),
    'Himalayan 450 Dual Tone': datetime(2024, 1, 15),
    'Himalayan 450 Summit Edition': datetime(2024, 3, 1)
}
ktm_variants = {
    'KTM 390 Adventure': datetime(2023, 1, 1),  # Ongoing
    'KTM 390 Adventure X': datetime(2025, 1, 30),
    'KTM 390 Adventure RS': datetime(2025, 1, 30)
}

bike_model_list = []
for _ in range(n_rows):
    if random.random() < 0.55:
        var = random.choice(list(himalayan_variants.keys()))
    else:
        var = random.choice(list(ktm_variants.keys()))
    bike_model_list.append(var)
bike_model = np.array(bike_model_list)

# Prices
prices = []
for model in bike_model:
    if 'Himalayan' in model:
        prices.append(np.random.normal(285000, 15000))
    else:
        prices.append(np.random.normal(343000, 18000))
price = np.round(np.array(prices), 2)

quantity = np.random.choice([1,2,3], n_rows, p=[0.8, 0.15, 0.05])

cities = ['Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Ahmedabad', 'Jaipur', 'Pimpri-Chinchwad', 'Nagpur', 'Lucknow', 'Indore']
city_weights = [0.15, 0.15, 0.12, 0.08, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.11]
city = np.random.choice(cities, n_rows, p=city_weights)

payment = np.random.choice(['Credit Card', 'UPI', 'Cash', 'Debit Card', 'Finance'], n_rows, p=[0.3, 0.35, 0.2, 0.1, 0.05])

age = np.clip(np.random.normal(38, 8, n_rows).astype(int), 25, 55)
age_rep = age.copy()

total = np.round(price * quantity, 2)

# Dates: variant-specific min date + ramp-up
end_date = datetime(2026, 4, 2)
dates = []
for i, model in enumerate(bike_model):
    if 'Himalayan' in model:
        min_date = himalayan_variants[model]
    else:
        min_date = ktm_variants[model]
    days_since_launch = np.random.exponential(450) + np.random.uniform(0, 200)  # Skew recent
    sale_date = min_date + timedelta(days=days_since_launch)
    dates.append(min(sale_date, end_date))

date = pd.to_datetime(dates)

df = pd.DataFrame({
    'cust_id': cust_id,
    'sales_id': sales_id,
    'product_code': product_code,
    'bike_model': bike_model,
    'price': price,
    'quantity': quantity,
    'city': city,
    'age': age,
    'payment': payment,
    'age_rep': age_rep,
    'total': total,
    'date': date
}).sort_values('date').reset_index(drop=True)

print("Launch-aligned date range:", df['date'].min(), "to", df['date'].max())
print("\\nVariant sales start:")
for var in set(bike_model):
    first_sale = df[df['bike_model']==var]['date'].min()
    print(f"{var}: {first_sale}")

df.to_excel('output/launch_refined_adv_bike_sales.xlsx', index=False)

print("\\nSaved: output/launch_refined_adv_bike_sales.xlsx")