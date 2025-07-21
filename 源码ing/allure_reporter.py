#!/usr/bin/env python3
"""
Allure报告增强模块 - 性能优化版本
提供详细的接口测试报告功能，支持延迟导入以提高启动性能
"""

import json
import time
import os
import subprocess
import webbrowser
import platform
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# 全局变量用于缓存导入的模块
_allure_module = None
_requests_module = None

def get_allure_module():
    """获取allure模块（延迟导入）"""
    global _allure_module
    if _allure_module is None:
        try:
            import allure
            _allure_module = allure
            logger.debug("Allure模块已成功导入")
        except ImportError as e:
            logger.warning(f"Allure模块导入失败: {e}")
            _allure_module = False
    return _allure_module if _allure_module is not False else None

def get_requests_module():
    """获取requests模块（延迟导入）"""
    global _requests_module
    if _requests_module is None:
        try:
            import requests
            _requests_module = requests
            logger.debug("Requests模块已成功导入")
        except ImportError as e:
            logger.warning(f"Requests模块导入失败: {e}")
            _requests_module = False
    return _requests_module if _requests_module is not False else None

@dataclass
class AllureConfig:
    """Allure配置"""
    results_dir: str = "allure-results"
    report_dir: str = "allure-report"
    clean_results: bool = True
    generate_report: bool = True
    open_report: bool = False
    server_url: Optional[str] = None

