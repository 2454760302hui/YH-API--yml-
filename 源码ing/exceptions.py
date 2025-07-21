"""
自定义异常模块

定义框架中使用的各种异常类型，提供更好的错误处理和调试信息。
"""

from typing import Optional, Any, Dict


class FrameworkError(Exception):
    """框架基础异常类"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """
        初始化异常

        Args:
            message: 错误消息
            details: 错误详情字典
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """返回异常字符串表示"""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class ConfigError(FrameworkError):
    """配置相关异常"""

    def __init__(self, message: str, config_key: Optional[str] = None, config_value: Optional[Any] = None):
        """
        初始化配置异常

        Args:
            message: 错误消息
            config_key: 配置键名
            config_value: 配置值
        """
        details = {}
        if config_key:
            details["config_key"] = config_key
        if config_value is not None:
            details["config_value"] = config_value

        super().__init__(message, details)
        self.config_key = config_key
        self.config_value = config_value


class ParserError(FrameworkError):
    """解析相关异常"""

    def __init__(self, message: str, file_path: Optional[str] = None, line_number: Optional[int] = None):
        """
        初始化解析异常

        Args:
            message: 错误消息
            file_path: 文件路径
            line_number: 行号
        """
        details = {}
        if file_path:
            details["file_path"] = file_path
        if line_number:
            details["line_number"] = line_number

        super().__init__(message, details)
        self.file_path = file_path
        self.line_number = line_number


class ValidationError(FrameworkError):
    """校验相关异常"""

    def __init__(self, message: str, actual_value: Optional[Any] = None,
                 expected_value: Optional[Any] = None, validation_type: Optional[str] = None):
        """
        初始化校验异常

        Args:
            message: 错误消息
            actual_value: 实际值
            expected_value: 期望值
            validation_type: 校验类型
        """
        details = {}
        if actual_value is not None:
            details["actual_value"] = actual_value
        if expected_value is not None:
            details["expected_value"] = expected_value
        if validation_type:
            details["validation_type"] = validation_type

        super().__init__(message, details)
        self.actual_value = actual_value
        self.expected_value = expected_value
        self.validation_type = validation_type


class ExtractExpressionError(FrameworkError):
    """提取表达式异常"""

    def __init__(self, message: str, expression: Optional[str] = None,
                 expression_type: Optional[str] = None, source_data: Optional[Any] = None):
        """
        初始化提取表达式异常

        Args:
            message: 错误消息
            expression: 提取表达式
            expression_type: 表达式类型 (jsonpath, jmespath, regex)
            source_data: 源数据
        """
        details = {}
        if expression:
            details["expression"] = expression
        if expression_type:
            details["expression_type"] = expression_type
        if source_data is not None:
            # 避免在异常中存储过大的数据
            if isinstance(source_data, (str, dict, list)) and len(str(source_data)) > 200:
                details["source_data"] = str(source_data)[:200] + "..."
            else:
                details["source_data"] = source_data

        super().__init__(message, details)
        self.expression = expression
        self.expression_type = expression_type
        self.source_data = source_data


class RequestError(FrameworkError):
    """请求相关异常"""

    def __init__(self, message: str, url: Optional[str] = None, method: Optional[str] = None,
                 status_code: Optional[int] = None, response_text: Optional[str] = None):
        """
        初始化请求异常

        Args:
            message: 错误消息
            url: 请求URL
            method: 请求方法
            status_code: 响应状态码
            response_text: 响应文本
        """
        details = {}
        if url:
            details["url"] = url
        if method:
            details["method"] = method
        if status_code:
            details["status_code"] = status_code
        if response_text:
            # 限制响应文本长度
            details["response_text"] = response_text[:500] + "..." if len(response_text) > 500 else response_text

        super().__init__(message, details)
        self.url = url
        self.method = method
        self.status_code = status_code
        self.response_text = response_text


# 保持向后兼容性的异常类
class ConnectTimeout(RequestError):
    """连接超时异常"""

    def __init__(self, message: str = "连接超时", **kwargs):
        super().__init__(message, **kwargs)


class MaxRetryError(RequestError):
    """最大重试次数异常"""

    def __init__(self, message: str = "达到最大重试次数", **kwargs):
        super().__init__(message, **kwargs)


class ConnectError(RequestError):
    """连接错误异常"""

    def __init__(self, message: str = "连接错误", **kwargs):
        super().__init__(message, **kwargs)


class DatabaseError(FrameworkError):
    """数据库相关异常"""

    def __init__(self, message: str, sql: Optional[str] = None,
                 database: Optional[str] = None, table: Optional[str] = None):
        """
        初始化数据库异常

        Args:
            message: 错误消息
            sql: SQL语句
            database: 数据库名
            table: 表名
        """
        details = {}
        if sql:
            details["sql"] = sql
        if database:
            details["database"] = database
        if table:
            details["table"] = table

        super().__init__(message, details)
        self.sql = sql
        self.database = database
        self.table = table


class VariableError(FrameworkError):
    """变量相关异常"""

    def __init__(self, message: str, variable_name: Optional[str] = None,
                 variable_scope: Optional[str] = None, available_variables: Optional[list] = None):
        """
        初始化变量异常

        Args:
            message: 错误消息
            variable_name: 变量名
            variable_scope: 变量作用域
            available_variables: 可用变量列表
        """
        details = {}
        if variable_name:
            details["variable_name"] = variable_name
        if variable_scope:
            details["variable_scope"] = variable_scope
        if available_variables:
            details["available_variables"] = available_variables

        super().__init__(message, details)
        self.variable_name = variable_name
        self.variable_scope = variable_scope
        self.available_variables = available_variables


