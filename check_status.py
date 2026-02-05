
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.getcwd())

from storage.database import init_db, get_session, ListingCRUD, ScrapeLogCRUD
from sqlalchemy import select, func
from storage.database import ScrapeLog
import logging
from loguru import logger

async def main():
    # Disable all logs
    logger.remove()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    
    output = []
    output.append(f"[{datetime.now()}] Checking Database Status...")
    
    await init_db()
    
    async with get_session() as session:
        # 1. Count Listings
        count = await ListingCRUD.count(session)
        output.append(f"📊 Total Listings: {count}")
        
        # 2. Check Recent Scrape Logs
        output.append("\n📜 Recent Scrape Logs (Last 5):")
        result = await session.execute(
            select(ScrapeLog)
            .order_by(ScrapeLog.started_at.desc())
            .limit(5)
        )
        logs = result.scalars().all()
        
        if not logs:
            output.append("   (No logs found)")
        
        for log in logs:
            duration = f"{log.duration_seconds:.1f}s" if log.duration_seconds else "running"
            output.append(f"   - [{log.started_at.strftime('%H:%M:%S')}] {log.platform}: {log.status} "
                  f"(Found: {log.listings_found}, New: {log.listings_new}) [{duration}]")
            if log.error_message:
                output.append(f"     ❌ Error: {log.error_message[:100]}...")
            if log.id:
                 output.append(f"     ID: {log.id}")

    with open("status_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
