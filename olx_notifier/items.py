# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OlxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    specs = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    date_published = scrapy.Field()
    date_collected = scrapy.Field()
    url = scrapy.Field()
