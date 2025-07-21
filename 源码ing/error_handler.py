"""
错误处理模块

提供统一的错误处理装饰器和工具函数。
"""

import functools
import traceback
from typing import Callable, Any, Optional, Type, Union, List
from logging_config import get_logger
log = get_logger()
from exceptions import (
    FrameworkError, RequestError, ParserError, ValidationError,
    ExtractExpressionError, ConfigError, DatabaseError, VariableError,
    FileError, NotificationError, TestCaseError, TestError, DataError,
    format_exception_message, create_user_friendly_error
)


def handle_exceptions(
    exceptions: Union[Type[Exception], List[Type[Exception]]] = None,
    default_return: Any = None,
    reraise: bool = True,
    log_error: bool = True,
    context: Optional[str] = None
):
    """
    异常处理装饰器
    
    Args:
        exceptions: 要捕获的异常类型或列表
        default_return: 异常时的默认返回值
        reraise: 是否重新抛出异常
        log_error: 是否记录错误日志
        context: 上下文信息
    """
    if exceptions is None:
        exceptions = [Exception]
    elif not isinstance(exceptions, list):
        exceptions = [exceptions]
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except tuple(exceptions) as e:
                error_context = context or f"{func.__module__}.{func.__name__}"
                
                if log_error:
                    if isinstance(e, FrameworkError):
                        log.error(f"{error_context}: {str(e)}")
                        if e.details:
                            log.debug(f"错误详情: {e.details}")
                    else:
                        log.error(f"{error_context}: {type(e).__name__}: {str(e)}")
                        log.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
                
                if reraise:
                    raise
                else:
                    return default_return
        
        return wrapper
    return decorator


def safe_execute(
    func: Callable,
    *args,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = None,
    default_return: Any = None,
    log_error: bool = True,
    context: Optional[str] = None,
    **kwargs
) -> Any:
    """
    安全执行函数
    
    Args:
        func: 要执行的函数
        *args: 位置参数
        exceptions: 要捕获的异常类型
        default_return: 异常时的默认返回值
        log_error: 是否记录错误日志
        context: 上下文信息
        **kwargs: 关键字参数
        
    Returns:
        函数执行结果或默认返回值
    """
    if exceptions is None:
        exceptions = [Exception]
    elif not isinstance(exceptions, list):
        exceptions = [exceptions]
    
    try:
        return func(*args, **kwargs)
    except tuple(exceptions) as e:
        error_context = context or f"{func.__module__}.{func.__name__}"
        
        if log_error:
            if isinstance(e, FrameworkError):
                log.error(f"{error_context}: {str(e)}")
                if e.details:
                    log.debug(f"错误详情: {e.details}")
            else:
                log.error(f"{error_context}: {type(e).__name__}: {str(e)}")
                log.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
        
        return default_return


def validate_and_handle_error(
    condition: bool,
    error_class: Type[FrameworkError],
    message: str,
    **error_kwargs
) -> None:
    """
    验证条件并处理错误
    
    Args:
        condition: 验证条件
        error_class: 异常类
        message: 错误消息
        **error_kwargs: 异常的额外参数
        
    Raises:
        error_class: 条件不满足时抛出指定异常
    """
    if not condition:
        raise error_class(message, **error_kwargs)


def convert_exception(
    source_exception: Exception,
    target_exception_class: Type[FrameworkError],
    message: Optional[str] = None,
    **error_kwargs
) -> FrameworkError:
    """
    转换异常类型
    
    Args:
        source_exception: 源异常
        target_exception_class: 目标异常类
        message: 新的错误消息
        **error_kwargs: 异常的额外参数
        
    Returns:
        转换后的异常
    """
    if message is None:
        message = str(source_exception)
    
    # 添加原始异常信息到详情中
    if 'details' not in error_kwargs:
        error_kwargs['details'] = {}
    
    error_kwargs['details']['original_exception'] = {
        'type': type(source_exception).__name__,
        'message': str(source_exception)
    }
    
    return target_exception_class(message, **error_kwargs)


def handle_request_errors(func: Callable) -> Callable:
    """HTTP请求错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 转换为RequestError
            if not isinstance(e, RequestError):
                error_msg = f"请求执行失败: {str(e)}"
                raise convert_exception(e, RequestError, error_msg)
            raise
    return wrapper


def handle_parser_errors(func: Callable) -> Callable:
    """解析错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 转换为ParserError
            if not isinstance(e, ParserError):
                error_msg = f"解析失败: {str(e)}"
                raise convert_exception(e, ParserError, error_msg)
            raise
    return wrapper


