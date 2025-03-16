"""
BrowserManager测试
"""

import pytest
from unittest.mock import MagicMock, patch

from scrapy_drissionpage.browser_manager import BrowserManager


class TestBrowserManager:
    """BrowserManager测试类"""
    
    @pytest.fixture
    def browser_manager(self, settings):
        """创建BrowserManager实例"""
        return BrowserManager(settings)
    
    @patch('scrapy_drissionpage.browser_manager.ChromiumPage')
    def test_get_browser_new_mode(self, mock_chromium_page, browser_manager, settings):
        """测试获取浏览器(new模式)"""
        # 设置为new模式
        settings.set('DRISSIONPAGE_INIT_MODE', 'new')
        
        # 第一次调用应该创建新的浏览器实例
        browser = browser_manager.get_browser()
        assert browser is not None
        mock_chromium_page.assert_called_once()
        
        # 再次调用应该返回已创建的实例
        mock_chromium_page.reset_mock()
        browser_again = browser_manager.get_browser()
        assert browser_again is browser
        mock_chromium_page.assert_not_called()
    
    @patch('scrapy_drissionpage.browser_manager.ChromiumPage')
    def test_get_browser_connect_mode(self, mock_chromium_page, browser_manager, settings):
        """测试获取浏览器(connect模式)"""
        # 设置为connect模式
        settings.set('DRISSIONPAGE_INIT_MODE', 'connect')
        settings.set('DRISSIONPAGE_CONNECT_HOST', '127.0.0.1')
        settings.set('DRISSIONPAGE_CONNECT_PORT', 9222)
        
        # 调用获取浏览器
        browser = browser_manager.get_browser()
        assert browser is not None
        mock_chromium_page.assert_called_once()
    
    @patch('scrapy_drissionpage.browser_manager.SessionPage')
    def test_get_session(self, mock_session_page, browser_manager):
        """测试获取会话"""
        # 第一次调用应该创建新的会话实例
        session = browser_manager.get_session()
        assert session is not None
        mock_session_page.assert_called_once()
        
        # 再次调用应该返回已创建的实例
        mock_session_page.reset_mock()
        session_again = browser_manager.get_session()
        assert session_again is session
        mock_session_page.assert_not_called()
    
    def test_close(self, browser_manager):
        """测试关闭方法"""
        # 模拟浏览器和会话
        mock_browser = MagicMock()
        mock_session = MagicMock()
        
        browser_manager._browser = mock_browser
        browser_manager._session = mock_session
        
        # 设置为关闭时退出
        browser_manager.settings.set('DRISSIONPAGE_QUIT_ON_CLOSE', True)
        browser_manager.settings.set('DRISSIONPAGE_QUIT_SESSION_ON_CLOSE', True)
        
        # 调用关闭方法
        browser_manager.close()
        
        # 验证浏览器和会话都已关闭
        mock_browser.quit.assert_called_once()
        mock_session.close.assert_called_once()
        assert browser_manager._browser is None
        assert browser_manager._session is None 