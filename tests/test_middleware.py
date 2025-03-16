"""
DrissionPageMiddleware测试
"""

import pytest
from unittest.mock import MagicMock, patch

from scrapy import signals
from scrapy.http import Request
from scrapy.crawler import Crawler

from scrapy_drissionpage.middleware import DrissionPageMiddleware
from scrapy_drissionpage.request import DrissionRequest
from scrapy_drissionpage.response import DrissionResponse


class TestDrissionPageMiddleware:
    """DrissionPageMiddleware测试类"""
    
    @pytest.fixture
    def middleware(self):
        """创建中间件实例"""
        return DrissionPageMiddleware()
    
    @pytest.fixture
    def crawler(self):
        """创建模拟的Crawler实例"""
        crawler = MagicMock(spec=Crawler)
        crawler.signals = MagicMock()
        crawler.signals.connect = MagicMock()
        return crawler
    
    def test_from_crawler(self, crawler):
        """测试from_crawler方法"""
        middleware = DrissionPageMiddleware.from_crawler(crawler)
        
        # 验证信号连接
        assert crawler.signals.connect.call_count == 2
        
        # 验证返回的是正确的实例
        assert isinstance(middleware, DrissionPageMiddleware)
    
    def test_process_request_normal_request(self, middleware):
        """测试处理普通请求"""
        # 创建普通请求
        request = Request(url='https://example.com')
        
        # 处理请求
        result = middleware.process_request(request, MagicMock())
        
        # 验证返回None，表示交给其他下载器处理
        assert result is None
    
    @patch('scrapy_drissionpage.middleware.DrissionResponse')
    def test_process_request_drission_request(self, mock_response, middleware, spider):
        """测试处理DrissionRequest"""
        # 模拟页面和响应
        mock_tab = MagicMock()
        mock_tab.url = 'https://example.com'
        mock_tab.html = '<html><body>Test</body></html>'
        
        mock_browser_manager = MagicMock()
        mock_browser_manager.get_browser.return_value.latest_tab = mock_tab
        
        # 创建DrissionRequest
        request = DrissionRequest(
            url='https://example.com',
            callback=spider.parse,
            page_type='chromium'
        )
        
        # 模拟_get_browser_manager方法
        middleware._get_browser_manager = MagicMock(return_value=mock_browser_manager)
        
        # 创建模拟响应
        mock_response_instance = MagicMock(spec=DrissionResponse)
        mock_response.return_value = mock_response_instance
        
        # 处理请求
        result = middleware.process_request(request, spider)
        
        # 验证返回了正确的响应
        assert result is mock_response_instance
        
        # 验证浏览器访问了正确的URL
        mock_tab.get.assert_called_once_with('https://example.com')
    
    def test_get_browser_manager(self, middleware, spider):
        """测试_get_browser_manager方法"""
        # 第一种情况：爬虫已有浏览器管理器
        mock_browser_manager = MagicMock()
        spider._browser_manager = mock_browser_manager
        
        # 获取浏览器管理器
        result = middleware._get_browser_manager(spider)
        
        # 验证返回了爬虫的浏览器管理器
        assert result is mock_browser_manager
        
        # 第二种情况：爬虫没有浏览器管理器，中间件缓存中有
        delattr(spider, '_browser_manager')
        middleware.browser_managers[spider.name] = mock_browser_manager
        
        # 获取浏览器管理器
        result = middleware._get_browser_manager(spider)
        
        # 验证返回了缓存中的浏览器管理器
        assert result is mock_browser_manager
    
    def test_spider_closed(self, middleware, spider):
        """测试spider_closed方法"""
        # 模拟浏览器管理器
        mock_browser_manager = MagicMock()
        middleware.browser_managers[spider.name] = mock_browser_manager
        
        # 调用spider_closed方法
        middleware.spider_closed(spider)
        
        # 验证浏览器管理器已关闭
        mock_browser_manager.close.assert_called_once()
        
        # 验证已从缓存中删除
        assert spider.name not in middleware.browser_managers 