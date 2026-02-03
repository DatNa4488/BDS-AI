import asyncio
import os
import sys
from datetime import datetime

# Disable logging before imports
os.environ["LOG_LEVEL"] = "ERROR"
os.environ["DEBUG"] = "false"

# Force encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from storage.database import Listing, ScrapeLog
from config import settings

async def check_analytics_data():
    print("--- DEBUG ANALYTICS DATA ---")
    
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with async_session() as session:
            # 1. Check Listings for Price Trends
            print("\n1. Checking Listings for Price Trends (active & has price_per_m2)...")
            result = await session.execute(
                select(Listing.id, Listing.title, Listing.price_per_m2, Listing.scraped_at, Listing.status)
                .limit(5)
            )
            listings = result.all()
            print(f"Total Listings found: {len(listings)}")
            for l in listings:
                print(f"   - [{l.status}] {l.title[:30]}... | Price/m2: {l.price_per_m2} | ScrapedAt: {l.scraped_at}")
                if l.price_per_m2 is None:
                    print(f"     ⚠️ WARNING: price_per_m2 is None! (Price Trends will ignore this)")

            # 2. Check Scrape Logs for Stats
            print("\n2. Checking Scrape Logs (status='completed' & last 7 days)...")
            from datetime import timedelta
            threshold = datetime.utcnow() - timedelta(days=7)
            print(f"   Query Threshold (UTC): {threshold}")
            print(f"   Current UTC: {datetime.utcnow()}")

            result = await session.execute(
                select(ScrapeLog)
                .order_by(ScrapeLog.started_at.desc())
                .limit(5)
            )
            logs = result.scalars().all()
            print(f"Total Logs found: {len(logs)}")
            for log in logs:
                print(f"   - ID: {log.id} | Status: '{log.status}' | Found: {log.listings_found} | Started: {log.started_at} (UTC)")
                
                # Verify match
                match_time = log.started_at >= threshold
                match_status = log.status == "completed"
                print(f"     -> Time match? {match_time} | Status match? {match_status}")

    except Exception as e:
        print(f"Error accessing database: {e}")
    finally:
        await engine.dispose()
    print("\n--- END DEBUG ---")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_analytics_data())
