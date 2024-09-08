from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScrapeRequest(BaseModel):
    pages_limit: int = 1
    proxy: Optional[str] = None

class ScrapeResponse(BaseModel):
    scraped_count: int
    updated_count: int
    products: List[Product]
