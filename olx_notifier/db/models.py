import scrapy
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from .connection import engine

BaseModel = declarative_base()


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
            "R$ {price} - {specs}"
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
            "<h1>[{source}] {title}</h2>"
            "<br/>"
            "<b>R$ {price}</b> - {specs}"
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
            "*[{source}] {title}*"
            "\n"
            "R$ *{price}* - {specs}"
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


class AdModel(BaseModel):
    __tablename__ = "ads"

    pk = Column(Integer, primary_key=True)
    ad_id = Column(String)
    source = Column(String(32))
    title = Column(String(256))
    price = Column(Float)
    specs = Column(String(512))
    address = Column(String(256))
    date_published = Column(DateTime)
    date_collected = Column(DateTime)
    url = Column(String(1024))

    def __init__(
        self,
        ad_id=None,
        source=None,
        title=None,
        price=None,
        specs=None,
        address=None,
        date_published=None,
        date_collected=None,
        url=None,
    ):
        self.ad_id = ad_id
        self.source = source
        self.title = title
        self.price = price
        self.specs = specs
        self.address = address
        self.date_published = date_published
        self.date_collected = date_collected
        self.url = url

    @classmethod
    def from_item(cls, item: scrapy.Item):
        return cls(
            ad_id=item["id"],
            source=item["source"],
            title=item["title"],
            specs=item["specs"],
            price=item["price"],
            address=item["address"],
            date_published=item["date_published"],
            date_collected=item["date_collected"],
            url=item["url"],
        )


BaseModel.metadata.create_all(engine)
