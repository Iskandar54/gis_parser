import os
from dotenv import load_dotenv
from parser import process_branch_reviews
from db_manager import init_db
from utils import get_restaurants
from logger_config import setup_logger
from concurrent.futures import ThreadPoolExecutor

logger = setup_logger('parser')

def main():
    load_dotenv()
    init_db()

    urls_str = os.getenv("BRANCH_URLS")
    if not urls_str:
        logger.warning("Не найдена переменная окружения BRANCH_URLS")
        return

    urls = [u.strip() for u in urls_str.split(",") if u.strip()]
    restaurants = get_restaurants(urls)

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(process_branch_reviews, urls, restaurants)

if __name__ == "__main__":
    main()
