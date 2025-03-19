# Scrapy DrissionPage 集成工具

## 📌 项目简介

Scrapy DrissionPage 是一个将 DrissionPage 与 Scrapy 框架无缝集成的扩展工具，让您可以在 Scrapy 爬虫中使用 DrissionPage 的全部功能。本扩展工具支持浏览器自动化和数据包收发两种模式，并可以自由切换，大幅提高爬虫开发效率与稳定性。

### 主要特性：

- 🌐 **模式自由切换**：支持在浏览器模式（chromium）和会话模式（session）间动态切换
- 🚀 **性能优化**：提供数据读取加速功能，支持静态解析，提高数据提取速度
- 📦 **数据包监听**：可监听网络请求，轻松获取AJAX加载的数据
- 📥 **文件下载**：集成下载功能，支持自定义保存路径和文件名
- 🔍 **简洁语法**：兼容DrissionPage的简洁元素定位语法，大大减少代码量

## 📥 安装方法

### 依赖项

- Python 3.6+
- Scrapy
- DrissionPage 4.0+

### 安装命令

```bash
# 安装DrissionPage
pip install DrissionPage

# 安装扩展工具
pip install scrapy-drissionpage
```

## ⚙️ 基本配置

在 Scrapy 项目的 `settings.py` 中添加以下配置：

```python
# 启用中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy_drissionpage.middleware.DrissionPageMiddleware': 543,
}

# DrissionPage配置
DRISSIONPAGE_HEADLESS = True  # 是否无头模式
DRISSIONPAGE_LOAD_MODE = 'normal'  # 页面加载模式：normal, eager, none
DRISSIONPAGE_DOWNLOAD_PATH = 'downloads'  # 下载路径
DRISSIONPAGE_TIMEOUT = 30  # 请求超时时间
DRISSIONPAGE_RETRY_TIMES = 3  # 重试次数
DRISSIONPAGE_RETRY_INTERVAL = 2  # 重试间隔（秒）

# 浏览器设置
DRISSIONPAGE_BROWSER_PATH = None  # 浏览器路径，None使用默认浏览器
DRISSIONPAGE_INCOGNITO = True  # 是否使用无痕模式
DRISSIONPAGE_CHROME_OPTIONS = ['--disable-gpu']  # Chrome启动选项
```

## 🧰 使用方法

### 1. 创建爬虫

继承 `DrissionSpider` 类创建爬虫：

```python
from scrapy_drissionpage.spider import DrissionSpider

class MySpider(DrissionSpider):
    name = 'myspider'
    
    def start_requests(self):
        # 创建浏览器模式请求
        yield self.drission_request(
            'https://example.com',
            page_type='chromium',  # 使用浏览器模式
            callback=self.parse
        )
        
        # 创建会话模式请求
        yield self.drission_request(
            'https://example.com/api',
            page_type='session',  # 使用会话模式
            callback=self.parse_api
        )
    
    def parse(self, response):
        # 使用DrissionPage的语法查找元素
        title = response.ele('tag:h1').text
        yield {'title': title}
```

### 2. 模式切换

您可以在不同的请求间动态切换模式：

```python
def parse_login(self, response):
    # 先使用浏览器模式登录
    response.page.ele('#username').input('user123')
    response.page.ele('#password').input('password123')
    response.page.ele('#login-btn').click()
    
    # 登录成功后，发送会话模式请求
    # 登录状态会自动同步
    yield self.drission_request(
        'https://example.com/api/data',
        page_type='session',  # 切换到会话模式
        callback=self.parse_data
    )
```

### 3. 数据提取加速

使用 `s_ele` 和 `s_eles` 方法进行静态解析，提高数据提取速度：

```python
def parse(self, response):
    # 常规方式
    # links = response.eles('t:a')  # 速度较慢
    
    # 加速方式
    links = response.s_eles('t:a')  # 速度提升约10倍
    
    for link in links:
        yield {
            'text': link.text,
            'url': link.attr('href')
        }
```

### 4. 数据包监听

监听和拦截页面上的网络请求：

```python
def parse_with_monitor(self, response):
    # 开始监听API请求
    self.listen_packets('api/data')
    
    # 点击按钮触发AJAX请求
    response.page.ele('#load-more').click()
    
    # 等待并获取数据包
    packet = self.wait_packet(timeout=10)
    
    # 处理数据包
    data = packet.response.body
    yield {'data': data}
    
    # 获取完数据后停止加载（适用于none加载模式）
    response.page.stop_loading()
```

