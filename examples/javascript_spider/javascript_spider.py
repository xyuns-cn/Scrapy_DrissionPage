"""
JavaScript处理示例 - 展示如何处理JavaScript渲染的内容
"""

from scrapy_drissionpage import DrissionSpider


class JavaScriptExampleSpider(DrissionSpider):
    """JavaScript处理示例，演示如何处理动态加载内容"""
    
    name = "javascript_example"
    
    # 自定义设置
    custom_settings = {
        'DRISSIONPAGE_HEADLESS': False,  # 显示浏览器界面，便于观察
    }
    
    def start_requests(self):
        """开始请求"""
        # 获取当前标签页
        tab = self.current_tab
        
        # 访问包含JavaScript动态内容的页面
        # 这里使用一个示例页面，您可以替换为其他JavaScript渲染的页面
        tab.get('https://spa.jd.com/')
        
        # 等待页面JavaScript执行完成
        tab.wait.load_complete()
        
        # 等待特定元素出现，表示JavaScript已加载内容
        tab.wait.ele_display('css:.cate_menu_item', timeout=10)
        
        # 创建请求
        yield self.drission_request(
            url=tab.url,
            callback=self.parse,
            wait_time=2,  # 额外等待时间，确保所有内容加载完成
            dont_filter=True
        )
    
    def parse(self, response):
        """解析响应，提取JavaScript渲染后的内容"""
        # 使用response.page直接操作页面元素
        categories = response.page.eles('css:.cate_menu_item')
        
        for i, category in enumerate(categories[:5]):  # 只处理前5个分类，避免过多
            category_name = category.text
            self.logger.info(f'处理分类: {category_name}')
            
            # 点击分类，触发JavaScript加载子分类
            category.click()
            response.page.wait.time(1)  # 等待子分类加载
            
            # 获取子分类
            sub_categories = response.page.eles('css:.cate_detail_item')
            sub_category_names = [sub.text for sub in sub_categories[:5]]  # 只提取前5个子分类
            
            yield {
                'category': category_name,
                'sub_categories': sub_category_names
            } 