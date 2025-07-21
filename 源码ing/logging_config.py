"""
日志配置模块

提供统一的日志配置和管理功能。
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""
    
    # 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
        'RESET': '\033[0m'      # 重置
    }
    
    def format(self, record):
        """格式化日志记录"""
        # 添加颜色
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class TestFrameworkLogger:
    """测试框架日志管理器"""
    
    def __init__(self, name: str = "pytest-yaml"):
        """
        初始化日志管理器
        
        Args:
            name: 日志器名称
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 防止重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # 彩色格式化器
        console_formatter = ColoredFormatter(
            '%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # 文件处理器
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 普通日志文件
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "pytest-yaml.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # 错误日志文件
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "error.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
    
    def set_level(self, level: str):
        """
        设置日志级别
        
        Args:
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {level}')
        
        self.logger.setLevel(numeric_level)
        
        # 更新控制台处理器级别
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.setLevel(numeric_level)
    
    def debug(self, message: str, *args, **kwargs):
        """记录调试信息"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """记录信息"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """记录警告"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """记录错误"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """记录严重错误"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """记录异常信息（包含堆栈跟踪）"""
        self.logger.exception(message, *args, **kwargs)


class RequestLogger:
    """HTTP请求日志记录器"""
    
    def __init__(self, logger: TestFrameworkLogger):
        """
        初始化请求日志记录器
        
        Args:
            logger: 主日志记录器
        """
        self.logger = logger
    
    def log_request(self, method: str, url: str, headers: Optional[Dict] = None, 
                   data: Any = None, params: Optional[Dict] = None):
        """
        记录HTTP请求信息
        
        Args:
            method: 请求方法
            url: 请求URL
            headers: 请求头
            data: 请求数据
            params: 请求参数
        """
        self.logger.info(f"🚀 发送请求: {method.upper()} {url}")
        
        if params:
            self.logger.debug(f"请求参数: {params}")
        
        if headers:
            # 过滤敏感信息
            safe_headers = self._filter_sensitive_data(headers)
            self.logger.debug(f"请求头: {safe_headers}")
        
        if data:
            # 限制数据长度并过滤敏感信息
            safe_data = self._filter_sensitive_data(data)
            data_str = str(safe_data)
            if len(data_str) > 1000:
                data_str = data_str[:1000] + "... (truncated)"
            self.logger.debug(f"请求数据: {data_str}")
    
    def log_response(self, response, duration: float = None):
        """
        记录HTTP响应信息
        
        Args:
            response: 响应对象
            duration: 请求耗时（秒）
        """
        status_emoji = "✅" if 200 <= response.status_code < 300 else "❌"
        duration_str = f" ({duration:.3f}s)" if duration else ""
        
        self.logger.info(f"{status_emoji} 响应状态: {response.status_code}{duration_str}")
        
        # 记录响应头
        if hasattr(response, 'headers') and response.headers:
            safe_headers = self._filter_sensitive_data(dict(response.headers))
            self.logger.debug(f"响应头: {safe_headers}")
        
        # 记录响应内容
        try:
            if hasattr(response, 'text'):
                content = response.text
                if len(content) > 1000:
                    content = content[:1000] + "... (truncated)"
                self.logger.debug(f"响应内容: {content}")
        except Exception as e:
            self.logger.debug(f"无法记录响应内容: {e}")
    
    def _filter_sensitive_data(self, data: Any) -> Any:
        """
        过滤敏感数据
        
        Args:
            data: 原始数据
            
        Returns:
            过滤后的数据
        """
        if isinstance(data, dict):
            filtered = {}
            for key, value in data.items():
                if any(sensitive in key.lower() for sensitive in 
                      ['password', 'token', 'secret', 'key', 'auth']):
                    filtered[key] = "***"
                else:
                    filtered[key] = self._filter_sensitive_data(value)
            return filtered
        elif isinstance(data, list):
            return [self._filter_sensitive_data(item) for item in data]
        else:
            return data


class TestCaseLogger:
    """测试用例日志记录器"""
    
    def __init__(self, logger: TestFrameworkLogger):
        """
        初始化测试用例日志记录器
        
        Args:
            logger: 主日志记录器
        """
        self.logger = logger
    
    def log_test_start(self, test_name: str, test_data: Optional[Dict] = None):
        """
        记录测试开始
        
        Args:
            test_name: 测试名称
            test_data: 测试数据
        """
        self.logger.info(f"🧪 开始执行测试: {test_name}")
        if test_data:
            self.logger.debug(f"测试数据: {test_data}")
    
    def log_test_end(self, test_name: str, result: str, duration: float = None):
        """
        记录测试结束
        
        Args:
            test_name: 测试名称
            result: 测试结果 (PASSED, FAILED, SKIPPED)
            duration: 测试耗时（秒）
        """
        emoji_map = {
            'PASSED': '✅',
            'FAILED': '❌',
            'SKIPPED': '⏭️'
        }
        emoji = emoji_map.get(result, '❓')
        duration_str = f" ({duration:.3f}s)" if duration else ""
        
        self.logger.info(f"{emoji} 测试结果: {test_name} - {result}{duration_str}")
    
    def log_validation(self, expression: str, expected: Any, actual: Any, result: bool):
        """
        记录校验信息
        
        Args:
            expression: 校验表达式
            expected: 期望值
            actual: 实际值
            result: 校验结果
        """
        emoji = "✅" if result else "❌"
        self.logger.info(f"{emoji} 校验: {expression}")
        self.logger.debug(f"期望值: {expected}")
        self.logger.debug(f"实际值: {actual}")
    
    def log_extraction(self, expression: str, value: Any):
        """
        记录数据提取信息
        
        Args:
            expression: 提取表达式
            value: 提取的值
        """
        self.logger.info(f"📤 数据提取: {expression} = {value}")


# 全局日志实例
_main_logger: Optional[TestFrameworkLogger] = None
_request_logger: Optional[RequestLogger] = None
_test_logger: Optional[TestCaseLogger] = None


def get_logger() -> TestFrameworkLogger:
    """获取主日志记录器"""
    global _main_logger
    if _main_logger is None:
        _main_logger = TestFrameworkLogger()
    return _main_logger


def get_request_logger() -> RequestLogger:
    """获取请求日志记录器"""
    global _request_logger, _main_logger
    if _request_logger is None:
        if _main_logger is None:
            _main_logger = TestFrameworkLogger()
        _request_logger = RequestLogger(_main_logger)
    return _request_logger


def get_test_logger() -> TestCaseLogger:
    """获取测试日志记录器"""
    global _test_logger, _main_logger
    if _test_logger is None:
        if _main_logger is None:
            _main_logger = TestFrameworkLogger()
        _test_logger = TestCaseLogger(_main_logger)
    return _test_logger


def setup_logging(level: str = "INFO", log_dir: str = "logs"):
    """
    设置日志配置
    
    Args:
        level: 日志级别
        log_dir: 日志目录
    """
    # 创建日志目录
    Path(log_dir).mkdir(exist_ok=True)
    
    # 获取并配置主日志记录器
    logger = get_logger()
    logger.set_level(level)
    
    return logger


# 为了向后兼容，提供简单的日志接口
log = get_logger()
