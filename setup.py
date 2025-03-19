import os
from setuptools import setup, find_packages

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), "r", encoding="utf-8") as f:
        return f.read()

def read_requirements(filename):
    return [
        line.strip()
        for line in read_file(filename).splitlines()
        if not line.startswith("#")
    ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrapy-drissionpage",
    version="0.1.0",
    author="Xinnn",
    author_email="xyuns.cc@gmail.com",
    description="将Scrapy爬虫框架与DrissionPage网页自动化工具进行无缝集成",
    long_description=long_description,
    url="https://github.com/xyuns-cn/scrapy-drissionpage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements("requirements.txt"),
    keywords="scrapy, drissionpage, crawler, spider, web scraping, automation, commercial-use, personal-use",
) 