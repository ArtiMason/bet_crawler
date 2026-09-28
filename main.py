import asyncio
from urllib.parse import urljoin, parse_qs
from search.duckduckgo import DuckDuckGoSearch
from fetcher.browser import BrowserHandler
from fetcher.parser import ContentParser
from core.ranker import LinkRanker

async def clean_links(ddg_links: list) -> list:
    cleaned = []
    for link in ddg_links:
        if "duckduckgo.com/l" in link:
            parsed = parse_qs(urljoin("https://duckduckgo.com", link))
            real_url = parsed.get("uddg",[link])[0]
            cleaned.append(real_url)
        else: 
            cleaned.append(link)
            
    return cleaned

async def main():
    match_query = "Зенит - Краснодар"
    search_query = f"{match_query} прогноз"
    print(f"---Начинаем поиск прогнозов для {match_query} ---")

    search_engine = DuckDuckGoSearch()
    browser = BrowserHandler()
    ranker = LinkRanker()
    parser = ContentParser()

    try:
        print("\n[1/4]Поиск ссылок...")
        ddg_links = await search_engine.search(search_query)
        links = await clean_links(ddg_links)
        print(f"Найдено {len(links)} прямых ссылок")

        print("\n[2/4]Фильтрация по релевантности...")
        await browser.start()
        pairs = []
        for url in links[:10]:
            title = await browser.get_title(url)
            if title:
                pairs.append((url, title))
        final_links = ranker.rank_link(pairs)
        print(f"Отобрано {len(final_links)} наиболее подходящих сайтов")

        print("\n[3/4] Извлечение текстов прогнозов...")
        results = []
        for url in final_links[:3]:
            print(f"Парсим {url[:60]}...")
            html = await browser.get_content(url)
            if html:
                prediction = parser.extract_prediction(html)
                if prediction:
                    results.append({"url": url, "text": prediction})

        print("\n" + "="*50)
        print(f"ИТОГОВЫЕ ПРОГНОЗЫ ДЛЯ {match_query.upper()}:")
        print("="*50)
        if not results:
            print("К сожалению, не удалось извлечь текст прогноза.")
        else:
            for i, res in enumerate(results, 1):
                print(f"\nПрогноз №{i}:")
                print(f"Источник: {res['url']}")
                print(f"Текст: {res['text']}")
        print("="*50)
    finally:
        await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())    