import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

BASE_URL = "https://careers.google.com/jobs/results/"
COMPANY_NAME = "Google"
MAX_PAGES = 10   # safety limit


def fetch_google_jobs():
    all_jobs = []
    seen_urls = set()

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0"
    })

    for page in range(1, MAX_PAGES + 1):
        params = {
            "q": "data engineer",
            "page": page
        }

        response = session.get(BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            print(f"Google page fetch failed at page {page}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.select("li.gc-card")

        if not job_cards:
            break  # no more jobs

        new_count = 0

        for card in job_cards:
            title = card.select_one("h2").get_text(strip=True)
            location = card.select_one(".gc-job-location").get_text(strip=True)

            link_tag = card.find("a", href=True)
            job_url = "https://careers.google.com" + link_tag["href"]

            if job_url in seen_urls:
                continue

            seen_urls.add(job_url)
            new_count += 1

            all_jobs.append({
                "company": COMPANY_NAME,
                "job_title": title,
                "location": location,
                "job_url": job_url
            })

        if new_count == 0:
            break

        time.sleep(1)  # polite delay

    return all_jobs


def main():
    jobs = fetch_google_jobs()
    print(jobs)
if __name__ == "__main__":
    main()