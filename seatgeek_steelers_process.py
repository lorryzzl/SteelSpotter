import pandas as pd


def process_seatgeek_steelers(input_file):

    # Load the CSV file
    data = pd.read_csv(input_file)

    # Process the data to extract necessary information
    processed_data = pd.DataFrame({
        'category': ['Mens Football' for _ in range(len(data))],  # Fixed category value
        'away': data['Event Title'].str.split(' at ').str[0],  # Text before 'at'
        'home': data['Event Title'].str.split(' at ').str[1],  # Text after 'at'
        'month': data['Date'].apply(lambda x: 'TBD' if 'Date TBD' in x else x.split(' ')[0]),  # Month or TBD
        'date': data['Date'].apply(lambda x: 'TBD' if 'Date TBD' in x else int(x.split(' ')[1]) if len(x.split(' ')) > 1 else 'TBD'),
        'year': data['Date'].apply(lambda x: 'TBD' if 'Date TBD' in x else int(x.split(' ')[-1]) if len(x.split(' ')) > 1 and len(x.split(' ')[-1]) == 4 else 2024),
        'day': data['Time'].apply(lambda x: 'TBD' if 'Time TBD' in x else x.split(' · ')[0]),  # Day or TBD
        'time': data['Time'].apply(lambda x: 'TBD' if 'Time TBD' in x else x.split(' · ')[1] if ' · ' in x else 'TBD'),
        'price': data['Price'].str.extract(r'From \$(\d+)')[0].fillna(0).astype(float),  # Extract price
        'platform':['Seatgeek' for _ in range(len(data))]
    })

    print("SeatGeek Steelers Processed!")
    return pd.DataFrame(processed_data)

# # Display the processed DataFrame
# print(processed_data)
# processed_data.to_csv('processed_seatgeek_steelers_tickets.csv', index=False)
