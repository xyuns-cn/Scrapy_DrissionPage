"""
DrissionRequest类 - 自定义的集成DrissionPage功能的请求类
"""

from typing import Optional, Dict, Any, Callable, Union
from scrapy.http import Request


class DrissionRequest(Request):
    """
    集成DrissionPage功能的Scrapy请求对象
    """

    def __init__(
        self,
        url: str,
        callback: Optional[Callable] = None,
        method: str = 'GET',
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Union[str, bytes]] = None,
        cookies: Optional[Dict[str, str]] = None,
        meta: Optional[Dict[str, Any]] = None,
        encoding: str = 'utf-8',
        priority: int = 0,
        dont_filter: bool = False,
        errback: Optional[Callable] = None,
        flags: Optional[list] = None,
        cb_kwargs: Optional[Dict[str, Any]] = None,
        page_type: str = 'chromium',
        timeout: Optional[int] = None,
        load_mode: Optional[str] = None,
        wait_time: Optional[float] = None,
        wait_element: Optional[str] = None,
        proxy: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        初始化DrissionRequest
        
        参数:
            url: 请求URL
            callback: 回调函数
            method: 请求方法
            headers: 请求头
            body: 请求体
            cookies: Cookie字典
            meta: 元数据字典
            encoding: 编码
            priority: 优先级
            dont_filter: 是否不过滤重复请求
            errback: 错误回调函数
            flags: 请求标志
            cb_kwargs: 回调函数关键字参数
            page_type: 页面类型，'chromium'或'session'
            timeout: 请求超时时间
            load_mode: 加载模式，'normal'、'eager'或'none'
            wait_time: 加载后等待时间(秒)
            wait_element: 等待特定元素出现
            proxy: 代理地址
            **kwargs: 其他参数
        """
        # 初始化元数据
        meta = meta.copy() if meta else {}
        
        # 添加DrissionPage特有的元数据
        meta['drission'] = meta.get('drission', {})
        meta['drission']['page_type'] = page_type
        
        # 添加可选参数
        if timeout is not None:
            meta['drission']['timeout'] = timeout
        if load_mode is not None:
            meta['drission']['load_mode'] = load_mode
        if wait_time is not None:
            meta['drission']['wait_time'] = wait_time
        if wait_element is not None:
            meta['drission']['wait_element'] = wait_element
        
        # 设置代理
        if proxy:
            meta['proxy'] = proxy
        
        # 调用父类初始化方法
        super().__init__(
            url=url,
            callback=callback,
            method=method,
            headers=headers,
            body=body,
            cookies=cookies,
            meta=meta,
            encoding=encoding,
            priority=priority,
            dont_filter=dont_filter,
            errback=errback,
            flags=flags,
            cb_kwargs=cb_kwargs,
            **kwargs
        )
    
    def __str__(self) -> str:
        """返回请求的字符串表示"""
        page_type = self.meta.get('drission', {}).get('page_type', 'chromium')
        return f"<DrissionRequest [{self.method}] {self.url} [{page_type}]>"
    
    __repr__ = __str__ 