from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Crawler:
    """
      |  Classe genérica de web crawler.
      |
      |   Parameters
      |  ----------
      |  driver : selenium.webdriver.Chrome
      |     Driver Chrome responsável por gerenciar, automatizar ações de
      |     navegação web usando o Chrome browser.
      |     Permite maior interação com a página e recuperar elementos de
      |     carregamento dinâmico (javascript).
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
        """
          |  Procura na página o padrão passado xpath e extrai um link.
          |            |
          |   Parameters
          |  ----------
          |  xpath : str
          |     xpath padrão relativo ao elemento clicável de onde se deseja
          |     extrair o link (atributo href)
          |
          |  ----------
          |
          |   Returns str
          |     string com link.
          |
          """
        return self.driver.find_element_by_xpath(xpath).get_attribute('href')

    def load_more_wait_preloader(self, xpath, xpath_preloader, patience_time=3000):
        """
          |  Interage com a página para que o conteúdo seja totalmente carregado.
          |  Ex.: botões `load more`
          |
          |   Parameters
          |  ----------
          |  xpath : str
          |     xpath padrão relativo ao elemento clicável responsável por carregar
          |     o conteúdo na página (link, input, button, ...)
          |
          |  xpath_preloader : str
          |     xpath padrão, ou classe, relativo ao elemento que se deseja esperar que fique
          |     invisível.
          |     Ex.: pre loader animações.
          |
          |   patience_time : int
          |     Tempo de espera utilizado com a classe WebDriverWait
          |
          |  ----------
          |
          |   Returns
          |
          """
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
                        (By.CLASS_NAME, xpath_preloader)
                    )
                )
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except ElementClickInterceptedException as error:
                WebDriverWait(self.driver, patience_time)
            except NoSuchElementException:
                load_more_exists = False
