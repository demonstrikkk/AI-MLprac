import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
print()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
}
response = requests.get('https://books.toscrape.com/catalogue/page-1.html', headers=headers)
final = pd.DataFrame()
namez = []
ratie = []
prize = []
stonk = []

for h in range(1, 51):
    webpage = requests.get(f'https://books.toscrape.com/catalogue/page-{h}.html').text
    soup = BeautifulSoup(webpage, 'lxml')

    company = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    for i in company:
        # Book Name
        img_tag = i.find('img')
        namez.append(img_tag['alt'].strip() if img_tag and 'alt' in img_tag.attrs else 'No name found')

        # Rating
        rating_tag = i.find('p', class_='star-rating')
        rating_class = [cls for cls in rating_tag['class'] if cls != 'star-rating']
        ratie.append(rating_class[0] if rating_class else 'No rating found')

        # Price
        price_tag = i.find('p', class_='price_color')
        prize.append(price_tag.text.strip() if price_tag else 'No price found')

        # Stock
        stock_tag = i.find('p', class_='instock availability')
        stonk.append(stock_tag.text.strip() if stock_tag else 'No stock found')

df = pd.DataFrame({
    'name': namez,
    'rating': ratie,
    'price': prize,
    'stock': stonk,
})
final = pd.concat([final, df], ignore_index=True)

# Fill missing prices, rename column, and convert prices
df = df.fillna('Â£25.02')
df.rename(columns={'price': 'price(in Rs)'}, inplace=True)
df['price(in Rs)'] = df['price(in Rs)'].str.replace(r'^(Â£)\s*', '', regex=True).astype(float) * 91.36

# Use the updated profiling library
from ydata_profiling import ProfileReport

# Generate the profile report
profile = ProfileReport(df, title="Books stall", explorative=True)

# Save the report to an HTML file
profile.to_file("report.html")
