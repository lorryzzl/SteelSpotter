import time
import pandas as pd
from playwright.sync_api import sync_playwright

tickets_data = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://seatgeek.com/pittsburgh-panthers-mens-basketball-tickets')

    page.wait_for_selector('[data-testid="event-item-title"]', timeout=60000)

    # Scroll to load all events
    previous_height = None

    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        current_height = page.evaluate("document.body.scrollHeight")
        if previous_height == current_height:
            break
        previous_height = current_height

    # Scrape event data
    events = page.locator('[data-testid="event-item-title"]').all()
    dates = page.locator('[data-testid="date"]').all()
    times = page.locator('[data-testid="time"]').all()
    prices = page.locator('span.Button__ButtonContents-sc-5deaac4-2').all()

    for i in range(len(events)):
        try:
            event_title = events[i].text_content()
        except:
            event_title = "N/A"
        try:
            event_date = dates[i].text_content()
        except:
            event_date = "N/A"
        try:
            event_time = times[i].text_content()
        except:
            event_time = "N/A"
        try:
            ticket_price = prices[i].text_content()
        except:
            ticket_price = "N/A"

        tickets_data.append([event_title, event_date, event_time, ticket_price])

    browser.close()

# Save the data to a DataFrame and export as CSV
df = pd.DataFrame(tickets_data, columns=["Event Title", "Date", "Time", "Price"])
df.to_csv('seatgeek_panthers_tickets.csv', index=False)
print("Panthers done!")