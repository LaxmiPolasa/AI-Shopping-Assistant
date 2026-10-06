from bs4 import BeautifulSoup


def scrape_products(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "lxml")

    products = []

    for item in soup.select(".product"):
        name = item.select_one(".name")
        price = item.select_one(".price")

        if name and price:
            products.append({
                "name": name.get_text(strip=True),
                "price": price.get_text(strip=True)
            })

    return products