from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_team_and_individual_stats():
    # set up
    driver = webdriver.Chrome()
    url = "https://pittsburghpanthers.com/sports/mens-basketball/stats"
    driver.get(url)

    # wait for page to load

    time.sleep(2)

    team_tab = driver.find_element(By.ID, "ui-id-3")  # Team ID
    team_tab.click()

    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    team_table = soup.find('table')
    headers = [header.text.strip() for header in team_table.find_all('th')]
    rows = []

    for row in team_table.find_all('tr')[1:]:  # Skip header row
        cells = row.find_all('td')
        rows.append([cell.text.strip() for cell in cells])

    team_stats_df = pd.DataFrame(rows, columns=headers)
    team_stats_df.to_csv("team_stats.csv", index=False)

    print("Team statistics saved successfully!")

    # Forindividual
    wait = WebDriverWait(driver, 10)
    individual_tab = wait.until(EC.element_to_be_clickable((By.ID, "ui-id-4")))  # 4 for individual section
    individual_tab.click()
    time.sleep(3)  # Allow content to load

    section_id = "individual-overall"
    section_element = wait.until(EC.presence_of_element_located((By.ID, section_id)))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("section", id=section_id).find("table")
    if table:

        headers = [header.text.strip() for header in table.find_all("th")]

        # Extract table rows
        rows = []
        for row in table.find("tbody").find_all("tr"):
            cells = [cell.text.strip() for cell in row.find_all(["td", "th"])]

            if len(cells) != len(headers):
                # Pad the row with empty strings to match the headers
                cells += [""] * (len(headers) - len(cells))
            rows.append(cells)

        df = pd.DataFrame(rows, columns=headers)
        df.columns = [
            f"{col}_{i}" if duplicate else col
            for i, (col, duplicate) in
            enumerate(zip(df.columns, df.columns.duplicated()))
        ]
        # Save the DataFrame as a CSV
        df.to_csv("individual_overall_fixed.csv", index=False)
        print("Data saved to 'individual_overall_fixed.csv'.")
    else:
        print(f"No table found in section '{section_id}'.")

    driver.quit()
    return team_stats_df, df

if __name__ == "__main__":
    team, individual = scrape_team_and_individual_stats()
    print(team)
    print(individual)



