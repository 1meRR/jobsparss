import time
import random
import requests
from bs4 import BeautifulSoup

from config import AREA, BASE_URL, KEYWORD, PAGES
from utils import clean_text


HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def build_params(page):
    return {
        "text": KEYWORD,
        "area": AREA,
        "page": page,
        "items_on_page": 20,
        "search_period": 7,
    }


def fetch_page(page):
    params = build_params(page)
    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    return response.text


def parse_card(card):
    title_tag = card.select_one("a.serp-item__title")
    company_tag = card.select_one("a.bloko-link_kind-secondary")
    salary_tag = card.select_one("span.bloko-header-section-3")
    city_tag = card.select_one("div.bloko-text[data-qa='vacancy-serp__vacancy-address']")
    snippet_tag = card.select_one("div.g-user-content")
    data = {
        "title": clean_text(title_tag.text if title_tag else ""),
        "link": title_tag["href"] if title_tag else "",
        "company": clean_text(company_tag.text if company_tag else ""),
        "salary": clean_text(salary_tag.text if salary_tag else ""),
        "city": clean_text(city_tag.text if city_tag else ""),
        "snippet": clean_text(snippet_tag.text if snippet_tag else ""),
    }
    return data


def parse_jobs():
    rows = []
    for page in range(PAGES):
        html = fetch_page(page)
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select("div.serp-item")
        for card in cards:
            rows.append(parse_card(card))
        time.sleep(random.uniform(0.5, 1.5))
    return rows


def filter_rows(rows):
    filtered = []
    for row in rows:
        if "python" not in row["title"].lower():
            continue
        filtered.append(row)
    return filtered


def prepare_rows(rows):
    result = []
    for row in rows:
        result.append(
            {
                "title": row["title"],
                "company": row["company"],
                "link": row["link"],
                "salary": row["salary"],
                "city": row["city"],
            }
        )
    return result
