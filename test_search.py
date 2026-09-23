import asyncio
from search.duckduckgo import DuckDuckGoSearch
from core.ranker import LinkRanker

async def main():
    query = "Арсенал - Лидс прогноз"
    ddg = DuckDuckGoSearch()
    print(f"Searching for: {query}")
    ddg_links = await ddg.search(query)
    print(f"DDG found {len(ddg_links)} links")
    ranker = LinkRanker()
    filtered_links = ranker.rank_link(ddg_links)
    print(f"Output filtered links: {len(filtered_links)}")
    print("\nRelevant links:")
    for link in filtered_links[:5]:
        print(link)

if __name__ == "__main__":
    asyncio.run(main())    