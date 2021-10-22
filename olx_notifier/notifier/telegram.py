from telegram.ext import Updater
from telegram.ext.extbot import ExtBot
from telegram.error import RetryAfter
from time import sleep
from scrapy.settings import Settings
from .abstract import BaseNotifier
from logging import getLogger

log = getLogger(__name__)


class TelegramNotifier(BaseNotifier):
    _bot: ExtBot
    chat_id: str
    max_retries: int

    def __init__(
        self,
        bot: ExtBot,
        chat_id: str,
        max_retries: int = 5,
    ):
        self._bot = bot
        self.chat_id = chat_id
        self.max_retries = max_retries

    def send_message(self, message: str, retry: int = 0, **opts):
        try:
            self._bot.send_message(self.chat_id, text=message, **opts)
        except RetryAfter as e:
            if retry < self.max_retries:
                log.warn(
                    "Too many requests. Sending after {t}.".format(t=e.retry_after)
                )
                sleep(e.retry_after)
                self.send_message(message, retry + 1, **opts)
            else:
                log.error("Max attempts reached. Ignoring this message.")
                raise e

    @classmethod
    def new(cls, settings: Settings):
        updater = Updater(settings.get("TELEGRAM_BOT_ID"))
        return cls(
            updater.bot,
            settings.get("TELEGRAM_CHAT_ID"),
            settings.get("TELEGRAM_MAX_RETRIES", 5),
        )
