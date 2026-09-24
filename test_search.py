import asyncio
from search.duckduckgo import DuckDuckGoSearch
from fetcher.request import RequestHandler
from core.ranker import LinkRanker

async def main():
    query = "Арсенал - Лидс прогноз"

    search_engine = DuckDuckGoSearch()
    fetcher = RequestHandler()
    ranker = LinkRanker()

    print("Searching...")
    ddg_links = await search_engine.search(query)
    print(f"Found {len(ddg_links)} links")

    print("Fetching titles for accuracy...")
    links = []
    for url in ddg_links[:15]:
        title = await fetcher.get_title(url)
        if title:
            links.append((url,title))
            print(f"OK, {title[:50]}..")

    final_links = ranker.rank_link(links)
    print(f"\nFinal filtered links: {len(final_links)}")
    for i, link in enumerate(final_links[:5],1):
        print(f"{i}. {link}")        

if __name__ == "__main__":
    asyncio.run(main())    