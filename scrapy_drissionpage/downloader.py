"""
DrissionPageDownloader类 - 自定义下载器，处理DrissionRequest请求
"""

from scrapy.core.downloader import Downloader
from twisted.internet import defer

from .request import DrissionRequest
from .middleware import DrissionPageMiddleware


class DrissionPageDownloader(Downloader):
    """
    自定义下载器，处理DrissionRequest请求
    
    扩展了Scrapy的Downloader类，添加了对DrissionRequest的特殊处理
    """
    
    def __init__(self, crawler):
        """
        初始化下载器
        
        参数:
            crawler (Crawler): Scrapy crawler对象
        """
        super().__init__(crawler)
        self.drission_middleware = DrissionPageMiddleware.from_crawler(crawler)
    
    @defer.inlineCallbacks
    def fetch(self, request, spider):
        """
        获取请求的响应
        
        参数:
            request (Request): 请求对象
            spider (Spider): 爬虫实例
            
        返回:
            Response: 响应对象
        """
        # 如果是DrissionRequest，使用DrissionPageMiddleware处理
        if isinstance(request, DrissionRequest):
            response = self.drission_middleware.process_request(request, spider)
            if response:
                defer.returnValue(response)
        
        # 否则使用默认下载器处理
        response = yield super().fetch(request, spider)
        defer.returnValue(response) 