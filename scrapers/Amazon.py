import requests
import time
import random
import csv


URL = "https://www.amazon.jobs/en/search.json"
CSV_FILE = "amazon_data_engineer_jobs.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_PARAMS = {
    "keywords": "data engineer",
    "location": "India"
}

PAGE_SIZE = 10   

def fetch_all_amazon_jobs():
    offset = 0
    all_jobs = []

    while True:
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
        if len(all_jobs) >100: return all_jobs

    return all_jobs
def save_jobs_to_csv(jobs):
    fieldnames = [
        "company",
        "job_title",
        "location",
        "job_url"
    ]

    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs:
            job_path = job.get("jobPath")

            writer.writerow({
                "company": "Amazon",
                "job_title": job.get("title", ""),
                "location": job.get("location", ""),
                "job_url": f"https://www.amazon.jobs{job_path}" if job_path else ""
            })

    print(f"\nSaved {len(jobs)} jobs to {CSV_FILE}")



if __name__ == "__main__":
    try:
        jobs = fetch_all_amazon_jobs()
        save_jobs_to_csv(jobs)
    except Exception as e:
        print("Error occurred:", e)
