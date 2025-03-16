"""
增强选择器 - 整合Scrapy选择器和DrissionPage元素定位功能
"""

from typing import Union, List, Optional, Any
import logging
from scrapy.selector import Selector, SelectorList
from DrissionPage import ChromiumPage, SessionPage, WebElement


class EnhancedSelector:
    """
    增强选择器类
    
    整合Scrapy选择器和DrissionPage元素定位功能
    """
    
    def __init__(self, page: Union[ChromiumPage, SessionPage, None] = None):
        """
        初始化增强选择器
        
        参数:
            page: DrissionPage页面对象
        """
        self.page = page
        self.logger = logging.getLogger(__name__)
    
    def css(self, selector: str, html: Optional[str] = None) -> List[WebElement]:
        """
        使用CSS选择器查找元素
        
        参数:
            selector: CSS选择器
            html: HTML内容，如果提供则使用该内容，否则使用页面内容
            
        返回:
            List[WebElement]: 元素列表
        """
        if not self.page and not html:
            self.logger.error("需要提供页面对象或HTML内容")
            return []
        
        try:
            if html:
                # 使用Scrapy选择器处理HTML内容
                scrapy_selector = Selector(text=html)
                elements = scrapy_selector.css(selector)
                return self._convert_to_elements(elements)
            else:
                # 使用DrissionPage的元素定位功能
                return self.page.eles(f'css:{selector}')
        except Exception as e:
            self.logger.error(f"CSS选择器查找失败: {e}")
            return []
    
    def xpath(self, selector: str, html: Optional[str] = None) -> List[WebElement]:
        """
        使用XPath选择器查找元素
        
        参数:
            selector: XPath选择器
            html: HTML内容，如果提供则使用该内容，否则使用页面内容
            
        返回:
            List[WebElement]: 元素列表
        """
        if not self.page and not html:
            self.logger.error("需要提供页面对象或HTML内容")
            return []
        
        try:
            if html:
                # 使用Scrapy选择器处理HTML内容
                scrapy_selector = Selector(text=html)
                elements = scrapy_selector.xpath(selector)
                return self._convert_to_elements(elements)
            else:
                # 使用DrissionPage的元素定位功能
                return self.page.eles(f'xpath:{selector}')
        except Exception as e:
            self.logger.error(f"XPath选择器查找失败: {e}")
            return []
    
    def regex(self, pattern: str, html: Optional[str] = None) -> List[str]:
        """
        使用正则表达式查找内容
        
        参数:
            pattern: 正则表达式模式
            html: HTML内容，如果提供则使用该内容，否则使用页面内容
            
        返回:
            List[str]: 匹配结果列表
        """
        import re
        
        if not self.page and not html:
            self.logger.error("需要提供页面对象或HTML内容")
            return []
        
        try:
            # 获取HTML内容
            content = html if html else self.page.html
            
            # 使用正则表达式查找
            matches = re.findall(pattern, content)
            return matches
        except Exception as e:
            self.logger.error(f"正则表达式查找失败: {e}")
            return []
    
    def _convert_to_elements(self, selector_list: SelectorList) -> List[WebElement]:
        """
        将Scrapy选择器列表转换为WebElement列表
        
        参数:
            selector_list: Scrapy选择器列表
            
        返回:
            List[WebElement]: WebElement列表
        """
        # 注意：这是一个不完整的实现，因为无法直接将Scrapy选择器转换为WebElement
        # 这里只是返回选择器的文本内容
        self.logger.warning("转换为WebElement的功能不完整，只返回文本内容")
        return [selector.get() for selector in selector_list] 