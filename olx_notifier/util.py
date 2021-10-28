import re
from logging import getLogger

log = getLogger(__name__)


def parse_price(price: str) -> float:
    if not price:
        return

    try:
        price_regex = r"(?:R\$)?\s*([\d.,]+)"
        m = re.match(price_regex, price)

        # parse brazilian price into float format
        parsed = m[1].replace(".", "").replace(",", ".")
        return float(parsed)
    except Exception:
        log.warn("Could not parse price {price}.".format(price=price))
        return
