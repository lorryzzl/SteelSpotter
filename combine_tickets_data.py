import pandas as pd
from stubhub_steelers_process import process_steelers_data
from stubhub_panthers_process import process_panthers_data
from seatgeek_panthers_process import process_seatgeek_panthers
from seatgeek_steelers_process import process_seatgeek_steelers

def combine_tickets_data(stubhub_steelers_file, stubhub_panthers_file, seatgeek_steelers_file, seatgeek_panthers_file, output_file):
    """Combine all processed ticket data into one file."""
    steelers_stubhub = process_steelers_data(stubhub_steelers_file)
    panthers_stubhub = process_panthers_data(stubhub_panthers_file)
    steelers_seatgeek = process_seatgeek_steelers(seatgeek_steelers_file)
    panthers_seatgeek = process_seatgeek_panthers(seatgeek_panthers_file)

    combined_data = pd.concat([steelers_stubhub, panthers_stubhub, steelers_seatgeek, panthers_seatgeek], ignore_index=True)
    combined_data.to_csv(output_file, index=False)

def main():
    """Main execution function."""
    stubhub_steelers_file = 'stubhub_steelers_tickets.csv'
    stubhub_panthers_file = 'stubhub_panthers_tickets.csv'
    seatgeek_steelers_file = 'seatgeek_steelers_tickets.csv'
    seatgeek_panthers_file = 'seatgeek_panthers_tickets.csv'
    output_file = 'combined_tickets_data.csv'

    # Call the function to combine data
    combine_tickets_data(
        stubhub_steelers_file=stubhub_steelers_file,
        stubhub_panthers_file=stubhub_panthers_file,
        seatgeek_steelers_file=seatgeek_steelers_file,
        seatgeek_panthers_file=seatgeek_panthers_file,
        output_file=output_file
    )



if __name__ == "__main__":
    main()
    print(f"Combined data done！")