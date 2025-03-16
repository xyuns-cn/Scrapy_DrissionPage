"""
模式切换爬虫示例 - 展示如何在d模式和s模式之间切换
"""

from scrapy_drissionpage import DrissionSpider
from scrapy_drissionpage.utils import ModeSwitcher


class ModeSwitchExampleSpider(DrissionSpider):
    """模式切换爬虫示例，演示在驱动模式和会话模式间切换"""
    
    name = "mode_switch_example"
    
    def start_requests(self):
        """开始请求，演示模式切换"""
        # 获取当前标签页
        tab = self.current_tab
        
        # 使用d模式(驱动模式)访问页面
        self.logger.info('使用驱动模式(d模式)访问页面')
        tab.get('https://httpbin.org/forms/post')
        
        # 填写表单
        tab.ele('input[name="custname"]').input('测试用户')
        tab.ele('input[name="custtel"]').input('12345678901')
        tab.ele('input[name="custemail"]').input('test@example.com')
        
        # 方法1: 使用内置切换方法
        self.logger.info('使用内置方法切换到会话模式(s模式)')
        tab.change_mode()
        self.logger.info(f'切换后的模式: {"s模式" if tab.mode == "s" else "d模式"}')
        
        # 方法2: 使用ModeSwitcher工具类
        # 先切回驱动模式
        tab.change_mode('d')
        self.logger.info('使用ModeSwitcher切换到会话模式')
        session_page = ModeSwitcher.to_session(tab)
        self.logger.info(f'ModeSwitcher切换后URL: {session_page.url}')
        
        # 使用会话模式提交表单
        session_page.ele('button[type="submit"]').click()
        
        # 创建请求
        yield self.drission_request(
            url=session_page.url,
            callback=self.parse,
            page_type='session',
            dont_filter=True
        )
    
    def parse(self, response):
        """解析响应"""
        # 提取数据
        yield {
            'url': response.url,
            'title': response.page.title,
            'mode': 'session' if response.is_session else 'chromium'
        } 