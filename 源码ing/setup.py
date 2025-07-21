#!/usr/bin/env python3
"""
API测试框架安装脚本
支持pip install安装方式
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "高效易用的API接口测试框架"

# 读取requirements文件
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements-enhanced.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'pytest>=7.0.0',
        'requests>=2.28.0',
        'PyYAML>=6.0',
        'jsonpath-ng>=1.5.3',
        'allure-pytest>=2.12.0',
        'faker>=19.0.0',
        'lxml>=4.9.0',
        'redis>=4.5.0',
        'pymysql>=1.0.2',
        'fastapi>=0.104.0',
        'uvicorn>=0.24.0',
        'jinja2>=3.1.0',
        'colorama>=0.4.6',
        'rich>=13.0.0',
        'click>=8.1.0',
        'websockets>=11.0.0',
        'httpx>=0.24.0',
        'pydantic>=2.0.0',
        'aiohttp>=3.8.0',
        'paramiko>=3.0.0',
        'cryptography>=41.0.0',
        'schedule>=1.2.0',
        'python-dotenv>=1.0.0',
        'openpyxl>=3.1.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
    ]

setup(
    name="api-test-yh-pro",
    version="3.0.0",
    author="YH API Test Framework Team",
    author_email="support@api-test-yh.com",
    description="YH主题专业级API接口测试框架 - 智能高效的测试工具",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yh-api-test/api-test-yh-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'full': [
            'selenium>=4.0.0',
            'playwright>=1.30.0',
            'grpcio>=1.50.0',
            'websocket-client>=1.5.0',
        ],
        'enterprise': [
            'pymongo>=4.4.0',
            'sqlalchemy>=2.0.0',
            'celery>=5.3.0',
            'rabbitmq>=0.2.0',
        ],
        'socket': [
            'websockets>=11.0.0',
            'paramiko>=3.0.0',
            'scapy>=2.5.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'api-test-yh=yh_shell:main',
            'yh-test=yh_shell:main',
            'fadeaway=yh_shell:fadeaway_main',
            'inspire=yh_shell:inspire_main',
            'api-test-yh-shell=yh_shell:main',
            'api-test-yh-docs=swagger_docs:main',
            'api-test-yh-ai=ai_tester:main',
            'api-test-yh-quickstart=quick_start:main',
        ],
        'pytest11': [
            'api_test_framework=plugin',
        ]
    },
    include_package_data=True,
    package_data={
        'api_test_framework': [
            'templates/*.yaml',
            'templates/*.json',
            'static/*.css',
            'static/*.js',
            'static/*.html',
            'docs/*.html',
            'examples/*.py',
            'examples/*.yaml',
        ]
    },
    zip_safe=False,
    keywords=[
        'api', 'testing', 'automation', 'pytest', 'yaml', 'yh', 'intelligent',
        'http', 'rest', 'json', 'concurrent', 'data-driven', 'allure',
        '接口测试', '自动化测试', 'API测试框架', 'YH', '智能高效'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/yh-api-test/api-test-yh-pro/issues',
        'Source': 'https://github.com/yh-api-test/api-test-yh-pro',
        'Documentation': 'https://api-test-yh-pro.readthedocs.io/',
    },
)
