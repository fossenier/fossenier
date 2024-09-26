from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

# Set up the Selenium WebDriver (Chrome in this case)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)

# URL of the website
url = "https://www.scotiafunds.com/en/home/investment-documents/fund-facts.html"


# Function to download a file
def download_file(url, folder):
    local_filename = url.split("/")[-1]
    local_path = os.path.join(folder, local_filename)
    # NOTE the stream=True parameter
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path


# Function to get all PDF links and download them
def get_pdfs_and_download(url, folder="downloads"):
    # Create folder if not exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Open the URL with Selenium
    driver.get(url)

    try:
        # Wait for the page to load any link
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
        )

        # Attempt to close cookie consent popup if exists
        try:
            cookie_close_button = driver.find_element(
                By.ID, "onetrust-accept-btn-handler"
            )
            if cookie_close_button:
                cookie_close_button.click()
                time.sleep(2)
        except Exception as e:
            print("No cookie consent popup found or could not close it:", e)

    except Exception as e:
        print("Error waiting for initial elements:", e)
        driver.quit()
        return

    # Find all tab buttons
    try:
        tabs = driver.find_elements(By.CSS_SELECTOR, "a[role='tab']")
        if not tabs:
            print("No tabs found.")
            driver.quit()
            return
    except Exception as e:
        print("Error finding tab buttons:", e)
        driver.quit()
        return

    # Iterate through each tab
    for tab in tabs:
        try:
            tab_text = tab.text
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(2)  # Add a small delay to ensure content loads
            # Wait for the tab panel to be visible
            panel_id = tab.get_attribute("href").split("#")[1]
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, panel_id))
            )
            # Find all links in the current tab
            panel = driver.find_element(By.ID, panel_id)
            links = panel.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
            if not links:
                print(f"No download links found in tab: {tab_text}")
            else:
                # Download each PDF
                for link in links:
                    pdf_url = link.get_attribute("href")
                    print(f"Downloading {pdf_url}")
                    download_file(pdf_url, folder)
        except Exception as e:
            print(f"Error processing tab {tab_text}: {e}")


# Execute the function
get_pdfs_and_download(url)

# Close the Selenium WebDriver
driver.quit()
