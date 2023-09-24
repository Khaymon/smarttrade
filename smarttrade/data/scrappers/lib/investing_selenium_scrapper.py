from selenium.webdriver.common.by import By
import datetime
import pathlib
import typing as T

from smarttrade.data.containers import TextContainer

from .base_selenium_scrapper import BaseSeleniumScrapper


class InvestingSeleniumScrapper(BaseSeleniumScrapper):
    ARTICLES_DIV_CLASSNAME = "largeTitle"
    ARTICLE_TITLE_CLASSNAME = "title"
    ARTICLE_HEADER = "articleHeader"
    ARTICLE_PAGE = "articlePage"
    CONTENT_SECTION_DETAILS = "contentSectionDetails"

    def __init__(self, driver_path: pathlib.Path, driver_timeout: int, page_limit: int = 100) -> None:
        super().__init__(driver_path, driver_timeout)

        self._page_limit = page_limit

    def _get_page_links(self, link: str) -> T.List[str]:
        self._load_page(link)

        links = []
        try:
            div_articles = self._find_element_by_xpath("class", self.ARTICLES_DIV_CLASSNAME, "div")
            links = [ref.get_attribute("href") for ref in div_articles.find_elements(By.CLASS_NAME, self.ARTICLE_TITLE_CLASSNAME)]
        except:
            pass

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
    
    def _get_link_data(self, link: str) -> T.Optional[TextContainer]:
        self._load_page(link)
    
        try:
            header_element = self._find_element_by_xpath("class", self.ARTICLE_HEADER)
            header = header_element.text
            
            body_element = self._find_element_by_xpath("class", self.ARTICLE_PAGE, "div")
            body = body_element.text
            
            content_element = self._find_element_by_xpath("class", self.CONTENT_SECTION_DETAILS, "div")
            span_element = content_element.find_element(By.TAG_NAME, "span")
            date = span_element.text
            
            return TextContainer(
                date=datetime.datetime.fromisoformat(date),
                text=body,
                header=header,
                link=link,
            )
        except:
            pass

        return None

    def _get_links_data(self, links: T.List[str], limit: int) -> T.List[TextContainer]:
        data = []
        for link in links[:limit]:
            link_data = self._get_link_data(link)
            if link_data:
                data.append[link_data]

        return data

    def get_data(self, base_link: str, limit: int, start_page: int = 1) -> T.List[TextContainer]:
        links = self._get_links(base_link, limit, start_page)
        return self._get_links_data(links, limit)
