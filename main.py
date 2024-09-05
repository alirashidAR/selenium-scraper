from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

# Setting up Chrome driver
chrome_options = Options()
service = Service(executable_path=r"C:\Users\Lenovo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Replace with actual path

# Launch browser with driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# List to store all anchor hrefs
all_links = []

def process_page():
    try:
        # Get <div> elements with the specified class
        div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'w-full') and contains(@class, 'border-y-[1px]') and contains(@class, 'border-outline') and contains(@class, 'flex') and contains(@class, 'flex-col') and contains(@class, 'gap-4') and contains(@class, 'md:gap-0')]")
        
        for div in div_elements:
            # Find anchor tags within the div that contain '/events/' in the href
            anchors = div.find_elements(By.XPATH, ".//a[contains(@href, '/events/')]")
            
            for anchor in anchors:
                try:
                    href = anchor.get_attribute("href")
                    all_links.append(href)
                    print("Anchor href:", href)
                    
                except Exception as e:
                    print("Error accessing anchor:", e)
    
    except Exception as e:
        print("Error processing page:", e)

def navigate_pages():
    page = 1
    while True:
        if page >= 33:
            break
        print("Processing page:", page)
        page += 1
        print('-'*50)
        process_page()
        
        try:
            # Find the <p> tag that contains the text 'Next'
            next_buttons = driver.find_elements(By.XPATH, "//p[contains(text(), 'Next')]")
            
            if not next_buttons:
                print("No 'Next' button found.")
                break
            
            # Click the first <p> tag that contains the text 'Next'
            next_button = next_buttons[-1]
            next_button.click()
            
            # Wait for the new page to load
            time.sleep(5)  # Adjust sleep time as needed for the page to load fully
            
        except Exception as e:
            print("No more pages or an error occurred:", e)
            break

# Open the desired URL
url = "https://gravitas.vit.ac.in/events"
driver.get(url)

# Start navigating and processing pages
navigate_pages()

# Close the driver
driver.quit()

# Write all links to a CSV file
with open('event_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['URL'])  # Write header
    for link in all_links:
        csv_writer.writerow([link])  # Write each URL

print("All links have been written to event_links.csv")
