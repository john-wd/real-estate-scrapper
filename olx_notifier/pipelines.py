# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import List
from itemadapter import ItemAdapter
from sqlalchemy import desc
from datetime import datetime
from .notifier import BaseNotifier, TelegramNotifier

from .db.connection import db
from .db.models import AdModel, AdItem


class AdPipeline:
    item_cls = AdItem
    notifiers: List[BaseNotifier]

    def __init__(self, notifiers: List[BaseNotifier]):
        self.notifiers = notifiers

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            [TelegramNotifier.new(crawler.settings)],
        )

    def process_item(self, item, spider):
        existing = self.fetch_item(item)
        if existing:
            if item["price"] < existing.price:
                self.insert_item(item)
                self.notify(
                    (
                        "*Preço baixou!!*"
                        "\n"
                        "R${prev} -> *R${current}*"
                        "\n\n"
                        "{ad}"
                    ).format(
                        prev=existing.price,
                        current=item["price"],
                        ad=item.markdown(),
                    )
                )
        else:
            self.insert_item(item)
            self.notify(item.markdown())
        return item

    def notify(self, message):
        for notifier in self.notifiers:
            notifier.send_message(message, parse_mode="markdown")

    def insert_item(self, item: AdItem):
        record = AdModel.from_item(item)
        db.add(record)
        db.commit()

    def fetch_item(self, item: AdItem):
        return (
            db.query(AdModel)
            .filter_by(ad_id=item["id"], source=item["source"])
            .order_by(desc("date_collected"))
            .first()
        )
