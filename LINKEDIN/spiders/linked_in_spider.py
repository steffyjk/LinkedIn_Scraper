import scrapy


class LinkedInSpider(scrapy.Spider):
    name = "jobsearch"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://linkedin.com"]

    def parse(self, response):
        job = "Python"
        country = "India"
        linkedin_job_url = f'https://www.linkedin.com/jobs/search?keywords={job}&location={country}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        yield scrapy.Request(url=linkedin_job_url, callback=self.parse_jobs,
                             meta={'job': job,
                                   'country': country,
                                   'linkedin_url': linkedin_job_url})

    def parse_jobs(self, response):
        item = {'job': response.meta['job'], 'country': response.meta['country']}

        list_items = response.css('.jobs-search__results-list li')
        data = [item]
        for item in list_items:
            job = {}
            title = item.css('.base-search-card__title::text').get().strip()
            if title:
                job["job_title"] = title
            company_name = item.css('.base-search-card__subtitle a::text').get().strip()
            if company_name:
                job["company_name"] = company_name
            location = item.css('.job-search-card__location::text').get().strip()
            if location:
                job["job_location"] = location
            list_date = item.css('.job-search-card__listdate::text').get()
            if list_date:
                job["job_listing_date"] = list_date.strip()

            data.append(job)


        import json

        with open("job_search.json", 'w') as json_file:
            json.dump(data, json_file, indent=4)

