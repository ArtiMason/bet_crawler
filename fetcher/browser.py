from playwright.async_api import async_playwright
from typing import Optional

class BrowserHandler:
    def __init__(self, timeout: int = 30000):
        self.timeout = timeout

    async def get_title(self, url:str) -> Optional[str]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = await context.new_page()

            try:
                await page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
                title = await page.title()
                return title
            except Exception as e:
                print(f"Browser error fot {url} : {e}")
                return None
            finally:
                await browser.close()


       