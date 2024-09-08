# Use Python 3.11 as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /web_scraper

# Copy the current directory contents into the container at /app
COPY . /web_scraper

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]
