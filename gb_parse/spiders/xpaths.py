SELECTORS = {
    "vacancy_pagination": "//div[@data-qa='pager-block']//a[@data-qa='pager-page']/@href",
    "vacancy_url": "//div[@class='vacancy-serp']//a[@data-qa='vacancy-serp__vacancy-title']/@href",
    "company_url": "//div[@data-qa='vacancy-company']//a[@data-qa='vacancy-company-name']/@href",
    "company_vacancies": '//div[@class="employer-sidebar-block"]'
                         '/a[@data-qa="employer-page__employer-vacancies-link"]/@href',
}

DATA_VACANCY_SELECTORS = {
    "title": '//div[@class="vacancy-title"]/h1[@data-qa="vacancy-title"]/text()',
    "salary": '//div[@class="vacancy-title"]//p[@class="vacancy-salary"]/span/text()',
    "description": '//div[@data-qa="vacancy-description"]//text()',
    "company_url": "//div[@data-qa='vacancy-company']//a[@data-qa='vacancy-company-name']/@href",
    "tags": '//div[@class="bloko-tag-list"]//div//div["bloko-tag bloko-tag_inline"]'
            '/span[@class="bloko-tag__section bloko-tag__section_text"]/text()',
}

DATA_COMPANY_SELECTORS = {
    "title": '//div[@class="company-header"]//span[@data-qa="company-header-title-name"]/text()',
    "site": '//div[@class="employer-sidebar-content"]/a[@data-qa="sidebar-company-site"]/@href',
    "area_of_activity": '//div[@class="employer-sidebar-block"]/p/text()',
    "description": '//div[@data-qa="company-description-text"]/div[@class="g-user-content"]//text()',
}
