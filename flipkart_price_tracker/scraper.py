import requests
from bs4 import BeautifulSoup

def scrape_flipkart(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Update the class names based on the current HTML structure
    title_tag = soup.find("span", {"class": "VU-ZEz"})  # Check and replace with actual class name
    title = title_tag.get_text(strip=True) if title_tag else "Title Not Found"

    price_tag = soup.find("div", {"class": "Nx9bqj CxhGGd"})  # Check and replace with actual class name
    price = price_tag.get_text(strip=True) if price_tag else "Price Not Found"

    description_tag = soup.find("div", {"class": "_2418kt"})  # Check and replace with actual class name
    description = description_tag.get_text(strip=True) if description_tag else "Description Not Found"

    reviews_tag = soup.find("div", {"class": "Wphh3N"})  # Check and replace with actual class name
    reviews = reviews_tag.get_text(strip=True) if reviews_tag else "Reviews Not Found"

    purchases_tag = soup.find("span", {"class": "Nx9bqj CxhGGd"})  # Check and replace with actual class name
    total_purchases = purchases_tag.get_text(strip=True) if purchases_tag else "Total Purchases Not Found"

    return {
        'title': title,
        'price': price,
        'description': description,
        'reviews': reviews,
        'total_purchases': total_purchases
    }
