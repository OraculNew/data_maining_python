import scrapy
from ..loaders import VacancyLoader, CompanyLoader
from ..items import VacancyItem, CompanyItem
from .xpaths import SELECTORS, DATA_VACANCY_SELECTORS, DATA_COMPANY_SELECTORS


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response, SELECTORS["vacancy_pagination"], self.parse
        )
        yield from self._get_follow(
            response, SELECTORS["vacancy_url"], self.vacancy_parse
        )

    def vacancy_parse(self, response):
        item = VacancyItem()
        vacancy_loader = VacancyLoader(response=response, item=item)
        vacancy_loader.add_value("url", response.url)
        for key, xpath in DATA_VACANCY_SELECTORS.items():
            vacancy_loader.add_xpath(key, xpath)
        yield from self._get_follow(
            response, SELECTORS["company_url"], self.company_parse
        )
        yield vacancy_loader.load_item()

    def company_parse(self, response):
        item = CompanyItem()
        company_loader = CompanyLoader(response=response, item=item)
        company_loader.add_value("url", response.url)
        for key, xpath in DATA_COMPANY_SELECTORS.items():
            company_loader.add_xpath(key, xpath)
        yield from self._get_follow(
            response, SELECTORS["company_vacancies"], self.parse
        )
        yield company_loader.load_item()
