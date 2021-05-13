AVITO_PAGE_XPATH = {
    "pagination": '//div[contains(@class, "pagination-hidden")]//a[@class="pagination-page"]/@href',
    "offer": '//div[contains(@class, "iva-item-root")]//div[contains(@class, "iva-item-titleStep")]//'
    'a[contains(@class, "title-root")]/@href',
}

AVITO_OFFER_XPATH = {
    "title": '//span[@class="title-info-title-text"]/text()',
    "price": '//div[@id="price-value"]//span[@class="js-item-price"]/@content',
    "address": '//span[@class="item-address__string"]/text()',
    "description": '//div[@class="item-params-title" and contains(text(), "О квартире")]'
                   '/following-sibling::ul/li/text()',
    "author": '//div[@data-marker="seller-info/name"]/a/@href',
}