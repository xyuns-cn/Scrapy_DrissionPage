"""
登录爬虫示例 - 展示如何使用Scrapy-DrissionPage处理登录
"""

from scrapy_drissionpage import DrissionSpider


class LoginExampleSpider(DrissionSpider):
    """登录爬虫示例，演示如何处理登录表单"""
    
    name = "login_example"
    
    # 自定义设置
    custom_settings = {
        'DRISSIONPAGE_HEADLESS': False,  # 显示浏览器界面，便于观察
    }
    
    def start_requests(self):
        """开始请求，处理登录流程"""
        # 获取当前标签页
        tab = self.current_tab
        
        # 访问登录页面
        tab.get('https://quotes.toscrape.com/login')
        
        # 填写登录表单
        tab.ele('input[name="username"]').input('user')
        tab.ele('input[name="password"]').input('password')
        
        # 提交表单
        tab.ele('input[type="submit"]').click()
        
        # 等待页面加载完成
        tab.wait.load_complete()
        
        # 创建请求
        yield self.drission_request(
            url=tab.url,
            callback=self.parse,
            dont_filter=True
        )
    
    def parse(self, response):
        """解析响应，验证登录状态并提取数据"""
        # 检查是否登录成功
        if 'Logout' in response.text:
            self.logger.info('登录成功')
            
            # 提取数据
            for quote in response.css('div.quote'):
                yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall(),
                }
        else:
            self.logger.error('登录失败') 