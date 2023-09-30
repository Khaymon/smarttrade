from selenium.webdriver.common.by import By
from selenium import webdriver
import typing as T

from smarttrade.utils.logging import BaseLogger



class BaseSeleniumScrapper:
    def __init__(self, driver_timeout: int, logger: BaseLogger) -> None:
        self._driver = webdriver.Firefox()
        self._driver.set_page_load_timeout(driver_timeout)

        self._logger = logger

    def _load_page(self, link: str) -> bool:
        self._logger.info(f"Try to load the page {link}")
        try:
            self._driver.get(link)
        except Exception as e:
            self._logger.error(f"Unable to load the page {link}, got the exception {e}")
            return False
        return True
    
    def _find_elements_by_xpath(self, attribute: str, value: str, element: str = "*"):
        return self._driver.find_elements(By.XPATH, f"//{element}[contains(@{attribute}, '{value}')]")

    def _find_element_by_xpath(self, attribute: str, value: str, element: str = "*"):
        return self._driver.find_element(By.XPATH, f"//{element}[contains(@{attribute}, '{value}')]")

    def get_data(self, base_page: str, limit: int, **kwargs) -> T.List[T.Any]:
        raise NotImplementedError()
