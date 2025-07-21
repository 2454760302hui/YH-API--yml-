"""
内置函数模块
提供测试框架的内置函数和工具
"""

import json
import time
import random
import string
import hashlib
import base64
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union, Optional
import re


def current_time(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间
    
    Args:
        format_str: 时间格式字符串
        
    Returns:
        格式化的时间字符串
    """
    return datetime.now().strftime(format_str)


def timestamp() -> int:
    """
    获取当前时间戳
    
    Returns:
        时间戳
    """
    return int(time.time())


def random_string(length: int = 10, chars: str = None) -> str:
    """
    生成随机字符串
    
    Args:
        length: 字符串长度
        chars: 字符集合
        
    Returns:
        随机字符串
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def random_int(min_val: int = 0, max_val: int = 100) -> int:
    """
    生成随机整数
    
    Args:
        min_val: 最小值
        max_val: 最大值
        
    Returns:
        随机整数
    """
    return random.randint(min_val, max_val)


def random_email(domain: str = "example.com") -> str:
    """
    生成随机邮箱
    
    Args:
        domain: 邮箱域名
        
    Returns:
        随机邮箱地址
    """
    username = random_string(8, string.ascii_lowercase)
    return f"{username}@{domain}"


def random_phone() -> str:
    """
    生成随机手机号
    
    Returns:
        随机手机号
    """
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    prefix = random.choice(prefixes)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return prefix + suffix


def md5_hash(text: str) -> str:
    """
    计算MD5哈希值
    
    Args:
        text: 输入文本
        
    Returns:
        MD5哈希值
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256_hash(text: str) -> str:
    """
    计算SHA256哈希值
    
    Args:
        text: 输入文本
        
    Returns:
        SHA256哈希值
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def base64_encode(text: str) -> str:
    """
    Base64编码
    
    Args:
        text: 输入文本
        
    Returns:
        Base64编码结果
    """
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def base64_decode(encoded_text: str) -> str:
    """
    Base64解码
    
    Args:
        encoded_text: Base64编码的文本
        
    Returns:
        解码结果
    """
    return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')


def generate_uuid() -> str:
    """
    生成UUID
    
    Returns:
        UUID字符串
    """
    return str(uuid.uuid4())


def json_loads(json_str: str) -> Any:
    """
    JSON字符串转对象
    
    Args:
        json_str: JSON字符串
        
    Returns:
        Python对象
    """
    return json.loads(json_str)


def json_dumps(obj: Any, indent: int = None) -> str:
    """
    对象转JSON字符串
    
    Args:
        obj: Python对象
        indent: 缩进
        
    Returns:
        JSON字符串
    """
    return json.dumps(obj, indent=indent, ensure_ascii=False)


def sleep(seconds: Union[int, float]) -> None:
    """
    休眠
    
    Args:
        seconds: 休眠秒数
    """
    time.sleep(seconds)


def regex_match(pattern: str, text: str) -> bool:
    """
    正则表达式匹配
    
    Args:
        pattern: 正则表达式模式
        text: 待匹配文本
        
    Returns:
        是否匹配
    """
    return bool(re.match(pattern, text))


def regex_search(pattern: str, text: str) -> Optional[str]:
    """
    正则表达式搜索
    
    Args:
        pattern: 正则表达式模式
        text: 待搜索文本
        
    Returns:
        匹配结果
    """
    match = re.search(pattern, text)
    return match.group() if match else None


def regex_findall(pattern: str, text: str) -> List[str]:
    """
    正则表达式查找所有匹配
    
    Args:
        pattern: 正则表达式模式
        text: 待搜索文本
        
    Returns:
        所有匹配结果
    """
    return re.findall(pattern, text)


def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    格式化日期
    
    Args:
        date_obj: 日期对象
        format_str: 格式字符串
        
    Returns:
        格式化的日期字符串
    """
    return date_obj.strftime(format_str)


def add_days(days: int, base_date: datetime = None) -> datetime:
    """
    日期加天数
    
    Args:
        days: 要加的天数
        base_date: 基准日期，默认为当前日期
        
    Returns:
        新的日期对象
    """
    if base_date is None:
        base_date = datetime.now()
    return base_date + timedelta(days=days)


def get_dict_value(data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    从嵌套字典中获取值
    
    Args:
        data: 字典数据
        key_path: 键路径，用点号分隔
        default: 默认值
        
    Returns:
        获取的值
    """
    keys = key_path.split('.')
    current = data
    
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default


def set_dict_value(data: Dict[str, Any], key_path: str, value: Any) -> None:
    """
    设置嵌套字典的值
    
    Args:
        data: 字典数据
        key_path: 键路径，用点号分隔
        value: 要设置的值
    """
    keys = key_path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value


# 导出所有函数到全局命名空间
__all__ = [
    'current_time', 'timestamp', 'random_string', 'random_int', 'random_email',
    'random_phone', 'md5_hash', 'sha256_hash', 'base64_encode', 'base64_decode',
    'generate_uuid', 'json_loads', 'json_dumps', 'sleep', 'regex_match',
    'regex_search', 'regex_findall', 'format_date', 'add_days', 'get_dict_value',
    'set_dict_value'
]
