"""
DrissionSpider类 - 集成DrissionPage功能的Scrapy爬虫基类
"""

from scrapy import Spider
from scrapy.http import Request
from DrissionPage import ChromiumPage, SessionPage

from .request import DrissionRequest
from .browser_manager import BrowserManager


class DrissionSpider(Spider):
    """
    集成DrissionPage功能的Scrapy爬虫基类
    提供浏览器和会话管理、模式切换等增强功能
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 确保中间件启用
        if 'DOWNLOADER_MIDDLEWARES' not in self.settings:
            self.settings['DOWNLOADER_MIDDLEWARES'] = {}
        if 'scrapy_drissionpage.middleware.DrissionPageMiddleware' not in self.settings['DOWNLOADER_MIDDLEWARES']:
            self.settings['DOWNLOADER_MIDDLEWARES']['scrapy_drissionpage.middleware.DrissionPageMiddleware'] = 543
        
        # 初始化浏览器管理器
        self._browser_manager = BrowserManager(self.settings)
        self._global_proxy = None
    
    @property
    def chromium(self):
        """获取浏览器实例"""
        return self._browser_manager.get_browser()
    
    @property
    def session(self):
        """获取会话实例(新增属性)"""
        return self._browser_manager.get_session()
    
    @property
    def current_tab(self):
        """获取当前标签页"""
        return self.chromium.latest_tab
    
    def new_tab(self, url=None, background=False, new_window=False, new_context=False):
        """
        创建新标签页并返回(利用4.0新特性)
        
        参数:
            url: 新标签页要访问的URL
            background: 是否在后台打开
            new_window: 是否创建新窗口
            new_context: 是否创建新的上下文(隐身窗口)
        
        返回:
            新标签页对象
        """
        tab = self.chromium.new_tab(
            background=background, 
            new_window=new_window, 
            new_context=new_context
        )
        if url:
            tab.get(url)
        return tab
    
    def get_tab(self, id_or_num):
        """
        获取标签页对象
        
        参数:
            id_or_num: 标签页ID或序号(从0开始)
        
        返回:
            标签页对象
        """
        return self.chromium.get_tab(id_or_num)
    
    def drission_request(self, url, callback=None, page_type='chromium', 
                         timeout=None, load_mode=None, wait_time=None, wait_element=None,
                         **kwargs):
        """
        创建DrissionRequest对象
        
        参数:
            url (str): 请求URL
            callback (callable): 回调函数
            page_type (str): 页面类型，'chromium'或'session'
            timeout (int): 请求超时时间
            load_mode (str): 加载模式，'normal'、'eager'或'none'
            wait_time (float): 加载后等待时间(秒)
            wait_element (str): 等待特定元素出现
            **kwargs: 其他参数
        
        返回:
            DrissionRequest: 自定义请求对象
        """
        # 如果设置了全局代理且未指定特定代理，使用全局代理
        if self._global_proxy and 'proxy' not in kwargs:
            kwargs['proxy'] = self._global_proxy
            
        # 创建DrissionRequest
        return DrissionRequest(
            url=url,
            callback=callback or self.parse,
            page_type=page_type,
            timeout=timeout,
            load_mode=load_mode,
            wait_time=wait_time,
            wait_element=wait_element,
            **kwargs
        )
    
    def set_proxy(self, proxy):
        """
        设置全局代理
        
        参数:
            proxy (str): 代理地址，如'http://proxy.example.com:8080'，None表示清除代理
        """
        self._global_proxy = proxy
        # 同时设置浏览器和会话的代理
        self._browser_manager.set_proxy(proxy)
    
    def listen_packets(self, pattern, tab=None):
        """
        启动数据包监听(新增功能，利用4.0的监听特性)
        
        参数:
            pattern: 匹配模式
            tab: 指定标签页，默认为当前标签页
        
        返回:
            监听器对象
        """
        tab = tab or self.current_tab
        tab.listen.start(pattern)
        return tab.listen
    
    def wait_packet(self, pattern=None, timeout=None, tab=None):
        """
        等待数据包(新增功能)
        
        参数:
            pattern: 匹配模式
            timeout: 超时时间
            tab: 指定标签页，默认为当前标签页
        
        返回:
            数据包对象
        """
        tab = tab or self.current_tab
        return tab.listen.wait(pattern=pattern, timeout=timeout)
    
    def set_download_path(self, path, tab=None):
        """
        设置下载路径(新增功能)
        
        参数:
            path: 下载路径
            tab: 指定标签页，默认为当前标签页
        """
        tab = tab or self.current_tab
        tab.set.download_path(path)
    
    def set_download_file_name(self, name, tab=None):
        """
        设置下载文件名(新增功能)
        
        参数:
            name: 文件名
            tab: 指定标签页，默认为当前标签页
        """
        tab = tab or self.current_tab
        tab.set.download_file_name(name)
    
    def wait_download_begin(self, timeout=None, tab=None):
        """
        等待下载开始(新增功能)
        
        参数:
            timeout: 超时时间
            tab: 指定标签页，默认为当前标签页
        
        返回:
            下载任务对象
        """
        tab = tab or self.current_tab
        return tab.wait.download_begin(timeout=timeout)
    
    def closed(self, reason):
        """
        爬虫关闭时调用，清理资源
        
        参数:
            reason (str): 关闭原因
        """
        # 关闭浏览器管理器
        self._browser_manager.close()
        super().closed(reason) 