import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from playwright.sync_api import sync_playwright
import time
from ExpediaScrape1203 import expedia_scrape  # Assume this module exists for hotel scraping
import combine_tickets_data  # Import the module
from UPitts_Team_And_Individual import scrape_team_and_individual_stats
from stubhub_basketball_scraper import scrape_stubhub_basketball, download_csv
from stubhub_football_scraper import scrape_stubhub_football
import sys
import asyncio

# Streamlit Interface
st.title("SteelSpotter")
st.sidebar.header("Step Selection")

# Step Selection: Query Games or Hotels
step = st.sidebar.radio("Choose a Step", ("Search Games", "Search Hotels","Team Stats"))

if step == "Search Games":
    # Load the data
    # Call the main function from combine_tickets_data.py to generate the combined CSV
    combine_tickets_data.main()
    file_path = 'combined_tickets_data.csv'
    data = pd.read_csv(file_path)

    # Combine year, month, and date into a single datetime column
    data['game_date'] = pd.to_datetime(
        data[['year', 'month', 'date']].astype(str).agg('-'.join, axis=1),
        errors='coerce'
    )
    data['game_date_str'] = data['game_date'].dt.strftime('%Y-%m-%d')
    data['game_date_str'] = data['game_date_str'].fillna('TBD')

    # Streamlit interface
    st.title("Ticket Price and Game Information")

    # 1. Draw a line chart of ticket prices over time for two platforms
    # Filter non-TBD data
    non_tbd_data = data[data['game_date'].notna()].sort_values('game_date')
    # Ensure there's a 'platform' column; this can be StubHub or SeatGeek
    if 'platform' not in data.columns:
        st.warning("No 'platform' column found in the dataset. Please add one to distinguish platforms.")
    else:
        # Create a plot for each platform for both football and basketball games
        non_tbd_data_basketball = non_tbd_data[non_tbd_data['category']=='Mens Basketball']
        non_tbd_data_football = non_tbd_data[non_tbd_data['category']=='Mens Football']

        fig, ax = plt.subplots(figsize=(9, 5))
        for platform, platform_data in non_tbd_data_basketball.groupby('platform'):
            ax.plot(platform_data['game_date'], platform_data['price'], marker='o', label=platform)

        # Set plot properties
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.set_title("Pittsburgh Panthers Basketball Ticket Prices Over Time")
        ax.legend(title="Platform")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(9, 5))
        for platform, platform_data in non_tbd_data_football.groupby('platform'):
            ax.plot(platform_data['game_date'], platform_data['price'], marker='o', label=platform)

        # Set plot properties
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.set_title("Pittsburgh Steelers Football Ticket Prices Over Time")
        ax.legend(title="Platform")
        plt.xticks(rotation=45)
        st.pyplot(fig)



    # Let uers scrape the data online and download the data as a csv file.
    import asyncio
    import sys

    if st.button("Scrape Basketball Game Data From StubHub and Download (~ 3 mins)"):
        # Set the event loop policy for Windows
        if sys.platform.lower().startswith("win"):
            loop = asyncio.ProactorEventLoop()
            #loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            # Use the default SelectorEventLoop on macOS and other platforms
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            with st.spinner("Scraping data..."):
                # Perform scraping
                scraped_stubhub_basketball_data = loop.run_until_complete(scrape_stubhub_basketball())
            st.success("Scraping completed!")
            
            # Prepare CSV for download
            scraped_stubhub_basketball_data_csv = download_csv(scraped_stubhub_basketball_data)
            st.download_button(
                label="Download Scraped Data",
                data=scraped_stubhub_basketball_data_csv,
                file_name="scraped_stubhub_basketball_data.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Scrape Footaball Game Data From StubHub and Download (~ 1 min)"):
        # Set the event loop policy for Windows
        if sys.platform.lower().startswith("win"):
            loop = asyncio.ProactorEventLoop()
            #loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            # Use the default SelectorEventLoop on macOS and other platforms
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            with st.spinner("Scraping data..."):
                # Perform scraping
                scraped_stubhub_football_data = loop.run_until_complete(scrape_stubhub_football())
            st.success("Scraping completed!")
            
            # Prepare CSV for download
            scraped_stubhub_football_data_csv = download_csv(scraped_stubhub_football_data)
            st.download_button(
                label="Download Scraped Data",
                data=scraped_stubhub_football_data_csv,
                file_name="scraped_stubhub_football_data.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # 2. Let users choose a category
    st.subheader("Filter by Category")
    category = st.selectbox("Select Category", data['category'].unique())

    # Filter data by selected category
    filtered_data = data[data['category'] == category]

    # Remove duplicates based on year, month, date, and home team
    filtered_data_game = filtered_data.drop_duplicates(subset=['year', 'month', 'date', 'home'])

    # Sort the filtered data by date
    filtered_data_game = filtered_data.sort_values('game_date')

    # 3. Show all games for the selected category without index
    st.subheader(f"Games for {category}")
    # Use style to hide the index

    # Further data process
    filtered_data_game = filtered_data_game.drop_duplicates(subset=['game_date_str', 'platform'])
    df_stubhub = filtered_data_game[filtered_data_game['platform']=='Stubhub']
    df_seatgeek = filtered_data_game[filtered_data_game['platform']=='Seatgeek']
    merged_filtered_data_game = pd.merge(df_stubhub, df_seatgeek, on=['game_date_str'], how='outer')
    cols_keep = ['game_date_str', 'away_x', 'home_x', 'day_x', 'time_x', 'price_x', 'price_y']
    merged_filtered_data_game = merged_filtered_data_game[cols_keep]
    merged_filtered_data_game.columns = ['date', 'away', 'home', 'day', 'time','Stubhub price','Seatgeek price']
    filtered_data_game = merged_filtered_data_game.copy()

    st.dataframe(filtered_data_game[['date', 'away', 'home', 'day', 'time', 'Stubhub price','Seatgeek price']].reset_index(drop=True))

    # 4. Let users choose the date of one game
    st.subheader("Select a Game Date")
    game_date_str = st.selectbox(
        "Game Date",
        filtered_data['game_date_str'].unique()
    )
    # 5. Show information about the selected game for both platforms
    if game_date_str:
        # Filter data for the selected date
        selected_game = filtered_data[filtered_data['game_date_str'] == game_date_str]

        # Remove exact duplicate rows
        selected_game = selected_game.drop_duplicates()

        if not selected_game.empty:
            st.write("### Game Details")

            # Group data by unique game information and collect platform-specific prices
            grouped_game = (
                selected_game
                .groupby(['game_date_str', 'away', 'home', 'day', 'time'])
                .apply(lambda group: ", ".join(
                    [f"{platform}: ${price}" for platform, price in zip(group['platform'], group['price'])]
                ))
                .reset_index(name='prices_by_platform')
            )

            # Display the game information along with consolidated prices from both platforms
            for _, row in grouped_game.iterrows():
                st.write(f"**Away Team:** {row['away']}")
                st.write(f"**Home Team:** {row['home']}")
                st.write(f"**Day:** {row['day']}")
                st.write(f"**Time:** {row['time']}")
                st.write(f"**Prices:** {row['prices_by_platform']}")
                st.write("---")  # Divider for readability
        else:
            st.write("No game found for the selected date.")

elif step == "Search Hotels":
    st.header("Search for Hotels")

    # User input for hotel query
    destination = st.text_input("Enter Destination", "Pittsburgh Pennsylvania")
    check_in_date = st.date_input("Check-In Date")
    check_out_date = st.date_input("Check-Out Date")
    # Convert date objects to strings in "YYYY-MM-DD" format
    check_in_date_str = check_in_date.strftime("%Y-%m-%d")
    check_out_date_str = check_out_date.strftime("%Y-%m-%d")

    if st.button("Search for Hotels"):
        if sys.platform.lower().startswith("win"):
            loop = asyncio.ProactorEventLoop()
            #loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            # Use the default SelectorEventLoop on macOS and other platforms
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        st.write("Fetching hotel data, please wait...")
        with st.spinner("Scraping hotel data..."):
            #try:
            # Call expedia_scrape function
            df_hotels = loop.run_until_complete(expedia_scrape(destination, check_in_date_str, check_out_date_str))
            st.session_state['df_hotels'] = df_hotels  # Store DataFrame in session state
            st.success("Hotel data fetched successfully!")
            st.write(f"Found {len(df_hotels)} hotels.")
            #except Exception as e:
            #    st.error(f"An error occurred: {e}")

    # Retrieve the stored DataFrame
    if 'df_hotels' in st.session_state:
        df_hotels = st.session_state['df_hotels']

        # Convert price column to numeric, handle missing or invalid values
        if 'Price' in df_hotels.columns:
            # Convert the column to string first to handle .str operations
            df_hotels['Price'] = df_hotels['Price'].astype(str)

            # Extract numeric values and convert them to float
            df_hotels['Price'] = df_hotels['Price'].str.extract('(\d+)').astype(float)

        # Plot the price distribution
        st.subheader("Price Distribution")
        if 'Price' in df_hotels.columns and not df_hotels['Price'].isna().all():
            fig, ax = plt.subplots()
            ax.hist(df_hotels['Price'].dropna(), bins=20, edgecolor="k", alpha=0.7)
            ax.set_title("Distribution of Hotel Prices")
            ax.set_xlabel("Price ($)")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
        else:
            st.warning("No valid price data available to display the distribution.")

        # Filter by price range
        st.subheader("Filter by Price Range")
        min_price, max_price = st.slider(
            "Select Price Range ($)",
            int(df_hotels['Price'].min()) if 'Price' in df_hotels.columns and not df_hotels['Price'].isna().all() else 0,
            int(df_hotels['Price'].max()) if 'Price' in df_hotels.columns and not df_hotels['Price'].isna().all() else 1000,
            (50, 300)
        )
        if 'Price' in df_hotels.columns:
            filtered_df = df_hotels[(df_hotels['Price'] >= min_price) & (df_hotels['Price'] <= max_price)]

            # Handle empty DataFrame gracefully
            if not filtered_df.empty:
                st.write(f"Hotels in the price range ${min_price} - ${max_price}:")
                st.dataframe(filtered_df)
            else:
                st.warning(f"No hotels found in the price range ${min_price} - ${max_price}. Showing all hotels instead.")
                st.dataframe(df_hotels)  # Display the full DataFrame if filter results are empty

            # Option to download the filtered data
            csv_hotels = filtered_df.to_csv(index=False, encoding='utf-8-sig') if not filtered_df.empty else ""
            st.download_button(label="Download Filtered Hotel Data", data=csv_hotels,
                               file_name="filtered_hotels_data.csv", mime="text/csv")
    else:
        st.info("Please search for hotels to display data.")

elif step == "Team Stats":
    st.header("Team and Individual Statistics")

    # Check if data already exists in session_state
    if 'team_stats_df' not in st.session_state or 'individual_stats_df' not in st.session_state:
        with st.spinner("Fetching team and individual statistics..."):
            try:
                # Scrape data and store in session_state
                team_stats_df, individual_stats_df = scrape_team_and_individual_stats()
                st.session_state['team_stats_df'] = team_stats_df
                st.session_state['individual_stats_df'] = individual_stats_df
                st.success("Statistics fetched successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        # Retrieve data from session_state
        team_stats_df = st.session_state['team_stats_df']
        individual_stats_df = st.session_state['individual_stats_df']

    # Display team statistics
    st.subheader("Team Statistics")
    st.dataframe(team_stats_df)

    # Display individual statistics
    st.subheader("Individual Statistics")
    st.dataframe(individual_stats_df)

    # Allow users to download the statistics
    team_csv = team_stats_df.to_csv(index=False, encoding='utf-8-sig')
    individual_csv = individual_stats_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(label="Download Team Statistics", data=team_csv, file_name="team_stats.csv", mime="text/csv")
    st.download_button(label="Download Individual Statistics", data=individual_csv,
                       file_name="individual_stats.csv", mime="text/csv")