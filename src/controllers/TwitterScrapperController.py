import datetime
import os
from socket import gethostbyname, gethostname
from src.models.mongodb import collection
from src.services.TwitterScrapper import TwitterScraper

async def get_trends_data():
    # Fetch the latest record from MongoDB
    latest_record = collection.find_one(sort=[("timestamp", -1)])
    if latest_record:
        latest_record["_id"] = str(latest_record["_id"])  
    return latest_record


async def run_trends_script():
    try:
        twitter_email = os.getenv("TWITTER_EMAIL")
        twitter_password = os.getenv("TWITTER_PASSWORD")
        twitter_user_id = os.getenv("TWITTER_USER_ID")
        scraper = TwitterScraper(twitter_email, twitter_password, twitter_user_id)
        result = scraper.get_latest_trends()
        print(result)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = gethostbyname(gethostname())

        # Create the record to save in MongoDB
        record = {
            "timestamp": timestamp,
            "ip_address": ip_address,
            "trends": result
        }

        # Insert the record into MongoDB
        inserted_record = collection.insert_one(record)

        # Convert the _id to a string
        record["_id"] = str(inserted_record.inserted_id)

        return {
            "message": "Script executed successfully.",
            "record": record
        }

    except Exception as e:
        # Handle exceptions and return error information
        return {"message": "Script execution failed.", "error": str(e)}