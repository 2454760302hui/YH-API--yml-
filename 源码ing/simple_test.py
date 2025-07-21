print("开始测试...")

try:
    with open('swagger_docs.py', 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"文件读取成功，长度: {len(content)}")
    
    # 检查语法
    compile(content, 'swagger_docs.py', 'exec')
    print("语法检查通过")
    
    print("编码修复成功！")
    
except UnicodeDecodeError as e:
    print(f"编码错误: {e}")
except SyntaxError as e:
    print(f"语法错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
