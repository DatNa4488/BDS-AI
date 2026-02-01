import asyncio
from playwright.async_api import async_playwright

async def debug_scrape():
    print("Starting debug scrape...")
    async with async_playwright() as p:
        # Use a real-looking user agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=user_agent
        )
        
        page = await context.new_page()
        
        # Test Chotot
        print("1. Checking Chotot...")
        try:
            await page.goto("https://nha.chotot.com/toan-quoc/mua-ban-bat-dong-san", timeout=30000)
            await page.wait_for_timeout(5000) # Wait for hydration
            content_chotot = await page.content()
            with open("debug_chotot.html", "w", encoding="utf-8") as f:
                f.write(content_chotot)
            print(f"   Saved debug_chotot.html ({len(content_chotot)} bytes)")
        except Exception as e:
            print(f"   Error Chotot: {e}")
            
        # Test Batdongsan
        print("2. Checking Batdongsan...")
        try:
            await page.goto("https://batdongsan.com.vn/ban-nha-dat-ha-noi", timeout=30000)
            await page.wait_for_timeout(5000)
            content_bds = await page.content()
            with open("debug_bds.html", "w", encoding="utf-8") as f:
                f.write(content_bds)
            print(f"   Saved debug_bds.html ({len(content_bds)} bytes)")
        except Exception as e:
            print(f"   Error BDS: {e}")
            
        await browser.close()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(debug_scrape())
