from bs4 import BeautifulSoup
from typing import Optional
import re

class ContentParser:
    def __init__(self):
        self.target_markers = ["prediction", "forecast", "itog", "result", "tip", "bet", "ставка"]

    def extract_prediction(self, html: str) -> Optional[str]:
        soup = BeautifulSoup(html, "html.parser")

        for noise in soup(["script", "style", "nav", "footer", "aside", "header"]):
            noise.decompose()

        for marker in self.target_markers:
            element = soup.find(lambda tag: (
                (tag.has_attr("class") and any(marker in c.lower() for c in tag["class"])) or 
                (tag.has_attr("id") and marker in tag["id"].lower())

            ))  
            if element:
                text = element.get_text(separator=" ", strip=True)
                if len(text) > 50:
                    return self._clean_text(text)  

        main_content = soup.find("article") or soup.find("main") or soup.find("div",class_="content")
        if main_content:
            paragraphs = main_content.find_all("p")
        else:
            paragraphs = soup.find_all("p")

        valid_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text() > 40) ]
        if valid_paragraphs:
            best_text = max(valid_paragraphs, key=len)
            return self._clean_text(best_text)
        return None  

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text> 500):
            return text[:497] + '...'
        return text
