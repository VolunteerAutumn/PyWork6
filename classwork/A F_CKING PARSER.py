import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.olx.ua/uk/transport/legkovye-avtomobili/"
HOST = "https://www.olx.ua"
CSV = "cards.csv"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}


def get_html(url, params=""):
    request = requests.get(url, headers=HEADERS, params=params)
    return request


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="css-1r93q13")
    cards = []
    for item in items:
        title_item = item.find_next('h4', class_="css-1g61gc2")
        title = title_item.get_text()

        price_item = item.find_next('p', class_="css-uj7mm0")
        price = price_item.get_text()

        location_time_item = item.find_next('p', class_="css-vbz67q")
        location_time = location_time_item.get_text()

        run_item = item.find_next('span', class_="css-6as4g5")
        run = run_item.get_text()

        link_item = item.find_next('a', class_="css-1tqlkj0")
        link = link_item.get("href")
        link = HOST + str(link)

        cards.append({
            "title": title,
            "price": price,
            "location & date": location_time,
            "facture date & run": run,
            "link": link,
        })
    return cards


def save_to_csv(cards, path):
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(['Title', 'Price', 'Location & Date', 'Facture Date & Run', 'Link'])
        for card in cards:
            writer.writerow([card['title'], card['price'], card['location & date'], card['facture date & run'], card['link']])


def parser():
    pagination = int(input("Enter the number of pages to parse > "))
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, pagination+1):
            print(f"Parsing page {str(page)}/{pagination}...")
            html = get_html(URL, params={"page": page})
            cards.extend(get_content(html.text))
            save_to_csv(cards, CSV)
    else:
        print("Error")


parser()
