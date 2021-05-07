import re
import base64

import pymongo
import scrapy


class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    data_query = {
        "title": lambda response: response.css("div.AdvertCard_advertTitle__1S1Ak::text").get(),
        "price": lambda response: float(
            response.css("div.AdvertCard_price__3dDCr::text").get().replace("\u2009", "")
        ),
        "photos": lambda response: [
            itm.attrib.get("src") for itm in response.css("figure.PhotoGallery_photo__36e_r img")
        ],
        "characteristics": lambda response: [
            {
                "name": itm.css(".AdvertSpecs_label__2JHnS::text").extract_first(),
                "value": itm.css(".AdvertSpecs_data__xK2Qx::text").extract_first()
                or itm.css(".AdvertSpecs_data__xK2Qx a::text").extract_first(),
            }
            for itm in response.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")
        ],
        "descriptions": lambda response: response.css(
            ".AdvertCard_descriptionInner__KnuRi::text"
        ).extract_first(),
        "author": lambda response: AutoyoulaSpider.get_author_id(response),
        "phone": lambda response: AutoyoulaSpider.get_author_phone(response),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def _get_follow(self, response, selector_str, callback):
        for itm in response.css(selector_str):
            url = itm.attrib["href"]
            yield response.follow(url, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response,
            ".TransportMainFilters_brandsList__2tIkv .ColumnItemList_column__5gjdt a.blackLink",
            self.brand_parse,
        )

    def brand_parse(self, response):
        yield from self._get_follow(
            response, ".Paginator_block__2XAPy a.Paginator_button__u1e7D", self.brand_parse
        )
        yield from self._get_follow(
            response,
            "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu.blackLink",
            self.car_parse,
        )

    def car_parse(self, response):
        data = {}
        for key, selector in self.data_query.items():
            try:
                data[key] = selector(response)
            except (ValueError, AttributeError):
                continue
        self.db_client["gb_parse_spiders"][self.name].insert_one(data)

    @staticmethod
    def get_author_id(response):
        marker = "window.transitState = decodeURIComponent"
        for script in response.css("script"):
            try:
                if marker in script.css("::text").extract_first():
                    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                    result = re.findall(re_pattern, script.css("::text").extract_first())
                    return (
                        response.urljoin(f"/user/{result[0]}").replace("auto.", "", 1)
                        if result
                        else None
                    )
            except TypeError:
                pass

    @staticmethod
    def get_author_phone(response):
        marker = "window.transitState = decodeURIComponent"
        for script in response.css("script"):
            try:
                if marker in script.css("::text").extract_first():
                    re_pattern = re.compile(r"phone%22%2C%22([a-zA-Z|\d]+)Xw%3D%3D%22%2C%22time")
                    result = re.findall(re_pattern, script.css("::text").extract_first())
                    result = base64.b64decode(base64.b64decode(result[0]).decode('UTF-8'))
                    return result
            except TypeError:
                pass
