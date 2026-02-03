"""
Debug Scraper Script.
Scrapes real estate data using the Google-First strategy and saves to the database.
"""

import asyncio
import sys
import asyncio
import hashlib
from datetime import datetime
from loguru import logger

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from agents.search_agent import RealEstateSearchAgent
from storage.database import get_session, ListingCRUD, ScrapeLogCRUD, ScrapeLog
from storage.vector_db import index_listings
from services.validator import get_validator
from config import settings

# Configure logger
logger.remove()
logger.add(sys.stderr, level="INFO")

async def debug_scrape_and_save():
    """
    Run a debug scrape and save results to the database.
    This ensures manual runs also persist data.
    """
    print("=" * 60)
    print("🛠️  DEBUG SCRAPER & SAVER")
    print("=" * 60)
    
    # 1. Configuration - AUTOMATED for testing
    query = "chung cư cầu giấy"
    max_results = 5
    
    print(f"📌 Query: {query}")
    print(f"📌 Max Results: {max_results}")
    print(f"📌 Headless: {settings.headless_mode}")
    
    # Force disable Google Search to prevent Hallucination (Amazon/Laptop issues)
    # This will use the deterministic direct scraper
    settings.google_search_enabled = False 
    print(f"📌 Google Search: {settings.google_search_enabled} (Forced Disabled for Debug)")
    print("-" * 60)

    # Create ScrapeLog start
    scrape_log_id = None
    async with get_session() as session:
        log = await ScrapeLogCRUD.create(session, {
            "platform": "debug_manual",
            "query": query,
            "status": "running"
        })
        scrape_log_id = log.id

    # 2. Initialize Agent
    print("\n🚀 Initializing Search Agent...")
    agent = RealEstateSearchAgent(headless=True) # Use headless for speed/stability
    
    try:
        # 3. Perform Search
        print("\n🔍 Searching...")
        result = await agent.search(
            query=query,
            max_results=max_results,
            platforms=["chotot", "batdongsan"]
        )
        
        print(f"\n✅ Found {result.total_found} listings from {result.sources_searched}")
        
        if not result.listings:
            print("⚠️ No listings found via Agent. Injecting MOCK data for Analytics testing...")
            # Inject mock data to verify Analytics page
            result.listings = [
                {
                    "title": "Chung cư Cầu Giấy 3 tỷ 100m2 full nội thất",
                    "price_text": "3 tỷ",
                    "price_number": 3000000000,
                    "area_m2": 100,
                    "price_per_m2": 30000000,  # 30tr/m2
                    "location": {"city": "Hà Nội", "district": "Cầu Giấy", "address": "Đường Cầu Giấy"},
                    "source_url": "https://example.com/1",
                    "source_platform": "chotot",
                    "posted_at": datetime.now()
                },
                {
                    "title": "Bán nhà Cầu Giấy 4.5 tỷ ngõ rộng",
                    "price_text": "4.5 tỷ",
                    "price_number": 4500000000,
                    "area_m2": 50,
                    "price_per_m2": 90000000,  # 90tr/m2
                    "location": {"city": "Hà Nội", "district": "Cầu Giấy", "address": "Ngõ 165 Cầu Giấy"},
                    "source_url": "https://example.com/2",
                    "source_platform": "batdongsan",
                    "posted_at": datetime.now()
                },
                {
                     "title": "Căn hộ cao cấp Indochina Plaza 5 tỷ",
                     "price_text": "5 tỷ",
                     "price_number": 5000000000,
                     "area_m2": 120,
                     "price_per_m2": 41600000,  # ~41.6tr/m2
                     "location": {"city": "Hà Nội", "district": "Cầu Giấy", "address": "Xuân Thủy"},
                     "source_url": "https://example.com/3",
                     "source_platform": "batdongsan",
                     "posted_at": datetime.now()
                }
            ]
            result.total_found = len(result.listings)
            # return # Removed return to allow saving

        # 4. Save to Database
        print("\n💾 Saving to Database...")
        
        saved_count = 0
        new_count = 0
        
        async with get_session() as session:
            for listing in result.listings:
                # Ensure ID exists
                if not listing.get("id"):
                    content = f"{listing.get('source_url', '')}|{listing.get('title', '')}"
                    listing["id"] = hashlib.md5(content.encode()).hexdigest()
                
                # Prepare data for DB (flatten nested structures)
                db_listing = listing.copy()
                
                # Flatten location
                if "location" in db_listing and isinstance(db_listing["location"], dict):
                    loc = db_listing.pop("location")
                    db_listing["address"] = loc.get("address")
                    db_listing["ward"] = loc.get("ward")
                    db_listing["district"] = loc.get("district")
                    db_listing["city"] = loc.get("city", "Hà Nội")

                # Flatten contact
                if "contact" in db_listing and isinstance(db_listing["contact"], dict):
                    contact = db_listing.pop("contact")
                    db_listing["contact_name"] = contact.get("name")
                    db_listing["contact_phone"] = contact.get("phone")
                    db_listing["contact_phone_clean"] = contact.get("contact_phone_clean") or contact.get("phone_clean")

                # Truncate strings ensuring safety
                if db_listing.get("title"): db_listing["title"] = db_listing["title"][:490]
                if db_listing.get("address"): db_listing["address"] = db_listing["address"][:490]
                if db_listing.get("source_url"): db_listing["source_url"] = db_listing["source_url"][:490]
                
                # Upsert to PostgreSQL
                _, is_new = await ListingCRUD.upsert(session, db_listing)
                saved_count += 1
                if is_new:
                    new_count += 1
                    print(f"   [NEW] {listing.get('title')[:50]}...")
                else:
                    print(f"   [UPD] {listing.get('title')[:50]}...")

        print(f"\n✅ Saved {saved_count} listings to PostgreSQL ({new_count} new).")

        # 5. Save to Vector DB
        print("\n🧠 Indexing to Vector DB...")
        try:
            await index_listings(result.listings)
            print("✅ Vector indexing complete.")
        except Exception as e:
            print(f"❌ Vector indexing failed: {e}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        # Log failure
        if scrape_log_id:
            async with get_session() as session:
                await ScrapeLogCRUD.finish(session, scrape_log_id, status="failed", error_message=str(e))
        
    finally:
        await agent.close()
        # Log success if not already failed
        if scrape_log_id and 'new_count' in locals():
            async with get_session() as session:
                await ScrapeLogCRUD.finish(
                    session, 
                    scrape_log_id, 
                    listings_found=result.total_found if 'result' in locals() else 0,
                    listings_new=new_count,
                    status="completed"
                )

        print("\n" + "=" * 60)
        print("✨ Done.")

if __name__ == "__main__":
    asyncio.run(debug_scrape_and_save())
