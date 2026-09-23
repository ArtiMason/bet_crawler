import asyncio
from search.duckduckgo import DuckDuckGoSearch

async def main():
    query = "Арсенал - Лидс прогноз"
    ddg = DuckDuckGoSearch()
    print(f"Searching for: {query}")
    ddg_links = await ddg.search(query)
    print(f"DDG found {len(ddg_links)} links")
    print("\nFirst 3 DDG links: ", ddg_links[:3])

if __name__ == "__main__":
    asyncio.run(main())    