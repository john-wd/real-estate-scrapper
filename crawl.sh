#!/bin/bash

cd $(dirname $0)
source ./venv/bin/activate
scrapy crawl olx &
scrapy crawl zapimoveis &
wait
