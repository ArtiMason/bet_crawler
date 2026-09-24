import httpx
from bs4 import BeautifulSoup
from typing import Optional

class RequestHandler:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {            
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def get_title(self, url: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers,
            follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                title_tag = soup.find("title")
                return title_tag.string.strip() if title_tag else ""
        except Exception as e:
            print(f"Error fetching title for {url} : {e}")
            return None

     
        