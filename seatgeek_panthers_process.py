import pandas as pd


def process_seatgeek_panthers(input_file):
    # Load the CSV file
    data = pd.read_csv(input_file)

    # Process the data to extract necessary information
    processed_data = pd.DataFrame({
        'category': data['Event Title'].str.split().str[-2:].str.join(' '),  # Last two words
        'away': data['Event Title'].str.split(' at ').str[0],  # Text before 'at'
        'home': data['Event Title'].str.extract(r'at (.*) (?:\w+ \w+)$')[0],  # Text after 'at' except last two words
        'month': data['Date'].str.split(' ').str[0],
        'date': data['Date'].str.extract(r'(\d+)')[0].fillna(0).astype(int),
        'year': data['Date'].str.extract(r'(\d{4})')[0].fillna(2024).astype(int),
        'day': data['Time'].str.split(' · ').str[0],
        'time': data['Time'].str.split(' · ').str[1].fillna('TBD'),
        'price': data['Price'].str.extract(r'From \$(\d+)')[0].fillna(0).astype(float),
        'platform':['Seatgeek' for _ in range(len(data))]
    })
    print("SeatGeek Panthers Processed!")
    return pd.DataFrame(processed_data)
    # # Display the processed DataFrame
    # print(processed_data)
    # processed_data.to_csv('processed_seatgeek_panthers_tickets.csv', index=False)
