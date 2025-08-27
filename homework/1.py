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
        title = title_item.get_text() if title_item else "No title"

        price_item = item.find_next('p', class_="css-uj7mm0")
        price = price_item.get_text() if price_item else "No price"

        location_time_item = item.find_next('p', class_="css-vbz67q")
        location_time = location_time_item.get_text() if location_time_item else "No location/date"

        run_item = item.find_next('span', class_="css-6as4g5")
        run = run_item.get_text() if run_item else "No run"

        link_item = item.find_next('a', class_="css-1tqlkj0")
        link = HOST + link_item.get("href") if link_item else None

        image_url = get_high_quality_image(link) if link else "No image"

        cards.append({
            "title": title,
            "price": price,
            "location & date": location_time,
            "facture date & run": run,
            "link": link,
            "image": image_url
        })
    return cards


def get_high_quality_image(car_url):
    html = get_html(car_url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, "html.parser")
        image_tag = soup.find("img", class_="css-1bmvjcs")
        if image_tag:
            return image_tag.get("src")
    return "No image found"


def save_to_csv(cards, path):
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Title', 'Price', 'Location & Date', 'Facture Date & Run', 'Link', 'Image'])
        for card in cards:
            writer.writerow([
                card['title'], 
                card['price'], 
                card['location & date'], 
                card['facture date & run'], 
                card['link'],
                card['image']
            ])


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

