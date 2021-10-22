# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import OlxItem
from sqlalchemy.engine import Engine, create_engine
from datetime import datetime


class OlxPipeline:
    tablename = "scrapy_olx"
    item_cls = OlxItem
    sql_engine: Engine

    def __init__(self, eng: Engine):
        self.sql_engine = eng

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            create_engine(
                crawler.settings.get("DATABASE_URL", "sqlite3:///results.sqlite3"),
                echo=True,
            )
        )

    def open_spider(self, spider):
        self.init_table()

    def process_item(self, item, spider):
        self.insert_item(item)
        return item

    def init_table(self):
        stmt = "CREATE TABLE IF NOT EXISTS {table} ({fields});".format(
            table=self.tablename,
            fields=",".join(
                ["{x} TEXT".format(x=x) for x in self.item_cls.fields.keys()]
            ),
        )
        self.sql_engine.execute(stmt)

    def insert_item(self, item):
        fields = item.fields.keys()
        values = [process_field(item[k]) for k in fields]
        stmt = "INSERT INTO {table} ({keys}) VALUES ({vals});".format(
            table=self.tablename,
            keys=",".join(fields),
            vals=",".join(values),
        )
        self.sql_engine.execute(stmt)


def process_field(value):
    if isinstance(value, datetime):
        return quote(value.isoformat())
    elif isinstance(value, str):
        return quote(value)
    return value


def quote(value: str, single: bool = True) -> str:
    if single:
        return "'" + value + "'"
    return '"' + value + '"'