### 5. 文件下载

使用内置的下载功能：

```python
def parse_download(self, response):
    # 设置下载路径和文件名
    self.set_download_path('files')
    self.set_download_file_name('document')
    
    # 点击下载按钮
    response.page.ele('#download-btn').click()
    
    # 等待下载开始并获取任务
    mission = self.wait_download_begin()
    
    # 等待下载完成
    mission.wait()
    
    yield {'file_path': mission.path}
```

## 📚 高级功能

### 1. 多标签页操作

```python
def parse_multi_tabs(self, response):
    # 创建新标签页
    tab2 = self.new_tab('https://example.com/page2')
    
    # 从第一个标签页获取数据
    title1 = response.page.title
    
    # 从第二个标签页获取数据
    title2 = tab2.title
    
    yield {
        'title1': title1,
        'title2': title2
    }
```

### 2. iframe 操作

```python
def parse_iframe(self, response):
    # 获取iframe对象
    iframe = response.page.get_frame('#my-iframe')
    
    # 在iframe中查找元素
    data = iframe.ele('#data').text
    
    yield {'iframe_data': data}
```

### 3. 执行JavaScript

```python
def parse_with_js(self, response):
    # 执行JavaScript代码
    result = response.page.run_js('return document.title')
    
    # 修改页面元素
    response.page.run_js('document.getElementById("demo").innerHTML = "Hello JavaScript"')
    
    yield {'js_result': result}
```

## 🌰 完整示例

### 例1：爬取GiteeExplore页面项目列表

```python
import scrapy
from scrapy_drissionpage.spider import DrissionSpider

class GiteeSpider(DrissionSpider):
    name = 'gitee_spider'
    
    def start_requests(self):
        yield self.drission_request(
            'https://gitee.com/explore',
            page_type='session',  # 使用会话模式即可，不需要JavaScript
            callback=self.parse
        )
    
    def parse(self, response):
        # 使用静态解析加速
        ul_ele = response.s_ele('tag:ul@text():全部推荐项目')
        projects = ul_ele.s_eles('tag:a')
        
        for project in projects:
            # 只处理有href属性的链接
            if project.attr('href') and '/explore/' not in project.attr('href'):
                yield {
                    'name': project.text,
                    'url': response.urljoin(project.attr('href'))
                }
```

### 例2：处理需要登录的网站

```python
import scrapy
from scrapy_drissionpage.spider import DrissionSpider

class LoginSpider(DrissionSpider):
    name = 'login_spider'
    
    def start_requests(self):
        yield self.drission_request(
            'https://example.com/login',
            page_type='chromium',  # 使用浏览器模式处理登录
            callback=self.login
        )
    
    def login(self, response):
        # 填写登录表单
        response.page.ele('#username').input('your_username')
        response.page.ele('#password').input('your_password')
        response.page.ele('#login-btn').click()
        
        # 等待登录成功，页面跳转
        response.page.wait.url_change()
        
        # 登录成功后访问用户中心
        yield self.drission_request(
            'https://example.com/user/dashboard',
            page_type='session',  # 登录后切换到会话模式提高效率
            callback=self.parse_dashboard
        )
    
    def parse_dashboard(self, response):
        # 提取用户信息
        username = response.ele('.user-name').text
        points = response.ele('.user-points').text
        
        yield {
            'username': username,
            'points': points
        }
        
        # 获取所有订单链接
        order_links = response.s_eles('.order-item a')
        for link in order_links:
            yield self.drission_request(
                response.urljoin(link.attr('href')),
                page_type='session',
                callback=self.parse_order
            )
    
    def parse_order(self, response):
        # 提取订单信息
        order_id = response.ele('.order-id').text
        order_date = response.ele('.order-date').text
        order_amount = response.ele('.order-amount').text
        
        yield {
            'order_id': order_id,
            'date': order_date,
            'amount': order_amount
        }
```

### 例3：处理动态加载内容

