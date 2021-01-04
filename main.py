from selenium import webdriver
from bs4 import BeautifulSoup
import time


def create_headless_browser():
    # options = Options()
    # options.set_headless()
    # assert options.headless  # assert Operating in headless mode
    # return webdriver.Chrome(options=options)
    return webdriver.Chrome()


class ScrapePinterestSearch:
    def __init__(self, keyword, browser=None):
        self.base_url = f'https://www.pinterest.com/search/pins/?q={keyword}'
        if not browser:
            self.browser = create_headless_browser()
        else:
            self.browser = browser

    def __scroll_to_the_buttom(self):
        # * scroll to buttom of the webpage
        scrolling_script = "window.scrollTo(0,document.body.scrollHeight)"
        content_page = ""
        while content_page != self.browser.page_source:
            content_page = self.browser.page_source
            self.browser.execute_script(scrolling_script)
            try:
                see_more = self.browser.find_element_by_xpath(
                    "//*[contains(text(), 'Show More Posts from')]")
                see_more.click()
            except:
                pass
            time.sleep(5)

    def __scroll(self, max_scroll=2):
        scrolling_script = "window.scrollTo(0,document.body.scrollHeight)"
        for index in range(max_scroll):
            self.browser.execute_script(scrolling_script)
            time.sleep(5)

    def __load_full_page(self, url=None, callback=None):
        url = url or self.base_url
        self.browser.get(url)
        time.sleep(10)
        if callback:
            callback()
        print(f"@@@ {self.base_url} is fully loaded @@@")
        return self.browser.page_source

    @staticmethod
    def __get_pins_urls(source_code):
        soup = BeautifulSoup(source_code, 'html.parser')
        a_elements = soup.find_all('a')
        return {
            f'https://www.pinterest.com{element["href"]}'
            for element in a_elements
            if (element.has_attr('href')
                and 'pin/' in element['href'])
        }

    def __get_pin_details(self, url):
        source_code = self.__load_full_page(url=url)
        soup = BeautifulSoup(source_code, 'html.parser')
        original_link = soup.select_one('.linkModuleActionButton')['href']
        return {
            'url': url,
            'original_link': original_link
        }

    def __call__(self, *args, **kwargs):
        source_code = self.__load_full_page()
        urls = self.__get_pins_urls(source_code)
        # pins = [self.__get_pin_details(url) for url in urls]
        print(self.__get_pin_details(list(urls)[0]))


if __name__ == '__main__':
    keyword = 'recipes'
    headless_browser = create_headless_browser()
    sps = ScrapePinterestSearch(keyword, headless_browser)
    sps()
