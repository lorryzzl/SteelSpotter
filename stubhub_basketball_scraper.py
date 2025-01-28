import time
import pandas as pd
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from datetime import datetime
#import asyncio
from io import BytesIO

async def scrape_stubhub_basketball():
    tickets_data = []
    events_list = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False,
                                    args=["--disable-geolocation"])
        page = await browser.new_page()
        for j in [1,2,3]:
            url = f'https://www.stubhub.com/pittsburgh-panthers-basketball-tickets/performer/6847?restPage={j}'
            await page.goto(url)

            time.sleep(3)
            events = await page.locator('ul[data-testid="restGrid"] div.sc-1mafo1b-4.dvCFno').all()  # Event titles
            dates = await page.locator('ul[data-testid="restGrid"] div.sc-ja5jff-4.xDqPX').all()  # Event dates
            times = await page.locator('ul[data-testid="restGrid"] div.sc-ja5jff-9.hlAPsD').all()  # Event times
            addresses = await page.locator('ul[data-testid="restGrid"] div.sc-1pilhev-8.kArOQy').all()  # Event addresses
            prices_buttons = await page.locator('ul[data-testid="restGrid"] button.sc-6f7nfk-0.bRXaeK.sc-lub4vc-7.heBkB').all() # Buttons to view prices
            

            for i in range(len(events)):
                print('Crawling a new game...')
                event_title = await events[i].text_content()
                event_title = event_title.strip()
                if event_title in events_list:
                    print('Already exist. Pass.')
                    continue
                events_list.append(event_title)
                event_date = await dates[i].text_content()
                event_date = event_date.strip()           
                # Make sure all dates have the same format
                if len(event_date.split(' ')) == 2:
                    event_date = event_date + ' 2024'
                parsed_date = datetime.strptime(event_date, '%b %d %Y')
                # Format the parsed date to the desired format
                event_date = parsed_date.strftime('%Y-%m-%d')
                a = await times[2*i].text_content()
                b = await times[2*i+1].text_content()
                event_time = a.strip() + ' ' + b.strip()
                event_address = await addresses[i].text_content()
                event_address = event_address.strip()
                
                # Click the next button
                new_page = None
                context = browser.contexts[0]

                async with context.expect_page() as new_page_info:
                    next_button = prices_buttons[i]
                    await next_button.click()

                # Get the new page reference
                new_page = await new_page_info.value

                price_url = str(new_page.url)
                price_url = price_url + "?quantity=1"
                print(price_url)
                new_page = await browser.new_page()
                try:
                    await new_page.goto(price_url, timeout=30000)
                except TimeoutError:
                    continue

                time.sleep(3)
                price_container = new_page.locator('div.sc-xrltsx-2.gCDBVD').nth(1)
                print(await price_container.text_content())
                price_range = await price_container.locator('div.sc-1urpwzu-1.kFqMiL').text_content()
                price_range = price_range.strip()
                await new_page.close()

                tickets_data.append([event_title, event_date, event_time, event_address, price_range])

            # Go to page 4 from page 3:
            if j == 3:
                next_page_buttons = await page.locator("div.sc-12pgy4t-0.stRnx button.sc-6f7nfk-0.fLcQnj.sc-12pgy4t-1.iGPtIk").all()
                print(len(next_page_buttons))
                next_page_button = next_page_buttons[-1]
                next_page_button.click()
                time.sleep(3)
                events = await page.locator('ul[data-testid="restGrid"] div.sc-1mafo1b-4.dvCFno').all()  # Event titles
                dates = await page.locator('ul[data-testid="restGrid"] div.sc-ja5jff-4.xDqPX').all()  # Event dates
                times = await page.locator('ul[data-testid="restGrid"] div.sc-ja5jff-9.hlAPsD').all()  # Event times
                addresses = await page.locator('ul[data-testid="restGrid"] div.sc-1pilhev-8.kArOQy').all()  # Event addresses
                prices_buttons = await page.locator('ul[data-testid="restGrid"] button.sc-6f7nfk-0.bRXaeK.sc-lub4vc-7.heBkB').all() # Buttons to view prices
                
                print(len(events))

                for i in range(len(events)):
                    print('Crawling a new game...')
                    event_title = await events[i].text_content()
                    event_title = event_title.strip()
                    if event_title in events_list:
                        print('Already exist. Pass.')
                        continue
                    events_list.append(event_title)
                    event_date = await dates[i].text_content()
                    event_date = event_date.strip()           
                    # Make sure all dates have the same format
                    if len(event_date.split(' ')) == 2:
                        event_date = event_date + ' 2024'
                    parsed_date = datetime.strptime(event_date, '%b %d %Y')
                    # Format the parsed date to the desired format
                    event_date = parsed_date.strftime('%Y-%m-%d')
                    a = await times[2*i].text_content()
                    b = await times[2*i+1].text_content()
                    event_time = a.strip() + ' ' + b.strip()
                    event_address = await addresses[i].text_content()
                    event_address = event_address.strip()
                    
                    # Click the next button
                    new_page = None
                    context = browser.contexts[0]

                    with context.expect_page() as new_page_info:
                        next_button = prices_buttons[i]
                        next_button.click()

                    # Get the new page reference
                    new_page = await new_page_info.value

                    price_url = str(new_page.url)
                    price_url = price_url + "?quantity=1"
                    print(price_url)
                    new_page = await browser.new_page()
                    try:
                        await new_page.goto(price_url, timeout=30000)
                    except TimeoutError:
                        continue

                    time.sleep(3)
                    price_container = await new_page.locator('div.sc-xrltsx-2.gCDBVD').nth(1)
                    print( price_container.text_content())
                    price_range = await price_container.locator('div.sc-1urpwzu-1.kFqMiL').text_content()
                    price_range = price_range.strip()
                    await new_page.close()

                    tickets_data.append([event_title, event_date, event_time, event_address, price_range])

        await browser.close()  # Close the browser

    # Save the data to a DataFrame and export as CSV
    df = pd.DataFrame(tickets_data, columns=["Event Title", "Date", "Time", "Address", "Price Range"])
    return df

def download_csv(dataframe):
    output = BytesIO()
    dataframe.to_csv(output, index=False)
    output.seek(0)
    return output

#if __name__ == "__main__":
#    df = scrape_stubhub_basketball()
#    df.to_csv('stubhub_basketball_tickets.csv', index=False)