class AllureReporter:
    """Allure报告器"""

    def __init__(self, config: AllureConfig = None):
        self.config = config or AllureConfig()
        self.allure = None
        self.requests = None
        self._initialized = False
        self.ensure_directories()

    def _ensure_initialized(self):
        """确保allure模块已初始化"""
        if not self._initialized:
            self.allure = get_allure_module()
            self.requests = get_requests_module()
            self._initialized = True
    
    def ensure_directories(self):
        """确保目录存在"""
        os.makedirs(self.config.results_dir, exist_ok=True)
        os.makedirs(self.config.report_dir, exist_ok=True)
    
    def report_api_test(self, test_name: str, test_config: Dict[str, Any],
                       response: Optional[Any] = None,
                       error: Optional[Exception] = None) -> Dict[str, Any]:
        """报告API测试结果"""
        self._ensure_initialized()

        # 如果allure可用，使用allure功能
        if self.allure:
            # 设置测试信息
            self.allure.dynamic.title(test_name)
            self.allure.dynamic.description(f"API接口测试: {test_config.get('description', test_name)}")

            # 添加标签
            method = test_config.get('method', 'GET').upper()
            url = test_config.get('url', '')

            self.allure.dynamic.tag(f"method:{method}")
            self.allure.dynamic.tag(f"api")

            if 'tags' in test_config:
                for tag in test_config['tags']:
                    self.allure.dynamic.tag(tag)
        
            # 设置严重程度
            severity = test_config.get('severity', 'normal')
            if severity == 'critical':
                self.allure.dynamic.severity(self.allure.severity_level.CRITICAL)
            elif severity == 'high':
                self.allure.dynamic.severity(self.allure.severity_level.CRITICAL)
            elif severity == 'medium':
                self.allure.dynamic.severity(self.allure.severity_level.NORMAL)
            elif severity == 'low':
                self.allure.dynamic.severity(self.allure.severity_level.MINOR)
            else:
                self.allure.dynamic.severity(self.allure.severity_level.NORMAL)

            # 添加链接
            if 'issue' in test_config:
                self.allure.dynamic.issue(test_config['issue'])

            if 'testcase' in test_config:
                self.allure.dynamic.testcase(test_config['testcase'])
        
        # 记录请求信息
        self._attach_request_info(test_config)
        
        # 记录响应信息
        if response:
            self._attach_response_info(response)
        
        # 记录错误信息
        if error:
            self._attach_error_info(error)
        
        # 生成测试结果
        result = {
            'test_name': test_name,
            'method': method,
            'url': url,
            'success': response is not None and error is None,
            'timestamp': time.time()
        }
        
        if response:
            result.update({
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'response_size': len(response.content)
            })
        
        if error:
            result['error'] = str(error)
        
        return result
    
    def _attach_request_info(self, test_config: Dict[str, Any]):
        """附加请求信息"""
        request_info = {
            'method': test_config.get('method', 'GET'),
            'url': test_config.get('url', ''),
            'headers': test_config.get('headers', {}),
            'params': test_config.get('params', {}),
        }
        
        if 'json' in test_config:
            request_info['json'] = test_config['json']
        elif 'data' in test_config:
            request_info['data'] = test_config['data']
        
        if 'files' in test_config:
            request_info['files'] = list(test_config['files'].keys()) if isinstance(test_config['files'], dict) else str(test_config['files'])
        
        self.allure.attach(
            json.dumps(request_info, indent=2, ensure_ascii=False),
            name="请求信息",
            attachment_type=self.allure.attachment_type.JSON
        )
    
    def _attach_response_info(self, response: Any):
        """附加响应信息"""
        # 响应基本信息
        response_info = {
            'status_code': response.status_code,
            'reason': response.reason,
            'headers': dict(response.headers),
            'elapsed': response.elapsed.total_seconds(),
            'url': response.url
        }
        
        self.allure.attach(
            json.dumps(response_info, indent=2, ensure_ascii=False),
            name="响应信息",
            attachment_type=self.allure.attachment_type.JSON
        )
        
        # 响应体
        content_type = response.headers.get('content-type', '').lower()
        
        if 'application/json' in content_type:
            try:
                json_data = response.json()
                self.allure.attach(
                    json.dumps(json_data, indent=2, ensure_ascii=False),
                    name="响应体 (JSON)",
                    attachment_type=self.allure.attachment_type.JSON
                )
            except:
                self.allure.attach(
                    response.text,
                    name="响应体 (文本)",
                    attachment_type=self.allure.attachment_type.TEXT
                )
        elif 'text/' in content_type or 'application/xml' in content_type:
            self.allure.attach(
                response.text,
                name="响应体 (文本)",
                attachment_type=self.allure.attachment_type.TEXT
            )
        elif 'image/' in content_type:
            self.allure.attach(
                response.content,
                name="响应体 (图片)",
                attachment_type=self.allure.attachment_type.PNG
            )
        else:
            # 二进制数据，显示前1000字节的十六进制
            hex_data = response.content[:1000].hex()
            self.allure.attach(
                hex_data,
                name="响应体 (十六进制)",
                attachment_type=self.allure.attachment_type.TEXT
            )
    
    def _attach_error_info(self, error: Exception):
        """附加错误信息"""
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.allure.attach(
            json.dumps(error_info, indent=2, ensure_ascii=False),
            name="错误信息",
            attachment_type=self.allure.attachment_type.JSON
        )
    
    def verify_status_code(self, response: Any, expected_code: int):
        """验证状态码"""
        self._ensure_initialized()
        if self.allure:
            with self.allure.step(f"验证响应状态码: {expected_code}"):
                actual_code = response.status_code
                assert actual_code == expected_code, f"期望状态码 {expected_code}, 实际状态码 {actual_code}"
        else:
            actual_code = response.status_code
            assert actual_code == expected_code, f"期望状态码 {expected_code}, 实际状态码 {actual_code}"

    def verify_response_time(self, response: Any, max_time: float):
        """验证响应时间"""
        self._ensure_initialized()
        if self.allure:
            with self.allure.step(f"验证响应时间: <= {max_time}s"):
                actual_time = response.elapsed.total_seconds()
                assert actual_time <= max_time, f"响应时间 {actual_time:.3f}s 超过限制 {max_time}s"
        else:
            actual_time = response.elapsed.total_seconds()
            assert actual_time <= max_time, f"响应时间 {actual_time:.3f}s 超过限制 {max_time}s"

    def verify_json_field(self, response: Any, field_path: str, expected_value: Any):
        """验证JSON字段"""
        self._ensure_initialized()
        try:
            json_data = response.json()
            actual_value = self._get_nested_value(json_data, field_path)
            assert actual_value == expected_value, f"字段 {field_path} 期望值 {expected_value}, 实际值 {actual_value}"
        except Exception as e:
            self.allure.attach(
                f"JSON字段验证失败: {str(e)}",
                name="验证错误",
                attachment_type=self.allure.attachment_type.TEXT
            )
            raise
    
    def verify_response_contains(self, response, text: str):
        """验证响应包含指定文本"""
        self._ensure_initialized()
        if self.allure:
            with self.allure.step(f"验证响应包含文本: {text}"):
                assert text in response.text, f"响应中未找到文本: {text}"
        else:
            assert text in response.text, f"响应中未找到文本: {text}"
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """获取嵌套字段值"""
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and key.isdigit():
                index = int(key)
                if 0 <= index < len(current):
                    current = current[index]
                else:
                    raise KeyError(f"列表索引 {index} 超出范围")
            else:
                raise KeyError(f"字段路径 {path} 中的 {key} 不存在")
        
        return current
    
    def generate_environment_info(self, env_info: Dict[str, str]):
        """生成环境信息文件"""
        env_file = os.path.join(self.config.results_dir, "environment.properties")
        
        with open(env_file, 'w', encoding='utf-8') as f:
            for key, value in env_info.items():
                f.write(f"{key}={value}\n")
    
    def generate_categories_file(self, categories: List[Dict[str, Any]]):
        """生成分类文件"""
        categories_file = os.path.join(self.config.results_dir, "categories.json")
        
        with open(categories_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)
    
    def add_custom_attachment(self, content: Union[str, bytes], name: str,
                            attachment_type: str = "text"):
        """添加自定义附件"""
        self._ensure_initialized()
        if self.allure:
            if attachment_type == "text":
                attachment_type = self.allure.attachment_type.TEXT
            elif attachment_type == "json":
                attachment_type = self.allure.attachment_type.JSON
            elif attachment_type == "png":
                attachment_type = self.allure.attachment_type.PNG
            self.allure.attach(content, name=name, attachment_type=attachment_type)
    
    def add_screenshot(self, screenshot_path: str, name: str = "截图"):
        """添加截图"""
        if os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as f:
                self.allure.attach(
                    f.read(),
                    name=name,
                    attachment_type=self.allure.attachment_type.PNG
                )
    
    def add_log_file(self, log_path: str, name: str = "日志文件"):
        """添加日志文件"""
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                self.allure.attach(
                    f.read(),
                    name=name,
                    attachment_type=self.allure.attachment_type.TEXT
                )

    def generate_and_open_report(self):
        """生成并打开Allure报告"""
        try:
            # 生成报告
            self.generate_report()

            # 打开报告
            if self.config.open_report:
                self.open_report()

        except Exception as e:
            logger.error(f"生成或打开Allure报告失败: {e}")

    def generate_report(self):
        """生成Allure报告"""
        try:
            # 检查allure命令是否可用
            result = subprocess.run(['allure', '--version'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.warning("Allure命令不可用，请安装Allure CLI")
                return False

            # 清理旧报告
            if self.config.clean_results and os.path.exists(self.config.report_dir):
                import shutil
                shutil.rmtree(self.config.report_dir)

            # 生成新报告
            cmd = ['allure', 'generate', self.config.results_dir,
                   '-o', self.config.report_dir, '--clean']

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                logger.info(f"Allure报告生成成功: {self.config.report_dir}")
                return True
            else:
                logger.error(f"Allure报告生成失败: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Allure报告生成超时")
            return False
        except FileNotFoundError:
            logger.error("未找到allure命令，请安装Allure CLI")
            return False
        except Exception as e:
            logger.error(f"生成Allure报告时发生错误: {e}")
            return False

    def open_report(self):
        """打开Allure报告"""
        try:
            index_file = os.path.join(self.config.report_dir, 'index.html')

            if not os.path.exists(index_file):
                logger.warning(f"报告文件不存在: {index_file}")
                return False

            # 获取绝对路径
            abs_path = os.path.abspath(index_file)

            # 根据操作系统打开文件
            system = platform.system().lower()

            if system == 'windows':
                os.startfile(abs_path)
            elif system == 'darwin':  # macOS
                subprocess.run(['open', abs_path])
            else:  # Linux
                subprocess.run(['xdg-open', abs_path])

            logger.info(f"已打开Allure报告: {abs_path}")
            return True

        except Exception as e:
            logger.error(f"打开Allure报告失败: {e}")
            # 备用方案：使用webbrowser
            try:
                webbrowser.open(f'file://{abs_path}')
                logger.info("使用默认浏览器打开报告")
                return True
            except Exception as e2:
                logger.error(f"使用浏览器打开报告也失败: {e2}")
                return False

    def serve_report(self, port: int = 8080):
        """启动Allure报告服务器"""
        try:
            cmd = ['allure', 'serve', self.config.results_dir, '-p', str(port)]

            logger.info(f"启动Allure报告服务器，端口: {port}")
            subprocess.Popen(cmd)

            # 等待服务器启动
            time.sleep(3)

            # 打开浏览器
            webbrowser.open(f'http://localhost:{port}')

            return True

        except Exception as e:
            logger.error(f"启动Allure报告服务器失败: {e}")
            return False

class AllureTestSuite:
    """Allure测试套件"""
    
    def __init__(self, suite_name: str, reporter: AllureReporter = None):
        self.suite_name = suite_name
        self.reporter = reporter or AllureReporter()
        self.test_results = []
    
    def run_test_suite(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """运行测试套件"""
        if self.reporter.allure:
            self.reporter.allure.dynamic.title(f"测试套件: {self.suite_name}")
        
        for test_case in test_cases:
            try:
                result = self._run_single_test(test_case)
                self.test_results.append(result)
            except Exception as e:
                logger.error(f"测试用例执行失败: {e}")
                self.test_results.append({
                    'test_name': test_case.get('name', 'Unknown'),
                    'success': False,
                    'error': str(e)
                })
        
        return self.test_results
    
    def _run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """运行单个测试"""
        test_name = test_case.get('name', 'API Test')
        
        with self.allure.step(f"执行测试: {test_name}"):
            # 这里应该调用实际的HTTP客户端执行请求
            # 为了示例，我们模拟一个响应
            
            # 实际实现中，这里应该是:
            # response = http_client.request(test_case['method'], test_case['url'], ...)
            # return self.reporter.report_api_test(test_name, test_case, response)
            
            return {
                'test_name': test_name,
                'success': True,
                'timestamp': time.time()
            }

# 便捷装饰器
def allure_api_test(title: str = None, description: str = None,
                   severity: str = 'normal', tags: List[str] = None):
    """Allure API测试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 这个装饰器需要在有allure实例的上下文中使用
            # 暂时简化实现，只执行原函数
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 便捷函数
def create_allure_reporter(results_dir: str = "allure-results", 
                          report_dir: str = "allure-report") -> AllureReporter:
    """创建Allure报告器"""
    config = AllureConfig(results_dir=results_dir, report_dir=report_dir)
    return AllureReporter(config)
