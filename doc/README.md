# TwitterScraper Class

This is a reusable Python class for logging into Twitter (X.com) and scraping trending topics. It is designed to be used as a service.

## Features
- Securely logs into Twitter using an email, password, and user ID.
- Scrapes trending topics from Twitter.
- Supports proxy routing for anonymous and secure browsing.
- Includes error handling with screenshots for debugging purposes.

## Prerequisites

1. **Credentials**: An email, password, and user ID from a Twitter account.  
2. **Proxy Routes**: A list of proxy addresses to route requests through different IPs.  
3. **Headless Browser**: The browser is headless by default but may need adjustments based on Twitter's bot detection mechanisms.  

## Usage

### 1. Set Up Your Credentials
Replace the placeholders `email`, `password`, and `user_id` in the `TwitterScraper` class instantiation with your Twitter credentials.

### 2. Integrate into Your Project
Import the class into your codebase and use its methods as needed:

```python
from twitter_scraper import TwitterScraper

# Initialize scraper
scraper = TwitterScraper(email="your_email", password="your_password", user_id="your_user_id")

# Fetch the latest trends
trending_topics = scraper.get_latest_trends()

# Use the trends in your application
if trending_topics:
    for trend in trending_topics:
        print(trend)
else:
    print("No trends found or an error occurred.")
```

### 3. Proxy Setup
To enhance security and anonymity, update the `proxy_routes` list in the `TwitterScraper` class with additional proxy addresses as needed:

```python
self.proxy_routes = [
    "us-ca.proxymesh.com:31280",
    "another-proxy-address:port"
]
```

### 4. Debugging
- Screenshots are automatically saved in the working directory if errors occur during the login or scraping process.
