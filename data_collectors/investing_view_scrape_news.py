from typing import List, Dict
from tqdm import tqdm
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

EXECUTABLE_PATH = "./resources/chromedriver.exe"

STOCK_MARKET_NEWS_URL = "https://www.investing.com/news/stock-market-news/"
POLITICS_NEWS_URL = "https://www.investing.com/news/politics/"
WORLD_NEWS_URL = "https://www.investing.com/news/world-news"


def get_driver(executable_path: str, page_load_timeout: int = 2):
    driver = webdriver.Chrome(executable_path)
    driver.set_page_load_timeout(page_load_timeout)
    
    return driver


def load_page(driver: webdriver.Chrome, link: str) -> None:
    try:
        driver.get(link)
    except TimeoutException:
        pass
    
    
def get_page_articles_links(driver: webdriver.Chrome, link: str) -> List[str]:
    load_page(driver, link)

    try:
        div_articles = driver.find_element(By.XPATH, "//div[contains(@class, 'largeTitle')]")
        refs = div_articles.find_elements(By.CLASS_NAME, "title")

        links = []
        for ref in refs:
            links.append(ref.get_attribute("href"))
        
        return links
    except:
        return []


def get_all_links(driver, link: str, num_pages: int = 3000) -> List[str]:
    links = []
    for page in tqdm(range(1, num_pages + 1)):
        current_link = link + str(page)
        
        links.extend(get_page_articles_links(driver, current_link))
        
    return links


def get_page_data(driver: webdriver.Chrome, link: str) -> Dict:
    load_page(driver, link)
    
    try:
        header_element = driver.find_element(By.XPATH, "//*[contains(@class, 'articleHeader')]")
        header = header_element.text
        
        body_element = driver.find_element(By.XPATH, "//div[contains(@class, 'articlePage')]")
        body = body_element.text
        
        content_element = driver.find_element(By.XPATH, "//div[contains(@class, 'contentSectionDetails')]")
        span_element = content_element.find_element(By.TAG_NAME, "span")
        date = span_element.text
        
        return {
            "header": header,
            "body": body,
            "date": date
        }
    except NoSuchElementException:
        return {}
    

def get_pages_data(driver: webdriver.Chrome, links: List[str]) -> List[Dict]:
    data = []
    for link in tqdm(links):
        page_data = get_page_data(driver, link)
        if len(page_data) > 0:
            data.append(page_data)
            
    return data


def get_news(driver: webdriver.Chrome, link: str, num_pages: int = 3000) -> List[Dict]:
    links = get_all_links(driver, link, num_pages)
    data = get_pages_data(driver, links)
    
    return data


def preprocess_data(data: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    dates_parsed = df.date.str.findall("[^\(\)]+\sET")
    df.date = dates_parsed.apply(lambda date: pd.Timestamp(date[0], tz="US/Eastern").tz_convert(None))
    df = df.set_index("date")
    
    return df


if __name__ == "__main__":
    driver = get_driver(EXECUTABLE_PATH)
    data = get_news(driver, POLITICS_NEWS_URL, 100)

    df = preprocess_data(data)
    df.to_csv("politics_news.csv")