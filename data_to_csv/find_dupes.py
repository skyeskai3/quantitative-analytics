import csv

# Replace 'your_csv_file.csv' with the actual path to your CSV file
csv_file_path = 'SPY_v2_hourly.csv'


# Open the CSV file
with open(csv_file_path, 'r') as csvfile:
    # Create a CSV reader object
    csv_reader = csv.DictReader(csvfile)

    # Specify the required header fields (obfuscated for proprietary purposes)
    required_headers = ['val1_price', 'val1_ts', 'val2_price', 'val2_ts', 'val3_price', 'val3_ts', 'val4_price', 'val4_ts', 'val5_price', 'val5_ts']

    # Initialize a list to store tuples (index, row) for matching rows
    matching_rows = []
    matching_rows_count=0
    # Iterate through each row
    for index, row in enumerate(csv_reader):
        # Extract values from the specified columns
        val1_price, val1_ts, val2_price, val2_ts, val3_price, val3_ts, val4_price, val4_ts, val5_price, val5_ts = map(float, [row[header] for header in required_headers])

        # Check the conditions
        if val1_price ==val2_price and val1_price in [val3_price,val4_price,val5_price] and val1_ts==val2_ts and val1_ts in [val3_ts,val4_ts,val5_ts] and val1_price != 0 and val1_ts != 0:
            # If conditions are met, add the tuple (index, row) to matching_rows
            matching_rows.append((index, row))
            matching_rows_count += 1

# Print the matching rows with indices
for index, match in matching_rows:
    print(f"Index: {index+2} was affected")

print(f"{matching_rows_count} rows were affected.")
