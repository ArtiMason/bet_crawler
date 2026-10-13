from urllib.parse import urljoin, parse_qs
import httpx
from bs4 import BeautifulSoup
from typing import List
from .base import BaseSearch

class DuckDuckGoSearch(BaseSearch):
    def __init__(self, timeout = 10):
        super().__init__(timeout)
        self.url = "https://html.duckduckgo.com/html/"
        self.headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"        
        }

    async def search(self, query: str) -> List[str]:
        params = {"q": query}
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            response = await client.get(self.url, params=params)  
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            links = []

            for a in soup.find_all("a", class_="result__a"):
                link = a.get("href")
                if link:
                    if "duckduckgo.com/l" in link:
                        parsed_url = parse_qs(urljoin(self.url, link))
                        real_url = parsed_url.get("uddg",[link])[0]
                        links.append(real_url)
                    else:
                        links.append(urljoin(self.url, link))    

            return links        

