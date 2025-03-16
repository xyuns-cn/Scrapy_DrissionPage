"""
Scrapy-DrissionPage安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrapy-drissionpage",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="将Scrapy爬虫框架与DrissionPage网页自动化工具进行无缝集成",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/scrapy-drissionpage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Scrapy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "scrapy>=2.12.0",
        "DrissionPage>=4.1.0.17",
    ],
    keywords="scrapy, drissionpage, crawler, spider, web scraping, automation",
) 