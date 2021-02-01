from src.Crawler import Crawler


class FormFiller(Crawler):
    """
   |   Parameters
   |  ----------
   |  domain : string
   |      endereço do website alvo de scrapping
   |
   |  page_link : string, default None
   |      Se a página alvo de scrapping não for a página principal (domain)
   |      indica-se o padrão XPath para encontrar o link da página de interesse
   |
   |  load_more : string, default None
   |      Se na página alvo de scrapping houver carregamento sob demanda, botão 'load more',
   |      indicar o padrão XPath do botão para que interação do crawler e total carregamento do conteúdo.
   |
   |  load_more_text: string, default None
   |      Somente se 'load_more' for diferente de None. Texto do botão 'load more'.    |
   |
   |  target : string, default None
   |      Se existir uma seção específica da página para recuperação de código fonte indicar
   |      o padrão XPath para que somente o html daquele elemento seja recuperado.
   |
   |  patience_time : integer default 60
   |
   |  ----------
   |
   |   Returns
   |
   |   result : str

   """

    def __init__(self, driver):
        super().__init__(driver)

    def fill_form(self, fields_to_fill, button_xpath):
        for xpath, content in fields_to_fill.items():
            self.driver.find_element_by_xpath(xpath).send_keys(content)
        # self.__driver.find_element_by_xpath(button_xpath).click()
