"""
浏览器管理器 - 负责创建和管理浏览器实例
"""

import logging
from threading import RLock
from typing import Optional, Dict, Any

from DrissionPage import ChromiumPage, SessionPage


class BrowserManager:
    """
    浏览器管理器类
    
    负责创建和管理浏览器实例，支持共享浏览器和会话
    """
    
    def __init__(self, settings):
        """
        初始化浏览器管理器
        
        参数:
            settings: Scrapy设置对象
        """
        self.settings = settings
        self._browser = None
        self._session = None
        self._lock = RLock()  # 添加线程锁，确保线程安全
        self.logger = logging.getLogger(__name__)
    
    def get_browser(self) -> ChromiumPage:
        """
        获取浏览器实例
        
        如果浏览器实例不存在，则创建新的实例
        
        返回:
            ChromiumPage: 浏览器实例
        """
        with self._lock:  # 使用线程锁保护共享资源
            if self._browser is None:
                self.logger.info("创建新的浏览器实例")
                
                # 获取浏览器初始化模式
                init_mode = self.settings.get('DRISSIONPAGE_INIT_MODE', 'new')
                
                # 创建初始化选项
                browser_options = {}
                
                if init_mode == 'new':
                    # 浏览器路径和选项
                    browser_path = self.settings.get('DRISSIONPAGE_BROWSER_PATH')
                    if browser_path:
                        browser_options['browser_path'] = browser_path
                    
                    # 4.0版本的headless设置方式
                    headless = self.settings.get('DRISSIONPAGE_HEADLESS', True)
                    if headless:
                        browser_options['headless'] = headless
                    
                    # 隐身模式
                    incognito = self.settings.get('DRISSIONPAGE_INCOGNITO', False)
                    if incognito:
                        browser_options['incognito'] = incognito
                    
                    # Chrome选项
                    chrome_options = self.settings.get('DRISSIONPAGE_CHROME_OPTIONS', [])
                    if chrome_options:
                        browser_options['chrome_options'] = chrome_options
                    
                    # 设置下载路径(4.0新特性)
                    download_path = self.settings.get('DRISSIONPAGE_DOWNLOAD_PATH')
                    if download_path:
                        browser_options['download_path'] = download_path
                    
                    # 创建浏览器实例
                    try:
                        self._browser = ChromiumPage(**browser_options)
                        
                        # 设置加载模式(4.0新特性，替代page_load_strategy)
                        load_mode = self.settings.get('DRISSIONPAGE_LOAD_MODE', 'normal')
                        if load_mode == 'eager':
                            self._browser.set.load_mode.eager()
                        elif load_mode == 'none':
                            self._browser.set.load_mode.none()
                        
                        # 设置阻止URL(4.0新特性)
                        blocked_urls = self.settings.get('DRISSIONPAGE_BLOCKED_URLS')
                        if blocked_urls:
                            self._browser.set.blocked_urls(blocked_urls)
                            
                        # 设置超时时间
                        timeout = self.settings.get('DRISSIONPAGE_TIMEOUT')
                        if timeout:
                            self._browser.set.timeout(timeout)
                            
                        # 设置重试次数
                        retry_times = self.settings.get('DRISSIONPAGE_RETRY_TIMES')
                        if retry_times:
                            self._browser.set.retry_times(retry_times)
                            
                        # 设置重试间隔
                        retry_interval = self.settings.get('DRISSIONPAGE_RETRY_INTERVAL')
                        if retry_interval:
                            self._browser.set.retry_interval(retry_interval)
                            
                    except Exception as e:
                        self.logger.error(f"创建浏览器实例失败: {e}")
                        raise
                        
                elif init_mode == 'connect':
                    # 连接到已有的浏览器实例
                    host = self.settings.get('DRISSIONPAGE_CONNECT_HOST', '127.0.0.1')
                    port = self.settings.get('DRISSIONPAGE_CONNECT_PORT', 9222)
                    
                    try:
                        # 4.0版本支持直接传入端口号
                        if isinstance(port, int):
                            self._browser = ChromiumPage(port)
                        else:
                            self._browser = ChromiumPage(f'{host}:{port}')
                    except Exception as e:
                        self.logger.error(f"连接到浏览器实例失败: {e}")
                        raise
                else:
                    raise ValueError(f"不支持的浏览器初始化模式: {init_mode}")
            
            return self._browser
    
    def get_session(self) -> SessionPage:
        """
        获取会话实例，利用DrissionPage 4.0新特性
        
        如果会话实例不存在，则创建新的实例
        
        返回:
            SessionPage: 会话实例
        """
        with self._lock:  # 使用线程锁保护共享资源
            if self._session is None:
                self.logger.info("创建新的会话实例")
                
                # 创建会话选项
                session_options = {}
                
                # 获取会话选项
                user_agent = self.settings.get('DRISSIONPAGE_USER_AGENT')
                if user_agent:
                    session_options['user_agent'] = user_agent
                    
                # 获取超时设置
                timeout = self.settings.get('DRISSIONPAGE_TIMEOUT')
                if timeout:
                    session_options['timeout'] = timeout
                    
                # 获取重试次数
                retry_times = self.settings.get('DRISSIONPAGE_RETRY_TIMES')
                if retry_times:
                    session_options['retry'] = retry_times
                    
                # 获取重试间隔
                retry_interval = self.settings.get('DRISSIONPAGE_RETRY_INTERVAL')
                if retry_interval:
                    session_options['retry_interval'] = retry_interval
                
                # 创建会话实例
                try:
                    self._session = SessionPage(**session_options)
                    
                    # 设置代理
                    proxy = self.settings.get('DRISSIONPAGE_PROXY')
                    if proxy:
                        self._session.set.proxy(proxy)
                        
                except Exception as e:
                    self.logger.error(f"创建会话实例失败: {e}")
                    raise
            
            return self._session
    
    def set_proxy(self, proxy: Optional[str]) -> None:
        """
        设置代理，优化4.0的代理设置方式
        
        参数:
            proxy: 代理地址，如 'http://user:pass@host:port'，None表示清除代理
        """
        with self._lock:
            # 设置浏览器代理
            if self._browser is not None:
                try:
                    # 4.0版本的代理设置方法
                    self._browser.set.proxy(proxy)
                    self.logger.info(f"浏览器代理已设置为: {proxy}")
                except Exception as e:
                    self.logger.error(f"设置浏览器代理失败: {e}")
            
            # 设置会话代理
            if self._session is not None:
                try:
                    self._session.set.proxy(proxy)
                    self.logger.info(f"会话代理已设置为: {proxy}")
                except Exception as e:
                    self.logger.error(f"设置会话代理失败: {e}")
    
    def close(self) -> None:
        """
        关闭浏览器和会话实例
        """
        with self._lock:
            # 关闭浏览器
            if self._browser is not None:
                if self.settings.get('DRISSIONPAGE_QUIT_ON_CLOSE', True):
                    try:
                        self.logger.info("关闭浏览器实例")
                        # 4.0版本支持force参数强制关闭
                        force = self.settings.get('DRISSIONPAGE_FORCE_CLOSE', False)
                        self._browser.quit(force=force)
                    except Exception as e:
                        self.logger.error(f"关闭浏览器实例失败: {e}")
                self._browser = None
            
            # 关闭会话
            if self._session is not None:
                if self.settings.get('DRISSIONPAGE_QUIT_SESSION_ON_CLOSE', True):
                    try:
                        self.logger.info("关闭会话实例")
                        self._session.close()
                    except Exception as e:
                        self.logger.error(f"关闭会话实例失败: {e}")
                self._session = None
    
    def __del__(self):
        """
        析构函数，确保资源被正确释放
        """
        self.close() 