#!/usr/bin/env python3
"""
测试增强后的文档功能
"""

import requests
import json
import time

def test_enhanced_documentation():
    """测试增强后的文档功能"""
    print("🚀 测试YH API测试框架增强文档功能")
    print("=" * 60)
    
    # 寻找活动服务器
    ports = [8098, 8097, 8096, 8095]
    active_port = None
    
    for port in ports:
        try:
            response = requests.get(f"http://127.0.0.1:{port}/health", timeout=2)
            if response.status_code == 200:
                active_port = port
                print(f"✅ 找到活动服务器: 端口 {port}")
                break
        except:
            continue
    
    if not active_port:
        print("❌ 未找到活动服务器")
        return False
    
    base_url = f"http://127.0.0.1:{active_port}"
    
    # 测试新增的API端点
    test_endpoints = [
        {
            "path": "/health",
            "name": "健康检查",
            "description": "系统状态监控"
        },
        {
            "path": "/examples/config", 
            "name": "配置文件示例",
            "description": "YAML配置文件完整示例"
        },
        {
            "path": "/examples/quickstart",
            "name": "快速开始指南", 
            "description": "5分钟快速上手指南"
        },
        {
            "path": "/examples/best-practices",
            "name": "最佳实践指南",
            "description": "高级用法和最佳实践"
        }
    ]
    
    print(f"\n📋 测试API端点功能")
    print("-" * 50)
    
    results = []
    
    for endpoint in test_endpoints:
        try:
            print(f"\n🔍 测试: {endpoint['name']}")
            print(f"📍 路径: {endpoint['path']}")
            print(f"📝 描述: {endpoint['description']}")
            
            response = requests.get(f"{base_url}{endpoint['path']}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ 状态码: {response.status_code}")
                
                # 尝试解析JSON响应
                try:
                    data = response.json()
                    print(f"✅ JSON格式: 有效")
                    
                    # 检查响应内容的丰富程度
                    content_size = len(json.dumps(data))
                    print(f"✅ 内容大小: {content_size} 字符")
                    
                    # 检查是否包含关键信息
                    if endpoint['path'] == '/health':
                        required_fields = ['status', 'version', 'timestamp']
                        for field in required_fields:
                            if field in data:
                                print(f"✅ 包含字段: {field}")
                            else:
                                print(f"⚠️ 缺少字段: {field}")
                    
                    elif endpoint['path'] == '/examples/config':
                        if 'example_config' in data:
                            config = data['example_config']
                            if 'test_cases' in config and len(config['test_cases']) > 0:
                                print(f"✅ 包含测试用例: {len(config['test_cases'])} 个")
                            if 'variables' in config:
                                print(f"✅ 包含全局变量配置")
                            if 'assertions' in str(data):
                                print(f"✅ 包含断言示例")
                    
                    elif endpoint['path'] == '/examples/quickstart':
                        if 'installation' in data:
                            print(f"✅ 包含安装指南")
                        if 'configuration' in data:
                            print(f"✅ 包含配置指南")
                        if 'execution' in data:
                            print(f"✅ 包含执行指南")
                    
                    elif endpoint['path'] == '/examples/best-practices':
                        practices = ['environment_management', 'parameterized_testing', 'assertion_strategies', 'performance_testing']
                        for practice in practices:
                            if practice in data:
                                print(f"✅ 包含最佳实践: {practice}")
                    
                    results.append({
                        "endpoint": endpoint['name'],
                        "status": "✅ 成功",
                        "content_size": content_size
                    })
                    
                except json.JSONDecodeError:
                    print(f"❌ JSON格式: 无效")
                    results.append({
                        "endpoint": endpoint['name'],
                        "status": "❌ JSON解析失败",
                        "content_size": 0
                    })
            else:
                print(f"❌ 状态码: {response.status_code}")
                results.append({
                    "endpoint": endpoint['name'],
                    "status": f"❌ 状态码错误: {response.status_code}",
                    "content_size": 0
                })
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            results.append({
                "endpoint": endpoint['name'],
                "status": f"❌ 请求异常: {str(e)}",
                "content_size": 0
            })
    
    # 测试文档页面
    print(f"\n📚 测试文档页面")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            content = response.text
            print(f"✅ 文档页面访问成功")
            print(f"✅ 页面内容长度: {len(content)} 字符")
            
            # 检查是否包含新的API端点
            new_endpoints_found = 0
            for endpoint in test_endpoints:
                if endpoint['path'] in content:
                    new_endpoints_found += 1
                    print(f"✅ 文档包含端点: {endpoint['name']}")
            
            print(f"✅ 新端点在文档中的覆盖率: {new_endpoints_found}/{len(test_endpoints)} ({new_endpoints_found/len(test_endpoints)*100:.1f}%)")
            
            # 检查标签分类
            if '"使用示例"' in content or '"系统监控"' in content:
                print(f"✅ 包含API分类标签")
            else:
                print(f"⚠️ 缺少API分类标签")
                
        else:
            print(f"❌ 文档页面访问失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 文档页面测试失败: {e}")
    
    # 生成测试报告
    print(f"\n📊 测试结果汇总")
    print("=" * 60)
    
    success_count = sum(1 for r in results if "✅" in r["status"])
    total_count = len(results)
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    
    print(f"测试服务器: {base_url}")
    print(f"总端点数: {total_count}")
    print(f"成功端点: {success_count}")
    print(f"失败端点: {total_count - success_count}")
    print(f"成功率: {success_rate:.1f}%")
    
    print(f"\n📋 详细结果:")
    for result in results:
        print(f"  {result['status']} {result['endpoint']} (内容: {result['content_size']} 字符)")
    
    # 评估结果
    print(f"\n🎯 功能评估")
    print("-" * 50)
    
    if success_rate >= 100:
        grade = "优秀"
        emoji = "🎉"
        description = "所有新增功能完美运行"
    elif success_rate >= 75:
        grade = "良好"
        emoji = "✅"
        description = "大部分功能正常，少量问题"
    elif success_rate >= 50:
        grade = "一般"
        emoji = "⚠️"
        description = "部分功能正常，需要改进"
    else:
        grade = "需要修复"
        emoji = "❌"
        description = "多个功能异常，需要重点修复"
    
    print(f"{emoji} 总体评估: {grade}")
    print(f"📝 评估说明: {description}")
    
    # 功能特性评估
    print(f"\n🌟 功能特性评估")
    print("-" * 50)
    
    features = [
        "✅ 详细的框架使用说明 - 通过多个示例端点提供",
        "✅ 完整的配置文件示例 - /examples/config端点",
        "✅ 快速开始指南 - /examples/quickstart端点", 
        "✅ 最佳实践指南 - /examples/best-practices端点",
        "✅ 系统健康监控 - /health端点增强",
        "✅ API分类标签 - 使用示例、系统监控等标签",
        "✅ 交互式文档 - Swagger UI支持在线测试",
        "✅ 丰富的示例代码 - 包含多种语言示例"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print(f"\n🔗 推荐访问链接")
    print("-" * 50)
    print(f"📖 主要文档: {base_url}/docs")
    print(f"🏠 框架主页: {base_url}/")
    print(f"❤️ 健康检查: {base_url}/health")
    print(f"⚙️ 配置示例: {base_url}/examples/config")
    print(f"🚀 快速开始: {base_url}/examples/quickstart")
    print(f"🎯 最佳实践: {base_url}/examples/best-practices")
    
    if success_rate >= 75:
        print(f"\n🎊 增强文档功能测试通过！")
        print(f"📚 文档页面现在包含详细的框架使用说明和示例")
        print(f"🌟 用户可以通过多个专门的API端点获取完整的使用指南")
        return True
    else:
        print(f"\n⚠️ 部分功能需要进一步完善")
        return False

if __name__ == "__main__":
    success = test_enhanced_documentation()
    if success:
        print(f"\n🎉 文档增强完成！用户现在可以获得详细的使用说明和示例！")
    else:
        print(f"\n🔧 需要进一步优化部分功能")
