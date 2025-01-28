import pandas as pd

def process_steelers_data(input_file):
    """Process StubHub Steelers ticket data."""
    data = pd.read_csv(input_file)
    processed_data = []

    for index, row in data.iterrows():
        event = row['Event Title']
        date = row['Date']
        time_info = row['Time']
        price_range = row['Price Range']

        if ' at ' in event:
            away, home = event.split(' at ', 1)
            home = home.strip()
        else:
            continue

        if date != "TBD":
            year, month, day = pd.to_datetime(date).year, pd.to_datetime(date).strftime('%b'), pd.to_datetime(date).day
        else:
            year, month, day = "TBD", "TBD", "TBD"

        if time_info != "TBD":
            day_of_week, event_time = time_info.split(' ', 1) if ' ' in time_info else ('TBD', 'TBD')
        else:
            day_of_week, event_time = "TBD", "TBD"

        try:
            min_price = int(price_range.split(' ')[0].replace('$', '').replace('+', ''))
        except:
            min_price = "TBD"

        processed_data.append({
            "category": "Mens Football",
            "away": away.strip(),
            "home": home.strip(),
            "month": month,
            "date": day,
            "year": year,
            "day": day_of_week.strip(),
            "time": event_time.strip(),
            "price": min_price,
            'platform': 'Stubhub'
        })

    print("Stubhub Steelers Processed!")
    return pd.DataFrame(processed_data)

# import pandas as pd
#
# # File paths
# input_file = 'stubhub_steelers_tickets.csv'
# output_file = 'processed_stubhub_steelers_tickets.csv'
#
# # Read the data
# data = pd.read_csv(input_file)
#
# # Initialize result list
# processed_data = []
#
# # Processing logic
# for index, row in data.iterrows():
#     event = row['Event Title']
#     date = row['Date']
#     time_info = row['Time']
#     price_range = row['Price Range']
#
#     # Extract away and home teamsa
#     if ' at ' in event:
#         away, home = event.split(' at ', 1)  # Split into "away" and the rest after "at"
#         home = home.strip()  # Include all words after "at"
#     else:
#         continue  # Skip rows without valid event structure
#
#     # Parse date
#     if date != "TBD":
#         year, month, day = pd.to_datetime(date).year, pd.to_datetime(date).strftime('%b'), pd.to_datetime(date).day
#     else:
#         year, month, day = "TBD", "TBD", "TBD"
#
#     # Parse time
#     if time_info != "TBD":
#         day_of_week, event_time = time_info.split(' ', 1) if ' ' in time_info else ('TBD', 'TBD')
#     else:
#         day_of_week, event_time = "TBD", "TBD"
#
#     # Extract minimum price
#     try:
#         min_price = int(price_range.split(' ')[0].replace('$', '').replace('+', ''))
#     except:
#         min_price = "TBD"  # Handle cases where price is invalid
#
#     # Append processed row
#     processed_data.append({
#         "category": "Mens Football",
#         "away": away.strip(),
#         "home": home.strip(),
#         "month": month,
#         "date": day,
#         "year": year,
#         "day": day_of_week.strip(),
#         "time": event_time.strip(),
#         "price": min_price,
#         'platform': 'Stubhub'
#     })
#
# # Create DataFrame and save
# processed_df = pd.DataFrame(processed_data)
# processed_df.to_csv(output_file, index=False)
