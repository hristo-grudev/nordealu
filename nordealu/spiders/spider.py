import scrapy

from scrapy.loader import ItemLoader

from ..items import NordealuItem
from itemloaders.processors import TakeFirst


class NordealuSpider(scrapy.Spider):
	name = 'nordealu'
	start_urls = ['https://www.nordea.lu/en/private/press-release-archive/']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class, "box-active")]')
		for post in post_links:
			url = post.xpath('.//a[@class="wrapper"]/@href').get()
			title = post.xpath('.//p[@class="title"]/text()').get()
			date = post.xpath('.//p[@class="date"]/text()').get()

			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		print(response, date)
		description = response.xpath('//div[@class="col-lg-9"]//text()[normalize-space() and not(ancestor::h1 | ancestor::span[contains(@class, "text-")])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=NordealuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
