"""
代理使用爬虫示例 - 展示如何在Scrapy-DrissionPage中使用代理
"""

from scrapy_drissionpage import DrissionSpider


class ProxyExampleSpider(DrissionSpider):
    """代理使用爬虫示例，演示如何设置和使用代理"""
    
    name = "proxy_example"
    
    def start_requests(self):
        """开始请求，演示代理使用"""
        # 注意: 请替换为您的实际代理地址
        proxy1 = 'http://your-proxy1.example.com:8080'
        proxy2 = 'http://your-proxy2.example.com:8080'
        
        # 设置全局代理
        self.set_proxy(proxy1)
        self.logger.info(f'设置全局代理: {proxy1}')
        
        # 使用全局代理发送请求
        yield self.drission_request(
            url="https://httpbin.org/ip",
            callback=self.parse_global_proxy
        )
        
        # 使用特定代理发送单个请求
        self.logger.info(f'使用特定代理: {proxy2}')
        yield self.drission_request(
            url="https://httpbin.org/ip",
            callback=self.parse_specific_proxy,
            proxy=proxy2
        )
    
    def parse_global_proxy(self, response):
        """解析全局代理响应"""
        ip_info = response.json()
        self.logger.info(f'全局代理IP信息: {ip_info}')
        yield {
            'proxy_type': 'global',
            'ip_info': ip_info
        }
    
    def parse_specific_proxy(self, response):
        """解析特定代理响应"""
        ip_info = response.json()
        self.logger.info(f'特定代理IP信息: {ip_info}')
        yield {
            'proxy_type': 'specific',
            'ip_info': ip_info
        } 