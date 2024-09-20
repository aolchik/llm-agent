import os

from crewai_tools import BaseTool
import requests
from unstructured.partition.html import partition_html

SCRAPING_FISH_API_KEY = os.getenv("SCRAPING_FISH_API_KEY")


class ScrapingFishTool(BaseTool):
    name: str = "Scrape website content"
    description: str = """
      Useful to scrape a website content, just pass a string with
      only the full url, no need for a final slash `/`, eg:
      https://google.com or https://clearbit.com/about-us"""

    def _run(self, website: str) -> str:
        url = "https://scraping.narf.ai/api/v1/"
        payload = {
            "api_key": SCRAPING_FISH_API_KEY,
            "url": website
        }
        response = requests.get(url, params=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        chunks = []
        for chunk in content:
            chunks.append(chunk)
        content = "\n\n".join(chunks)
        return f'\nScrapped Content: {content}\n'
