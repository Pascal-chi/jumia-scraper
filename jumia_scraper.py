from helium import *
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time


def scrape_jumia_samsung_phones():
    # Start browser and navigate to Jumia Samsung phones page
    url = 'https://www.jumia.com.ng/phones-tablets/samsung/?q=samsung+phones#catalog-listing'
    browser = start_chrome(url, headless=True)

    # Wait for page to load completely
    time.sleep(3)

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Find all product cards
    product_cards = soup.find_all('article', {'class': 'prd _fb col c-prd'})

    phone_data = []

    for product in product_cards:
        try:
            # Extract phone name
            name_tag = product.find('h3', {'class': 'name'})
            name = name_tag.text.strip() if name_tag else "N/A"

            # Extract price
            price_tag = product.find('div', {'class': 'prc'})
            price = price_tag.text.strip() if price_tag else "N/A"

            # Extract product link
            link_tag = product.find('a', {'class': 'core'})
            relative_link = link_tag['href'] if link_tag else "#"
            link = urljoin(url, relative_link)

            # Only include actual Samsung phones (filter out accessories)
            if "samsung" in name.lower():
                phone_data.append({
                    'name': name,
                    'price': price,
                    'link': link
                })
        except Exception as e:
            print(f"Error processing a product: {e}")
            continue

    # Close the browser
    kill_browser()

    return pd.DataFrame(phone_data)


def save_to_csv(df, filename="jumia_samsung_phones.csv"):
  """save the saved data into a csv file"""
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    print("Starting Jumia Samsung phones scraper...")
    samsung_phones_df = scrape_jumia_samsung_phones()

    if not samsung_phones_df.empty:
        print("\nScraped Samsung Phones:")
        print(samsung_phones_df.head())
        save_to_csv(samsung_phones_df)
    else:
        print("No Samsung phones were scraped. Please check if the website structure has changed.")