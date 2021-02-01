from src.Crawler import Crawler
from bs4 import BeautifulSoup as bs
import pandas as pd


class BlogScraper(Crawler):

    def __init__(self, driver):
        super().__init__(driver)

    def scraps(self, xpath=None):
        """
        |   Parameters
        |  ----------
        |  xpath : string
        |      padrão xpath para recuperar conteúdo html desejado da página.
        |
        |  ----------
        |
        |   Returns
        |
        |   result : str
        |   string com o conteúdo html de interesse.
        """
        if xpath is not None:
            result = self.driver.find_element_by_xpath(xpath).get_attribute('outerHTML')
        else:
            result = self.driver.find_element_by_css_selector('html').get_attribute('outerHTML')

        return result

    def extract(self, data, post_fields, item_post_class):
        """
        |   Parameters
        |  ----------
        |  data : string
        |      conteúdo html de onde serão extraídos dados do scrapping.
        |
        |  post_fields : dict
        |      Dicionário com o nome do campo que se deseja extrair e sua classe.
        |      O nome do campo será o nome da coluna do dataframe.
        |
        |  item_post_class : string
        |      Nome da classe do elemento onde serão feitas as buscas.
        |      Ex.: node = 'isotope-item post' (item de post na listagem)
        |      Em node existirão outros elementos cujos textos serão extraídos.
        |
        |  ----------
        |
        |   Returns
        |
        |   result : dict
        |   dicionário com os campos extraídos

        """
        soup = bs(data, 'html.parser')
        soup = soup.find_all(
            attrs={'class': item_post_class}
        )

        data = {}
        for it in post_fields.keys():
            data.update({it: []})

        for post in soup:
            for k, v in post_fields.items():
                element = post.find(attrs={'class': [v]})
                if element:
                    if element.name == 'img':
                        data[k].append(element.attrs['src'])
                    else:
                        data[k].append(element.text)
                else:
                    data[k].append('')

        return data

    def export(self, data, path):
        """
        |   Recebe dados em dicionário e converte- o para pandas DataFrame.
        |   Faz pequenos ajustes, converte e exporta dados em arquivo CSV .
        |
        |   Parameters
        |  ----------
        |  data : dict (key: string, value: list)
        |      dicionário campos dos posts extraídos.
        |
        |  path : str
        |      Caminho para o diretório onde se deve salvar os dados em .csv.
        |
        |  ----------
        |
        |   Returns        |
        |   result : arquivo CSV
        |
        """
        result = pd.DataFrame(data=data)
        for col in result.columns:
            if result[col].dtype == 'object':
                result[col] = result[col].str.strip()

        result.to_csv(path, index=False)
