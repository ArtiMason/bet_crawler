from playwright.async_api import async_playwright
from typing import Optional
import asyncio

class BrowserHandler:
    def __init__(self, timeout: int = 30000):
        self.timeout = timeout
        self.browser = None
        self.context = None
        self.playwright = None

    async def start(self):
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context(user_agent="Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}) 

    async def get_title(self, url: str) -> Optional[str]:
        if not self.context:
            await self.start()

        page: Page = await self.context.new_page()
        try:
            await page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
            title = await page.title()
            return title if title else None
        except Exception as e:
            print(f"Playwright error for {url} : {e}")
            return None
        finally:
            await page.close()

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()            



       