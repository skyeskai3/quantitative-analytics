import pandas as pd

def count_weeks_with_orders(csv_file):
    df = pd.read_csv(csv_file)

    df['date_utc'] = pd.to_datetime(df['date_utc'])

    df['year'] = df['date_utc'].dt.year
    df['week'] = df['date_utc'].dt.strftime('%Y-%U')

    weekly_counts = df.groupby(['year', 'week']).apply(lambda x: (x['order_type'] != 0).any()).groupby('year').sum()

    total_weeks = df.groupby('year')['week'].nunique()

    weeks_without_orders = total_weeks - weekly_counts

    return weeks_without_orders, weekly_counts

def print_results_by_year(weeks_without_orders, weekly_counts):
    print("Year\tWeeks Without Orders\tWeekly Counts")
    for year in weeks_without_orders.index:
        print(f"{year}\t{weeks_without_orders[year]}\t\t\t{weekly_counts.get(year, 0)}")

csv_file = 'SPY_v2_hourly.csv'
weeks_without_orders, weekly_counts = count_weeks_with_orders(csv_file)
print_results_by_year(weeks_without_orders, weekly_counts)

