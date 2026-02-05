import asyncio
from storage.database import get_session, ListingCRUD, init_db
from storage.vector_db import get_vector_db, index_listings
from api.routes.search import search_listings
from api.models import SearchRequest, SearchFilters

async def test_fallback():
    # 1. Initialize DBs
    await init_db()
    get_vector_db() # Explicitly init vector db

    # 2. Seed a dummy listing in "Ba Đình" if none exists
    async with get_session() as session:
        dummy = {
            "id": "test_fallback_01",
            "title": "Căn hộ Test Fallback Ba Đình",
            "price_text": "3 tỷ",
            "price_number": 3000000000,
            "area_m2": 50.0,
            "address": "Kim Mã, Ba Đình, Hà Nội",
            "district": "Ba Đình",
            "city": "Hà Nội",
            "source_platform": "test",
            "source_url": "http://test.com/1",
            "property_type": "chung cư"
        }
        await ListingCRUD.upsert(session, dummy)
        # Manually index it
        # from storage.vector_db import get_vector_db
        db = get_vector_db()
        await db.add_listings([dummy])
        print("✅ Seeded test data for Ba Đình")

    # 3. Simulate Search Request that will FAIL scraping (headless=False will run but find nothing for this query)
    # We use a query that definitely has no real results or forces timeout, but matches district "Ba Đình"
    req = SearchRequest(
        query="Biệt thự dát vàng Ba Đình giá 500 tỷ", # Absurd query
        search_realtime=True,
        max_results=5
    )

    print("\n🚀 Sending Search Request...")
    response = await search_listings(req)

    print("\n--- Search Results ---")
    print(f"Total: {response.total}")
    print(f"Sources: {response.sources}")
    print(f"Synthesis: {response.synthesis}")

    found_fallback = any("Ba Đình" in r.title for r in response.results)
    
    if found_fallback and "vector_db_fallback" in response.sources:
        print("✅ SUCCESS: Fallback triggered and found local data!")
    elif response.total > 0:
        print("⚠️ WARNING: Found results but maybe not via fallback source check?")
    else:
        print("❌ FAIL: No results found even with fallback data seeded.")

if __name__ == "__main__":
    try:
        asyncio.run(test_fallback())
    except Exception as e:
        import traceback
        traceback.print_exc()
