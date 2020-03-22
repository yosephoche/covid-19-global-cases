import scrapy
import json
import csv
import logging

from datetime import datetime, date, timedelta

from ..items import Covid19CrawlingItem, CountryItem

logger = logging.getLogger()


class CoronaSpider(scrapy.Spider):
    name = "corona"
    start_urls = [
        # "https://corona.lmao.ninja/all",
        # "https://corona.lmao.ninja/jhucsse",
        # "03-20-2020.csv",
        # "https://covid19.mathdro.id/api",

    ]
    url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    date_today = date.today()
    date_today = date_today.strftime("%m-%d-%Y")

    if date_today:
        start_urls.append(url + str(date_today) + ".csv")

    def parse(self, response):
        # TODO:
        #  [] Store data to database using postgres
        items = Covid19CrawlingItem()
        country_items = CountryItem()

        if response.status == 404:
            date_today = date.today() - timedelta(days=1)
            date_today = date_today.strftime("%m-%d-%Y")
            url = self.url + str(date_today) + ".csv"
            yield scrapy.Request(url, self.parse)

        th = response.xpath('//tr[@id="LC1"]//th/text()').get()
        table = response.xpath('//tbody//tr[@class="js-file-line"]')
        current_country = []
        for row in table:
            country = row.xpath('td[3]//text()').extract_first()

            if country not in current_country:
                country_items["country"] = country
                yield country_items
                current_country.append(country)
                logger.info('Crawled data from country %s', country)

            items["country"] = row.xpath('td[3]//text()').extract_first()
            items["province"] = row.xpath('td[2]//text()').extract_first()
            items["confirmed"] = row.xpath('td[5]//text()').extract_first()
            items["deaths"] = row.xpath('td[6]//text()').extract_first()
            items["recovered"] = row.xpath('td[7]//text()').extract_first()
            items["latitude"] = row.xpath('td[8]//text()').extract_first()
            items["longitude"] = row.xpath('td[9]//text()').extract_first()
            items["last_updated"] = row.xpath('td[4]//text()').extract_first()

            yield items
