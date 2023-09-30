from selenium.webdriver.common.by import By
import datetime
import typing as T

from smarttrade.utils.common import HTMLAttributes, HTMLElements
from smarttrade.data.containers.base import ArticleContainer
from smarttrade.utils.logging import BaseLogger

from .base_selenium_scrapper import BaseSeleniumScrapper


class InvestingSeleniumScrapper(BaseSeleniumScrapper):
    class ParseNames:
        ARTICLES_DIV = "largeTitle"
        ARTICLE_TITLE = "title"
        ARTICLE_HEADER = "articleHeader"
        ARTICLE_BODY = "articlePage"
        DATE_DIV = "contentSectionDetails"
        DATE_TAG = "span"

    def __init__(self, driver_timeout: int, logger: BaseLogger, page_limit: int = 100) -> None:
        super().__init__(driver_timeout, logger)

        self._page_limit = page_limit

    def _get_page_links(self, link: str) -> T.List[str]:
        self._load_page(link)

        links = []
        try:
            div_articles = self._find_element_by_xpath(
                HTMLAttributes.CLASS, InvestingSeleniumScrapper.ParseNames.ARTICLES_DIV, HTMLElements.DIV,
            )
            articles_titles = div_articles.find_elements(
                By.CLASS_NAME, InvestingSeleniumScrapper.ParseNames.ARTICLE_TITLE
            )
            links = [title.get_attribute(HTMLAttributes.HREF) for title in articles_titles]
        except Exception as e:
            self._logger.error(f"Got the exception {e} while parsing articles links")

        return links

    def _get_links(self, base_link: str, limit: int, start_page: int) -> T.List[str]:
        links = []

        for page_num in range(start_page, start_page + self._page_limit):
            current_link = base_link + str(page_num)
            current_articles_links = self._get_page_links(current_link)

            if len(links) + len(current_articles_links) > limit:
                break
            links.extend(current_articles_links)
        
        return links
    
    def _get_link_data(self, link: str) -> T.Optional[ArticleContainer]:
        self._load_page(link)
    
        try:
            header_element = self._find_element_by_xpath(
                HTMLAttributes.CLASS, InvestingSeleniumScrapper.ParseNames.ARTICLE_HEADER
            )
            header = header_element.text
            
            body_element = self._find_element_by_xpath(
                HTMLAttributes.CLASS, InvestingSeleniumScrapper.ParseNames.ARTICLE_BODY, HTMLElements.DIV
            )
            body = body_element.text
            
            content_element = self._find_element_by_xpath(
                HTMLAttributes.CLASS, InvestingSeleniumScrapper.ParseNames.DATE_DIV, HTMLElements.DIV
            )
            span_element = content_element.find_element(
                By.TAG_NAME, InvestingSeleniumScrapper.ParseNames.DATE_TAG
            )
            date = span_element.text
            
            return ArticleContainer(
                date=datetime.datetime.fromisoformat(date),
                text=body,
                header=header,
                link=link,
            )
        except Exception as e:
            self._logger.error(f"Exception {e} occured when parsing the page {link}")

        return None

    def _get_links_data(self, links: T.List[str], limit: int) -> T.List[ArticleContainer]:
        data = []
        for link in links[:limit]:
            link_data = self._get_link_data(link)
            if link_data:
                data.append[link_data]

        self._logger.info(f"Got {len(data)} articles links")
        return data

    def get_data(self, base_link: str, limit: int, start_page: int = 1) -> T.List[ArticleContainer]:
        links = self._get_links(base_link, limit, start_page)
        return self._get_links_data(links, limit)
