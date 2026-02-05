import asyncio
from agents.search_agent import RealEstateSearchAgent, SearchIntent

async def test_direct_scrape():
    print("🚀 Initializing Search Agent...")
    agent = RealEstateSearchAgent(headless=False) # Run visible to see browser
    
    # Test Query: Specific enough to trigger direct logic
    query = "Chung cư Cầu Giấy dưới 5 tỷ"
    
    print(f"🔎 Testing Query: {query}")
    
    # Manually constructed intent to isolate scraping from LLM parsing issues
    intent = SearchIntent(
        property_type="chung cư",
        city="Hà Nội",
        district="Cầu Giấy",
        price_max=5000000000,
        intent="mua"
    )
    
    print(f"📋 Intent: {intent}")
    
    # search() now defaults to direct scrape
    result = await agent.search(query, intent=intent, max_results=5)
    
    print("\n" + "="*50)
    print(f"✅ Found {result.total_found} listings")
    print("="*50)
    
    for i, item in enumerate(result.listings):
        print(f"\n[Listing {i+1}]")
        print(f"  - Title: {item.get('title')}")
        print(f"  - Price: {item.get('price_text')} ({item.get('price_number')})")
        print(f"  - Area: {item.get('area_m2')} m2")
        print(f"  - Location: {item.get('location')}")
        print(f"  - Source: {item.get('source_platform')}")
        print(f"  - URL: {item.get('source_url')}")

    if result.total_found > 0:
        print("\n✅ TEST PASSED: Listings extracted successfully without Google Search.")
    else:
        print("\n❌ TEST FAILED: No listings found.")

if __name__ == "__main__":
    asyncio.run(test_direct_scrape())
