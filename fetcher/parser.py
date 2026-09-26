from bs4 import BeautifulSoup
from typing import Optional

class ContentParser:
    def __init__(self):
        self.target_classes = ["prediction", "forecast", "itog", "result", "tip"]

    def extract_prediction(self, html: str) -> Optional[str]:
        soup = BeautifulSoup(html, "html.parser")

        for keyword in self.target_classes:
            element = soup.find(lambda tag: tag.has_attr("class") and any(keyword in c.lower() for c in tag["class"])) or \
            soup.find(lambda tag: tag.has_attr("id")and keyword in tag["id"].lower())

            if element:
                text = element.get_text(separator="",strip=True)
                if len(text) > 20:
                    return self._clean_text(text)

        paragraphs = soup.find_all("p")
        best_p = max(paragraphs[:10], key=lambda p: len(p.get_text()), default=None)
        if best_p:
            return self._clean_text(best_p.get_text())
        return None

    def _clean_text(self, text: str) -> str:
        text = " ".join(text.split())
        sestences = text.split(". ")
        return ". ".join(sestences[:3]) + "."  if len(sestences) > 1 else text

