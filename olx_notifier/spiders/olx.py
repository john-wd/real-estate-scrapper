import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup, element
from ..items import OlxItem
from datetime import datetime, timedelta


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["olx.com.br"]
    start_urls = [
        # Alugueis de casas na grande florianopolis com 2 quartos e até R$1700,00, ordenado pelos mais recentes
        "https://sc.olx.com.br/florianopolis-e-regiao/grande-florianopolis/imoveis/aluguel/casas?pe=1700&ros=2&sd=2507&sd=2516&sd=2509&sd=2518&sd=2513&sd=2517&sd=2510&sd=2512&sd=2514&sd=2508&sd=2511&sd=2515&sf=1",
        "https://sc.olx.com.br/florianopolis-e-regiao/continente/imoveis/aluguel/casas?pe=1700&ros=2&sf=1",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.TextResponse):
        body = BeautifulSoup(response.text)
        ad_list = body.select("#ad-list li")
        # skips native ads
        for ad in filter(lambda x: not x.select("li > div"), ad_list):
            olx_item = OlxItem()
            olx_item["date_collected"] = datetime.now()
            self.parse_ad_link(olx_item, ad)
            self.parse_ad_price(olx_item, ad)
            self.parse_ad_description(olx_item, ad)
            self.parse_ad_address(olx_item, ad)
            yield olx_item

    def parse_ad_link(self, item: OlxItem, ad: element.Tag):
        bs_link = ad.select_one("a[data-lurker-detail='list_id']")
        item["title"] = bs_link["title"]
        item["id"] = bs_link["data-lurker_list_id"]
        item["url"] = bs_link["href"]
        item["date_published"] = item["date_collected"] - timedelta(
            seconds=int(bs_link["data-lurker_last_bump_age_secs"])
        )

    def parse_ad_price(self, item: OlxItem, ad: element.Tag):
        item["price"] = ad.select_one(".sc-ifAKCX.eoKYee").text

    def parse_ad_description(self, item: OlxItem, ad: element.Tag):
        item["specs"] = ad.select_one(".sc-1j5op1p-0.lnqdIU").text

    def parse_ad_address(self, item: OlxItem, ad: element.Tag):
        item["address"] = ad.select_one(".sc-7l84qu-0.gmtqTp").text
