import scrapy
from scrapy.http import Response
import json
from urllib.parse import quote_plus as encodeURIElement
from datetime import datetime

from ..db.models import AdItem


class VivaRealSpider(scrapy.Spider):
    name = "vivareal"
    allowed_domains = ["vivareal.com.br"]
    api_url = "https://glue-api.vivareal.com/v2/listings"
    headers = {
        "x-domain": "www.vivareal.com.br",
    }
    options = {
        "bedrooms": 2,
        "priceMax": 1200,
        "business": "RENTAL",
        "usageTypes": "RESIDENTIAL",
        "unitTypes": "APARTMENT,HOME",
        "unitTypesV3": "APARTMENT,HOME",
        "categoryPage": "RESULT",
        "listingType": "USED",
        "size": 70,
    }
    state = "Santa Catarina"
    places = [
        "Joinville",
        "Itajai",
    ]

    @property
    def domain(self):
        return self.allowed_domains[0]

    def query_args(self) -> str:
        return (
            "?"
            + "&".join(
                f"{k}={encodeURIElement(str(v))}" for k, v in self.options.items()
            )
            + "&addressLocationId="
            + encodeURIElement(self.get_locations())
        )

    def get_locations(self) -> str:
        return ",".join(
            "BR>{state}>NULL>{place}".format(state=self.state, place=place)
            for place in self.places
        )

    def start_requests(self):
        url = self.api_url + self.query_args()
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            headers=self.headers,
        )

    def parse(self, response: Response):
        payload = json.loads(response.body)
        for ad in payload["search"]["result"]["listings"]:
            listing = ad["listing"]
            link = ad["link"]
            account = ad["account"]
            if listing["pricingInfos"][0]["rentalInfo"]["period"] == "DAILY":
                # we do not want daily rentals
                continue

            item = AdItem()
            item["id"] = listing["id"]
            item["title"] = listing["title"]
            item["source"] = self.get_id(account["name"])
            item["url"] = self.get_full_url(link["href"])
            item["address"] = self.get_address(listing["address"])
            item["specs"] = self.get_specs(listing)
            item["price"] = self.get_price(listing["pricingInfos"][0])
            item["date_collected"] = datetime.now()
            item["date_published"] = self.get_datetime_from_string(listing["createdAt"])
            yield item

    #################################
    # Helper functions

    @staticmethod
    def get_address(address: dict) -> str:
        return "{street}{number} - {neighborhood} - {city} / {state} - {cep}".format(
            street=address.get("street", ""),
            number=", " + address.get("streetNumber")
            if "streetNumber" in address
            else "",
            neighborhood=address.get("neighborhood", ""),
            city=address.get("city", ""),
            state=address.get("stateAcronym", address.get("state", "")),
            cep=address.get("zipCode", ""),
        )

    @staticmethod
    def get_specs(listing: dict) -> str:
        return "{type_} | {size}m² | {parking} vagas | {bedrooms} quartos | {bathrooms} banheiros".format(
            type_=",".join(str(x) for x in listing["usageTypes"]),
            size=",".join(str(x) for x in listing["usableAreas"]),
            parking=",".join(str(x) for x in listing["parkingSpaces"]),
            bedrooms=",".join(str(x) for x in listing["bedrooms"]),
            bathrooms=",".join(str(x) for x in listing["bathrooms"]),
        )

    @staticmethod
    def get_datetime_from_string(dateentry: str):
        return datetime.fromisoformat(dateentry.split("Z")[0])

    @staticmethod
    def get_price(priceInfo: dict) -> int:
        price = int(priceInfo["price"])
        iptu = float(priceInfo.get("yearlyIptu", 0)) / 12
        condotax = int(priceInfo.get("monthlyCondoFee", 0))
        return price + condotax + iptu

    def get_full_url(self, partial: str) -> str:
        return self.domain + partial

    def get_id(self, agency: str) -> str:
        return "{bot} ({agency})".format(bot=self.name, agency=agency)
