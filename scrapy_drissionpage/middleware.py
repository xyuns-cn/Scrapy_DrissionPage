"""
DrissionPage 中间件 - 处理 DrissionRequest 请求
"""

import logging
from typing import Optional, Dict, Any, Union, Callable, TypeVar

from scrapy import signals
from scrapy.http import Request, Response
from scrapy.crawler import Crawler
from scrapy.spiders import Spider

from .browser_manager import BrowserManager
from .request import DrissionRequest
from .response import DrissionResponse

# 定义类型变量
SpiderType = TypeVar('SpiderType', bound=Spider)
ResponseType = TypeVar('ResponseType', bound=Response)


class DrissionPageMiddleware:
    """
    DrissionPage 中间件
    
    处理 DrissionRequest 请求，使用 DrissionPage 获取页面
    """
    
    def __init__(self):
        """初始化中间件"""
        # 存储每个爬虫的浏览器管理器
        self.browser_managers: Dict[str, BrowserManager] = {}
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler: Crawler) -> 'DrissionPageMiddleware':
        """
        从 Crawler 创建中间件
        
        参数:
            crawler: Crawler 实例
            
        返回:
            DrissionPageMiddleware: 中间件实例
        """
        # 创建中间件实例
        middleware = cls()
        
        # 注册信号处理器
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        
        return middleware
    
    def spider_opened(self, spider: SpiderType) -> None:
        """
        爬虫开启时调用
        
        参数:
            spider: 爬虫实例
        """
        self.logger.info(f"爬虫 {spider.name} 已开启")
    
    def spider_closed(self, spider: SpiderType) -> None:
        """
        爬虫关闭时调用
        
        参数:
            spider: 爬虫实例
        """
        # 关闭浏览器管理器
        if spider.name in self.browser_managers:
            self.logger.info(f"关闭爬虫 {spider.name} 的浏览器管理器")
            try:
                self.browser_managers[spider.name].close()
                del self.browser_managers[spider.name]
            except Exception as e:
                self.logger.error(f"关闭浏览器管理器时出错: {e}")
    
    def process_request(
        self, request: Request, spider: SpiderType
    ) -> Optional[Union[Request, ResponseType]]:
        """
        处理请求，利用DrissionPage 4.0新特性
        
        参数:
            request: 请求对象
            spider: 爬虫实例
            
        返回:
            None: 继续处理请求
            Response: 跳过下载器，直接返回响应
            Request: 替换原请求
        """
        # 只处理 DrissionRequest
        if not isinstance(request, DrissionRequest):
            return None
        
        self.logger.debug(f"处理 DrissionRequest: {request.url}")
        
        try:
            # 获取浏览器管理器
            browser_manager = self._get_browser_manager(spider)
            
            # 获取页面类型和配置
            drission_meta = request.meta.get('drission', {})
            page_type = drission_meta.get('page_type', 'chromium')
            load_mode = drission_meta.get('load_mode')
            wait_time = drission_meta.get('wait_time')
            wait_element = drission_meta.get('wait_element')
            timeout = drission_meta.get('timeout')
            
            # 设置代理
            if 'proxy' in request.meta:
                proxy = request.meta['proxy']
                self.logger.debug(f"为请求设置代理: {proxy}")
                browser_manager.set_proxy(proxy)
            
            # 根据页面类型获取页面
            if page_type == 'chromium':
                # 获取浏览器实例
                browser = browser_manager.get_browser()
                
                # 设置加载模式(如果指定)
                if load_mode:
                    if load_mode == 'eager':
                        browser.set.load_mode.eager()
                    elif load_mode == 'none':
                        browser.set.load_mode.none()
                    elif load_mode == 'normal':
                        browser.set.load_mode.normal()
                
                # 获取当前标签页
                page = browser.latest_tab
                
                # 访问URL
                page.get(request.url, timeout=timeout)
                
                # 等待处理
                if wait_time is not None:
                    page.wait(wait_time)
                
                # 等待特定元素出现(4.0新特性)
                if wait_element:
                    page.wait.ele_loaded(wait_element)
                    
            elif page_type == 'session':
                # 获取会话实例
                page = browser_manager.get_session()
                
                # 访问URL
                page.get(request.url, timeout=timeout)
            else:
                raise ValueError(f"不支持的页面类型: {page_type}")
            
            # 创建响应
            self.logger.debug(f"创建 DrissionResponse: {page.url}")
            return DrissionResponse(
                url=page.url,
                body=page.html.encode('utf-8'),
                request=request,
                page=page
            )
        except Exception as e:
            self.logger.error(f"处理 DrissionRequest 时出错: {e}", exc_info=True)
            # 重新抛出异常，让 Scrapy 处理
            raise
    
    def _get_browser_manager(self, spider: SpiderType) -> BrowserManager:
        """
        获取浏览器管理器
        
        参数:
            spider: 爬虫实例
            
        返回:
            BrowserManager: 浏览器管理器实例
        """
        # 如果爬虫已有浏览器管理器，直接使用
        if hasattr(spider, '_browser_manager'):
            return spider._browser_manager
        
        # 如果缓存中已有，直接返回
        if spider.name in self.browser_managers:
            return self.browser_managers[spider.name]
        
        # 创建新的浏览器管理器
        self.logger.info(f"为爬虫 {spider.name} 创建新的浏览器管理器")
        browser_manager = BrowserManager(spider.settings)
        self.browser_managers[spider.name] = browser_manager
        
        return browser_manager 