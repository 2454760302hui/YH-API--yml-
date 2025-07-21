"""
API测试框架 - 高效易用的接口自动化测试工具

Features:
- YAML配置驱动的测试用例
- 支持所有HTTP方法和Socket测试
- 数据驱动和参数化测试
- 并发测试执行
- JSONPath参数提取
- 全局登录状态管理
- 企业微信消息推送
- Allure测试报告
- 本地HTML文档和在线调试
"""

__version__ = "2.0.0"
__author__ = "API Test Framework Team"
__email__ = "support@api-test-framework.com"
__description__ = "高效易用的API接口测试框架"

# 导出主要类和函数
try:
    from .core.runner import TestRunner
    from .core.session import HTTPSession
    from .core.config import ConfigManager
    from .utils.logger import get_logger
except ImportError:
    # 兼容旧版本结构
    TestRunner = None
    HTTPSession = None
    ConfigManager = None
    get_logger = None

__all__ = [
    'TestRunner',
    'HTTPSession',
    'ConfigManager',
    'get_logger',
    '__version__',
]
