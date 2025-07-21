#!/usr/bin/env python3
"""
诊断Swagger UI显示问题
"""

import requests
import time

def diagnose_swagger_ui():
    """诊断Swagger UI显示问题"""
    ports = [8080, 8095, 8094]
    
    print("🔍 诊断Swagger UI显示问题")
    print("=" * 50)
    
    for port in ports:
        print(f"\n📋 测试端口 {port}")
        base_url = f"http://127.0.0.1:{port}"
        
        try:
            # 1. 测试健康检查
            health_response = requests.get(f"{base_url}/health", timeout=3)
            print(f"✅ 健康检查: {health_response.status_code}")
            
            # 2. 测试OpenAPI JSON
            openapi_response = requests.get(f"{base_url}/openapi.json", timeout=3)
            print(f"✅ OpenAPI JSON: {openapi_response.status_code}")
            
            if openapi_response.status_code == 200:
                openapi_data = openapi_response.json()
                print(f"   - OpenAPI版本: {openapi_data.get('openapi')}")
                print(f"   - API标题: {openapi_data.get('info', {}).get('title')}")
                print(f"   - 端点数量: {len(openapi_data.get('paths', {}))}")
            
            # 3. 测试文档页面
            docs_response = requests.get(f"{base_url}/docs", timeout=3)
            print(f"✅ 文档页面: {docs_response.status_code}")
            
            if docs_response.status_code == 200:
                content = docs_response.text
                print(f"   - 内容长度: {len(content)} 字符")
                
                # 检查关键元素
                checks = [
                    ("Swagger UI CSS", "swagger-ui.css" in content),
                    ("Swagger UI JS", "swagger-ui-bundle.js" in content),
                    ("SwaggerUIBundle", "SwaggerUIBundle" in content),
                    ("swagger-ui div", 'id="swagger-ui"' in content),
                    ("OpenAPI URL", "'/openapi.json'" in content),
                ]
                
                for check_name, check_result in checks:
                    status = "✅" if check_result else "❌"
                    print(f"   - {status} {check_name}")
                
                # 检查可能的问题
                if "BaseLayout" in content:
                    print("   - ⚠️  发现BaseLayout配置，可能导致显示问题")
                
                if content.count("layout:") > 1:
                    print("   - ⚠️  发现重复的layout配置")
            
            print(f"🌟 端口 {port} 测试完成")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ 端口 {port} 无法连接")
        except Exception as e:
            print(f"❌ 端口 {port} 测试失败: {e}")
    
    print(f"\n" + "=" * 50)
    print("🎯 诊断建议")
    print("=" * 50)
    
    print("1. 检查浏览器控制台是否有JavaScript错误")
    print("2. 检查网络是否能访问 unpkg.com CDN")
    print("3. 确认OpenAPI JSON格式正确")
    print("4. 检查Swagger UI配置是否有语法错误")
    
    print(f"\n💡 推荐测试步骤:")
    print("1. 打开浏览器开发者工具 (F12)")
    print("2. 访问 /docs 页面")
    print("3. 查看Console标签页的错误信息")
    print("4. 查看Network标签页的资源加载情况")

if __name__ == "__main__":
    diagnose_swagger_ui()
