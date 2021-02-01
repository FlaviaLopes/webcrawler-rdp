# -*- coding: utf-8 -*-
from decouple import config
from selenium.webdriver import Chrome
from src.BlogScraper import BlogScraper
from src.FormFiller import FormFiller
from time import time

begin = time()


def blog_scraper(driver):
    vars = {
        'domain': 'http://www.csa-ma.com.br/',
        'blog_link_xpath': '//*[@id="header-navigation"]//a[child::*[contains(text(), "Blog")]]',
        'load_more_xpath': '//a[@class="load-more-button"]',
        'load_more_preloader_xpath': 'load-more-pre-loader',
        'posts_xpath': '//*[@class="isotope posts"]',
        'post_fields': {
            'thumbnail': 'attachment-post-thumbnail',
            'title': 'post-title',
            'date': 'post-date',
            'excerpt': 'post-excerpt'
        },
        'item_post_xpath': 'isotope-item post',
        'csv_file_path': 'data/page-blog-scrapping.csv'
    }

    blog = BlogScraper(driver)
    blog.navigate_to(vars['domain'])
    # ---------------------------------------------
    print(f'{round((time() - begin), 2)} s > ✓Página principal do site')
    # ---------------------------------------------
    blog.navigate_to(
        blog.scrape_link(vars['blog_link_xpath'])
    )
    blog.load_more_wait_preloader(vars['load_more_xpath'], vars['load_more_preloader_xpath'])
    extracted_html = blog.scraps(vars['posts_xpath'])
    # ---------------------------------------------
    print(f'{round((time() - begin), 2)} s > ✓Posts do Blog raspados')
    # ---------------------------------------------
    extracted_fields = blog.extract(
        extracted_html,
        vars['post_fields'],
        vars['item_post_xpath']
    )
    # ---------------------------------------------
    print(f'{round((time() - begin), 2)} s > ✓Posts extraídos do HTML')
    # ---------------------------------------------
    blog.export(extracted_fields, vars['csv_file_path'])
    # ---------------------------------------------
    print(f'{round((time() - begin), 2)} s > ✓CSV salvo no diretório `data`')
    # ---------------------------------------------


def form_filler(driver):
    vars = {
        'domain': 'http://www.csa-ma.com.br/',
        'contact_link_xpath': '//*[@id="header-navigation"]//a[child::*[contains(text(), "Contato")]]',
        'fields_to_fill': {
            '//*[@id="contact-form"]//input[@name="your-name"]': config('name'),
            '//*[@id="contact-form"]//input[@name="empresa"]': config('organization'),
            '//*[@id="contact-form"]//input[@name="telefone"]': config('phone'),
            '//*[@id="contact-form"]//input[@name="your-email"]': config('email'),
            '//*[@id="contact-form"]//input[@name="website"]': config('website'),
            '//*[@id="contact-form"]//textarea[@name="your-message"]': config('message')
        },
        'button_xpath': '//*[@id="contact-form"]//input[@type="submit"]'
    }
    form = FormFiller(driver)
    form.navigate_to(vars['domain'])
    # ---------------------------------------------
    print(f'{round((time() - begin), 2)} s > ✓Página principal do site')
    # ---------------------------------------------
    form.navigate_to(
        form.scrape_link(vars['contact_link_xpath'])
    )
    # ---------------------------------------------
    print(f'{round((time() - begin), 2)} s > ✓Página de Contato')
    # ---------------------------------------------
    form.fill_form(
        vars['fields_to_fill'],
        vars['button_xpath']
    )
    # ---------------------------------------------
    print(f'{round((time() - begin), 2)} s > ✓Formulário submetido')
    # ---------------------------------------------


def main():
    driver = Chrome(executable_path=config('chromedriver_path'))
    driver.implicitly_wait(30)
    driver.maximize_window()

    blog_scraper(driver)
    form_filler(driver)

    driver.implicitly_wait(30)
    driver.quit()
    print(f'Total: {round((time() - begin), 2)} s')


if __name__ == '__main__':
    main()
