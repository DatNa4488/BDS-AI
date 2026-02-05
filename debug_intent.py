import asyncio
from agents.search_agent import RealEstateSearchAgent

async def test_parsing():
    agent = RealEstateSearchAgent(headless=True)
    
    queries = [
        "Chung cư Hồ Tây",
        "Mua nhà quận 1",
        "Thuê căn hộ gần Landmark 81"
    ]
    
    print("--- Testing Intent Parsing ---")
    for q in queries:
        print(f"\nQuery: {q}")
        intent = await agent.parse_query(q)
        print(f"Result City: '{intent.city}'")
        print(f"Result District: '{intent.district}'")
        print(f"Result Intent: '{intent.intent}'")

        if "|" in intent.city:
            print("❌ FAIL: City contains ambiguous pipe character!")
        else:
            print("✅ PASS: City is clean.")

if __name__ == "__main__":
    asyncio.run(test_parsing())
