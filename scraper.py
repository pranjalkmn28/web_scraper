import json
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from models import Product
from database import Database
from cache import Cache
import asyncio

class ProductScraper:
    def __init__(self, pages_limit=1, proxy=None, data_file='products.json'):
        self.pages_limit = pages_limit
        self.proxy = proxy
        self.data_file = data_file
        self.scraped_data = []
        self.updated_data_count = 0
        self.scraped_data_count = 0
        self.existing_data = []  # Initialize as an empty list

    async def initialize(self):
        """Initialize the scraper by loading existing data."""
        self.existing_data = await self.load_existing_data()


    async def load_existing_data(self):
        """Load existing data from the JSON file asynchronously."""
        try:
            async with aiofiles.open(self.data_file, 'r') as file:
                content = await file.read()
                # Convert dictionaries back to Product objects
                data = json.loads(content)
                return [Product(**item) for item in data] if isinstance(data, list) else []
        except FileNotFoundError:
            return []  # Return an empty list if the file doesn't exist


    async def save_data(self):
        """Save the data to the JSON file asynchronously."""
        await Database.save_to_json(self.existing_data)


    async def fetch_url_with_retries(self, url, retries=3, timeout=10):
        """Fetch a URL with retries and exponential backoff asynchronously."""
        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=timeout) as response:
                        print(response)
                        response.raise_for_status()
                        return await response.text()
            except aiohttp.ClientError as e:
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Error: {e}, retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"Failed to fetch URL after {retries} attempts: {e}")
                    raise


    async def scrape_data(self):
        """Scrape data from the specified number of pages asynchronously."""
        for page_num in range(1, self.pages_limit + 1):
            url = f"https://dentalstall.com/shop/page/{page_num}/"
            try:
                html = await self.fetch_url_with_retries(url)
                soup = BeautifulSoup(html, 'html.parser')
                products = soup.find_all("li", class_="product")
                print(f"Found {len(products)} products.")

                for product in products:
                    title = self.extract_title(product)
                    price = self.extract_price(product)
                    image_url = self.extract_image_url(product)

                    if title and price is not None:
                        image_path = await Database.download_image(image_url) if image_url else None
                        product_obj = Product(
                            product_title=title,
                            product_price=price,
                            path_to_image=image_path
                        )

                        # Check cache before updating
                        print("product_obj -----", product_obj)
                        if not await Cache.cache_product(product_obj):
                            self.scraped_data.append(product_obj)
                            self.update_existing_data(title, price, image_path)
                            self.updated_data_count += 1
                        self.scraped_data_count += 1
            except aiohttp.ClientError as e:
                print(f"Error scraping {url}: {e}")

        await self.save_data()  # Save updated data to JSON file
        print(f"Scraped {self.scraped_data_count} products, updated {self.updated_data_count} entries in JSON.")
        return self.scraped_data, self.scraped_data_count, self.updated_data_count


    def extract_title(self, product):
        """Extract the product title from the HTML element."""
        title_elem = product.find("h2", class_="woo-loop-product__title")
        if title_elem:
            return title_elem.find("a").text.strip()
        print("Title not found")
        return None


    def extract_price(self, product):
        """Extract the product price from the HTML element."""
        price_elem = product.find("span", class_="woocommerce-Price-amount amount")
        if price_elem:
            price_str = price_elem.text.strip().replace("₹", "").replace(",", "")
            try:
                return float(price_str)
            except ValueError:
                print(f"Price conversion error: {price_str}")
                return None
        print("Price not found")
        return None


    def extract_image_url(self, product):
        """Extract the product image URL from the HTML element."""
        image_elem = product.find("img")
        if image_elem:
            return image_elem.get("data-lazy-src")
        print("Image URL not found")
        return None


    def update_existing_data(self, title, price, image_path):
        """Update existing data with the new product information."""
        for existing_product in self.existing_data:
            if existing_product['product_title'] == title:
                existing_product['product_price'] = price
                existing_product['path_to_image'] = image_path
                break
        else:
            self.existing_data.append({
                "product_title": title,
                "product_price": price,
                "path_to_image": image_path
            })