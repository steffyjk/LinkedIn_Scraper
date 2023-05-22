import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install())
)
driver.get("https://in.linkedin.com/")
time.sleep(2)
navbar = driver.find_elements(By.CLASS_NAME, "text-center")
time.sleep(2)
navbar_data_list = [x.text for x in navbar]
print(navbar_data_list)
time.sleep(2)
navbar_job_search_btn = navbar[3]
navbar_job_search_btn.click()
time.sleep(1)

search_job_title = "Java"
search_job_location = "India"

driver.find_element(By.ID, "job-search-bar-keywords").send_keys(search_job_title)
search_location_input = driver.find_element(By.ID, "job-search-bar-location")
search_location_input.clear()
search_location_input.send_keys(search_job_location, Keys.ENTER)
time.sleep(2)

job_search_list = driver.find_elements(By.XPATH, "//ul[@class='jobs-search__results-list']/li")
job_details = []
for job in job_search_list:
    job_role = job.find_element(By.CLASS_NAME, "base-search-card__title")
    job_company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle")
    job_location = job.find_element(By.CLASS_NAME, "job-search-card__location")
    list_date = job.find_element(By.TAG_NAME, "time")
    job_details.append({
        "job_title": job_role.text,
        "company_name": job_company.text,
        "location": job_location.text,
        "listing_date": list_date.text
    })

# Write the dictionary to the JSON file with 4-space indentation
import json

with open("OUTPUTS/job_search.json", 'w') as json_file:
    json.dump(job_details, json_file, indent=4)
