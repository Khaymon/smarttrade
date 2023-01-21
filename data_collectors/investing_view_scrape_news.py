import argparse
from typing import List, Dict
from tqdm import tqdm
import pandas as pd
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

BASE_URL = "https://www.investing.com/news/[AREA]/"


def get_driver(executable_path: str, timeout: int):
    driver = webdriver.Chrome(executable_path)
    driver.set_page_load_timeout(timeout)
    
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


def get_all_links(driver, link: str, num_pages: int = 3000, from_page: int = 1) -> List[str]:
    links = []
    for page in tqdm(range(from_page, from_page + num_pages)):
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
    

def get_pages_data(driver: webdriver.Chrome, links: List[str], max_news: int) -> List[Dict]:
    data = []
    for link in tqdm(links[:max_news]):
        page_data = get_page_data(driver, link)
        if len(page_data) > 0:
            data.append(page_data)
            
    return data


def get_news(driver: webdriver.Chrome,
             link: str, 
             num_pages: int = 3_000,
             from_page: int = 1,
             max_news: int = 10_000) -> List[Dict]:
    links = get_all_links(driver=driver, link=link, num_pages=num_pages, from_page=from_page)
    data = get_pages_data(driver=driver, links=links, max_news=max_news)
    
    return data


def preprocess_data(data: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    dates_parsed = df.date.str.findall("[^\(\)]+\sET")
    df.date = dates_parsed.apply(lambda date: pd.Timestamp(date[0], tz="US/Eastern"))
    df = df.set_index("date")
    
    return df


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="investing.com news scraper",
        description="Tool for scraping news from the investing.com",
        add_help=True
    )
    
    parser.add_argument("-d", "--driver", type=str, dest="driver_path", 
                        help="Path to the Chrome driver executable", required=True)
    parser.add_argument("-a", "--area", type=str, dest="area", choices=["stock-market", "politics", "economy"],
                        help="News area to scrape", required=True)
    parser.add_argument("-n", "--num-pages", type=int, dest="num_pages", default=500,
                        help="Number of news pages to scrape")
    parser.add_argument("-b", "--begin-page", type=int, dest="from_page", default=1,
                        help="Page number to start with")
    parser.add_argument("-o", "--output-path", type=str, dest="output_path",
                        help="Path for the output .parquet file", required=True)
    parser.add_argument("-m", "--max-news", type=int, dest="max_news",
                        help="Maximal number of news", required=False, default=10_000)
    parser.add_argument("-t", "--timeout", type=int, dest="timeout",
                        help="Page load timeout in seconds", required=False, default=1)
    
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    
    print(arguments)
    driver = get_driver(arguments.driver_path, timeout=arguments.timeout)
    
    if arguments.area == "stock-market":
        area_url = re.sub("\[AREA\]", "stock-market-news", BASE_URL)
    elif arguments.area == "politics":
        area_url = re.sub("\[AREA\]", "politics", BASE_URL)
    elif arguments.area == "economy":
        area_url = re.sub("\[AREA\]", "economy", BASE_URL)
    else:
        raise ValueError("Unknown news area")
    
    data = get_news(driver=driver, link=area_url, num_pages=arguments.num_pages,
                    from_page=arguments.from_page, max_news=arguments.max_news)

    df = preprocess_data(data)
    df.to_parquet(arguments.output_path)


if __name__ == "__main__":
    main()
    