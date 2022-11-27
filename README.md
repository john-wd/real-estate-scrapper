# Real estate ad scrapper and notifier

This quick and simple scrapy application crawls some well known real estate websites to fetch new listings and notify me through a Telegram bot so I can track fresh deals that may arise.

It is supposed to be scheduled in a cronjob to run with some recurrence.

As of now, it has the following spiders implemented:

- OLX: general product listing; since it works by given a query ID, you can track any kind of products listed in the website
- Vivareal
- Zapimoveis

The last two are big real estate aggregators that contains listings for may different agencies throughout Brazil.

### External dependencies

The crawler works with selenium using the Firefox headless driver, so please install both `firefox` and `geckodriver` to your distro.

### Installation

First clone this repo and set up a new virtual environment

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dependencies

```bash
(venv) $ pip install -r requirements.txt
```

Create a custom [telegram bot](https://core.telegram.org/bots) and configure it in a [.env](/.env.example) file in the root of this repo.

Run the application

```bash
(venv) $ ./crawl.sh
```

### Configuring cronjob

[crawl.sh](/crawl.sh) is really an utility script that enters the virtualenv and runs the spiders configured in it, so you can just configure your crontab to invoke it.