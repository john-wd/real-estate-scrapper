# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    specs = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    date_published = scrapy.Field()
    date_collected = scrapy.Field()
    url = scrapy.Field()

    def __str__(self) -> str:
        return (
            "[{source}] {title}"
            "\n"
            "{price} - {specs}"
            "\n\n"
            "{address}"
            "\n\n"
            "{url}"
        ).format(
            source=self["source"],
            title=self["title"],
            price=self["price"],
            specs=self["specs"],
            address=self["address"],
            url=self["url"],
        )

    def html(self) -> str:
        return (
            "<h2>[{source}] {title}</h2>"
            "<br/>"
            "<b>{price}</b> - {specs}"
            "<br/>"
            "Endereço: <i>{address}</i>"
            "<br/>"
            "{url}"
        ).format(
            source=self["source"],
            title=self["title"],
            price=self["price"],
            specs=self["specs"],
            address=self["address"],
            url=self["url"],
        )

    def markdown(self) -> str:
        return (
            "**[{source}] {title}**"
            "\n"
            "**{price}** - {specs}"
            "\n\n"
            "Endereço: _{address}_"
            "\n\n"
            "{url}"
        ).format(
            source=self["source"],
            title=self["title"],
            price=self["price"],
            specs=self["specs"],
            address=self["address"],
            url=self["url"],
        )
