# -*- coding: utf-8 -*-
from decouple import config
from selenium.webdriver import Chrome
from src.BlogScraper import BlogScraper
from src.FormFiller import FormFiller
from time import time

begin = time()


def blog_scraper(driver):
    blog = BlogScraper(driver)
    blog.navigate_to('http://www.csa-ma.com.br/')
    print(f'{round((time() - begin), 2) } s > ✓Página principal do site')
    blog.navigate_to(
        blog.scrape_link('//*[@id="header-navigation"]//a[child::*[contains(text(), "Blog")]]')
    )
    blog.load_more('//a[@class="load-more-button"]')
    extracted_html = blog.scraps('//*[@class="isotope posts"]')
    print(f'{round((time() - begin), 2) } s > ✓Posts do Blog raspados')
    extracted_fields = blog.extract(
        extracted_html,
        post_fields={
            'thumbnail': 'attachment-post-thumbnail',
            'title': 'post-title',
            'date': 'post-date',
            'excerpt': 'post-excerpt'
        },
        item_post_class='isotope-item post'
    )
    print(f'{round((time() - begin), 2) } s > ✓Posts extraídos do HTML')
    blog.export(extracted_fields, 'data/page-blog-scrapping.csv')
    print(f'{round((time() - begin), 2) } s > ✓CSV salvo no diretório `data`')

def form_filler(driver):
    form = FormFiller(driver)
    form.navigate_to('http://www.csa-ma.com.br/')
    print(f'{round((time() - begin), 2) } s > ✓Página principal do site')
    form.navigate_to(
        form.scrape_link('//*[@id="header-navigation"]//a[child::*[contains(text(), "Contato")]]')
    )
    print(f'{round((time() - begin), 2) } s > ✓Página de Contato')
    form.fill_form(
        fields_to_fill={
            '//*[@id="contact-form"]//input[@name="your-name"]': config('name'),
            '//*[@id="contact-form"]//input[@name="empresa"]': config('organization'),
            '//*[@id="contact-form"]//input[@name="telefone"]': config('phone'),
            '//*[@id="contact-form"]//input[@name="your-email"]': config('email'),
            '//*[@id="contact-form"]//input[@name="website"]': config('website'),
            '//*[@id="contact-form"]//textarea[@name="your-message"]': config('message')
        },
        button_xpath='//*[@id="contact-form"]//input[@type="submit"]'
    )
    print(f'{round((time() - begin), 2) } s > ✓Formulário submetido')


def main():
    driver = Chrome(executable_path=config('chromedriver_path'))
    driver.implicitly_wait(30)
    driver.maximize_window()

    blog_scraper(driver)
    form_filler(driver)

    driver.implicitly_wait(30)
    driver.quit()
    print(f'Total: {round((time() - begin), 2) } s')



if __name__ == '__main__':
    main()
