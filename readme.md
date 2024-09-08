# Web Scraper Project

## Overview

The Web Scraper Project is a FastAPI-based web scraping application designed to extract product information from a specified e-commerce website. The application uses asynchronous requests to scrape product details, such as titles, prices, and image URLs. It supports caching with Redis and stores scraped data in JSON files. The project is containerized using Docker for easy deployment and execution.

## Features

- Asynchronous web scraping with aiohttp
- Caching using Redis
- Data storage in JSON format
- Image downloading and storage
- Token-based authentication for API endpoints

## Prerequisites

Before running the project, ensure you have the following installed:

- Docker
- Docker Compose

## Setup and Configuration

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/pranjalkmn28/web_scraper.git
cd web_scraper
```

### 2. Create a .env File

Create a `.env` file in the root directory of the project to store environment variables. You can use the provided `.env.example` file as a template. Make sure to set the following variables:

```
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CACHE_TIMEOUT=86400
AUTH_TOKEN=your_auth_token
```

### 3. Build and Run with Docker

Build and run the Docker containers using Docker Compose:

```bash
docker-compose up --build
```

This command will build the Docker images and start the necessary services, including the FastAPI application and Redis.

### 4. Access the Application

Once the containers are up and running, you can access the FastAPI application at:

```
http://localhost:8000
```

You can test the `/scrape` endpoint by sending a POST request with the necessary payload and an Authorization header containing the Bearer token.

## API Endpoints

### POST /scrape

**Description:** Scrapes product data from the e-commerce website.

**Request:**

- **Headers:**
  - Authorization: Bearer <your_auth_token>
- **Body:**
  ```json
  {
    "pages_limit": 1,
    "proxy": "http://your_proxy_url"
  }
  ```

**Response:**

- **200 OK:**
  ```json
  {
    "scraped_count": 10,
    "updated_count": 5,
    "products": [
      {
        "product_title": "Product Name",
        "product_price": 100.0,
        "path_to_image": "images/product_name.jpg"
      }
    ]
  }
  ```

- **403 Forbidden:** If the Authorization header is missing or invalid.

## Directory Structure

- `main.py`: Entry point for the FastAPI application.
- `scraper.py`: Contains the ProductScraper class for web scraping.
- `cache.py`: Manages Redis caching.
- `database.py`: Handles data storage and image downloading.
- `notification.py`: Contains notification functionality.
- `models.py`: Defines data models used in the application.
- `auth.py`: Handles authentication for the application.
- `Dockerfile`: Dockerfile for building the FastAPI application image.
- `docker-compose.yml`: Docker Compose configuration for running the application and Redis.
- `.env`: Environment variables configuration.
- `output/`: Directory where JSON files are saved.
- `images/`: Directory where downloaded images are stored.

## Troubleshooting

If you encounter issues:

- **500 Internal Server Error**: Check the logs for details about the error.
- **FileNotFoundError**: Ensure that directories specified in the code (e.g., `output/`, `images/`) are properly created and accessible.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to adjust any specific details related to your project or usage.
