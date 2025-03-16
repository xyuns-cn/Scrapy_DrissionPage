"""
DrissionRequest和DrissionResponse测试
"""

import pytest
from unittest.mock import MagicMock

from scrapy_drissionpage.request import DrissionRequest
from scrapy_drissionpage.response import DrissionResponse
from DrissionPage import ChromiumPage, SessionPage


class TestDrissionRequest:
    """DrissionRequest测试类"""
    
    def test_init(self):
        """测试初始化"""
        url = 'https://example.com'
        callback = lambda x: x
        
        # 创建请求
        request = DrissionRequest(
            url=url,
            callback=callback,
            page_type='chromium',
            wait_time=2,
            actions=[{'method': 'click', 'args': ['button']}],
            proxy='http://proxy.example.com:8080',
            browser_options={'headless': True},
            session_options={'timeout': 30}
        )
        
        # 验证基本属性
        assert request.url == url
        assert request.callback == callback
        
        # 验证meta中的drission配置
        drission_meta = request.meta['drission']
        assert drission_meta['page_type'] == 'chromium'
        assert drission_meta['wait_time'] == 2
        assert len(drission_meta['actions']) == 1
        assert drission_meta['proxy'] == 'http://proxy.example.com:8080'
        assert drission_meta['browser_options']['headless'] is True
        assert drission_meta['session_options']['timeout'] == 30


class TestDrissionResponse:
    """DrissionResponse测试类"""
    
    @pytest.fixture
    def mock_chromium_page(self):
        """创建模拟的ChromiumPage"""
        mock_page = MagicMock(spec=ChromiumPage)
        mock_page.url = 'https://example.com'
        mock_page.html = '<html><body><h1>Example</h1></body></html>'
        return mock_page
    
    @pytest.fixture
    def mock_session_page(self):
        """创建模拟的SessionPage"""
        mock_page = MagicMock(spec=SessionPage)
        mock_page.url = 'https://example.com'
        mock_page.html = '<html><body><h1>Example</h1></body></html>'
        return mock_page
    
    def test_init(self, request_obj, mock_chromium_page):
        """测试初始化"""
        # 创建响应
        response = DrissionResponse(
            url=mock_chromium_page.url,
            body=mock_chromium_page.html.encode('utf-8'),
            request=request_obj,
            page=mock_chromium_page
        )
        
        # 验证基本属性
        assert response.url == mock_chromium_page.url
        assert response.body == mock_chromium_page.html.encode('utf-8')
        assert response.request == request_obj
        assert response.page is mock_chromium_page
    
    def test_is_chromium(self, request_obj, mock_chromium_page, mock_session_page):
        """测试is_chromium属性"""
        # 创建ChromiumPage响应
        chromium_response = DrissionResponse(
            url=mock_chromium_page.url,
            body=mock_chromium_page.html.encode('utf-8'),
            request=request_obj,
            page=mock_chromium_page
        )
        
        # 创建SessionPage响应
        session_response = DrissionResponse(
            url=mock_session_page.url,
            body=mock_session_page.html.encode('utf-8'),
            request=request_obj,
            page=mock_session_page
        )
        
        # 验证is_chromium属性
        assert chromium_response.is_chromium is True
        assert session_response.is_chromium is False
    
    def test_is_session(self, request_obj, mock_chromium_page, mock_session_page):
        """测试is_session属性"""
        # 创建ChromiumPage响应
        chromium_response = DrissionResponse(
            url=mock_chromium_page.url,
            body=mock_chromium_page.html.encode('utf-8'),
            request=request_obj,
            page=mock_chromium_page
        )
        
        # 创建SessionPage响应
        session_response = DrissionResponse(
            url=mock_session_page.url,
            body=mock_session_page.html.encode('utf-8'),
            request=request_obj,
            page=mock_session_page
        )
        
        # 验证is_session属性
        assert chromium_response.is_session is False
        assert session_response.is_session is True
    
    def test_click(self, request_obj, mock_chromium_page):
        """测试click方法"""
        # 模拟元素
        mock_element = MagicMock()
        mock_element.click.return_value = True
        mock_chromium_page.ele.return_value = mock_element
        
        # 创建响应
        response = DrissionResponse(
            url=mock_chromium_page.url,
            body=mock_chromium_page.html.encode('utf-8'),
            request=request_obj,
            page=mock_chromium_page
        )
        
        # 调用click方法
        result = response.click('button')
        
        # 验证结果
        assert result is True
        mock_chromium_page.ele.assert_called_once_with('button')
        mock_element.click.assert_called_once()
    
    def test_input(self, request_obj, mock_chromium_page):
        """测试input方法"""
        # 模拟元素
        mock_element = MagicMock()
        mock_element.input.return_value = True
        mock_chromium_page.ele.return_value = mock_element
        
        # 创建响应
        response = DrissionResponse(
            url=mock_chromium_page.url,
            body=mock_chromium_page.html.encode('utf-8'),
            request=request_obj,
            page=mock_chromium_page
        )
        
        # 调用input方法
        result = response.input('input[name="username"]', 'testuser')
        
        # 验证结果
        assert result is True
        mock_chromium_page.ele.assert_called_once_with('input[name="username"]')
        mock_element.input.assert_called_once_with('testuser') 