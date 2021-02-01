from src.Crawler import Crawler


class FormFiller(Crawler):
    """
   |  Crawler que acessa uma página de contato, preenche os campos de formulário,
   |  submete formulário.
   |
   """

    def __init__(self, driver):
        super().__init__(driver)

    def fill_form(self, fields_to_fill, button_xpath):
        """
        |  Preenche campos de formulários de acordo com os padrões passados e submete formulário.
        |
        |   Parameters
        |  ----------
        |  fields_to_fill : dict (key : xpath padrão do campo, value: valor a ser preenchido)
        |  Ex.: {"//*[@id='input']" : "valor do input"}
        |  ----------
        |
        |   Returns
        |
        """
        for xpath, content in fields_to_fill.items():
            self.driver.find_element_by_xpath(xpath).send_keys(content)
        self.driver.find_element_by_xpath(button_xpath).click()
