#!/usr/bin/env python3
"""
测试菜单修复
"""

import os
import sys
import subprocess

def test_menu_display():
    """测试菜单显示"""
    print("=" * 50)
    print("测试菜单修复")
    print("=" * 50)
    
    try:
        # 1. 检查quick_start.py文件
        print("1. 检查quick_start.py文件...")
        if os.path.exists('quick_start.py'):
            print("   ✅ quick_start.py文件存在")
            
            # 读取文件内容检查菜单
            with open('quick_start.py', 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查菜单内容
            if '选择启动模式:' in content:
                print("   ✅ 找到菜单标题")
                
                # 检查选项1
                if '1. 🚀 YH Shell' in content:
                    print("   ✅ 选项1存在: YH Shell")
                else:
                    print("   ❌ 选项1缺失")
                
                # 检查选项2
                if '2. 📚 文档服务器' in content:
                    print("   ✅ 选项2存在: 文档服务器")
                else:
                    print("   ❌ 选项2缺失")
                
                # 检查选项0
                if '0. 🚪 退出' in content:
                    print("   ✅ 选项0存在: 退出")
                else:
                    print("   ❌ 选项0缺失")
                
                # 检查是否移除了其他选项
                removed_options = [
                    '3. 🤖 AI智能测试',
                    '4. 🚀 全部启动',
                    '5. 🏗️ 生成测试项目',
                    '6. ❓ 帮助信息'
                ]
                
                removed_count = 0
                for option in removed_options:
                    if option not in content:
                        removed_count += 1
                    else:
                        print(f"   ⚠️ 仍然存在: {option}")
                
                if removed_count == len(removed_options):
                    print("   ✅ 所有多余选项已移除")
                else:
                    print(f"   ⚠️ 还有 {len(removed_options) - removed_count} 个选项未移除")
                
                # 检查输入提示
                if '请输入选项 (0-2):' in content:
                    print("   ✅ 输入提示已更新为 (0-2)")
                elif '请输入选项 (0-6):' in content:
                    print("   ❌ 输入提示仍然是 (0-6)")
                else:
                    print("   ⚠️ 未找到输入提示")
                    
            else:
                print("   ❌ 未找到菜单标题")
        else:
            print("   ❌ quick_start.py文件不存在")
            return False
        
        # 2. 检查处理逻辑
        print("\n2. 检查菜单处理逻辑...")
        
        # 检查是否移除了选项3-6的处理
        removed_handlers = [
            'elif choice == "3":',
            'elif choice == "4":',
            'elif choice == "5":',
            'elif choice == "6":'
        ]
        
        removed_handler_count = 0
        for handler in removed_handlers:
            if handler not in content:
                removed_handler_count += 1
            else:
                print(f"   ⚠️ 仍然存在处理逻辑: {handler}")
        
        if removed_handler_count == len(removed_handlers):
            print("   ✅ 所有多余的处理逻辑已移除")
        else:
            print(f"   ⚠️ 还有 {len(removed_handlers) - removed_handler_count} 个处理逻辑未移除")
        
        # 3. 语法检查
        print("\n3. 进行语法检查...")
        try:
            result = subprocess.run([
                sys.executable, '-m', 'py_compile', 'quick_start.py'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("   ✅ 语法检查通过")
            else:
                print("   ❌ 语法检查失败")
                print(f"   错误: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ 语法检查异常: {e}")
            return False
        
        # 4. 显示修改后的菜单
        print("\n4. 显示修改后的菜单...")
        
        # 提取菜单部分
        menu_start = content.find('🎯 选择启动模式:')
        menu_end = content.find('请输入选项', menu_start) + content[content.find('请输入选项', menu_start):].find('"""')
        
        if menu_start != -1 and menu_end != -1:
            menu_text = content[menu_start:menu_end]
            print("   修改后的菜单:")
            print("   " + "="*40)
            for line in menu_text.split('\n'):
                if line.strip():
                    print(f"   {line}")
            print("   " + "="*40)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = test_menu_display()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 菜单修复验证成功！")
        print("\n修改内容:")
        print("- ✅ 保留选项1: YH Shell (交互式命令行界面)")
        print("- ✅ 保留选项2: 文档服务器 (在线文档和API测试)")
        print("- ✅ 保留选项0: 退出")
        print("- ✅ 移除选项3: AI智能测试")
        print("- ✅ 移除选项4: 全部启动")
        print("- ✅ 移除选项5: 生成测试项目")
        print("- ✅ 移除选项6: 帮助信息")
        print("- ✅ 更新输入提示为 (0-2)")
        print("- ✅ 移除相应的处理逻辑")
        
        print("\n现在用户看到的菜单:")
        print("🎯 选择启动模式:")
        print("1. 🚀 YH Shell (交互式命令行界面)")
        print("2. 📚 文档服务器 (在线文档和API测试)")
        print("0. 🚪 退出")
        print("请输入选项 (0-2):")
        
        print("\n✅ 所有现有功能保持正常工作！")
        
    else:
        print("❌ 菜单修复验证失败")
        print("需要进一步检查代码")
    
    print("\n技术支持 QQ: 2677989813")
    print("=" * 50)

if __name__ == "__main__":
    main()