```python
import scrapy
from scrapy_drissionpage.spider import DrissionSpider

class AjaxSpider(DrissionSpider):
    name = 'ajax_spider'
    
    def start_requests(self):
        yield self.drission_request(
            'https://example.com/products',
            page_type='chromium',
            load_mode='none',  # 使用none加载模式，手动控制加载过程
            callback=self.parse
        )
    
    def parse(self, response):
        # 开始监听API请求
        self.listen_packets('api/products')
        
        # 点击"加载更多"按钮
        response.page.ele('#load-more').click()
        
        # 等待数据包
        packet = self.wait_packet(timeout=10)
        
        # 获取到数据后停止页面加载
        response.page.stop_loading()
        
        # 解析JSON数据
        products_data = packet.response.json()
        
        # 处理产品数据
        for product in products_data['products']:
            yield {
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'image': product['image']
            }
```

## 📋 常见问题

### Q: 如何选择使用哪种模式？

**A**: 
- 选择 `chromium` 模式（浏览器模式）当：
  - 页面需要JavaScript渲染
  - 需要执行点击、输入等交互操作
  - 需要处理登录验证码
  - 需要监听网络请求

- 选择 `session` 模式（会话模式）当：
  - 页面不需要JavaScript渲染
  - 主要是数据提取任务
  - 需要更高的性能和更低的资源消耗
  - 页面结构简单

### Q: 如何处理滑块验证码？

**A**: 使用浏览器模式和动作链：

```python
def solve_slider(self, response):
    # 获取滑块元素
    slider = response.page.ele('#slider')
    
    # 使用动作链操作滑块
    response.page.actions.hold(slider)
    for i in range(1, 60):
        response.page.actions.move(offset_x=i, offset_y=0, duration=0.1)
    response.page.actions.release()
```

### Q: 如何提高数据采集速度？

**A**:
1. 使用 `s_ele` 和 `s_eles` 进行静态解析
2. 对不需要JavaScript的页面使用 `session` 模式
3. 使用 `load_mode='none'` 并配合数据包监听，获取到关键数据后立即停止加载

## 🌟 配置参考

### 完整的 settings.py 配置选项：

```python
# 中间件设置
DOWNLOADER_MIDDLEWARES = {
    'scrapy_drissionpage.middleware.DrissionPageMiddleware': 543,
}

# 浏览器基本设置
DRISSIONPAGE_BROWSER_PATH = None  # 浏览器路径
DRISSIONPAGE_HEADLESS = True  # 无头模式
DRISSIONPAGE_INCOGNITO = True  # 无痕模式
DRISSIONPAGE_CHROME_OPTIONS = []  # Chrome选项

# 连接设置
DRISSIONPAGE_INIT_MODE = 'new'  # 初始化模式：new或connect
DRISSIONPAGE_CONNECT_HOST = '127.0.0.1'  # 连接主机
DRISSIONPAGE_CONNECT_PORT = 9222  # 连接端口

# 页面加载设置
DRISSIONPAGE_LOAD_MODE = 'normal'  # 加载模式：normal, eager, none
DRISSIONPAGE_TIMEOUT = 30  # 超时时间
DRISSIONPAGE_RETRY_TIMES = 3  # 重试次数
DRISSIONPAGE_RETRY_INTERVAL = 2  # 重试间隔

# 下载设置
DRISSIONPAGE_DOWNLOAD_PATH = 'downloads'  # 下载路径
DRISSIONPAGE_FORCE_CLOSE = False  # 是否强制关闭浏览器

# 会话设置
DRISSIONPAGE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'  # User-Agent

# 代理设置
DRISSIONPAGE_PROXY = None  # 代理地址

# 关闭设置
DRISSIONPAGE_QUIT_ON_CLOSE = True  # 爬虫关闭时是否关闭浏览器
DRISSIONPAGE_QUIT_SESSION_ON_CLOSE = True  # 爬虫关闭时是否关闭会话
```

## 📄 许可证

本项目采用 MIT 许可证，允许个人和商业使用。

- **个人使用**：任何个人可以自由使用、修改和分发本软件。
- **商业用途**：允许将本软件用于商业产品和服务，无需支付额外费用。

查看完整的 [LICENSE](LICENSE) 文件获取更多信息。

---

通过以上配置和示例，您可以开始使用Scrapy DrissionPage扩展工具进行高效的网页抓取。该工具结合了Scrapy的分布式抓取能力和DrissionPage的强大自动化功能，为您提供了一个强大而灵活的网络抓取解决方案。
