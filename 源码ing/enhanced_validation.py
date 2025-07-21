"""
增强的验证和提取模块

提供更强大的数据验证和提取功能，支持复杂的验证规则和提取表达式。
"""

import re
import json
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass
from datetime import datetime

from logging_config import get_logger
from error_handler import handle_validation_errors


@dataclass
class ValidationRule:
    """验证规则"""
    
    name: str
    expression: str
    expected: Any
    operator: str = 'eq'  # eq, ne, gt, lt, ge, le, in, not_in, contains, regex, custom
    message: Optional[str] = None
    severity: str = 'error'  # error, warning, info
    custom_validator: Optional[Callable] = None


@dataclass
class ExtractionRule:
    """提取规则"""
    
    name: str
    expression: str
    type: str = 'jsonpath'  # jsonpath, xpath, regex, css, custom
    default_value: Any = None
    post_processor: Optional[Callable] = None
    required: bool = True


class EnhancedValidator:
    """增强的验证器"""
    
    def __init__(self):
        """初始化验证器"""
        self.logger = get_logger()
        self.validation_results: List[Dict[str, Any]] = []
    
    @handle_validation_errors
    def validate(self, data: Any, rules: List[ValidationRule]) -> Dict[str, Any]:
        """
        执行验证
        
        Args:
            data: 要验证的数据
            rules: 验证规则列表
            
        Returns:
            验证结果字典
        """
        results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'details': []
        }
        
        for rule in rules:
            try:
                result = self._validate_single_rule(data, rule)
                results['details'].append(result)
                
                if result['status'] == 'PASSED':
                    results['passed'] += 1
                elif result['severity'] == 'warning':
                    results['warnings'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                self.logger.error(f"验证规则执行失败: {rule.name}, 错误: {e}")
                results['details'].append({
                    'rule_name': rule.name,
                    'status': 'ERROR',
                    'message': f"验证规则执行失败: {e}",
                    'severity': 'error'
                })
                results['failed'] += 1
        
        results['success'] = results['failed'] == 0
        return results
    
    def _validate_single_rule(self, data: Any, rule: ValidationRule) -> Dict[str, Any]:
        """验证单个规则"""
        # 提取实际值
        actual_value = self._extract_value(data, rule.expression)
        
        # 执行验证
        if rule.custom_validator:
            passed = rule.custom_validator(actual_value, rule.expected)
        else:
            passed = self._apply_operator(actual_value, rule.expected, rule.operator)
        
        # 构建结果
        result = {
            'rule_name': rule.name,
            'expression': rule.expression,
            'expected': rule.expected,
            'actual': actual_value,
            'operator': rule.operator,
            'status': 'PASSED' if passed else 'FAILED',
            'severity': rule.severity,
            'message': rule.message or self._generate_default_message(rule, actual_value, passed),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def _extract_value(self, data: Any, expression: str) -> Any:
        """从数据中提取值"""
        try:
            # 支持多种提取方式
            if expression.startswith('$.'):
                # JSONPath
                return self._extract_by_jsonpath(data, expression)
            elif expression.startswith('//') or expression.startswith('/'):
                # XPath (需要XML数据)
                return self._extract_by_xpath(data, expression)
            elif '.' in expression:
                # 点号分隔的属性路径
                return self._extract_by_dot_notation(data, expression)
            else:
                # 直接属性访问
                if isinstance(data, dict):
                    return data.get(expression)
                else:
                    return getattr(data, expression, None)
        except Exception as e:
            self.logger.warning(f"值提取失败: {expression}, 错误: {e}")
            return None
    
    def _extract_by_jsonpath(self, data: Any, expression: str) -> Any:
        """使用JSONPath提取值"""
        try:
            from jsonpath_ng import parse
            jsonpath_expr = parse(expression)
            matches = jsonpath_expr.find(data)
            if matches:
                return matches[0].value
            return None
        except ImportError:
            self.logger.warning("jsonpath_ng未安装，使用简单路径解析")
            return self._extract_by_simple_path(data, expression)
    
    def _extract_by_xpath(self, data: Any, expression: str) -> Any:
        """使用XPath提取值"""
        try:
            from lxml import etree
            if isinstance(data, str):
                root = etree.fromstring(data)
            else:
                root = data
            
            result = root.xpath(expression)
            if result:
                return result[0] if len(result) == 1 else result
            return None
        except ImportError:
            self.logger.warning("lxml未安装，无法使用XPath")
            return None
    
    def _extract_by_dot_notation(self, data: Any, expression: str) -> Any:
        """使用点号分隔的路径提取值"""
        parts = expression.split('.')
        current = data
        
        for part in parts:
            if current is None:
                return None
            
            # 处理数组索引
            if '[' in part and ']' in part:
                key, index_part = part.split('[', 1)
                index = int(index_part.rstrip(']'))
                
                if key:
                    current = current.get(key) if isinstance(current, dict) else getattr(current, key, None)
                
                if isinstance(current, (list, tuple)) and 0 <= index < len(current):
                    current = current[index]
                else:
                    return None
            else:
                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    current = getattr(current, part, None)
        
        return current
    
    def _extract_by_simple_path(self, data: Any, expression: str) -> Any:
        """简单路径提取（JSONPath的简化版本）"""
        # 移除 $. 前缀
        path = expression.lstrip('$.')
        return self._extract_by_dot_notation(data, path)
    
    def _apply_operator(self, actual: Any, expected: Any, operator: str) -> bool:
        """应用比较操作符"""
        try:
            if operator == 'eq':
                return actual == expected
            elif operator == 'ne':
                return actual != expected
            elif operator == 'gt':
                return actual > expected
            elif operator == 'lt':
                return actual < expected
            elif operator == 'ge':
                return actual >= expected
            elif operator == 'le':
                return actual <= expected
            elif operator == 'in':
                return actual in expected
            elif operator == 'not_in':
                return actual not in expected
            elif operator == 'contains':
                return expected in actual
            elif operator == 'regex':
                return bool(re.search(str(expected), str(actual)))
            elif operator == 'exists':
                return actual is not None
            elif operator == 'not_exists':
                return actual is None
            elif operator == 'type':
                return type(actual).__name__ == expected
            elif operator == 'length':
                return len(actual) == expected if hasattr(actual, '__len__') else False
            else:
                raise ValueError(f"不支持的操作符: {operator}")
        except Exception as e:
            self.logger.error(f"操作符应用失败: {operator}, 错误: {e}")
            return False
    
    def _generate_default_message(self, rule: ValidationRule, actual_value: Any, passed: bool) -> str:
        """生成默认验证消息"""
        if passed:
            return f"验证通过: {rule.name}"
        else:
            return f"验证失败: {rule.name}, 期望 {rule.expected} ({rule.operator}), 实际 {actual_value}"


class EnhancedExtractor:
    """增强的提取器"""
    
    def __init__(self):
        """初始化提取器"""
        self.logger = get_logger()
    
    @handle_validation_errors
    def extract(self, data: Any, rules: List[ExtractionRule]) -> Dict[str, Any]:
        """
        执行数据提取
        
        Args:
            data: 源数据
            rules: 提取规则列表
            
        Returns:
            提取结果字典
        """
        results = {}
        
        for rule in rules:
            try:
                value = self._extract_single_rule(data, rule)
                results[rule.name] = value
                
                self.logger.debug(f"提取成功: {rule.name} = {value}")
                
            except Exception as e:
                if rule.required:
                    self.logger.error(f"必需字段提取失败: {rule.name}, 错误: {e}")
                    raise
                else:
                    self.logger.warning(f"可选字段提取失败: {rule.name}, 使用默认值: {rule.default_value}")
                    results[rule.name] = rule.default_value
        
        return results
    
    def _extract_single_rule(self, data: Any, rule: ExtractionRule) -> Any:
        """提取单个规则"""
        # 根据类型选择提取方法
        if rule.type == 'jsonpath':
            value = self._extract_by_jsonpath(data, rule.expression)
        elif rule.type == 'xpath':
            value = self._extract_by_xpath(data, rule.expression)
        elif rule.type == 'regex':
            value = self._extract_by_regex(data, rule.expression)
        elif rule.type == 'css':
            value = self._extract_by_css(data, rule.expression)
        elif rule.type == 'custom':
            value = rule.post_processor(data) if rule.post_processor else None
        else:
            # 默认使用简单路径提取
            value = self._extract_by_simple_path(data, rule.expression)
        
        # 如果没有提取到值，使用默认值
        if value is None and rule.default_value is not None:
            value = rule.default_value
        
        # 应用后处理器
        if value is not None and rule.post_processor:
            value = rule.post_processor(value)
        
        return value
    
    def _extract_by_jsonpath(self, data: Any, expression: str) -> Any:
        """使用JSONPath提取"""
        try:
            from jsonpath_ng import parse
            jsonpath_expr = parse(expression)
            matches = jsonpath_expr.find(data)
            
            if not matches:
                return None
            elif len(matches) == 1:
                return matches[0].value
            else:
                return [match.value for match in matches]
        except ImportError:
            return self._extract_by_simple_path(data, expression)
    
    def _extract_by_xpath(self, data: Any, expression: str) -> Any:
        """使用XPath提取"""
        try:
            from lxml import etree, html
            
            if isinstance(data, str):
                # 尝试解析为XML或HTML
                try:
                    root = etree.fromstring(data)
                except:
                    root = html.fromstring(data)
            else:
                root = data
            
            result = root.xpath(expression)
            
            if not result:
                return None
            elif len(result) == 1:
                return result[0]
            else:
                return result
                
        except ImportError:
            self.logger.warning("lxml未安装，无法使用XPath")
            return None
    
    def _extract_by_regex(self, data: Any, expression: str) -> Any:
        """使用正则表达式提取"""
        text = str(data)
        matches = re.findall(expression, text)
        
        if not matches:
            return None
        elif len(matches) == 1:
            return matches[0]
        else:
            return matches
    
    def _extract_by_css(self, data: Any, expression: str) -> Any:
        """使用CSS选择器提取"""
        try:
            from bs4 import BeautifulSoup
            
            if isinstance(data, str):
                soup = BeautifulSoup(data, 'html.parser')
            else:
                soup = data
            
            elements = soup.select(expression)
            
            if not elements:
                return None
            elif len(elements) == 1:
                return elements[0].get_text().strip()
            else:
                return [elem.get_text().strip() for elem in elements]
                
        except ImportError:
            self.logger.warning("beautifulsoup4未安装，无法使用CSS选择器")
            return None
    
    def _extract_by_simple_path(self, data: Any, expression: str) -> Any:
        """简单路径提取"""
        parts = expression.split('.')
        current = data
        
        for part in parts:
            if current is None:
                return None
            
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list) and part.isdigit():
                index = int(part)
                current = current[index] if 0 <= index < len(current) else None
            else:
                current = getattr(current, part, None)
        
        return current


# 便捷函数
def create_validation_rule(name: str, expression: str, expected: Any, 
                         operator: str = 'eq', **kwargs) -> ValidationRule:
    """创建验证规则"""
    return ValidationRule(
        name=name,
        expression=expression,
        expected=expected,
        operator=operator,
        message=kwargs.get('message'),
        severity=kwargs.get('severity', 'error'),
        custom_validator=kwargs.get('custom_validator')
    )


def create_extraction_rule(name: str, expression: str, 
                         extraction_type: str = 'jsonpath', **kwargs) -> ExtractionRule:
    """创建提取规则"""
    return ExtractionRule(
        name=name,
        expression=expression,
        type=extraction_type,
        default_value=kwargs.get('default_value'),
        post_processor=kwargs.get('post_processor'),
        required=kwargs.get('required', True)
    )


# 常用后处理器
def to_int(value: Any) -> int:
    """转换为整数"""
    return int(value) if value is not None else 0


def to_float(value: Any) -> float:
    """转换为浮点数"""
    return float(value) if value is not None else 0.0


def to_datetime(value: Any, format_str: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    """转换为日期时间"""
    if isinstance(value, str):
        return datetime.strptime(value, format_str)
    return value


def strip_whitespace(value: Any) -> str:
    """去除空白字符"""
    return str(value).strip() if value is not None else ''


def to_upper(value: Any) -> str:
    """转换为大写"""
    return str(value).upper() if value is not None else ''


def to_lower(value: Any) -> str:
    """转换为小写"""
    return str(value).lower() if value is not None else ''
