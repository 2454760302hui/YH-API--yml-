"""
模板渲染模块
用于渲染YAML配置中的模板变量
"""

import re
import json
from typing import Any, Dict, List, Union, Optional
from jinja2 import Template, Environment, BaseLoader, TemplateError


class StringTemplateLoader(BaseLoader):
    """字符串模板加载器"""
    
    def __init__(self, template_string: str):
        self.template_string = template_string
    
    def get_source(self, environment, template):
        return self.template_string, None, lambda: True


def rend_template_any(data: Any, **context) -> Any:
    """
    渲染任意类型的数据中的模板变量
    
    Args:
        data: 要渲染的数据
        **context: 模板上下文变量
        
    Returns:
        渲染后的数据
    """
    if data is None:
        return data
    
    if isinstance(data, str):
        return render_template_string(data, **context)
    elif isinstance(data, dict):
        return render_template_dict(data, **context)
    elif isinstance(data, list):
        return render_template_list(data, **context)
    else:
        return data


def render_template_string(template_str: str, **context) -> str:
    """
    渲染模板字符串
    
    Args:
        template_str: 模板字符串
        **context: 模板上下文变量
        
    Returns:
        渲染后的字符串
    """
    if not isinstance(template_str, str):
        return template_str
    
    try:
        # 处理简单的变量替换 ${var} 或 {{var}}
        if '${' in template_str or '{{' in template_str:
            # 使用Jinja2模板引擎
            env = Environment(loader=BaseLoader())
            
            # 转换 ${var} 格式为 {{var}} 格式
            converted_template = re.sub(r'\$\{([^}]+)\}', r'{{\1}}', template_str)
            
            template = env.from_string(converted_template)
            return template.render(**context)
        else:
            return template_str
    except TemplateError as e:
        # 模板渲染失败时返回原字符串
        print(f"模板渲染失败: {e}")
        return template_str
    except Exception as e:
        print(f"渲染过程中出现错误: {e}")
        return template_str


def render_template_dict(data: Dict[str, Any], **context) -> Dict[str, Any]:
    """
    渲染字典中的模板变量
    
    Args:
        data: 字典数据
        **context: 模板上下文变量
        
    Returns:
        渲染后的字典
    """
    if not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        # 渲染键
        rendered_key = render_template_string(str(key), **context) if isinstance(key, str) else key
        # 渲染值
        rendered_value = rend_template_any(value, **context)
        result[rendered_key] = rendered_value
    
    return result


def render_template_list(data: List[Any], **context) -> List[Any]:
    """
    渲染列表中的模板变量
    
    Args:
        data: 列表数据
        **context: 模板上下文变量
        
    Returns:
        渲染后的列表
    """
    if not isinstance(data, list):
        return data
    
    result = []
    for item in data:
        rendered_item = rend_template_any(item, **context)
        result.append(rendered_item)
    
    return result


def extract_template_variables(template_str: str) -> List[str]:
    """
    提取模板字符串中的变量名
    
    Args:
        template_str: 模板字符串
        
    Returns:
        变量名列表
    """
    if not isinstance(template_str, str):
        return []
    
    variables = []
    
    # 匹配 ${var} 格式
    dollar_vars = re.findall(r'\$\{([^}]+)\}', template_str)
    variables.extend(dollar_vars)
    
    # 匹配 {{var}} 格式
    jinja_vars = re.findall(r'\{\{([^}]+)\}\}', template_str)
    variables.extend([var.strip() for var in jinja_vars])
    
    return list(set(variables))


def validate_template_context(template_str: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证模板上下文是否包含所需变量
    
    Args:
        template_str: 模板字符串
        context: 上下文字典
        
    Returns:
        验证结果字典
    """
    required_vars = extract_template_variables(template_str)
    missing_vars = []
    available_vars = []
    
    for var in required_vars:
        if var in context:
            available_vars.append(var)
        else:
            missing_vars.append(var)
    
    return {
        'required_variables': required_vars,
        'missing_variables': missing_vars,
        'available_variables': available_vars,
        'is_valid': len(missing_vars) == 0
    }


def render_with_functions(template_str: str, context: Dict[str, Any], functions: Dict[str, Any] = None) -> str:
    """
    使用自定义函数渲染模板
    
    Args:
        template_str: 模板字符串
        context: 上下文变量
        functions: 自定义函数字典
        
    Returns:
        渲染后的字符串
    """
    if functions is None:
        functions = {}
    
    # 合并上下文和函数
    full_context = {**context, **functions}
    
    return render_template_string(template_str, **full_context)


def render_json_template(json_str: str, **context) -> Any:
    """
    渲染JSON模板
    
    Args:
        json_str: JSON模板字符串
        **context: 模板上下文变量
        
    Returns:
        渲染后的Python对象
    """
    try:
        # 先渲染模板
        rendered_str = render_template_string(json_str, **context)
        # 再解析JSON
        return json.loads(rendered_str)
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return None
    except Exception as e:
        print(f"JSON模板渲染失败: {e}")
        return None


def create_template_environment(custom_filters: Dict[str, Any] = None, 
                              custom_functions: Dict[str, Any] = None) -> Environment:
    """
    创建自定义模板环境
    
    Args:
        custom_filters: 自定义过滤器
        custom_functions: 自定义函数
        
    Returns:
        Jinja2环境对象
    """
    env = Environment(loader=BaseLoader())
    
    # 添加自定义过滤器
    if custom_filters:
        for name, filter_func in custom_filters.items():
            env.filters[name] = filter_func
    
    # 添加自定义全局函数
    if custom_functions:
        for name, func in custom_functions.items():
            env.globals[name] = func
    
    return env


# 常用的模板过滤器
def upper_filter(value: str) -> str:
    """转大写过滤器"""
    return str(value).upper()


def lower_filter(value: str) -> str:
    """转小写过滤器"""
    return str(value).lower()


def json_filter(value: Any) -> str:
    """JSON序列化过滤器"""
    return json.dumps(value, ensure_ascii=False)


# 默认过滤器
DEFAULT_FILTERS = {
    'upper': upper_filter,
    'lower': lower_filter,
    'json': json_filter,
}


# 导出主要函数
__all__ = [
    'rend_template_any', 'render_template_string', 'render_template_dict',
    'render_template_list', 'extract_template_variables', 'validate_template_context',
    'render_with_functions', 'render_json_template', 'create_template_environment'
]