def handle_validation_errors(func: Callable) -> Callable:
    """校验错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 转换为ValidationError
            if not isinstance(e, ValidationError):
                error_msg = f"校验失败: {str(e)}"
                raise convert_exception(e, ValidationError, error_msg)
            raise
    return wrapper


def handle_extraction_errors(func: Callable) -> Callable:
    """提取错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 转换为ExtractExpressionError
            if not isinstance(e, ExtractExpressionError):
                error_msg = f"数据提取失败: {str(e)}"
                raise convert_exception(e, ExtractExpressionError, error_msg)
            raise
    return wrapper


def handle_database_errors(func: Callable) -> Callable:
    """数据库错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 转换为DatabaseError
            if not isinstance(e, DatabaseError):
                error_msg = f"数据库操作失败: {str(e)}"
                raise convert_exception(e, DatabaseError, error_msg)
            raise
    return wrapper


def handle_file_errors(func: Callable) -> Callable:
    """文件操作错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 转换为FileError
            if not isinstance(e, FileError):
                error_msg = f"文件操作失败: {str(e)}"
                raise convert_exception(e, FileError, error_msg)
            raise
    return wrapper


def handle_test_errors(func: Callable) -> Callable:
    """测试错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, FrameworkError):
                error_msg = f"测试执行失败: {str(e)}"
                raise convert_exception(e, TestError, error_msg)
            raise
    return wrapper


def handle_data_errors(func: Callable) -> Callable:
    """数据处理错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, FrameworkError):
                error_msg = f"数据处理失败: {str(e)}"
                raise convert_exception(e, DataError, error_msg)
            raise
    return wrapper


class ErrorContext:
    """错误上下文管理器"""
    
    def __init__(self, context: str, log_errors: bool = True):
        """
        初始化错误上下文
        
        Args:
            context: 上下文描述
            log_errors: 是否记录错误
        """
        self.context = context
        self.log_errors = log_errors
        self.errors: List[Exception] = []
    
    def __enter__(self):
        """进入上下文"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if exc_val:
            self.errors.append(exc_val)
            
            if self.log_errors:
                if isinstance(exc_val, FrameworkError):
                    log.error(f"{self.context}: {str(exc_val)}")
                    if exc_val.details:
                        log.debug(f"错误详情: {exc_val.details}")
                else:
                    log.error(f"{self.context}: {type(exc_val).__name__}: {str(exc_val)}")
                    log.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
        
        # 不抑制异常
        return False
    
    def add_error(self, error: Exception) -> None:
        """添加错误"""
        self.errors.append(error)
        
        if self.log_errors:
            if isinstance(error, FrameworkError):
                log.error(f"{self.context}: {str(error)}")
            else:
                log.error(f"{self.context}: {type(error).__name__}: {str(error)}")
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def get_error_summary(self) -> str:
        """获取错误摘要"""
        if not self.errors:
            return "无错误"
        
        summary = f"{self.context} - 共 {len(self.errors)} 个错误:\n"
        for i, error in enumerate(self.errors, 1):
            if isinstance(error, FrameworkError):
                summary += f"{i}. {str(error)}\n"
            else:
                summary += f"{i}. {type(error).__name__}: {str(error)}\n"
        
        return summary


def create_error_reporter(context: str = "测试执行"):
    """
    创建错误报告器
    
    Args:
        context: 上下文描述
        
    Returns:
        错误上下文管理器
    """
    return ErrorContext(context)


def log_and_reraise(exc: Exception, context: str = None) -> None:
    """
    记录错误并重新抛出
    
    Args:
        exc: 异常对象
        context: 上下文信息
    """
    error_context = context or "未知上下文"
    
    if isinstance(exc, FrameworkError):
        log.error(f"{error_context}: {str(exc)}")
        if exc.details:
            log.debug(f"错误详情: {exc.details}")
    else:
        log.error(f"{error_context}: {type(exc).__name__}: {str(exc)}")
        log.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
    
    raise exc


def get_error_suggestion(exc: Exception) -> str:
    """
    获取错误建议
    
    Args:
        exc: 异常对象
        
    Returns:
        错误建议字符串
    """
    return create_user_friendly_error(exc)
