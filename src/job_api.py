from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()

apify_client= ApifyClient(os.getenv("APIFY_API_TOKEN"))


# fetch the Linkdin jobs based on search quesry and location
def fetch_linkedin_jobs(search_query, location="india", rows=60):
    """
    Fetch job listings from LinkedIn based on search query and location.

    Args:
        search_query (str): The search query for jobs.
        location (str): The location to search for jobs.
        rows (int): The number of jobs to fetch.

    Returns:
        list: A list of dictionaries containing job information.
    """
    run_input = {
        "urls": ["https://www.linkedin.com/jobs/search/?position=1&pageNum=0"],
        "title" : search_query,
        "location" : location,
        "rows" : rows,
        "scrapeCompany": True,
        "proxy": {
            "userApifyProxy" : True,
            "apifyProxyGroups" : ["RESIDENTIAL"]
        }
    }
    run= apify_client.actor("hKByXkMQaC5Qt9UMN").call(run_input= run_input)
    jobs = list(apify_client.dataset(run.default_dataset_id).iterate_items())
    return jobs


# fetch the Naukri jobs based on search quesry and location
def fetch_naukri_jobs(search_query, location="india", rows=60):
    """
    Fetch job listings from LinkedIn based on search query and location.

    Args:
        search_query (str): The search query for jobs.
        location (str): The location to search for jobs.
        rows (int): The number of jobs to fetch.

    Returns:
        list: A list of dictionaries containing job information.
    """
    run_input = {
        "keywords" : search_query,
        "maxjobs" : 60,
        "freshness" : "all",
        "experience" : "all",
        "sortBy" : "relevance"
    }
    run= apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input= run_input)
    jobs = list(apify_client.dataset(run.default_dataset_id).iterate_items())
    return jobs
