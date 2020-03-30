import scrapy

from datetime import datetime, date, timedelta

from ..items import CountryItem


class CovidSpider(scrapy.Spider):
    pass
    name = "covid-spider"
    start_urls = ["https://www.worldometers.info/coronavirus/#countries"]

    def parse(self, response):
        table = response.xpath('//tbody//tr')
        count_not_found_link = 0
        for row in table:
            link = row.xpath('td[1]//a/@href').extract_first()
            if not link:
                self.process_empty_link(response)
                count_not_found_link += 1

            url = f"https://www.worldometers.info/coronavirus/{link}"
            yield scrapy.Request(url, callback=self.get_country_data)

    def process_empty_link(self, response):
        pass

    def get_country_data(self, response):
        items = CountryItem()
        items["country"] = response.xpath('//*[@id="page-top"]/text()[2]').extract_first()

        div = response.xpath('//div[@class="content-inner"]')
        for span in div:
            total_case = span.xpath('//*[@id="maincounter-wrap"][1]/div/span/text()').extract_first()
            death = span.xpath('//*[@id="maincounter-wrap"][2]/div/span/text()').extract_first()
            recovered = span.xpath('//*[@id="maincounter-wrap"][3]/div/span/text()').extract_first()

            items["total_cases"] = total_case
            items["death"] = death
            items["recovered"] = recovered

        row = response.xpath('//div[@class="content-inner"]//div[@class="row"]')
        for col in row:
            active_cases = col.xpath('//div[@class="col-md-6"][1]//div//div[2]//div[1]//div[1]//div[1]/text()').extract_first()
            closed_cases = col.xpath('//div[@class="col-md-6"][2]//div//div[2]//div[1]//div[1]//div[1]/text()').extract_first()

            items["active_case"] = active_cases
            items["closed_case"] = closed_cases

        items["last_updated"] = date.today()

        yield items
