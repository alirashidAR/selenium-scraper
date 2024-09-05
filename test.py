from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Setting up Chrome driver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start browser maximized

service = Service(executable_path=r"C:\Users\Lenovo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Replace with actual path

# Launch browser with driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the desired web page
driver.get('https://gravitas.vit.ac.in/events')  # Replace with your actual URL

def scroll_to_bottom():
    """Scroll to the bottom of the page."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

try:
    # Scroll to the bottom of the page
    scroll_to_bottom()
    
    # Wait for a few seconds to observe the scroll action
    time.sleep(3)

finally:
    # Close the WebDriver
    driver.quit()
