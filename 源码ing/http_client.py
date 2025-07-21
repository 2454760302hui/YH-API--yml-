"""
HTTP客户端模块

提供改进的HTTP请求功能，支持重试、超时、代理等配置。
"""

import time
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin, urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from logging_config import get_logger
from exceptions import RequestError, ConnectTimeout, MaxRetryError, ConnectError

log = get_logger()


class HttpClient:
    """HTTP客户端"""
    
    def __init__(self, 
                 base_url: Optional[str] = None,
                 timeout: int = 30,
                 retry_count: int = 3,
                 retry_backoff_factor: float = 0.3,
                 proxies: Optional[Dict[str, str]] = None,
                 verify_ssl: bool = True,
                 headers: Optional[Dict[str, str]] = None):
        """
        初始化HTTP客户端
        
        Args:
            base_url: 基础URL
            timeout: 超时时间（秒）
            retry_count: 重试次数
            retry_backoff_factor: 重试退避因子
            proxies: 代理配置
            verify_ssl: 是否验证SSL证书
            headers: 默认请求头
        """
        self.base_url = base_url
        self.timeout = timeout
        self.retry_count = retry_count
        self.verify_ssl = verify_ssl
        
        # 创建会话
        self.session = requests.Session()
        
        # 设置默认请求头
        if headers:
            self.session.headers.update(headers)
        
        # 设置代理
        if proxies:
            self.session.proxies.update(proxies)
        
        # 配置重试策略
        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=retry_backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        log.debug(f"创建HTTP客户端: base_url={base_url}, timeout={timeout}")
    
    def _build_url(self, url: str) -> str:
        """
        构建完整URL
        
        Args:
            url: 相对或绝对URL
            
        Returns:
            完整URL
        """
        if not url:
            raise RequestError("URL不能为空")
        
        # 如果是绝对URL，直接返回
        if url.startswith(('http://', 'https://')):
            return url
        
        # 如果没有base_url，抛出异常
        if not self.base_url:
            raise RequestError("相对URL需要设置base_url", url=url)
        
        # 拼接URL
        return urljoin(self.base_url, url)
    
    def _prepare_request_data(self, **kwargs) -> Dict[str, Any]:
        """
        准备请求数据
        
        Args:
            **kwargs: 请求参数
            
        Returns:
            处理后的请求参数
        """
        # 设置默认超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        # 设置SSL验证
        if 'verify' not in kwargs:
            kwargs['verify'] = self.verify_ssl
        
        return kwargs
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            url: 请求URL
            **kwargs: 其他请求参数
            
        Returns:
            响应对象
            
        Raises:
            RequestError: 请求失败时抛出
        """
        # 构建完整URL
        full_url = self._build_url(url)
        
        # 准备请求数据
        request_data = self._prepare_request_data(**kwargs)
        
        # 记录请求信息
        log.info(f"发送请求: {method} {full_url}")
        log.debug(f"请求参数: {request_data}")
        
        start_time = time.time()
        
        try:
            response = self.session.request(method, full_url, **request_data)
            
            # 计算响应时间
            response_time = time.time() - start_time
            
            # 添加响应时间到响应对象
            response.response_time = response_time
            
            # 记录响应信息
            log.info(f"收到响应: {response.status_code} ({response_time:.3f}s)")
            log.debug(f"响应头: {dict(response.headers)}")
            
            return response
            
        except requests.exceptions.Timeout as e:
            error_msg = f"请求超时: {method} {full_url}"
            log.error(error_msg)
            raise ConnectTimeout(error_msg, url=full_url, method=method)
        
        except requests.exceptions.ConnectionError as e:
            error_msg = f"连接错误: {method} {full_url}"
            log.error(f"{error_msg}: {str(e)}")
            raise ConnectError(error_msg, url=full_url, method=method)
        
        except requests.exceptions.RetryError as e:
            error_msg = f"达到最大重试次数: {method} {full_url}"
            log.error(f"{error_msg}: {str(e)}")
            raise MaxRetryError(error_msg, url=full_url, method=method)
        
        except Exception as e:
            error_msg = f"请求失败: {method} {full_url}"
            log.error(f"{error_msg}: {str(e)}")
            raise RequestError(error_msg, url=full_url, method=method)
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self.request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """发送POST请求"""
        return self.request('POST', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> requests.Response:
        """发送PUT请求"""
        return self.request('PUT', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        return self.request('DELETE', url, **kwargs)
    
    def patch(self, url: str, **kwargs) -> requests.Response:
        """发送PATCH请求"""
        return self.request('PATCH', url, **kwargs)
    
    def head(self, url: str, **kwargs) -> requests.Response:
        """发送HEAD请求"""
        return self.request('HEAD', url, **kwargs)
    
    def options(self, url: str, **kwargs) -> requests.Response:
        """发送OPTIONS请求"""
        return self.request('OPTIONS', url, **kwargs)
    
    def set_auth(self, auth: Union[tuple, requests.auth.AuthBase]) -> None:
        """
        设置认证信息
        
        Args:
            auth: 认证对象或(username, password)元组
        """
        self.session.auth = auth
        log.debug("设置认证信息")
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        设置请求头
        
        Args:
            headers: 请求头字典
        """
        self.session.headers.update(headers)
        log.debug(f"更新请求头: {headers}")
    
    def set_cookies(self, cookies: Dict[str, str]) -> None:
        """
        设置Cookie
        
        Args:
            cookies: Cookie字典
        """
        self.session.cookies.update(cookies)
        log.debug(f"更新Cookie: {list(cookies.keys())}")
    
    def clear_cookies(self) -> None:
        """清除所有Cookie"""
        self.session.cookies.clear()
        log.debug("清除所有Cookie")
    
    def close(self) -> None:
        """关闭会话"""
        self.session.close()
        log.debug("关闭HTTP会话")


# 为了向后兼容，提供HTTPClient别名
HTTPClient = HttpClient


class HttpClientFactory:
    """HTTP客户端工厂"""

    @staticmethod
    def create_from_config(env_name: Optional[str] = None) -> HttpClient:
        """
        从配置创建HTTP客户端

        Args:
            env_name: 环境名称

        Returns:
            HTTP客户端实例
        """
        from config import TestEnv

        # 使用默认配置
        env_config = TestEnv()

        return HttpClient(
            base_url=env_config.BASE_URL,
            timeout=getattr(env_config, 'TIMEOUT', 30),
            retry_count=getattr(env_config, 'RETRY_COUNT', 3),
            verify_ssl=True,
            headers={},
            proxies={}
        )
    
    @staticmethod
    def create_with_base_url(base_url: str, **kwargs) -> HttpClient:
        """
        使用基础URL创建HTTP客户端
        
        Args:
            base_url: 基础URL
            **kwargs: 其他配置参数
            
        Returns:
            HTTP客户端实例
        """
        return HttpClient(base_url=base_url, **kwargs)


def validate_url(url: str) -> bool:
    """
    验证URL格式
    
    Args:
        url: 待验证的URL
        
    Returns:
        是否为有效URL
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def build_query_string(params: Dict[str, Any]) -> str:
    """
    构建查询字符串
    
    Args:
        params: 参数字典
        
    Returns:
        查询字符串
    """
    if not params:
        return ""
    
    query_parts = []
    for key, value in params.items():
        if value is not None:
            if isinstance(value, (list, tuple)):
                for item in value:
                    query_parts.append(f"{key}={item}")
            else:
                query_parts.append(f"{key}={value}")
    
    return "&".join(query_parts)
