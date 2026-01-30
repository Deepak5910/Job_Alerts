import requests
import time
import random


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_PARAMS = {
    "keywords": "data engineer",
    "location": "India"
}


PAGE_SIZE = 10   

def fetch_all_amazon_jobs(URL):
    offset = 0
    all_jobs = []
    MAX_PAGES = 20

    while MAX_PAGES>0:
        params = {
            **BASE_PARAMS,
            "offset": offset
        }

        response = requests.get(
            URL,
            params=params,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])

        if not jobs:
            break

        all_jobs.extend(jobs)

        print(f"Fetched {len(jobs)} jobs (offset={offset})")

        offset += PAGE_SIZE
        time.sleep(random.uniform(1, 3))  # polite delay
        MAX_PAGES-=1

    return all_jobs
