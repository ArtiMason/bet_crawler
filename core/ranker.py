from typing import List, Tuple

class LinkRanker:
    def __init__(self):
        self.keywords = ["прогноз", "ставка", "матч", "bet", "tip", "analyze", "prediction"]

    def rank_link(self, links: List[str]) -> List[str]:
        filtered_links = []
        for link in links:
            link_lower = link.lower()
            if any(word in link_lower for word in self.keywords):
                filtered_links.append(link)
        return filtered_links
    def score_link(self, url: str, title: str = "") -> int:
        score = 0 
        text_to_analyze = (url + " " + title).lower()
        for word in self.keywords:
            if word in text_to_analyze:
                score += 1
        return score                
