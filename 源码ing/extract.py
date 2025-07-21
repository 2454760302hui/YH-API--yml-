from requests import Response
import jsonpath
import jmespath
import re
import exceptions
import json
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional, Union
from error_handler import handle_extraction_errors
from logging_config import get_logger
log = get_logger()


@handle_extraction_errors
def extract_by_ws(resp: Dict[str, Any], extract_expression: str) -> Any:
    """
    从 websocket 返回结果中提取数据

    Args:
        resp: websocket 返回结果字典，包含 status 和 recv 字段
        extract_expression: 提取表达式

    Returns:
        提取的值，可能是任意类型

    Raises:
        ExtractExpressionError: 提取失败时抛出
    """
    if not isinstance(extract_expression, str):
        return extract_expression
    if extract_expression in ["status_code", "status", "getstatus"]:
        return resp.get('status')
    elif extract_expression in ['text', 'body']:
        return resp.get('recv')
    elif extract_expression.startswith('$.'):
        try:
            response_parse_dict = json.loads(resp.get('recv'))
            return extract_by_jsonpath(response_parse_dict, extract_expression)
        except JSONDecodeError as msg:
            log.error(f"JSON解析失败，响应内容: {resp.get('recv')}")
            raise exceptions.ExtractExpressionError(f"JSON解析失败，返回的不是有效JSON格式: {msg}")
        except Exception as msg:
            log.error(f"JSONPath提取失败，表达式: {extract_expression}, 错误: {msg}")
            raise exceptions.ExtractExpressionError(f'JSONPath提取失败 - 表达式:<{extract_expression}>, 错误: {msg}')
    elif '.+?' in extract_expression or '.*?' in extract_expression:
        # 正则匹配
        return extract_by_regex(resp.get('recv'), extract_expression)
    elif 'body.' in extract_expression or 'content.' in extract_expression:
        try:
            response_parse_dict = json.loads(resp.get('recv'))
            return extract_by_jmespath({"body": response_parse_dict}, extract_expression)
        except JSONDecodeError as msg:
            log.error(f"JSON解析失败，响应内容: {resp.get('recv')}")
            raise exceptions.ExtractExpressionError(f"JSON解析失败，返回的不是有效JSON格式: {msg}")
        except Exception as msg:
            log.error(f"JMESPath提取失败，表达式: {extract_expression}, 错误: {msg}")
            raise exceptions.ExtractExpressionError(f'JMESPath提取失败 - 表达式:<{extract_expression}>, 错误: {msg}')
    else:
        # 其它非取值表达式，直接返回
        return extract_expression


@handle_extraction_errors
def extract_by_object(response: Union[Response, Dict[str, Any]], extract_expression: str) -> Any:
    """
    从 response 对象或字典中提取数据

    Args:
        response: Response 对象或字典
        extract_expression: 提取表达式，支持 status_code, url, ok, headers, cookies, text, body 等

    Returns:
        提取的值，可能是任意类型

    Raises:
        ExtractExpressionError: 提取失败时抛出
    """
    if not isinstance(extract_expression, str):
        return extract_expression
    if isinstance(response, dict):
        # ws 返回结果提取
        return extract_by_ws(response, extract_expression)
    res = {
        "headers": response.headers if response else {},
        "cookies": dict(response.cookies if response else {})
    }
    if extract_expression in ["status_code", "url", "ok", "encoding", "text"]:
        return getattr(response, extract_expression)
    elif extract_expression.startswith('headers') or extract_expression.startswith('cookies'):
        return extract_by_jmespath(res, extract_expression)
    elif extract_expression.startswith('body') or extract_expression.startswith('content'):
        try:
            response_parse_dict = response.json()
            return extract_by_jmespath({"body": response_parse_dict}, extract_expression)
        except Exception as msg:
            raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')
    elif extract_expression.startswith('$.'):
        try:
            response_parse_dict = response.json()
            return extract_by_jsonpath(response_parse_dict, extract_expression)
        except Exception as msg:
            raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')
    elif '.+?' in extract_expression or '.*?' in extract_expression:
        # 正则匹配
        return extract_by_regex(response.text, extract_expression)
    elif 'body.' in extract_expression or 'content.' in extract_expression:
        try:
            response_parse_dict = response.json()
            return extract_by_jmespath({"body": response_parse_dict}, extract_expression)
        except Exception as msg:
            raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')
    else:
        # 其它非取值表达式，直接返回
        return extract_expression


@handle_extraction_errors
def extract_by_jsonpath(extract_value: Dict[str, Any], extract_expression: str) -> Any:
    """
    使用 JSONPath 表达式提取数据

    Args:
        extract_value: 要提取数据的字典
        extract_expression: JSONPath 表达式，如 '$.code'

    Returns:
        提取的值：None（未找到）、单个值或值列表

    Raises:
        ExtractExpressionError: 提取失败时抛出
    """
    if not isinstance(extract_expression, str):
        return extract_expression
    extract_value = jsonpath.jsonpath(extract_value, extract_expression)
    if not extract_value:
        return
    elif len(extract_value) == 1:
        return extract_value[0]
    else:
        return extract_value


@handle_extraction_errors
def extract_by_jmespath(extract_obj: Dict[str, Any], extract_expression: str) -> Any:
    """
    使用 JMESPath 表达式提取数据

    Args:
        extract_obj: 要提取数据的字典，通常包含 body, cookies, headers 等字段
        extract_expression: JMESPath 表达式，如 'body.code'

    Returns:
        提取的值，未找到时返回 None

    Raises:
        ExtractExpressionError: 提取失败时抛出
    """
    if not isinstance(extract_expression, str):
        return extract_expression
    try:
        extract_value = jmespath.search(extract_expression, extract_obj)
        return extract_value
    except Exception as msg:
        raise exceptions.ExtractExpressionError(f'expression:<{extract_expression}>, error: {msg}')


@handle_extraction_errors
def extract_by_regex(extract_obj: str, extract_expression: str) -> Union[str, List[str]]:
    """
    使用正则表达式提取数据

    Args:
        extract_obj: 要提取数据的字符串，通常是 response.text
        extract_expression: 正则表达式

    Returns:
        提取的值：空字符串（未找到）、单个字符串或字符串列表

    Raises:
        ExtractExpressionError: 提取失败时抛出
    """
    if not isinstance(extract_expression, str):
        return extract_expression
    extract_value = re.findall(extract_expression, extract_obj, flags=re.S)
    if not extract_value:
        return ''
    elif len(extract_value) == 1:
        return extract_value[0]
    else:
        return extract_value
