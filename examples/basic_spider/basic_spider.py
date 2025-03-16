"""
基础爬虫示例 - 展示Scrapy-DrissionPage的基本用法
"""

from scrapy_drissionpage import DrissionSpider


class BasicExampleSpider(DrissionSpider):
    """基础爬虫示例，爬取quotes.toscrape.com的名言"""
    
    name = "basic_example"
    start_urls = ["https://quotes.toscrape.com/"]
    
    def parse(self, response):
        """解析响应，提取名言数据"""
        # 使用Scrapy选择器提取数据
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            
        # 获取下一页链接
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse) 