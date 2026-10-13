import asyncio
from search.duckduckgo import DuckDuckGoSearch
from fetcher.browser import BrowserHandler
from core.ranker import LinkRanker

async def main():
    query = "Арсенал - Лидс прогноз"

    search_engine = DuckDuckGoSearch()
    browser = BrowserHandler()
    ranker = LinkRanker()

    try:
        ddg_links = await search_engine.search(query)

        await browser.start()
        print("Fetching titles..")
        links = []
        for url in ddg_links[:10]:
            title = await browser.get_title(url)
            if title:
                links.append((url,title))
                print(f"OK: {title[:50]}...") 

        final_links = ranker.rank_link(links)
        print(f"\nFinal filtered links: {len(final_links)}")
        for i, link in enumerate(final_links,1):
            print(f"{i}. {link}")

    finally:
        await browser.stop()                

if __name__ == "__main__":
    asyncio.run(main())    