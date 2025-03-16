"""
工具模块测试
"""

import pytest
from unittest.mock import MagicMock, patch

from scrapy_drissionpage.utils.mode_switcher import ModeSwitcher
from scrapy_drissionpage.utils.selector import EnhancedSelector


class TestModeSwitcher:
    """ModeSwitcher测试类"""
    
    @patch('scrapy_drissionpage.utils.mode_switcher.SessionPage')
    def test_to_session(self, mock_session_page):
        """测试to_session方法"""
        # 创建模拟的ChromiumPage
        mock_chromium_page = MagicMock()
        mock_chromium_page.url = 'https://example.com'
        mock_chromium_page.cookies = [{'name': 'test', 'value': 'value'}]
        
        # 模拟change_mode方法
        mock_chromium_page.change_mode = MagicMock()
        mock_chromium_page.mode = 'd'
        
        # 测试使用内置方法切换模式
        result = ModeSwitcher.to_session(mock_chromium_page)
        
        # 验证结果
        mock_chromium_page.change_mode.assert_called_once_with('s')
        assert result is mock_chromium_page
    
    @patch('scrapy_drissionpage.utils.mode_switcher.ChromiumPage')
    def test_to_chromium(self, mock_chromium_page):
        """测试to_chromium方法"""
        # 创建模拟的SessionPage
        mock_session_page = MagicMock()
        mock_session_page.url = 'https://example.com'
        mock_session_page.cookies = [{'name': 'test', 'value': 'value'}]
        
        # 模拟change_mode方法
        mock_session_page.change_mode = MagicMock()
        mock_session_page.mode = 's'
        
        # 测试使用内置方法切换模式
        result = ModeSwitcher.to_chromium(mock_session_page)
        
        # 验证结果
        mock_session_page.change_mode.assert_called_once_with('d')
        assert result is mock_session_page


class TestEnhancedSelector:
    """EnhancedSelector测试类"""
    
    def test_css_with_page(self):
        """测试使用页面对象的css方法"""
        # 创建模拟的页面对象
        mock_page = MagicMock()
        mock_page.eles.return_value = ['element1', 'element2']
        
        # 创建选择器
        selector = EnhancedSelector(mock_page)
        
        # 调用css方法
        result = selector.css('div.test')
        
        # 验证结果
        mock_page.eles.assert_called_once_with('css:div.test')
        assert result == ['element1', 'element2']
    
    @patch('scrapy_drissionpage.utils.selector.Selector')
    def test_css_with_html(self, mock_selector_class):
        """测试使用HTML内容的css方法"""
        # 创建模拟的Scrapy选择器
        mock_selector = MagicMock()
        mock_selector_class.return_value = mock_selector
        
        mock_selector_list = MagicMock()
        mock_selector_list.__iter__.return_value = [MagicMock(), MagicMock()]
        mock_selector.css.return_value = mock_selector_list
        
        # 创建选择器
        selector = EnhancedSelector()
        
        # 调用css方法
        result = selector.css('div.test', html='<html><div class="test">Test</div></html>')
        
        # 验证结果
        mock_selector.css.assert_called_once_with('div.test')
        assert len(result) == 2 