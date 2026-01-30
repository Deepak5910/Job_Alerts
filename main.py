import json
import scrapers.Amazon
import csv
import importlib
import scrapers.cleaner as cleaner
import auto_mailer.mailer as mailer

output_file = "data/job_master.csv"

def save_jobs_to_csv(company_name, url,  jobs, CSV_FILE):
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
            writer.writerow({
                "company": company_name,
                "job_title": job.get("title", ""),
                "location": job.get("location", ""),
                "job_url": url
            })

    print(f"\nSaved {len(jobs)} jobs to {CSV_FILE}")
   



def main():
    with open("configs/company_master.json", "r") as file:
        data  = json.load(file)
        write_mode='w'
        for company in data:
            try:
                module_name = importlib.import_module(data[company]["module"])
                #jobs = module_name.fetch_all_amazon_jobs(data[company]["job_search_url"])
                #save_jobs_to_csv(company,data[company]["job_search_url"],jobs, data[company]["output_csv"])
                #cleaner.data_cleaner(data[company]["output_csv"],output_file,write_mode=write_mode)
                write_mode='a'
            except Exception as e:  
                print(f"Error fetching jobs for {company}: {e}")
             
    mailer.send_emmail()
    

if "__main__" == __name__:
    main()
     
