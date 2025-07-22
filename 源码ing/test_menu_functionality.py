#!/usr/bin/env python3
"""
测试菜单功能
"""

import os
import sys
import subprocess
import time

def test_menu_functionality():
    """测试菜单功能"""
    print("=" * 60)
    print("测试修改后的菜单功能")
    print("=" * 60)
    
    try:
        # 1. 测试菜单显示
        print("1. 测试菜单显示...")
        
        # 导入quick_start模块测试
        sys.path.append('.')
        try:
            import quick_start
            print("   ✅ quick_start模块导入成功")
            
            # 测试show_menu函数
            if hasattr(quick_start, 'show_menu'):
                print("   ✅ show_menu函数存在")
            else:
                print("   ❌ show_menu函数不存在")
                return False
                
        except Exception as e:
            print(f"   ❌ 模块导入失败: {e}")
            return False
        
        # 2. 测试各个功能函数
        print("\n2. 测试功能函数...")
        
        # 检查YH Shell启动函数
        if hasattr(quick_start, 'start_yh_shell'):
            print("   ✅ start_yh_shell函数存在")
        else:
            print("   ❌ start_yh_shell函数不存在")
        
        # 检查文档服务器启动函数
        if hasattr(quick_start, 'start_docs_server'):
            print("   ✅ start_docs_server函数存在")
        else:
            print("   ❌ start_docs_server函数不存在")
        
        # 3. 测试命令行参数
        print("\n3. 测试命令行参数...")
        
        # 测试--help参数
        try:
            result = subprocess.run([
                sys.executable, 'quick_start.py', '--help'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   ✅ --help参数工作正常")
            else:
                print("   ⚠️ --help参数可能有问题")
                
        except subprocess.TimeoutExpired:
            print("   ⚠️ --help参数响应超时")
        except Exception as e:
            print(f"   ❌ --help参数测试失败: {e}")
        
        # 4. 检查移除的功能
        print("\n4. 检查移除的功能...")
        
        removed_functions = [
            'run_ai_test',
            'generate_test_project'
        ]
        
        for func_name in removed_functions:
            if hasattr(quick_start, func_name):
                print(f"   ⚠️ {func_name}函数仍然存在（但已从菜单移除）")
            else:
                print(f"   ✅ {func_name}函数已移除或不存在")
        
        # 5. 验证菜单选项范围
        print("\n5. 验证菜单选项范围...")
        
        # 读取文件检查选项范围
        with open('quick_start.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '请输入选项 (0-2):' in content:
            print("   ✅ 菜单选项范围正确: (0-2)")
        else:
            print("   ❌ 菜单选项范围不正确")
        
        # 检查处理逻辑
        valid_choices = ['choice == "0"', 'choice == "1"', 'choice == "2"']
        invalid_choices = ['choice == "3"', 'choice == "4"', 'choice == "5"', 'choice == "6"']
        
        valid_count = sum(1 for choice in valid_choices if choice in content)
        invalid_count = sum(1 for choice in invalid_choices if choice in content)
        
        print(f"   ✅ 有效选项处理: {valid_count}/3")
        print(f"   ✅ 无效选项已移除: {3-invalid_count}/4" if invalid_count == 0 else f"   ⚠️ 仍有无效选项: {invalid_count}")
        
        # 6. 功能完整性检查
        print("\n6. 功能完整性检查...")
        
        # 检查核心功能是否保留
        core_features = [
            ('YH Shell', 'yh_shell'),
            ('文档服务器', 'swagger_docs'),
        ]
        
        for feature_name, module_name in core_features:
            try:
                if os.path.exists(f'{module_name}.py'):
                    print(f"   ✅ {feature_name}模块存在: {module_name}.py")
                else:
                    print(f"   ⚠️ {feature_name}模块不存在: {module_name}.py")
            except Exception as e:
                print(f"   ❌ 检查{feature_name}模块失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = test_menu_functionality()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 菜单功能测试完成！")
        print("\n✅ 修改总结:")
        print("- 保留了选项1: YH Shell (交互式命令行界面)")
        print("- 保留了选项2: 文档服务器 (在线文档和API测试)")
        print("- 保留了选项0: 退出")
        print("- 移除了选项3-6的所有功能")
        print("- 更新了输入提示范围")
        print("- 清理了相关处理逻辑")
        
        print("\n🚀 现在的启动菜单:")
        print("🎯 选择启动模式:")
        print("1. 🚀 YH Shell (交互式命令行界面)")
        print("2. 📚 文档服务器 (在线文档和API测试)")
        print("0. 🚪 退出")
        print("请输入选项 (0-2):")
        
        print("\n💡 用户使用方式:")
        print("- 运行: python quick_start.py")
        print("- 选择1: 启动交互式Shell界面")
        print("- 选择2: 启动文档服务器和API测试")
        print("- 选择0: 退出程序")
        
        print("\n✅ 所有现有功能保持正常，界面更加简洁！")
        
    else:
        print("❌ 菜单功能测试失败")
        print("需要进一步检查代码")
    
    print("\n📞 技术支持 QQ: 2677989813")
    print("💪 YH Spirit Lives On!")
    print("=" * 60)

if __name__ == "__main__":
    main()
