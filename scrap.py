import requests
from bs4 import BeautifulSoup
import csv

def scrape_amazon_product_data(url):
  """Scrape product data from Amazon."""
  print(f" inside scrap_amazon_product_data-url: {url}")
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  
  print(f" inside scrap_amazon_product_data-soup: {soup}")
  
  product_data = {}
  product_data["product_url"] = url
  product_data["product_name"] = soup.find("span", class_="a-size-medium a-color-base").text
  product_data["product_price"] = soup.find("span", class_="a-price").text
  product_data["rating"] = soup.find("span", class_="a-icon-alt").text
  product_data["number_of_reviews"] = soup.find("span", class_="a-size-small").text

  print(f" inside scrap_amazon_product_data-product-data: {len(product_data)}")
  return product_data

def get_product_urls(base_url, page_num):
  """Get product URLs for a given page number."""
  url = base_url + "&page=" + str(page_num)
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  product_urls = []
  for product in soup.find_all("div", class_="a-section a-spacing-small product-tile"):
    product_url = product.find("a")["href"]
    product_urls.append(product_url)

  return product_urls

def scrape_all_products(base_url, num_pages):
  """Scrape all products from a given base URL and number of pages."""
  product_data = []

  for page_num in range(1, num_pages + 1):
    product_urls = get_product_urls(base_url, page_num)

    for product_url in product_urls:
      product_data.append(scrape_amazon_product_data(product_url))

  return product_data

def write_product_data_to_csv(product_data, filename):
  """Write product data to a CSV file."""
  with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["product_url", "product_name", "product_price", "rating", "number_of_reviews",
                    "description", "asin", "product_description", "manufacturer"])

    for product in product_data:
      writer.writerow(product.values())


if __name__ == "__main__":
  base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
  num_pages = 20

  product_data = scrape_all_products(base_url, num_pages)
  print(product_data)
  filename = "amazon_products.csv"
  write_product_data_to_csv(product_data, filename)
