# 开发指南

感谢您考虑为Scrapy-DrissionPage项目做出贡献！以下是开发和贡献代码的指南。

## 环境设置

1. 克隆仓库
```bash
git clone https://github.com/yourusername/scrapy-drissionpage.git
cd scrapy-drissionpage
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装开发依赖
```bash
pip install -e ".[dev]"
```

## 代码规范

- 遵循PEP 8风格指南
- 使用有意义的变量和函数名
- 添加适当的文档字符串
- 为新功能编写测试

## 测试

运行测试套件：
```bash
pytest
```

运行单个测试文件：
```bash
pytest tests/test_spider.py
```

## 提交代码

1. 创建新分支
```bash
git checkout -b feature/your-feature-name
```

2. 提交更改
```bash
git add .
git commit -m "添加了新功能: xxx"
```

3. 推送到GitHub
```bash
git push origin feature/your-feature-name
```

4. 创建Pull Request

## 项目结构

- `scrapy_drissionpage/`: 主要源代码
  - `browser_manager.py`: 浏览器管理器
  - `middleware.py`: Scrapy中间件
  - `request.py`: 请求对象
  - `response.py`: 响应对象
  - `settings.py`: 默认设置
  - `spider.py`: 爬虫基类
  - `utils/`: 工具函数
- `examples/`: 示例爬虫
- `tests/`: 测试代码
- `docs/`: 文档

## 发布新版本

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建发布标签
4. 发布到PyPI
```bash
python -m build
python -m twine upload dist/*
``` 