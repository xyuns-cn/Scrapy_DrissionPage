"""
DrissionResponse类 - 自定义的集成DrissionPage功能的响应类
"""

from typing import Optional, Any, Union, Dict, List, Callable, Tuple, Set
import logging
from scrapy.http import TextResponse
from DrissionPage import ChromiumPage, SessionPage


class DrissionResponse(TextResponse):
    """
    集成DrissionPage功能的Scrapy响应对象
    """

    def __init__(self, url, body, encoding=None, request=None, page=None):
        """
        初始化DrissionResponse
        
        参数:
            url (str): 响应URL
            body (bytes): 响应内容
            encoding (str): 编码方式
            request (Request): 请求对象
            page (ChromiumPage|SessionPage): 页面对象
        """
        super().__init__(url=url, body=body, encoding=encoding, request=request)
        self._page = page
        
    @property
    def page(self):
        """
        获取页面对象
        
        返回:
            页面对象(ChromiumPage或SessionPage)
        """
        return self._page
    
    def xpath(self, xpath, **kwargs):
        """
        使用XPath查找元素(利用DrissionPage的查找功能)
        
        参数:
            xpath (str): XPath表达式
            **kwargs: 其他参数
        
        返回:
            查找结果
        """
        if self._page is None:
            return super().xpath(xpath, **kwargs)
        
        return [self._create_selector(ele) for ele in self._page.eles(f'xpath:{xpath}')]
    
    def css(self, css_selector, **kwargs):
        """
        使用CSS选择器查找元素(利用DrissionPage的查找功能)
        
        参数:
            css_selector (str): CSS选择器
            **kwargs: 其他参数
        
        返回:
            查找结果
        """
        if self._page is None:
            return super().css(css_selector, **kwargs)
        
        return [self._create_selector(ele) for ele in self._page.eles(f'css:{css_selector}')]
    
    def ele(self, locator, timeout=None):
        """
        查找单个元素(新增功能)
        
        参数:
            locator: 定位符
            timeout: 超时时间
            
        返回:
            元素对象
        """
        if self._page is None:
            raise ValueError("页面对象不存在，无法使用此方法")
        
        return self._page.ele(locator, timeout=timeout)
    
    def eles(self, locator, timeout=None):
        """
        查找多个元素(新增功能)
        
        参数:
            locator: 定位符
            timeout: 超时时间
            
        返回:
            元素列表
        """
        if self._page is None:
            raise ValueError("页面对象不存在，无法使用此方法")
        
        return self._page.eles(locator, timeout=timeout)
    
    def s_ele(self, locator):
        """
        使用静态方式查找单个元素(新增功能)
        
        参数:
            locator: 定位符
            
        返回:
            静态元素对象
        """
        if self._page is None:
            raise ValueError("页面对象不存在，无法使用此方法")
        
        return self._page.s_ele(locator)
    
    def s_eles(self, locator):
        """
        使用静态方式查找多个元素(新增功能)
        
        参数:
            locator: 定位符
            
        返回:
            静态元素列表
        """
        if self._page is None:
            raise ValueError("页面对象不存在，无法使用此方法")
        
        return self._page.s_eles(locator)
    
    def _create_selector(self, element):
        """
        将DrissionPage元素转换为Scrapy选择器
        
        参数:
            element: DrissionPage元素
            
        返回:
            Scrapy选择器
        """
        from scrapy.selector import Selector
        return Selector(text=element.html)
    
    def follow(self, url, callback=None, **kwargs):
        """
        根据URL创建新请求
        
        参数:
            url (str): 要访问的URL
            callback (callable): 回调函数
            **kwargs: 其他参数
            
        返回:
            DrissionRequest
        """
        from .request import DrissionRequest
        
        # 获取页面类型
        page_type = self.request.meta.get('drission', {}).get('page_type', 'chromium')
        
        # 创建新请求
        return DrissionRequest(
            url=url,
            callback=callback,
            page_type=page_type,
            **kwargs
        )
    
    def screenshot(self, path=None, name=None, full_page=False):
        """
        截屏功能(利用DrissionPage 4.0的截屏功能)
        
        参数:
            path (str): 保存路径
            name (str): 文件名
            full_page (bool): 是否截取整个页面
            
        返回:
            截图保存路径或二进制数据
        """
        if self._page is None or not hasattr(self._page, 'screenshot'):
            raise ValueError("无法截图，当前响应对象不包含页面对象或页面对象不支持截图")
        
        return self._page.screenshot(path=path, name=name, full_page=full_page)
    
    def json(self):
        """
        解析JSON响应内容
        
        返回:
            解析后的JSON数据
        """
        if self._page is not None and hasattr(self._page, 'json'):
            return self._page.json
        return super().json()
    
    def click(self, selector: str, timeout: float = 10) -> bool:
        """
        点击元素
        
        参数:
            selector: 元素选择器
            timeout: 等待元素出现的超时时间
            
        返回:
            bool: 是否点击成功
        """
        if not self._page:
            self.logger.warning("页面对象不存在，无法执行点击操作")
            return False
        
        try:
            element = self._page.ele(selector, timeout=timeout)
            element.click()
            return True
        except Exception as e:
            self.logger.error(f"点击元素失败: {e}")
            return False
    
    def input(self, selector: str, text: str, timeout: float = 10) -> bool:
        """
        输入文本
        
        参数:
            selector: 元素选择器
            text: 要输入的文本
            timeout: 等待元素出现的超时时间
            
        返回:
            bool: 是否输入成功
        """
        if not self._page:
            self.logger.warning("页面对象不存在，无法执行输入操作")
            return False
        
        try:
            element = self._page.ele(selector, timeout=timeout)
            element.input(text)
            return True
        except Exception as e:
            self.logger.error(f"输入文本失败: {e}")
            return False
    
    def scroll(self, selector: str = None, direction: str = 'down', distance: int = None) -> bool:
        """
        滚动页面或元素
        
        参数:
            selector: 元素选择器，None表示滚动整个页面
            direction: 滚动方向，'up', 'down', 'left', 'right'
            distance: 滚动距离，None表示自动
            
        返回:
            bool: 是否滚动成功
        """
        if not self._page:
            self.logger.warning("页面对象不存在，无法执行滚动操作")
            return False
        
        try:
            # 滚动整个页面
            if selector is None:
                if direction == 'down':
                    self._page.scroll.to_bottom(smooth=True)
                elif direction == 'up':
                    self._page.scroll.to_top(smooth=True)
                elif direction in ('left', 'right'):
                    # 处理水平滚动
                    distance = distance or 300
                    self._page.scroll.by(
                        x=distance if direction == 'right' else -distance, 
                        y=0
                    )
            # 滚动特定元素
            else:
                element = self._page.ele(selector)
                if direction == 'down':
                    element.scroll.to_bottom(smooth=True)
                elif direction == 'up':
                    element.scroll.to_top(smooth=True)
                elif direction in ('left', 'right'):
                    distance = distance or 100
                    element.scroll.by(
                        x=distance if direction == 'right' else -distance, 
                        y=0
                    )
            return True
        except Exception as e:
            self.logger.error(f"滚动操作失败: {e}")
            return False
    
    def wait(self, time: float) -> 'DrissionResponse':
        """
        等待指定时间
        
        参数:
            time: 等待时间(秒)
            
        返回:
            DrissionResponse: 响应对象自身
        """
        if not self._page:
            self.logger.warning("页面对象不存在，无法执行等待操作")
            return self
        
        try:
            self._page.wait.time(time)
        except Exception as e:
            self.logger.error(f"等待操作失败: {e}")
        
        return self
    
    def refresh(self) -> 'DrissionResponse':
        """
        刷新页面
        
        返回:
            DrissionResponse: 响应对象自身
        """
        if not self._page:
            self.logger.warning("页面对象不存在，无法执行刷新操作")
            return self
        
        try:
            self._page.refresh()
        except Exception as e:
            self.logger.error(f"刷新页面失败: {e}")
        
        return self
    
    def execute_script(self, script: str, *args: Any) -> Any:
        """
        执行JavaScript脚本
        
        参数:
            script: JavaScript脚本
            *args: 脚本参数
            
        返回:
            Any: 脚本执行结果
        """
        if not self._page or not self._is_chromium:
            self.logger.warning("页面对象不存在或不是ChromiumPage，无法执行JavaScript脚本")
            return None
        
        try:
            return self._page.run_js(script, *args)
        except Exception as e:
            self.logger.error(f"执行JavaScript脚本失败: {e}")
            return None
    
    def __str__(self) -> str:
        """返回响应的字符串表示"""
        page_type = 'chromium' if self._is_chromium else 'session' if self._is_session else 'unknown'
        return f"<DrissionResponse {self.status} {self.url} [{page_type}]>"
    
    __repr__ = __str__ 