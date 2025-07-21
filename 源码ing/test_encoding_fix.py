#!/usr/bin/env python3
"""
测试编码修复是否成功
"""

def test_encoding_fix():
    """测试编码修复"""
    print("🔍 测试编码修复结果")
    print("=" * 50)
    
    try:
        # 1. 测试文件读取
        print("1. 测试文件读取...")
        with open('swagger_docs.py', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ 文件读取成功，长度: {len(content)} 字符")
        
        # 2. 检查是否有问题字符
        print("\n2. 检查问题字符...")
        problem_chars = ['\x85', '\ufffd']
        found_problems = []
        
        for char in problem_chars:
            if char in content:
                found_problems.append(char)
        
        if found_problems:
            print(f"⚠️  发现问题字符: {found_problems}")
        else:
            print("✅ 未发现问题字符")
        
        # 3. 测试模块导入
        print("\n3. 测试模块导入...")
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("swagger_docs", "swagger_docs.py")
            module = importlib.util.module_from_spec(spec)
            print("✅ 模块规范创建成功")
            
            # 不执行模块，只检查语法
            with open('swagger_docs.py', 'r', encoding='utf-8') as f:
                code = f.read()
            
            compile(code, 'swagger_docs.py', 'exec')
            print("✅ 语法检查通过")
            
        except SyntaxError as e:
            print(f"❌ 语法错误: {e}")
        except Exception as e:
            print(f"⚠️  其他错误: {e}")
        
        # 4. 检查文件编码
        print("\n4. 检查文件编码...")
        import chardet
        
        with open('swagger_docs.py', 'rb') as f:
            raw_data = f.read()
        
        detected = chardet.detect(raw_data)
        print(f"检测到的编码: {detected}")
        
        if detected['encoding'].lower() in ['utf-8', 'ascii']:
            print("✅ 编码正确")
        else:
            print(f"⚠️  编码可能有问题: {detected['encoding']}")
        
        print("\n" + "=" * 50)
        print("🎉 编码修复验证完成！")
        
        if not found_problems:
            print("✅ 编码问题已完全修复")
            print("📝 建议：现在可以正常使用swagger_docs.py")
        else:
            print("⚠️  仍有一些问题需要处理")
        
        return len(found_problems) == 0
        
    except UnicodeDecodeError as e:
        print(f"❌ 编码错误仍然存在: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_encoding_fix()
    if success:
        print("\n🎊 编码修复成功！")
    else:
        print("\n❌ 编码修复失败，需要进一步处理")
