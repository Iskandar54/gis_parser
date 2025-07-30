import requests
import random
import re
import time
from datetime import datetime
from db_manager import is_review_exists, save_review
from tg_sendmess import send_telegram_message
from logger_config import setup_logger

logger = setup_logger("parser")

PROXIES = [
    {"http": "http://223.204.59.226:8081", "https": "http://223.204.59.226:8081"},
    {"http": "http://181.209.109.172:3128", "https": "http://181.209.109.172:3128"},
    {"http": "http://184.82.47.38:8080", "https": "http://184.82.47.38:8080"},
    {"http": "http://223.206.196.209:8081", "https": "http://223.206.196.209:8081"},
]

def safe_get(url, **kwargs):
    for _ in range(3):
        time.sleep(1)
        proxy = random.choice(PROXIES)
        kwargs["proxies"] = proxy
        kwargs.setdefault("timeout", 10)

        try:
            r = requests.get(url, **kwargs)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка с прокси {proxy['http']}: {e}")
            time.sleep(2)
    try:
        kwargs.pop("proxies", None)
        kwargs.setdefault("timeout", 20)   # поставил 20 так как часто делал запросы и не хотелось получить блок
        return requests.get(url, **kwargs)
    except Exception as e:
        logger.error(f"Не удалось подключиться даже без прокси: {e}")
        return None

def get_review_api_key(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html",
        "Accept-Language": "ru-RU,ru;q=0.8",
        "Referer": "https://2gis.ru/"
    }
    res = safe_get(url, headers=headers)
    if res and res.status_code == 200:
        m = re.search(r'"reviewApiKey":\s*"([a-f0-9-]+)"', res.text)
        if m:
            return m.group(1)
    logger.warning("API ключ не найден")
    return None

def get_reviews(branch_id, api_key, offset=0, limit=50):
    url = f"https://public-api.reviews.2gis.com/2.0/branches/{branch_id}/reviews"
    params = {
        "limit": limit,
        "offset": offset,
        "sort_by": "friends",
        "key": api_key,
        "locale": "ru_RU",
        "is_advertiser": "false",
        "fields": "meta.providers,meta.branch_rating,meta.branch_reviews_count,reviews.is_verified",
        "without_my_first_review": "false",
        "rated": "true"
    }
    res = safe_get(url, params=params)
    if res:
        return res.json()
    return None

def format_review_text(r):
    author = r.get("user", {}).get("name", "Неизвестный автор")
    date = r.get("date_created", "")
    try:
        date = datetime.fromisoformat(date).strftime('%d.%m.%Y')
    except:
        pass
    rating = r.get("rating", "?")
    text = r.get("text", "").replace("\n", " ")[:200]
    return f"{author} ({date}) ★{rating}\n{text}"

def process_branch_reviews(url, restaurant):
    logger.info(f"Парсинг: {url}")
    m = re.search(r'/firm/(\d+)', url)
    if not m:
        return
    branch_id = m.group(1)

    time.sleep(random.uniform(1, 3))
    api_key = get_review_api_key(url)
    if not api_key:
        return

    first = get_reviews(branch_id, api_key)
    if not first or 'reviews' not in first:
        return

    new_reviews = [r for r in first['reviews'] if not is_review_exists(r['id'])]

    if not new_reviews:
        send_telegram_message(f"Новых отзывов для <b>{restaurant['name']}</b>: Не найдено")
        return

    total = first.get("meta", {}).get("branch_reviews_count", 0)
    logger.info(f"Найденно отзывов {total}")

    all_reviews = first['reviews'][:]
    for offset in range(50, total, 50):
        chunk = get_reviews(branch_id, api_key, offset=offset)
        if chunk and 'reviews' in chunk:
            all_reviews.extend(chunk['reviews'])
        else:
            logger.error(f"Не удалось загрузить отзывы с offset={offset}")
            break
        time.sleep(random.uniform(1.5, 3))

    saved = []
    for r in all_reviews:
        save_review(r, branch_id)
        saved.append(r)

    if len(saved) <= 10:
        text = f"Новые отзывы для <b>{restaurant['name']}</b>:\n" + \
               "\n\n".join(format_review_text(r) for r in saved)
    else:
        text = f"Новые отзывы для <b>{restaurant['name']}</b>:\nДобавлено: {len(saved)} отзывов"
    send_telegram_message(text)
    time.sleep(1)
