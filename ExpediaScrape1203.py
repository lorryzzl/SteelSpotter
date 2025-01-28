import time
import pandas as pd
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import sys


async def expedia_scrape(destination, check_in_date, check_out_date):
    hotels_data = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()

        url = (
            #f'https://www.expedia.com/Hotel-Search?destination=Pittsburgh%2C+Pennsylvania%2C+United+States+of+America'
            f'https://www.expedia.com/Hotel-Search?'
            f'destination={destination}&startDate={check_in_date}&endDate={check_out_date}'
        )
        await page.goto(url)


        page.wait_for_selector('.uitk-card', timeout=60000)


        previous_height = 0
        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            current_height = await page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break
            previous_height = current_height


        cards = await page.locator('[data-stid="lodging-card-responsive"]').all()
        print(f"Found {len(cards)} hotels")

        for card in cards:
            content = card.locator('div.uitk-card-content-section')
            title = await content.locator('h3').text_content(timeout=1000) if await content.locator('h3').count() > 0 else "N/A"


            rating_elements = content.locator('span.uitk-badge-base-text')
            rating = "N/A"
            count = await rating_elements.count()
            for i in range(count):
                text = await rating_elements.nth(i).text_content()
                if text.replace('.', '').isdigit():
                    rating = text
                    break


            price = (
                await content.locator('div.uitk-type-500').text_content(timeout=1000)
                if await content.locator('div.uitk-type-500').count() > 0
                else "N/A"
            )

            hotels_data.append([title, price, rating])


        df = pd.DataFrame(hotels_data, columns=['Hotel Name', 'Price', 'Rating'])
        df.to_csv('pittsburgh_hotels.csv', index=False, encoding='utf-8-sig')
        print("Saved to pittsburgh_hotels.csv")

        await browser.close()

    return df


#if __name__ == "__main__":
#    destination = 'Pittsburgh Pennsylvania'
#    check_in_date = "2024-12-10"
#    check_out_date = "2024-12-15"
#    df = expedia_scrape(destination, check_in_date, check_out_date)