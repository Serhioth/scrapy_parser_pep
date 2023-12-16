from typing import Iterable

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name: str = 'pep'
    allowed_domains: list = ['peps.python.org']
    start_urls: list = ['https://peps.python.org/']

    def parse(
        self, response: scrapy.http.response
    ) -> Iterable[scrapy.Request]:
        pep_links = response.xpath(
            '//table[@class="pep-zero-table docutils align-default"]'
            '/tbody/tr/td/a[@class="pep reference internal"]/@href'
        ).getall()

        for pep_link in pep_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response: scrapy.http.response) -> PepParseItem:
        pep_content = response.xpath('//section[@id="pep-content"]')
        page_title = pep_content.xpath('h1[@class="page-title"]/text()').get()
        dl_tag = pep_content.xpath('dl[@class="rfc2822 field-list simple"]')
        status_tag = dl_tag.xpath(
            "//dt[text()='Status']/following-sibling::dd[1]"
        )
        number, name = page_title.split(' – ')
        status = status_tag[0].xpath('abbr/text()').get()

        data = {
            'number': number,
            'name': name,
            'status': status
        }

        yield PepParseItem(data)
