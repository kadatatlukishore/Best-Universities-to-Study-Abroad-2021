import scrapy


class Wikispider(scrapy.Spider):
    name = 'wikibot'
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    ]

    def parse(self, response, **kwargs):
        table = response.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[2]/td[1]/table/tbody/tr')
        for rows in table:
            yield {
                'Countries': rows.xpath('td[2]/a/text()').extract_first(),
                'GDP(US$millions)': rows.xpath('td[3]/text()').extract_first()
            }