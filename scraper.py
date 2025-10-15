import csv
import time
import random
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_job_data_automated():
    """
    Automates the process of scraping job data from Indeed.com, navigating through
    multiple pages and saving the data to a CSV file in real-time.
    """
    initial_url = input("Please enter the starting URL of the Indeed search results: ")
    output_csv = "indeed_jobs.csv"
    max_pages_to_scrape = 100
    base_url = "https://www.indeed.com"

    print("Setting up undetectable Chrome WebDriver...")
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    csv_file = None
    try:
        driver = uc.Chrome(options=options)
        
        csv_file = open(output_csv, 'w', newline='', encoding='utf-8')
        fieldnames = ["title", "href", "company_name"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        csv_writer.writeheader()
        
        print(f"Navigating to the initial URL: {initial_url}")
        driver.get(initial_url)
        
        page_counter = 0
        while page_counter < max_pages_to_scrape:
            page_counter += 1
            print(f"\nScraping page {page_counter}...")

            try:
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.mainContentTable')))
                sleep_time = random.uniform(4, 6)
                print(f"Waiting for {sleep_time:.2f} seconds to ensure page content loads.")
                time.sleep(sleep_time)
            except Exception as e:
                print(f"Could not find the main content table, or an error occurred: {e}")
                break

            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            all_tables = soup.find_all('table', class_='mainContentTable css-131ju4w eu4oa1w0')
            
            if not all_tables:
                print("No more job listings found. Ending scrape.")
                break

            for table in all_tables:
                row = table.find('tr')
                if row:
                    link_tag = row.find('a', class_='jcs-JobTitle')
                    company_span = row.find('span', {'data-testid': 'company-name'})
                    
                    if link_tag and company_span:
                        relative_href = link_tag.get('href')
                        full_href = base_url + relative_href
                        title_span = link_tag.find('span')
                        title = title_span.get('title') if title_span and title_span.get('title') else 'N/A'
                        company_name = company_span.text.strip()
                        
                        job_data = {
                            "title": title,
                            "href": full_href,
                            "company_name": company_name
                        }
                        csv_writer.writerow(job_data)
            
            print(f"Scraped {len(all_tables)} jobs from this page.")

            try:
                next_page_link_tag = soup.find('a', {'data-testid': 'pagination-page-next'})
                if not next_page_link_tag:
                    print("End of pagination reached. No 'next page' link found.")
                    break
                
                next_page_url = base_url + next_page_link_tag.get('href')
                print(f"Navigating to the next page: {next_page_url}")
                driver.get(next_page_url)

            except Exception as e:
                print(f"Error navigating to the next page: {e}")
                break

    except Exception as e:
        print(f"An error occurred during the scraping process: {e}")
    finally:
        if driver:
            driver.quit()
            print("WebDriver closed.")
        if csv_file and not csv_file.closed:
            csv_file.close()
            print("CSV file closed.")

if __name__ == "__main__":
    scrape_job_data_automated()