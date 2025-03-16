"""
模式切换工具 - 提供在DrissionPage的d模式和s模式之间切换的工具
"""

from typing import Union, Optional
import logging
from DrissionPage import ChromiumPage, SessionPage


class ModeSwitcher:
    """
    模式切换工具类
    
    提供在DrissionPage的d模式和s模式之间切换的工具方法
    """
    
    logger = logging.getLogger(__name__)
    
    @staticmethod
    def to_session(page: ChromiumPage) -> SessionPage:
        """
        将ChromiumPage转换为SessionPage
        
        参数:
            page: ChromiumPage实例
            
        返回:
            SessionPage: 转换后的SessionPage实例
        """
        if not isinstance(page, ChromiumPage):
            ModeSwitcher.logger.error("输入参数必须是ChromiumPage实例")
            raise TypeError("输入参数必须是ChromiumPage实例")
        
        try:
            # 如果页面已经是s模式，直接返回
            if hasattr(page, 'mode') and page.mode == 's':
                return page
            
            # 使用内置方法切换到s模式
            if hasattr(page, 'change_mode'):
                page.change_mode('s')
                ModeSwitcher.logger.info(f"已使用内置方法将 {page.url} 切换到s模式")
                return page
            
            # 创建新的SessionPage，继承cookies
            cookies = page.cookies
            session = SessionPage()
            
            # 设置cookies
            for cookie in cookies:
                session.set.cookies(cookie)
            
            # 访问相同的URL
            current_url = page.url
            session.get(current_url)
            
            ModeSwitcher.logger.info(f"已手动将 {current_url} 从d模式切换到s模式")
            return session
            
        except Exception as e:
            ModeSwitcher.logger.error(f"模式切换失败: {e}")
            raise
    
    @staticmethod
    def to_chromium(page: SessionPage, browser: Optional[ChromiumPage] = None) -> ChromiumPage:
        """
        将SessionPage转换为ChromiumPage
        
        参数:
            page: SessionPage实例
            browser: 可选的ChromiumPage实例，用于创建新标签页
            
        返回:
            ChromiumPage: 转换后的ChromiumPage实例
        """
        if not isinstance(page, SessionPage):
            ModeSwitcher.logger.error("输入参数必须是SessionPage实例")
            raise TypeError("输入参数必须是SessionPage实例")
        
        try:
            # 如果页面已经是d模式，直接返回
            if hasattr(page, 'mode') and page.mode == 'd':
                return page
            
            # 使用内置方法切换到d模式
            if hasattr(page, 'change_mode'):
                page.change_mode('d')
                ModeSwitcher.logger.info(f"已使用内置方法将 {page.url} 切换到d模式")
                return page
            
            # 创建新的浏览器标签页
            if browser is None:
                browser = ChromiumPage()
                new_tab = browser.latest_tab
            else:
                new_tab = browser.new_tab()
            
            # 获取cookies
            cookies = page.cookies
            
            # 设置cookies
            for cookie in cookies:
                new_tab.set.cookies(cookie)
            
            # 访问相同的URL
            current_url = page.url
            new_tab.get(current_url)
            
            ModeSwitcher.logger.info(f"已手动将 {current_url} 从s模式切换到d模式")
            return new_tab
            
        except Exception as e:
            ModeSwitcher.logger.error(f"模式切换失败: {e}")
            raise 