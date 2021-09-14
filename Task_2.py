import bs4
import time
import pandas as pd
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Reads txt file and saves keywords to list
file = open('keywords.txt', 'r')
content = file.read()
keywords = content.split(',')

# Installs Chrome drivers and creates its instance
driver = webdriver.Chrome(ChromeDriverManager().install())

google_url = 'https://google.com/search?q='
search_link = 'site:https://www.searchenginejournal.com/ '

links = []
key_elements = []
for keyword in keywords:
    # Create url and ged the page with selenium
    url = google_url + search_link + keyword
    driver.get(url)
    time.sleep(3)

    temp_links = []
    while True:
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        elements = soup.find_all("div", class_="yuRUbf")

        for tag in elements:
            try:
                link = tag.find('a', href=True)
                if link != '':
                    temp_links.append(link['href'])
            except:
                continue

        # Try to accept google terms
        try:
            # Looks for a given id for 5 seconds
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "L2AGLb")))
            element.click()
        except:
            pass

        # Try to find and click next page link
        try:
            # Looks for a given id for 10 seconds
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pnnext")))
            element.click()
        except:
            break

    # Saves links to list
    print(temp_links)
    print(len(temp_links))
    key_elements.append(len(temp_links))
    links.extend(temp_links)

# Quit Chrome
driver.quit()

# Creates pandas data frames
df_links = pd.DataFrame({'Links': links})
df_info = pd.DataFrame({'Keyword': keywords, 'NumOfResults': key_elements})

# Saves the dataframe to csv file
df_links.to_csv('Links.csv')
df_info.to_csv('Information.csv')
