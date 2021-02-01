from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Crawler:
    """
      |   Parameters
      |  ----------
      |  driver : selenium.webdriver.Chrome
      |      driver Chrome responsável por gerenciar, automatizar ações com o
      |      navegador Chrome
      |
      |  ----------
      |
      |   Returns
      |
      """

    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url):
        self.driver.get(url)

    def scrape_link(self, xpath):
        return self.driver.find_element_by_xpath(xpath).get_attribute('href')

    def load_more(self, xpath, patience_time=3000):
        from selenium.common.exceptions import ElementClickInterceptedException
        from selenium.common.exceptions import NoSuchElementException

        load_more_exists = True
        while load_more_exists:
            try:
                self.driver.find_element_by_xpath(xpath)
                WebDriverWait(
                    self.driver, patience_time
                ).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, xpath)
                    )
                ).click()
                WebDriverWait(
                    self.driver, patience_time
                ).until(
                    EC.invisibility_of_element(
                        (By.CLASS_NAME, 'load-more-pre-loader')
                    )
                )
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except ElementClickInterceptedException as error:
                WebDriverWait(self.driver, patience_time)
            except NoSuchElementException:
                load_more_exists = False
