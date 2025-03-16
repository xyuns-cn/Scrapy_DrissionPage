"""
DrissionSpider测试
"""

import pytest
from unittest.mock import MagicMock, patch

from scrapy_drissionpage import DrissionSpider
from scrapy_drissionpage.request import DrissionRequest


class TestDrissionSpider:
    """DrissionSpider测试类"""
    
    def test_chromium_property(self, spider, mock_browser_manager):
        """测试chromium属性"""
        browser = spider.chromium
        assert browser is mock_browser_manager
    
    def test_current_tab_property(self, spider, mock_browser_manager):
        """测试current_tab属性"""
        tab = spider.current_tab
        assert tab is mock_browser_manager.latest_tab
    
    def test_new_tab_method(self, spider, mock_browser_manager):
        """测试new_tab方法"""
        tab = spider.new_tab()
        assert tab is not None
        mock_browser_manager.new_tab.assert_called_once()
    
    def test_drission_request_method(self, spider):
        """测试drission_request方法"""
        url = 'https://example.com'
        callback = spider.parse
        
        # 创建请求
        request = spider.drission_request(
            url=url,
            callback=callback,
            page_type='chromium'
        )
        
        # 验证请求属性
        assert isinstance(request, DrissionRequest)
        assert request.url == url
        assert request.callback == callback
        assert request.meta['drission']['page_type'] == 'chromium'
    
    def test_set_proxy_method(self, spider, mock_browser_manager):
        """测试set_proxy方法"""
        proxy = 'http://proxy.example.com:8080'
        
        # 设置代理
        spider.set_proxy(proxy)
        
        # 验证代理设置
        assert spider._global_proxy == proxy
        mock_browser_manager.set_proxy.assert_called_once_with(proxy)
    
    def test_closed_method(self, spider):
        """测试closed方法"""
        # 模拟浏览器管理器
        mock_browser_manager = MagicMock()
        spider._browser_manager = mock_browser_manager
        
        # 调用closed方法
        spider.closed('finished')
        
        # 验证浏览器管理器已关闭
        mock_browser_manager.close.assert_called_once() 