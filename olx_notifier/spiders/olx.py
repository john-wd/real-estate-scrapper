import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup, element
from ..db.models import AdItem
from ..util import parse_price
from datetime import datetime, timedelta


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["olx.com.br"]
    start_urls = [
        # Compra de terreno até R$500.000 com palavra chave 'hectar'
        "https://sc.olx.com.br/norte-de-santa-catarina/imoveis/terrenos/lotes/compra?pe=500000&q=hectar",                     # Itajai + região
        "https://sc.olx.com.br/florianopolis-e-regiao/outras-cidades/imoveis/terrenos/lotes/compra?pe=500000&q=hectar",       # interior da grande florianopolis
        "https://sc.olx.com.br/florianopolis-e-regiao/grande-florianopolis/imoveis/terrenos/lotes/compra?pe=500000&q=hectar", # grande florianopolis
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.TextResponse):
        body = BeautifulSoup(response.text)
        ad_list = body.select("#ad-list li")
        # skips native ads
        for ad in filter(lambda x: not x.select("li > div"), ad_list):
            olx_item = AdItem()
            olx_item["source"] = self.name
            olx_item["date_collected"] = datetime.now()
            self.parse_ad_link(olx_item, ad)
            self.parse_ad_price(olx_item, ad)
            self.parse_ad_description(olx_item, ad)
            self.parse_ad_address(olx_item, ad)
            yield olx_item

    def parse_ad_link(self, item: AdItem, ad: element.Tag):
        bs_link = ad.select_one("a[data-lurker-detail='list_id']")
        item["title"] = bs_link["title"]
        item["id"] = bs_link["data-lurker_list_id"]
        item["url"] = bs_link["href"]
        item["date_published"] = item["date_collected"] - timedelta(
            seconds=int(bs_link["data-lurker_last_bump_age_secs"])
        )

    def parse_ad_price(self, item: AdItem, ad: element.Tag):
        sel = ad.select_one(".fnmrjs-7.erUydy").select_one(".sc-ifAKCX.eoKYee")
        val = ""
        if sel:
            val = parse_price(sel.text)
        item["price"] = val

    def parse_ad_description(self, item: AdItem, ad: element.Tag):
        sel = ad.select_one(".sc-1j5op1p-0.lnqdIU")
        val = ""
        if sel:
            val = sel.text
        item["specs"] = val

    def parse_ad_address(self, item: AdItem, ad: element.Tag):
        sel = ad.select_one(".sc-7l84qu-0.gmtqTp")
        val = ""
        if sel:
            val = sel.text
        item["address"] = val
