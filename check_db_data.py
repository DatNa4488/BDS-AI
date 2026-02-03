import asyncio
import os
import sys

# Disable logging before imports
os.environ["LOG_LEVEL"] = "ERROR"
os.environ["DEBUG"] = "false"

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from storage.database import Listing, ScrapeLog
from config import settings

async def check_data():
    print("--- START DB CHECK ---")
    print(f"DB URL: {settings.database_url}")
    
    # Create engine locally to force echo=False
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with async_session() as session:
            # Check Listings
            result = await session.execute(select(func.count(Listing.id)))
            count = result.scalar_one()
            print(f"Total Listings: {count}")

            if count > 0:
                result = await session.execute(select(Listing).limit(1))
                listing = result.scalar_one()
                print(f"Sample Listing: '{listing.title}' | Price: {listing.price_text} | District: {listing.district} | Status: {listing.status}")
                
            # Check Scrape Logs
            result = await session.execute(select(func.count(ScrapeLog.id)))
            log_count = result.scalar_one()
            print(f"Total Scrape Logs: {log_count}")
            
            if log_count > 0:
                 result = await session.execute(select(ScrapeLog).order_by(ScrapeLog.started_at.desc()).limit(1))
                 log = result.scalar_one()
                 print(f"Last Scrape Log: {log.platform} | Found: {log.listings_found} | Error: {log.error_message}")

    except Exception as e:
        print(f"Error accessing database: {e}")
    finally:
        await engine.dispose()
    print("--- END DB CHECK ---")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_data())