class FileError(FrameworkError):
    """文件相关异常"""

    def __init__(self, message: str, file_path: Optional[str] = None,
                 operation: Optional[str] = None, file_type: Optional[str] = None):
        """
        初始化文件异常

        Args:
            message: 错误消息
            file_path: 文件路径
            operation: 操作类型 (read, write, parse)
            file_type: 文件类型 (yaml, json, csv)
        """
        details = {}
        if file_path:
            details["file_path"] = file_path
        if operation:
            details["operation"] = operation
        if file_type:
            details["file_type"] = file_type

        super().__init__(message, details)
        self.file_path = file_path
        self.operation = operation
        self.file_type = file_type


class NotificationError(FrameworkError):
    """通知相关异常"""

    def __init__(self, message: str, notification_type: Optional[str] = None,
                 webhook_url: Optional[str] = None, response_code: Optional[int] = None):
        """
        初始化通知异常

        Args:
            message: 错误消息
            notification_type: 通知类型 (dingtalk, feishu, wecom)
            webhook_url: Webhook URL
            response_code: 响应状态码
        """
        details = {}
        if notification_type:
            details["notification_type"] = notification_type
        if webhook_url:
            details["webhook_url"] = webhook_url
        if response_code:
            details["response_code"] = response_code

        super().__init__(message, details)
        self.notification_type = notification_type
        self.webhook_url = webhook_url
        self.response_code = response_code


class TestCaseError(FrameworkError):
    """测试用例相关异常"""

    def __init__(self, message: str, test_case_name: Optional[str] = None,
                 step_name: Optional[str] = None, step_index: Optional[int] = None):
        """
        初始化测试用例异常

        Args:
            message: 错误消息
            test_case_name: 测试用例名称
            step_name: 步骤名称
            step_index: 步骤索引
        """
        details = {}
        if test_case_name:
            details["test_case_name"] = test_case_name
        if step_name:
            details["step_name"] = step_name
        if step_index is not None:
            details["step_index"] = step_index

        super().__init__(message, details)
        self.test_case_name = test_case_name
        self.step_name = step_name
        self.step_index = step_index


class TestError(FrameworkError):
    """测试执行相关异常"""

    def __init__(self, message: str, test_name: Optional[str] = None,
                 test_type: Optional[str] = None, error_details: Optional[Dict[str, Any]] = None):
        """
        初始化测试异常

        Args:
            message: 异常消息
            test_name: 测试名称
            test_type: 测试类型
            error_details: 错误详情
        """
        details = {}
        if test_name:
            details['test_name'] = test_name
        if test_type:
            details['test_type'] = test_type
        if error_details:
            details.update(error_details)

        super().__init__(message, details)
        self.test_name = test_name
        self.test_type = test_type
        self.error_details = error_details


class DataError(FrameworkError):
    """数据处理相关异常"""

    def __init__(self, message: str, data_type: Optional[str] = None,
                 data_source: Optional[str] = None, processing_step: Optional[str] = None):
        """
        初始化数据异常

        Args:
            message: 异常消息
            data_type: 数据类型
            data_source: 数据源
            processing_step: 处理步骤
        """
        details = {}
        if data_type:
            details['data_type'] = data_type
        if data_source:
            details['data_source'] = data_source
        if processing_step:
            details['processing_step'] = processing_step

        super().__init__(message, details)
        self.data_type = data_type
        self.data_source = data_source
        self.processing_step = processing_step


def format_exception_message(exc: Exception, include_traceback: bool = False) -> str:
    """
    格式化异常消息

    Args:
        exc: 异常对象
        include_traceback: 是否包含堆栈跟踪

    Returns:
        str: 格式化的异常消息
    """
    if isinstance(exc, FrameworkError):
        message = str(exc)
        if include_traceback:
            import traceback
            message += f"\n\n堆栈跟踪:\n{traceback.format_exc()}"
        return message
    else:
        message = f"{type(exc).__name__}: {str(exc)}"
        if include_traceback:
            import traceback
            message += f"\n\n堆栈跟踪:\n{traceback.format_exc()}"
        return message


def create_user_friendly_error(exc: Exception, context: Optional[str] = None) -> str:
    """
    创建用户友好的错误消息

    Args:
        exc: 异常对象
        context: 上下文信息

    Returns:
        str: 用户友好的错误消息
    """
    error_messages = {
        ConfigError: "配置错误",
        ParserError: "解析错误",
        ValidationError: "校验失败",
        ExtractExpressionError: "数据提取错误",
        RequestError: "请求错误",
        DatabaseError: "数据库错误",
        VariableError: "变量错误",
        FileError: "文件操作错误",
        NotificationError: "通知发送错误",
        TestCaseError: "测试用例错误"
    }

    error_type = type(exc)
    friendly_type = error_messages.get(error_type, "未知错误")

    message = f"❌ {friendly_type}: {str(exc)}"

    if context:
        message = f"{context} - {message}"

    # 添加解决建议
    if isinstance(exc, ConfigError):
        message += "\n💡 建议: 检查配置文件中的相关配置项"
    elif isinstance(exc, ParserError):
        message += "\n💡 建议: 检查YAML文件格式和语法"
    elif isinstance(exc, ValidationError):
        message += "\n💡 建议: 检查期望值和实际值是否匹配"
    elif isinstance(exc, ExtractExpressionError):
        message += "\n💡 建议: 检查提取表达式语法和数据结构"
    elif isinstance(exc, RequestError):
        message += "\n💡 建议: 检查网络连接和API接口状态"
    elif isinstance(exc, VariableError):
        message += "\n💡 建议: 检查变量定义和作用域"

    return message
