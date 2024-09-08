from fastapi import FastAPI, Header
from models import ScrapeRequest, ScrapeResponse
from scraper import ProductScraper
from notification import Communication
from auth import Auth

app = FastAPI()

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest, authorization: str = Header(...)):  
    # Call the Auth class for authentication
    Auth.authenticate(authorization)
    
    scraper = ProductScraper(pages_limit=request.pages_limit, proxy=request.proxy)

    # Run the scraping asynchronously
    scraped_data, scraped_count, updated_count = await scraper.scrape_data()

    # Communicate the result
    Communication.notify(scraped_count, updated_count)
    
    return ScrapeResponse(scraped_count=scraped_count, updated_count=updated_count, products=scraped_data)