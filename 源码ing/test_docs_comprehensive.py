#!/usr/bin/env python3
"""
YH API测试框架文档功能全面自测
测试要求：功能正常、页面跳转正常、无404、框架功能说明清晰、易用、功能完整
"""

import requests
import time
import json
from urllib.parse import urljoin

class DocsComprehensiveTest:
    def __init__(self, base_url="http://127.0.0.1:8095"):
        self.base_url = base_url
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0

    def log_test(self, test_name, status, details=""):
        """记录测试结果"""
        self.total_tests += 1
        if status:
            self.passed_tests += 1
            print(f"✅ {test_name}: 通过 {details}")
        else:
            print(f"❌ {test_name}: 失败 {details}")

        self.test_results.append({
            "test": test_name,
            "status": "✅ 通过" if status else "❌ 失败",
            "details": details
        })

    def test_basic_connectivity(self):
        """测试基础连接性"""
        print("\n🔍 1. 基础连接性测试")
        print("-" * 40)

        try:
            # 健康检查
            response = requests.get(f"{self.base_url}/health", timeout=5)
            self.log_test("健康检查", response.status_code == 200, f"状态码: {response.status_code}")

            # 主页访问
            response = requests.get(f"{self.base_url}/", timeout=5)
            self.log_test("主页访问", response.status_code == 200, f"状态码: {response.status_code}")

            # OpenAPI规范
            response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
            if response.status_code == 200:
                openapi_data = response.json()
                version = openapi_data.get('openapi', 'unknown')
                title = openapi_data.get('info', {}).get('title', 'unknown')
                paths_count = len(openapi_data.get('paths', {}))
                self.log_test("OpenAPI规范", True, f"版本: {version}, 标题: {title}, 端点: {paths_count}个")
            else:
                self.log_test("OpenAPI规范", False, f"状态码: {response.status_code}")

        except Exception as e:
            self.log_test("基础连接", False, f"连接失败: {e}")

    def test_docs_page_functionality(self):
        """测试文档页面功能"""
        print("\n📚 2. 文档页面功能测试")
        print("-" * 40)

        try:
            # 文档页面访问
            response = requests.get(f"{self.base_url}/docs", timeout=10)
            if response.status_code == 200:
                content = response.text
                self.log_test("文档页面访问", True, f"内容长度: {len(content)} 字符")

                # 检查关键元素
                key_elements = [
                    ("Swagger UI CSS", "swagger-ui.css" in content),
                    ("Swagger UI JavaScript", "swagger-ui-bundle.js" in content),
                    ("SwaggerUIBundle对象", "SwaggerUIBundle" in content),
                    ("文档容器", 'id="swagger-ui"' in content),
                    ("OpenAPI数据源", "'/openapi.json'" in content),
                    ("页面标题", "YH API测试框架" in content),
                    ("框架描述", "API测试框架" in content),
                ]

                for element_name, check_result in key_elements:
                    self.log_test(f"文档元素-{element_name}", check_result)

                # 检查是否有配置问题
                layout_count = content.count("layout:")
                if layout_count > 1:
                    self.log_test("Layout配置检查", False, f"发现{layout_count}个layout配置，可能冲突")
                else:
                    self.log_test("Layout配置检查", True, "配置正常")

            else:
                self.log_test("文档页面访问", False, f"状态码: {response.status_code}")

        except Exception as e:
            self.log_test("文档页面功能", False, f"测试失败: {e}")

    def test_navigation_and_links(self):
        """测试导航和链接"""
        print("\n🔗 3. 导航和链接测试")
        print("-" * 40)

        # 测试所有主要页面
        pages_to_test = [
            ("/", "主页"),
            ("/docs", "Swagger UI文档"),
            ("/redoc", "ReDoc文档"),
            ("/health", "健康检查"),
            ("/openapi.json", "OpenAPI规范"),
        ]

        for path, description in pages_to_test:
            try:
                response = requests.get(f"{self.base_url}{path}", timeout=5)
                success = response.status_code == 200
                self.log_test(f"页面访问-{description}", success, f"状态码: {response.status_code}")
            except Exception as e:
                self.log_test(f"页面访问-{description}", False, f"访问失败: {e}")

        # 测试静态资源（应该不返回404）
        static_resources = [
            ("/favicon.ico", "网站图标"),
            ("/manifest.json", "Web应用清单"),
            ("/flutter_service_worker.js", "Service Worker"),
        ]

        for path, description in static_resources:
            try:
                response = requests.get(f"{self.base_url}{path}", timeout=5)
                success = response.status_code in [200, 204]  # 200 OK 或 204 No Content 都可以
                self.log_test(f"静态资源-{description}", success, f"状态码: {response.status_code}")
            except Exception as e:
                self.log_test(f"静态资源-{description}", False, f"访问失败: {e}")

    def test_404_handling(self):
        """测试404错误处理"""
        print("\n🚫 4. 404错误处理测试")
        print("-" * 40)

        # 测试不存在的页面
        non_existent_pages = [
            ("/nonexistent-page", "不存在的页面"),
            ("/api/nonexistent", "不存在的API"),
            ("/docs/nonexistent", "不存在的文档页面"),
        ]

        for path, description in non_existent_pages:
            try:
                response = requests.get(f"{self.base_url}{path}", timeout=5)
                if response.status_code == 404:
                    # 检查是否返回友好的404页面
                    content = response.text
                    has_friendly_404 = "页面未找到" in content or "404" in content
                    self.log_test(f"404处理-{description}", has_friendly_404, "返回友好404页面")
                else:
                    self.log_test(f"404处理-{description}", False, f"状态码: {response.status_code}")
            except Exception as e:
                self.log_test(f"404处理-{description}", False, f"测试失败: {e}")

        # 测试不存在的静态资源
        non_existent_static = [
            ("/nonexistent.js", "不存在的JS文件"),
            ("/nonexistent.css", "不存在的CSS文件"),
            ("/nonexistent.png", "不存在的图片文件"),
        ]

        for path, description in non_existent_static:
            try:
                response = requests.get(f"{self.base_url}{path}", timeout=5)
                # 静态资源应该返回204 No Content 而不是404
                success = response.status_code == 204
                self.log_test(f"静态404处理-{description}", success, f"状态码: {response.status_code}")
            except Exception as e:
                self.log_test(f"静态404处理-{description}", False, f"测试失败: {e}")

    def test_content_quality(self):
        """测试内容质量"""
        print("\n📝 5. 内容质量测试")
        print("-" * 40)

        try:
            # 获取OpenAPI规范
            response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
            if response.status_code == 200:
                openapi_data = response.json()

                # 检查API标题和描述
                info = openapi_data.get('info', {})
                title = info.get('title', '')
                description = info.get('description', '')
                version = info.get('version', '')

                self.log_test("API标题", bool(title), f"标题: {title}")
                self.log_test("API描述", bool(description), f"描述长度: {len(description)} 字符")
                self.log_test("API版本", bool(version), f"版本: {version}")

                # 检查路径和操作
                paths = openapi_data.get('paths', {})
                if paths:
                    # 统计端点数量
                    endpoint_count = len(paths)
                    self.log_test("API端点数量", endpoint_count > 0, f"共 {endpoint_count} 个端点")

                    # 检查每个端点的文档质量
                    endpoints_with_description = 0
                    endpoints_with_responses = 0

                    for path, operations in paths.items():
                        for method, operation in operations.items():
                            if operation.get('description') or operation.get('summary'):
                                endpoints_with_description += 1
                            if operation.get('responses'):
                                endpoints_with_responses += 1

                    # 计算文档覆盖率
                    description_coverage = endpoints_with_description / endpoint_count * 100
                    response_coverage = endpoints_with_responses / endpoint_count * 100

                    self.log_test("端点描述覆盖率", description_coverage > 80,
                                 f"{description_coverage:.1f}% ({endpoints_with_description}/{endpoint_count})")
                    self.log_test("响应文档覆盖率", response_coverage > 80,
                                 f"{response_coverage:.1f}% ({endpoints_with_responses}/{endpoint_count})")
                else:
                    self.log_test("API端点检查", False, "未找到API端点")
            else:
                self.log_test("OpenAPI规范获取", False, f"状态码: {response.status_code}")

        except Exception as e:
            self.log_test("内容质量测试", False, f"测试失败: {e}")

    def test_user_experience(self):
        """测试用户体验"""
        print("\n👤 6. 用户体验测试")
        print("-" * 40)

        try:
            # 获取文档页面
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                content = response.text

                # 检查用户体验元素
                ux_elements = [
                    ("页面标题", "<title>" in content),
                    ("响应式设计", "meta name=\"viewport\"" in content),
                    ("CSS样式", "<style>" in content or "<link rel=\"stylesheet\"" in content),
                    ("JavaScript交互", "<script>" in content),
                    ("API分组", "tags:" in content or "标签" in content),
                    ("请求示例", "example" in content.lower() or "示例" in content),
                    ("响应示例", "response" in content.lower() or "响应" in content),
                ]

                for element_name, check_result in ux_elements:
                    self.log_test(f"用户体验-{element_name}", check_result)

                # 检查文档结构
                structure_elements = [
                    ("导航元素", "nav" in content.lower() or "navigation" in content.lower()),
                    ("搜索功能", "search" in content.lower() or "搜索" in content.lower()),
                    ("折叠功能", "collapse" in content.lower() or "expand" in content.lower()),
                    ("复制功能", "copy" in content.lower() or "复制" in content.lower()),
                ]

                for element_name, check_result in structure_elements:
                    self.log_test(f"文档结构-{element_name}", check_result)

            else:
                self.log_test("文档页面获取", False, f"状态码: {response.status_code}")

        except Exception as e:
            self.log_test("用户体验测试", False, f"测试失败: {e}")

    def test_framework_completeness(self):
        """测试框架功能完整性"""
        print("\n🧩 7. 框架功能完整性测试")
        print("-" * 40)

        # 核心功能列表
        core_features = [
            "测试用例配置", "参数引用", "断言验证", "并发测试",
            "报告生成", "AI智能测试", "健康检查"
        ]

        try:
            # 获取文档内容
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                content = response.text.lower()

                # 检查每个核心功能是否在文档中有描述
                for feature in core_features:
                    feature_lower = feature.lower()
                    has_feature = feature_lower in content
                    self.log_test(f"核心功能-{feature}", has_feature)

                # 获取OpenAPI规范检查更详细的功能
                response = requests.get(f"{self.base_url}/openapi.json", timeout=5)
                if response.status_code == 200:
                    openapi_data = response.json()
                    paths = openapi_data.get('paths', {})

                    # 检查是否有健康检查端点
                    has_health_endpoint = "/health" in paths
                    self.log_test("健康检查端点", has_health_endpoint)

                    # 检查是否有文档端点
                    has_docs_endpoint = "/docs" in paths or any("docs" in path for path in paths)
                    self.log_test("文档端点", has_docs_endpoint)

                    # 检查标签是否包含核心功能
                    tags = []
                    for path_data in paths.values():
                        for operation in path_data.values():
                            if 'tags' in operation:
                                tags.extend(operation['tags'])

                    unique_tags = set(tags)
                    self.log_test("功能标签", len(unique_tags) > 0, f"共 {len(unique_tags)} 个功能标签")

                else:
                    self.log_test("OpenAPI规范获取", False, f"状态码: {response.status_code}")
            else:
                self.log_test("文档页面获取", False, f"状态码: {response.status_code}")

        except Exception as e:
            self.log_test("框架功能完整性测试", False, f"测试失败: {e}")

    def generate_report(self):
        """生成测试报告"""
        print("\n📊 测试报告")
        print("=" * 50)

        # 计算通过率
        pass_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0

        print(f"总测试数: {self.total_tests}")
        print(f"通过测试: {self.passed_tests}")
        print(f"通过率: {pass_rate:.1f}%")

        # 按类别统计
        categories = {
            "基础连接性": [],
            "文档页面功能": [],
            "导航和链接": [],
            "404错误处理": [],
            "内容质量": [],
            "用户体验": [],
            "框架功能完整性": []
        }

        for result in self.test_results:
            test_name = result["test"]
            if test_name.startswith("健康检查") or test_name.startswith("主页") or test_name.startswith("OpenAPI规范"):
                categories["基础连接性"].append(result)
            elif test_name.startswith("文档元素") or test_name.startswith("Layout") or test_name.startswith("文档页面访问"):
                categories["文档页面功能"].append(result)
            elif test_name.startswith("页面访问") or test_name.startswith("静态资源-"):
                categories["导航和链接"].append(result)
            elif test_name.startswith("404处理") or test_name.startswith("静态404处理"):
                categories["404错误处理"].append(result)
            elif test_name.startswith("API") or test_name.startswith("端点"):
                categories["内容质量"].append(result)
            elif test_name.startswith("用户体验") or test_name.startswith("文档结构"):
                categories["用户体验"].append(result)
            elif test_name.startswith("核心功能") or test_name.startswith("健康检查端点") or test_name.startswith("文档端点") or test_name.startswith("功能标签"):
                categories["框架功能完整性"].append(result)

        # 打印分类结果
        for category, results in categories.items():
            if results:
                passed = sum(1 for r in results if "✅" in r["status"])
                total = len(results)
                rate = (passed / total) * 100 if total > 0 else 0

                print(f"\n{category} 测试结果: {passed}/{total} ({rate:.1f}%)")

                # 只显示失败的测试
                failures = [r for r in results if "❌" in r["status"]]
                if failures:
                    print("  失败的测试:")
                    for failure in failures:
                        print(f"  - ❌ {failure['test']}: {failure['details']}")

        # 总体评估
        print("\n🎯 总体评估")
        print("-" * 40)

        if pass_rate >= 90:
            print("✅ 优秀: 文档功能完善，用户体验良好，几乎没有问题")
        elif pass_rate >= 80:
            print("✅ 良好: 文档功能基本完善，有少量问题需要改进")
        elif pass_rate >= 70:
            print("⚠️ 一般: 文档功能可用，但有多处需要改进的地方")
        else:
            print("❌ 需要改进: 文档功能存在较多问题，需要重点改进")

        # 具体建议
        print("\n💡 改进建议:")
        if any("❌" in r["status"] for r in categories["基础连接性"]):
            print("- 检查服务器连接和基础API功能")
        if any("❌" in r["status"] for r in categories["文档页面功能"]):
            print("- 修复文档页面显示问题")
        if any("❌" in r["status"] for r in categories["导航和链接"]):
            print("- 确保所有页面和资源可正常访问")
        if any("❌" in r["status"] for r in categories["404错误处理"]):
            print("- 改进404错误处理机制")
        if any("❌" in r["status"] for r in categories["内容质量"]):
            print("- 完善API文档内容和描述")
        if any("❌" in r["status"] for r in categories["用户体验"]):
            print("- 优化文档页面的用户体验")
        if any("❌" in r["status"] for r in categories["框架功能完整性"]):
            print("- 补充框架核心功能的文档说明")

    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始YH API测试框架文档功能全面自测")
        print("=" * 50)
        print(f"测试目标: {self.base_url}")
        print("=" * 50)

        # 运行所有测试
        self.test_basic_connectivity()
        self.test_docs_page_functionality()
        self.test_navigation_and_links()
        self.test_404_handling()
        self.test_content_quality()
        self.test_user_experience()
        self.test_framework_completeness()

        # 生成报告
        self.generate_report()

        return self.passed_tests, self.total_tests

if __name__ == "__main__":
    # 测试所有可能的服务器
    servers = [
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8093",
        "http://127.0.0.1:8094",
        "http://127.0.0.1:8095",
    ]

    # 找到第一个可用的服务器
    active_server = None
    for server in servers:
        try:
            response = requests.get(f"{server}/health", timeout=2)
            if response.status_code == 200:
                active_server = server
                print(f"找到活动服务器: {server}")
                break
        except:
            continue

    if active_server:
        tester = DocsComprehensiveTest(active_server)
        passed, total = tester.run_all_tests()

        # 最终结论
        pass_rate = (passed / total) * 100 if total > 0 else 0
        if pass_rate >= 80:
            print("\n🎉 文档功能测试通过！可以投入使用。")
        else:
            print("\n⚠️ 文档功能测试未完全通过，建议修复问题后再使用。")
    else:
        print("❌ 未找到活动的服务器，请确保YH API测试框架服务器正在运行。")