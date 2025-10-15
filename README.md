# IndeedJobScraper
IndeedJobScraper is a Python-based tool designed to automate the process of scraping job postings from Indeed.com and saving the collected data to a CSV file for easy analysis.

## scraper.py
The ```scraper.py``` file contains the main scraping logic. It uses Selenium (with undetected ChromeDriver) and BeautifulSoup to navigate Indeed job search result pages, extract job posting details, and save them into a CSV file.

### Key Features:

- Prompts the user for an initial Indeed search results URL.
- Navigates up to 100 pages of job listings.
- Extracts job title, company name, and job link for each posting.
- Writes the extracted data to a CSV file (indeed_jobs.csv) in real time.
- Handles dynamic content loading and pagination automatically.
- Uses randomized waits to mimic human browsing and avoid detection.

### How it works:

- The script sets up a Chrome WebDriver that is less detectable by anti-bot systems.
- It asks for the starting URL of your Indeed search.
- On each page, it finds all job listing tables, extracts the job title, company name, and link, and writes them to the CSV.
- It proceeds to the next page using the pagination link, repeating the process.
- The process stops when it reaches the end of the search results or after 100 pages.

## indeed_jobs.csv
The ```indeed_jobs.csv``` file is generated as the output of the scraper. It contains the following columns for each job found:

- title: The job title (e.g., "Software Engineer")
- href: The direct URL to the job posting on Indeed
- company_name: The name of the hiring company

## Requirements:

- Python
- Selenium (undetected_chromedriver)
- BeautifulSoup4

## Usage:

bash
```
pip install -r requirements.txt
python scraper.py
```

Follow the prompt to enter your Indeed search URL, and the tool will start scraping and saving results to indeed_jobs.csv.
