import pandas as pd

df = pd.read_csv('SPY_v2_hourly.csv')


df['date'] = pd.to_datetime(df['date_utc'])
df['date'] = df['date'].dt.floor('d')
df['year'] = df['date'].dt.year

df = df[df['order_type'] != 0]

average_non_zero_orders_per_week_by_year = df.groupby([df['year'], pd.Grouper(key='date', freq='W')]).size().groupby('year').mean()

print("Average non-zero orders per week for each year:")
print(average_non_zero_orders_per_week_by_year)
