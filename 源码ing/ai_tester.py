#!/usr/bin/env python3
"""
AI智能测试模块
基于AI的智能API测试生成和执行
"""

import json
import requests
import random
import time
from dataclasses import dataclass
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

@dataclass
class AITestConfig:
    """AI测试配置"""
    target_url: str
    test_depth: str = "basic"  # basic, medium, deep
    test_types: List[str] = None
    max_tests: int = 10
    include_edge_cases: bool = True
    include_security_tests: bool = False
    
    def __post_init__(self):
        if self.test_types is None:
            self.test_types = ["functional", "boundary", "negative"]

class AITester:
    """AI智能测试器"""
    
    def __init__(self):
        self.test_patterns = self._load_test_patterns()
        self.generated_tests = []
        
    def _load_test_patterns(self) -> Dict[str, Any]:
        """加载测试模式"""
        return {
            "http_methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            "common_endpoints": [
                "/api/users", "/api/user/{id}", "/api/login", "/api/logout",
                "/api/products", "/api/product/{id}", "/api/orders", "/api/order/{id}",
                "/health", "/status", "/version", "/info"
            ],
            "test_data_patterns": {
                "user": {
                    "valid": {"name": "张三", "email": "zhangsan@example.com", "age": 25},
                    "invalid": {"name": "", "email": "invalid-email", "age": -1},
                    "boundary": {"name": "a" * 255, "email": "test@" + "a" * 250 + ".com", "age": 150}
                },
                "product": {
                    "valid": {"name": "iPhone 15", "price": 8999.99, "category": "手机"},
                    "invalid": {"name": "", "price": -100, "category": None},
                    "boundary": {"name": "a" * 1000, "price": 999999999.99, "category": ""}
                }
            },
            "validation_rules": {
                "status_codes": [200, 201, 400, 401, 403, 404, 422, 500],
                "response_time": {"max": 5000, "warning": 2000},
                "content_types": ["application/json", "text/html", "text/plain"]
            }
        }
    
    def analyze_api_structure(self, base_url: str) -> Dict[str, Any]:
        """分析API结构"""
        print(f"🔍 正在分析API结构: {base_url}")

        analysis = {
            "base_url": base_url,
            "discovered_endpoints": [],
            "supported_methods": {},
            "response_patterns": {},
            "error_patterns": {},
            "security_headers": {}
        }

        # 首先尝试根路径
        try:
            root_response = requests.get(base_url, timeout=10)
            print(f"✅ 根路径响应: {root_response.status_code}")

            # 检查是否有API文档或OpenAPI规范
            if 'json' in root_response.headers.get('content-type', '').lower():
                try:
                    root_data = root_response.json()
                    if 'swagger' in root_data or 'openapi' in root_data:
                        print("🎯 发现OpenAPI/Swagger文档")
                        return self._analyze_openapi_spec(root_data, base_url)
                except:
                    pass

        except Exception as e:
            print(f"⚠️  根路径访问失败: {e}")

        # 尝试发现常见端点
        print("🔎 扫描常见API端点...")
        discovered_count = 0

        for endpoint in self.test_patterns["common_endpoints"]:
            try:
                url = urljoin(base_url, endpoint)
                response = requests.get(url, timeout=5, allow_redirects=True)

                if response.status_code < 500:  # 不是服务器错误
                    discovered_count += 1
                    endpoint_info = {
                        "endpoint": endpoint,
                        "url": url,
                        "status_code": response.status_code,
                        "content_type": response.headers.get("content-type", ""),
                        "response_size": len(response.content),
                        "response_time": response.elapsed.total_seconds()
                    }

                    analysis["discovered_endpoints"].append(endpoint_info)
                    print(f"  ✅ {endpoint} -> {response.status_code}")

                    # 分析支持的方法
                    methods = self._detect_supported_methods(url)
                    analysis["supported_methods"][endpoint] = methods

                    # 分析响应模式
                    if response.headers.get("content-type", "").startswith("application/json"):
                        try:
                            json_data = response.json()
                            analysis["response_patterns"][endpoint] = self._analyze_json_structure(json_data)
                        except:
                            pass

                    # 分析安全头
                    security_headers = self._analyze_security_headers(response.headers)
                    analysis["security_headers"][endpoint] = security_headers
                else:
                    print(f"  ❌ {endpoint} -> {response.status_code}")

            except Exception as e:
                print(f"  ⚠️  {endpoint} -> 连接失败")
                continue

        print(f"🎯 发现 {discovered_count} 个可用端点")
        return analysis

    def _analyze_openapi_spec(self, spec_data: Dict[str, Any], base_url: str) -> Dict[str, Any]:
        """分析OpenAPI规范"""
        analysis = {
            "base_url": base_url,
            "discovered_endpoints": [],
            "supported_methods": {},
            "response_patterns": {},
            "error_patterns": {},
            "security_headers": {},
            "openapi_info": spec_data.get("info", {})
        }

        paths = spec_data.get("paths", {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    endpoint_info = {
                        "endpoint": path,
                        "url": urljoin(base_url, path.lstrip('/')),
                        "method": method.upper(),
                        "summary": details.get("summary", ""),
                        "description": details.get("description", ""),
                        "parameters": details.get("parameters", []),
                        "responses": details.get("responses", {})
                    }
                    analysis["discovered_endpoints"].append(endpoint_info)

                    if path not in analysis["supported_methods"]:
                        analysis["supported_methods"][path] = []
                    analysis["supported_methods"][path].append(method.upper())

        return analysis

    def _detect_supported_methods(self, url: str) -> List[str]:
        """检测支持的HTTP方法"""
        supported = []
        
        for method in self.test_patterns["http_methods"]:
            try:
                response = requests.request(method, url, timeout=3)
                if response.status_code != 405:  # Method Not Allowed
                    supported.append(method)
            except:
                continue
                
        return supported
    
    def _analyze_json_structure(self, data: Any) -> Dict[str, Any]:
        """分析JSON结构"""
        if isinstance(data, dict):
            return {
                "type": "object",
                "fields": {k: self._analyze_json_structure(v) for k, v in data.items()},
                "field_count": len(data)
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "item_type": self._analyze_json_structure(data[0]) if data else None
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:100] if len(str(data)) > 100 else str(data)
            }
    
    def _analyze_security_headers(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """分析安全头"""
        security_headers = [
            "X-Frame-Options", "X-Content-Type-Options", "X-XSS-Protection",
            "Strict-Transport-Security", "Content-Security-Policy",
            "X-Permitted-Cross-Domain-Policies", "Referrer-Policy"
        ]
        
        found_headers = {}
        for header in security_headers:
            if header.lower() in [h.lower() for h in headers.keys()]:
                found_headers[header] = headers.get(header, "")
        
        return {
            "found_headers": found_headers,
            "security_score": len(found_headers) / len(security_headers) * 100
        }
    
    def generate_smart_tests(self, config: AITestConfig) -> List[Dict[str, Any]]:
        """生成智能测试用例"""
        logger.info(f"开始生成智能测试用例，目标: {config.target_url}")
        
        # 分析API结构
        api_analysis = self.analyze_api_structure(config.target_url)
        
        tests = []
        
        # 为每个发现的端点生成测试
        for endpoint_info in api_analysis["discovered_endpoints"]:
            endpoint = endpoint_info["endpoint"]
            supported_methods = api_analysis["supported_methods"].get(endpoint, ["GET"])
            
            # 生成功能测试
            if "functional" in config.test_types:
                tests.extend(self._generate_functional_tests(
                    config.target_url, endpoint, supported_methods
                ))
            
            # 生成边界测试
            if "boundary" in config.test_types:
                tests.extend(self._generate_boundary_tests(
                    config.target_url, endpoint, supported_methods
                ))
            
            # 生成负面测试
            if "negative" in config.test_types:
                tests.extend(self._generate_negative_tests(
                    config.target_url, endpoint, supported_methods
                ))
            
            # 生成安全测试
            if config.include_security_tests:
                tests.extend(self._generate_security_tests(
                    config.target_url, endpoint, supported_methods
                ))
        
        # 限制测试数量
        if len(tests) > config.max_tests:
            tests = random.sample(tests, config.max_tests)
        
        self.generated_tests = tests
        return tests

    def generate_test_cases(self, config: AITestConfig) -> List[Dict[str, Any]]:
        """生成测试用例 - generate_smart_tests的别名"""
        return self.generate_smart_tests(config)

    def execute_tests(self, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """执行测试用例 - execute_smart_tests的别名"""
        return self.execute_smart_tests(tests)

    def _generate_functional_tests(self, base_url: str, endpoint: str, methods: List[str]) -> List[Dict[str, Any]]:
        """生成功能测试"""
        tests = []
        
        for method in methods:
            test = {
                "name": f"功能测试_{method}_{endpoint.replace('/', '_')}",
                "method": method,
                "url": urljoin(base_url, endpoint),
                "description": f"测试 {endpoint} 端点的 {method} 方法基本功能",
                "validate": [
                    {"check": "status_code", "expect": [200, 201, 204]},
                    {"check": "response_time", "expect": {"max": 5000}}
                ]
            }
            
            # 根据方法添加请求数据
            if method in ["POST", "PUT", "PATCH"]:
                if "user" in endpoint.lower():
                    test["json"] = self.test_patterns["test_data_patterns"]["user"]["valid"]
                elif "product" in endpoint.lower():
                    test["json"] = self.test_patterns["test_data_patterns"]["product"]["valid"]
                else:
                    test["json"] = {"name": "测试数据", "value": "test_value"}
            
            tests.append(test)
        
        return tests
    
    def _generate_boundary_tests(self, base_url: str, endpoint: str, methods: List[str]) -> List[Dict[str, Any]]:
        """生成边界测试"""
        tests = []
        
        for method in methods:
            if method in ["POST", "PUT", "PATCH"]:
                test = {
                    "name": f"边界测试_{method}_{endpoint.replace('/', '_')}",
                    "method": method,
                    "url": urljoin(base_url, endpoint),
                    "description": f"测试 {endpoint} 端点的 {method} 方法边界条件",
                    "validate": [
                        {"check": "status_code", "expect": [200, 201, 400, 422]}
                    ]
                }
                
                # 添加边界数据
                if "user" in endpoint.lower():
                    test["json"] = self.test_patterns["test_data_patterns"]["user"]["boundary"]
                elif "product" in endpoint.lower():
                    test["json"] = self.test_patterns["test_data_patterns"]["product"]["boundary"]
                else:
                    test["json"] = {"name": "a" * 1000, "value": "x" * 10000}
                
                tests.append(test)
        
        return tests
    
    def _generate_negative_tests(self, base_url: str, endpoint: str, methods: List[str]) -> List[Dict[str, Any]]:
        """生成负面测试"""
        tests = []
        
        for method in methods:
            # 测试无效数据
            if method in ["POST", "PUT", "PATCH"]:
                test = {
                    "name": f"负面测试_无效数据_{method}_{endpoint.replace('/', '_')}",
                    "method": method,
                    "url": urljoin(base_url, endpoint),
                    "description": f"测试 {endpoint} 端点的 {method} 方法对无效数据的处理",
                    "validate": [
                        {"check": "status_code", "expect": [400, 422]}
                    ]
                }
                
                # 添加无效数据
                if "user" in endpoint.lower():
                    test["json"] = self.test_patterns["test_data_patterns"]["user"]["invalid"]
                elif "product" in endpoint.lower():
                    test["json"] = self.test_patterns["test_data_patterns"]["product"]["invalid"]
                else:
                    test["json"] = {"name": "", "value": None}
                
                tests.append(test)
            
            # 测试不存在的资源
            if "{id}" in endpoint:
                test = {
                    "name": f"负面测试_不存在资源_{method}_{endpoint.replace('/', '_')}",
                    "method": method,
                    "url": urljoin(base_url, endpoint.replace("{id}", "999999")),
                    "description": f"测试访问不存在的资源",
                    "validate": [
                        {"check": "status_code", "expect": [404]}
                    ]
                }
                tests.append(test)
        
        return tests
    
    def _generate_security_tests(self, base_url: str, endpoint: str, methods: List[str]) -> List[Dict[str, Any]]:
        """生成安全测试"""
        tests = []
        
        # SQL注入测试
        for method in methods:
            if method in ["GET", "POST"]:
                test = {
                    "name": f"安全测试_SQL注入_{method}_{endpoint.replace('/', '_')}",
                    "method": method,
                    "url": urljoin(base_url, endpoint),
                    "description": f"测试 {endpoint} 端点的SQL注入防护",
                    "validate": [
                        {"check": "status_code", "expect": [400, 403, 500]},
                        {"check": "response_not_contains", "expect": ["error", "sql", "database"]}
                    ]
                }
                
                if method == "GET":
                    test["params"] = {"id": "1' OR '1'='1"}
                else:
                    test["json"] = {"id": "1' OR '1'='1", "name": "'; DROP TABLE users; --"}
                
                tests.append(test)
        
        return tests
    
    def run_ai_tests(self, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """运行AI生成的测试"""
        logger.info(f"开始运行 {len(tests)} 个AI生成的测试")
        
        results = {
            "total_tests": len(tests),
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat(),
            "test_results": []
        }
        
        for i, test in enumerate(tests, 1):
            logger.info(f"运行测试 {i}/{len(tests)}: {test['name']}")
            
            try:
                result = self._execute_single_test(test)
                results["test_results"].append(result)
                
                if result["status"] == "passed":
                    results["passed"] += 1
                elif result["status"] == "failed":
                    results["failed"] += 1
                else:
                    results["errors"] += 1
                    
            except Exception as e:
                logger.error(f"测试执行异常: {e}")
                results["test_results"].append({
                    "name": test["name"],
                    "status": "error",
                    "error": str(e),
                    "execution_time": 0
                })
                results["errors"] += 1
        
        results["end_time"] = datetime.now().isoformat()
        results["success_rate"] = results["passed"] / results["total_tests"] * 100
        
        return results
    
    def _execute_single_test(self, test: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个测试"""
        start_time = time.time()
        
        try:
            # 准备请求参数
            kwargs = {
                "timeout": 10,
                "headers": test.get("headers", {}),
            }
            
            if "params" in test:
                kwargs["params"] = test["params"]
            if "json" in test:
                kwargs["json"] = test["json"]
            if "data" in test:
                kwargs["data"] = test["data"]
            
            # 发送请求
            response = requests.request(
                test["method"],
                test["url"],
                **kwargs
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            # 验证响应
            validation_results = self._validate_response(response, test.get("validate", []), execution_time)
            
            return {
                "name": test["name"],
                "status": "passed" if validation_results["all_passed"] else "failed",
                "response_code": response.status_code,
                "response_time": execution_time,
                "validations": validation_results["results"],
                "response_size": len(response.content),
                "url": test["url"],
                "method": test["method"]
            }
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "name": test["name"],
                "status": "error",
                "error": str(e),
                "execution_time": execution_time,
                "url": test["url"],
                "method": test["method"]
            }
    
    def _validate_response(self, response, validations: List[Dict], execution_time: float) -> Dict[str, Any]:
        """验证响应"""
        results = []
        all_passed = True
        
        for validation in validations:
            check_type = validation["check"]
            expected = validation["expect"]
            
            if check_type == "status_code":
                actual = response.status_code
                if isinstance(expected, list):
                    passed = actual in expected
                else:
                    passed = actual == expected
                    
            elif check_type == "response_time":
                actual = execution_time
                if isinstance(expected, dict) and "max" in expected:
                    passed = actual <= expected["max"]
                else:
                    passed = actual <= expected
                    
            elif check_type == "response_contains":
                actual = response.text
                passed = expected in actual
                
            elif check_type == "response_not_contains":
                actual = response.text
                if isinstance(expected, list):
                    passed = not any(item in actual for item in expected)
                else:
                    passed = expected not in actual
                    
            else:
                passed = True
                actual = "未知验证类型"
            
            results.append({
                "check": check_type,
                "expected": expected,
                "actual": actual,
                "passed": passed
            })
            
            if not passed:
                all_passed = False
        
        return {
            "all_passed": all_passed,
            "results": results
        }
    
    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """生成测试报告"""
        report = f"""
# 🤖 AI智能测试报告

## 测试概览
- **总测试数**: {results['total_tests']}
- **通过数**: {results['passed']} ✅
- **失败数**: {results['failed']} ❌
- **错误数**: {results['errors']} 🚫
- **成功率**: {results['success_rate']:.1f}%
- **开始时间**: {results['start_time']}
- **结束时间**: {results['end_time']}

## 详细结果

"""
        
        for result in results["test_results"]:
            status_icon = "✅" if result["status"] == "passed" else "❌" if result["status"] == "failed" else "🚫"
            
            report += f"""
### {status_icon} {result['name']}
- **状态**: {result['status']}
- **URL**: {result['url']}
- **方法**: {result['method']}
- **响应码**: {result.get('response_code', 'N/A')}
- **响应时间**: {result.get('response_time', 0):.2f}ms
- **响应大小**: {result.get('response_size', 0)} bytes

"""
            
            if "validations" in result:
                report += "**验证结果**:\n"
                for validation in result["validations"]:
                    check_icon = "✅" if validation["passed"] else "❌"
                    report += f"- {check_icon} {validation['check']}: 期望 {validation['expected']}, 实际 {validation['actual']}\n"
            
            if "error" in result:
                report += f"**错误信息**: {result['error']}\n"
            
            report += "\n"
        
        return report

def main():
    """主函数 - 用于测试"""
    # 创建AI测试器
    ai_tester = AITester()

    # 配置测试
    config = AITestConfig(
        target_url="https://httpbin.org",
        test_depth="basic",
        test_types=["functional", "negative"],
        max_tests=5
    )

    # 运行完整AI测试
    result = ai_tester.run_full_ai_test("https://httpbin.org", config)

    if result["success"]:
        print(f"🎉 AI测试成功完成！")
    else:
        print(f"❌ AI测试失败: {result['message']}")

def run_full_ai_test(self, target_url: str, config: AITestConfig = None) -> Dict[str, Any]:
    """运行完整的AI测试流程"""
    if config is None:
        config = AITestConfig(target_url=target_url)

    print(f"🤖 开始AI智能测试: {target_url}")
    print("=" * 60)

    # 第1步：分析API结构
    print("📊 第1步：分析API结构")
    analysis = self.analyze_api_structure(target_url)

    if not analysis["discovered_endpoints"]:
        print("❌ 未发现可用的API端点")
        return {
            "success": False,
            "message": "未发现可用的API端点",
            "analysis": analysis
        }

    # 第2步：生成智能测试用例
    print(f"\n🧠 第2步：生成智能测试用例")
    tests = self.generate_smart_tests(config)
    print(f"✅ 生成了 {len(tests)} 个测试用例")

    # 第3步：执行测试
    print(f"\n🚀 第3步：执行测试用例")
    results = self.run_ai_tests(tests)

    # 第4步：生成报告
    print(f"\n📋 第4步：生成测试报告")
    report = self.generate_test_report(results)

    # 保存报告
    report_file = f"ai_test_report_{int(time.time())}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ 测试完成！报告已保存到: {report_file}")
    print(f"📊 结果: {results['passed']}/{results['total_tests']} 通过")

    return {
        "success": True,
        "analysis": analysis,
        "tests": tests,
        "results": results,
        "report_file": report_file
    }

# 将方法添加到AITester类
AITester.run_full_ai_test = run_full_ai_test

if __name__ == "__main__":
    main()
