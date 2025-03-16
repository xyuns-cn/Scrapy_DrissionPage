"""
Pytest配置文件
"""

import os
import pytest
from scrapy.settings import Settings

# 导入需要测试的模块
from scrapy_drissionpage import DrissionSpider
from scrapy_drissionpage.browser_manager import BrowserManager
from scrapy_drissionpage.request import DrissionRequest
from scrapy_drissionpage.response import DrissionResponse


@pytest.fixture
def settings():
    """提供测试用的Scrapy设置"""
    settings = Settings()
    settings.set('DRISSIONPAGE_ENABLED', True)
    settings.set('DRISSIONPAGE_HEADLESS', True)
    settings.set('DRISSIONPAGE_BROWSER_PATH', None)
    settings.set('DRISSIONPAGE_INIT_MODE', 'new')
    return settings


@pytest.fixture
def mock_browser_manager(monkeypatch):
    """提供模拟的浏览器管理器"""
    from unittest.mock import MagicMock
    
    # 创建模拟对象
    mock_browser = MagicMock()
    mock_tab = MagicMock()
    mock_browser.latest_tab = mock_tab
    mock_browser.new_tab.return_value = MagicMock()
    
    # 模拟BrowserManager.get_browser方法
    def mock_get_browser(*args, **kwargs):
        return mock_browser
    
    # 应用模拟
    monkeypatch.setattr(BrowserManager, 'get_browser', mock_get_browser)
    
    return mock_browser


@pytest.fixture
def spider(settings, mock_browser_manager):
    """提供测试用的爬虫实例"""
    spider = DrissionSpider(name='test_spider')
    spider.settings = settings
    return spider


@pytest.fixture
def request_obj():
    """提供测试用的DrissionRequest实例"""
    return DrissionRequest(
        url='https://example.com',
        callback=lambda x: x,
        page_type='chromium'
    )


@pytest.fixture
def response_obj(request_obj):
    """提供测试用的DrissionResponse实例"""
    from unittest.mock import MagicMock
    
    # 创建模拟的页面对象
    mock_page = MagicMock()
    mock_page.url = 'https://example.com'
    mock_page.html = '<html><body><h1>Example</h1></body></html>'
    
    return DrissionResponse(
        url='https://example.com',
        body=mock_page.html.encode('utf-8'),
        request=request_obj,
        page=mock_page
    ) 