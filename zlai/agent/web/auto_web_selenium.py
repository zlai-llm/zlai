from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Any, List, Callable, Literal, Optional
from pydantic import BaseModel, Field

from ...schema.content import PageContent
from ..base import AgentMixin


__all__ = []


class ChangeURL(BaseModel):
    """"""
    upper: Optional[str] = Field(default=None, description="")
    lower: Optional[str] = Field(default=None, description="")
    mark: Optional[bool] = Field(default=None, description="")
    error: Optional[str] = Field(default=None, description="")
    change_type: Optional[str] = Field(default=None, description="")


class AutoWebAgent(AgentMixin):
    """"""
    max_deep: Optional[int] = 0

    def __init__(
            self,
            url: Optional[str] = None,
            max_deep: Optional[int] = 0,
            max_pages: Optional[int] = 10,
            key_words: Optional[List[str]] = None,
            browser: Literal["chrome", "firefox"] = "chrome",
            binary_location: Optional[str] = None,
            executable_path: Optional[str] = None,
            headless: bool = True,
            arguments: Optional[List[str]] = None,
            logger: Optional[Callable] = None,
            verbose: Optional[bool] = True,
            **kwargs: Any,
    ):
        """"""
        self._imp()
        self.url = url
        self.max_deep = max_deep
        self.max_pages = max_pages
        self.key_words = key_words
        self.browser = browser
        self.binary_location = binary_location
        self.executable_path = executable_path
        self.headless = headless
        self.arguments = arguments
        self.logger = logger
        self.verbose = verbose
        self.kwargs = kwargs

        self.driver = self.set_driver()
        self.visited_urls = set()

    def _imp(self):
        """"""
        try:
            import selenium
        except ImportError:
            raise ImportError(
                "selenium package not found, please install it with "
                "`pip install selenium`"
            )
        try:
            import unstructured
        except ImportError:
            raise ImportError(
                "unstructured package not found, please install it with "
                "`pip install unstructured`"
            )

    def set_driver(
            self,
    ):
        """"""
        if self.browser.lower() == "chrome":
            chrome_options = ChromeOptions()
            if self.arguments:
                for arg in self.arguments:
                    chrome_options.add_argument(arg)
            if self.headless:
                """"""
                chrome_options.add_argument("--blink-settings=imagesEnabled=false")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
            if self.binary_location is not None:
                chrome_options.binary_location = self.binary_location
            if self.executable_path is None:
                return Chrome(options=chrome_options)
            return Chrome(options=chrome_options,)
        elif self.browser.lower() == "firefox":
            firefox_options = FirefoxOptions()

            if self.arguments:
                for arg in self.arguments:
                    firefox_options.add_argument(arg)

            if self.headless:
                firefox_options.add_argument("--headless")
            if self.binary_location is not None:
                firefox_options.binary_location = self.binary_location
            if self.executable_path is None:
                return Firefox(options=firefox_options)
            return Firefox(options=firefox_options,)
        else:
            raise ValueError("Invalid browser specified. Use 'chrome' or 'firefox'.")

    def get_page_content(self, page_content: str) -> str:
        """"""
        from unstructured.partition.html import partition_html
        elements = partition_html(text=page_content)
        text = "\n\n".join([str(el) for el in elements])
        return text

    def _check_element(self, element: WebElement, current_pages: Optional[int]) -> bool:
        """"""
        try:
            if current_pages > self.max_pages:
                condition_key_words = False
                for key_word in self.key_words:
                    if key_word in element.text:
                        condition_key_words = True
            else:
                condition_key_words = True
            marks = [
                element.is_enabled(),
                element.is_displayed(),
                element.tag_name in ["button", "a"],
                len(element.text) <= 5,
                condition_key_words,
            ]
            if all(marks):
                return True
            else:
                return False
        except Exception as e:
            self._logger(msg=f"Check element error: {e}")

    def get_link_elements(self, url, wait=False):
        """"""
        self.driver.get(url)
        # if wait:
        #     wait = WebDriverWait(self.driver, timeout=5)
        #     # wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        #     # wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
        #     wait.until(EC.all_of(
        #         EC.presence_of_all_elements_located((By.TAG_NAME, "a")),
        #         EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
        #     ))
        # elements = self.driver.find_elements(by=By.XPATH, value="//*")
        elements = sum([
            self.driver.find_elements(by=By.TAG_NAME, value="a"),
            self.driver.find_elements(by=By.TAG_NAME, value="button"),
        ], [])
        current_pages = len(elements)
        elements = [element for element in elements if self._check_element(element, current_pages=current_pages)]
        return elements

    def _change_url_mark(self, change_url: ChangeURL):
        """"""
        if change_url.upper != change_url.lower:
            change_url.mark = True
        else:
            change_url.mark = False

    def click_element(self, element: Optional[WebElement]) -> ChangeURL:
        """"""
        change_url = ChangeURL(change_type="click")
        try:
            change_url.upper = self.driver.current_url
            element.click()
            change_url.lower = self.driver.current_url
            self._change_url_mark(change_url=change_url)
        except Exception as error:
            change_url.error = error
        return change_url

    def click_element_by_script(self, element: Optional[WebElement]) -> ChangeURL:
        """"""
        change_url = ChangeURL(change_type="script")
        try:
            change_url.upper = self.driver.current_url
            self.driver.execute_script("arguments[0].click();", element)
            change_url.lower = self.driver.current_url
            self._change_url_mark(change_url=change_url)
        except Exception as error:
            change_url.error = error
        return change_url

    def click_element_by_href(self, element: Optional[WebElement]) -> ChangeURL:
        """"""
        change_url = ChangeURL(change_type="href")
        try:
            change_url.upper = self.driver.current_url
            href = element.get_attribute('href')
            self.driver.get(url=href)
            change_url.lower = self.driver.current_url
            self._change_url_mark(change_url=change_url)
        except Exception as error:
            change_url.error = error
        return change_url

    def switch_lower_url(self, element: Optional[WebElement]) -> ChangeURL:
        """"""
        change_url = ChangeURL(mark=False)
        for click_fun in [self.click_element, self.click_element_by_script, self.click_element_by_href]:
            change_url = click_fun(element)
            if change_url.mark:
                return change_url
        else:
            return change_url

    def load_url_content(
            self,
            url: str,
            pages_content: List[PageContent],
            deep: Optional[int] = None,
    ):
        """"""
        if deep <= self.max_deep and url is not None:
            elements = self.get_link_elements(url, wait=True)
            elements_length = len(elements)
            self._logger(msg=f"Find {elements_length} elements.", color="green")
            for i in range(elements_length):
                elements = self.get_link_elements(url, wait=True)
                if i < len(elements):
                    try:
                        element = elements[i]
                        title = element.text
                        switch = self.switch_lower_url(element)
                        if switch.lower is not None and switch.lower not in self.visited_urls:
                            self.visited_urls.add(self.driver.current_url)
                            content = self.get_page_content(page_content=self.driver.page_source)
                            self._logger(msg=f"deep: {deep}, url: {self.driver.current_url}, urls: {len(self.visited_urls)}", color="green")
                            pages_content.append(
                                PageContent(url=self.driver.current_url, title=title, content=content, deep=deep,))
                            self.load_url_content(url=self.driver.current_url, pages_content=pages_content, deep=deep + 1)
                        else:
                            self._logger(msg=f"deep: {deep}, url: {switch.lower} exits.", color="green")
                        # self.driver.back()
                    except Exception as e:
                        self._logger(msg=f"error: {e}", color="red")
                        pass

    def load_pages_content(
            self,
            url: str,
            deep: Optional[int] = 0
    ) -> List[PageContent]:
        """
        列出所有可点击的标签
        参数：
        - url: 要访问的网页URL
        """
        pages_content = []
        self.load_url_content(url=url, pages_content=pages_content, deep=deep)
        self.driver.quit()
        return pages_content
