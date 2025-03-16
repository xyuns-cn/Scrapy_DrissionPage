"""
分页爬取示例 - 展示如何处理分页
"""

from scrapy_drissionpage import DrissionSpider


class PaginationExampleSpider(DrissionSpider):
    """分页爬取示例，演示如何处理网站分页"""
    
    name = "pagination_example"
    
    def start_requests(self):
        """开始请求"""
        # 获取当前标签页
        tab = self.current_tab
        
        # 访问目标网站
        tab.get('https://quotes.toscrape.com/')
        
        # 开始爬取第一页
        yield self.drission_request(
            url=tab.url,
            callback=self.parse,
            dont_filter=True
        )
    
    def parse(self, response):
        """解析响应，处理分页"""
        # 当前页码
        current_page = response.url.split('page=')[-1] if 'page=' in response.url else 1
        self.logger.info(f'正在爬取第 {current_page} 页')
        
        # 使用Scrapy选择器提取数据
        for quote in response.css('div.quote'):
            yield {
                'page': current_page,
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        # 获取下一页按钮
        next_button = response.page.ele('css:li.next > a', timeout=1)
        if next_button:
            # 点击下一页按钮
            self.logger.info('点击下一页按钮')
            next_button.click()
            response.page.wait.load_complete()
            
            # 创建下一页请求
            yield self.drission_request(
                url=response.page.url,
                callback=self.parse,
                dont_filter=True
            )
        else:
            self.logger.info('已到达最后一页') 