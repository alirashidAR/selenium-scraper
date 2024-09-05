import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
from datetime import datetime

# Setting up Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Runs browser in headless mode
service = Service(executable_path=r"C:\Users\Lenovo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Replace with actual path

# Launch browser with driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Read URLs from the CSV file
links_df = pd.read_csv('event_links.csv')
links = links_df['URL'].tolist()
print("URLs to process:", len(links))
unique_links = set(links)
print(len(unique_links))

# Prepare a list to collect data
data = []

if links:
    for link in links:
        try:
            driver.get(link)
            time.sleep(3)  # Wait for page to load

            section = driver.find_element(By.XPATH, "//section[contains(@class, 'main') and contains(@class, 'flex') and contains(@class, 'flex-col') and contains(@class, 'font-auxMono') and contains(@class, 'w-full') and contains(@class, 'md:w-[60%]') and contains(@class, 'px-2') and contains(@class, 'md:px-0')]")
            
            event_name = section.find_element(By.XPATH, ".//h1[@class='text-3xl md:text-4xl font-medium']").text
            club_chapter = section.find_element(By.XPATH, ".//p[@class='text-primary text-sm md:text-lg']").text
            venue = section.find_element(By.XPATH, ".//div[contains(@class, 'font-auxMono') and contains(@class, 'text-xs') and contains(@class, 'md:text-sm')]/h2").text
            num_participants = section.find_element(By.XPATH, ".//div[contains(@class, 'font-auxMono') and contains(@class, 'text-xs') and contains(@class, 'md:text-sm')][2]/h2").text
            
            slots_elements = section.find_elements(By.XPATH, ".//button[contains(@class, 'w-full') and contains(@class, 'px-2') and contains(@class, 'py-2') and contains(@class, 'border-[1px]') and contains(@class, 'border-black') and contains(@class, 'text-xs') and contains(@class, 'tracking-tighter')]")
            slots = [slot.text for slot in slots_elements]

            for slot in slots:
                # Updated regex to capture the 2024 year
                date_time_pattern = r'(\d{1,2}:\d{2} [AP]M, \d{1,2} [A-Za-z]{3}) - (\d{1,2}:\d{2} [AP]M, \d{1,2} [A-Za-z]{3})'
                match = re.search(date_time_pattern, slot)
                if match:
                    start_datetime, end_datetime = match.groups()
                    
                    # Add the year 2024 to the date format
                    start = datetime.strptime(start_datetime + ' 2024', "%I:%M %p, %d %b %Y")
                    end = datetime.strptime(end_datetime + ' 2024', "%I:%M %p, %d %b %Y")
                    
                    date = start.strftime("%Y-%m-%d")  # Format the date as YYYY-MM-DD
                    time_slot = f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"
                else:
                    date = 'N/A'
                    time_slot = slot

                print(f"Event Name: {event_name}")
                print(f"Club/Chapter: {club_chapter}")
                print(f"Venue: {venue}")
                print(f"Number of Participants: {num_participants}")
                print(f"Date: {date}")
                print(f"Slot: {time_slot}")
                print('-' * 50)
                
                # Append the extracted information to the data list
                data.append({
                    "Event Name": event_name,
                    "Club/Chapter": club_chapter,
                    "Venue": venue,
                    "Number of Participants": num_participants,
                    "Date": date,
                    "Slot": time_slot
                })

        except Exception as e:
            print(f"Error processing URL {link}: {e}")

else:
    print("No URLs found in the CSV file.")

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('event_details.csv', index=False)

# Close the driver
driver.quit()

print("Scraping completed, and data has been saved to event_details.csv.")
