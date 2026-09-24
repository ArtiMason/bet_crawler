from typing import List, Tuple

class LinkRanker:
    def __init__(self):
        self.keywords = ["прогноз", "ставка", "матч", "bet", "tip", "analyze", "prediction"]

    def rank_link(self, links: List[Tuple[str,str]]) -> List[str]:
        filtered_links = []
        for url, title in links:
            score = self.score_link(url, title)
            if score > 0:
                filtered_links.append((score, url))
        filtered_links.sort(key=lambda x: x[0], reverse=True)        
        return [url for score, url in filtered_links]
    def score_link(self, url: str, title: str = "") -> int:
        score = 0 
        text_to_analyze = (url + " " + title).lower()
        for word in self.keywords:
            if word in text_to_analyze:
                score += 1
        return score                
