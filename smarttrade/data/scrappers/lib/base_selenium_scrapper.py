from selenium.webdriver.common.by import By
from selenium import webdriver
import pathlib
import typing as T



class BaseSeleniumScrapper:
    def __init__(self, driver_path: pathlib.Path, driver_timeout: int) -> None:
        self._driver = webdriver.Firefox()
        self._driver.set_page_load_timeout(driver_timeout)

    def _load_page(self, link: str) -> bool:
        try:
            self._driver.get(link)
        except:
            return False
        return True
    
    def _find_elements_by_xpath(self, attribute: str, value: str, element: str = "*"):
        return self._driver.find_elements(By.XPATH, f"//{element}[contains(@{attribute}, '{value}')]")

    def _find_element_by_xpath(self, attribute: str, value: str, element: str = "*"):
        return self._driver.find_element(By.XPATH, f"//{element}[contains(@{attribute}, '{value}')]")

    def get_data(self, base_page: str, limit: int, **kwargs) -> T.List[T.Any]:
        raise NotImplementedError()
