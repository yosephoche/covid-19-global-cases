import scrapy
import json
from ..items import Covid19CrawlingItem

class CoronaSpider(scrapy.Spider):
    name = "corona"
    start_urls = [
        # "https://corona.lmao.ninja/all",
        "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/03-20-2020.csv"
    ]

    def parse(self, response):
        items = Covid19CrawlingItem()
        # json_response = json.loads(response.body)
        # print(json_response["cases"])
        th = response.xpath('//tr[@id="LC1"]//th/text()').get()
        for row in response.xpath('//tbody//tr[@class="js-file-line"]'):
            items["country_region"] = row.xpath('td[3]//text()').extract_first()
            items["province_state"] = row.xpath('td[2]//text()').extract_first()
            items["confirmed"] = row.xpath('td[5]//text()').extract_first()
            items["deaths"] = row.xpath('td[6]//text()').extract_first()
            items["recovered"] = row.xpath('td[7]//text()').extract_first()
            items["latitude"] = row.xpath('td[8]//text()').extract_first()
            items["longitude"] = row.xpath('td[9]//text()').extract_first()
            items["last_updated"] = row.xpath('td[4]//text()').extract_first()

            yield {
                "country_region": row.xpath('td[3]//text()').extract_first(),
                "province_state": row.xpath('td[2]//text()').extract_first(),
                "confirmed": row.xpath('td[5]//text()').extract_first(),
                "deaths": row.xpath('td[6]//text()').extract_first(),
                "recovered": row.xpath('td[7]//text()').extract_first(),
                "latitude": row.xpath('td[8]//text()').extract_first(),
                "longitude": row.xpath('td[9]//text()').extract_first(),
                "last_updated": row.xpath('td[4]//text()').extract_first(),
            }