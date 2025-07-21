#!/usr/bin/env python3
"""
测试OpenAPI规范生成
"""

import json
import sys
from swagger_docs import SwaggerDocsServer

def test_openapi_spec():
    """测试OpenAPI规范是否正确生成"""
    try:
        # 创建服务器实例
        server = SwaggerDocsServer(port=8084, host="127.0.0.1")
        
        # 确保初始化
        server._ensure_initialized()
        
        # 获取OpenAPI规范
        openapi_spec = server.app.openapi()
        
        print("OpenAPI规范生成成功！")
        print(f"OpenAPI版本: {openapi_spec.get('openapi', 'NOT SET')}")
        print(f"标题: {openapi_spec.get('info', {}).get('title', 'NOT SET')}")
        print(f"版本: {openapi_spec.get('info', {}).get('version', 'NOT SET')}")
        
        # 检查必要字段
        required_fields = ['openapi', 'info', 'paths']
        missing_fields = []
        
        for field in required_fields:
            if field not in openapi_spec:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ 缺少必要字段: {missing_fields}")
            return False
        
        # 检查OpenAPI版本格式
        openapi_version = openapi_spec.get('openapi', '')
        if not openapi_version.startswith('3.0'):
            print(f"❌ OpenAPI版本格式错误: {openapi_version}")
            return False
        
        print("✅ OpenAPI规范验证通过！")
        
        # 保存规范到文件以便检查
        with open('openapi_spec.json', 'w', encoding='utf-8') as f:
            json.dump(openapi_spec, f, indent=2, ensure_ascii=False)
        print("📄 OpenAPI规范已保存到 openapi_spec.json")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_openapi_spec()
    sys.exit(0 if success else 1)
