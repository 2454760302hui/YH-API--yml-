#!/usr/bin/env python3
"""
API测试项目运行脚本
使用YH API测试框架执行测试
"""

import os
import sys
import yaml
import json
import time
from pathlib import Path
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

def load_config():
    """加载配置文件"""
    config_path = Path("config/test_config.yaml")
    if not config_path.exists():
        print(f"{Fore.RED}❌ 配置❌ ❌ 文件不存在，请检查文件路径是否正确
💡 提示：使用相对路径或绝对路径，请检查文件路径是否正确
💡 提示：使用相对路径或绝对路径: {config_path}{Style.RESET_ALL}")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_test_cases():
    """加载测试用例"""
    test_path = Path("tests/api_tests.yaml")
    if not test_path.exists():
        print(f"{Fore.RED}❌ 测试用例❌ ❌ 文件不存在，请检查文件路径是否正确
💡 提示：使用相对路径或绝对路径，请检查文件路径是否正确
💡 提示：使用相对路径或绝对路径: {test_path}{Style.RESET_ALL}")
        return None

    with open(test_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_tests():
    """运行测试"""
    print(f"{Fore.YELLOW + Style.BRIGHT}🚀 YH API测试框架 - 项目测试{Style.RESET_ALL}")
    print("=" * 60)

    # 加载配置
    config = load_config()
    if not config:
        return False

    # 加载测试用例
    test_cases = load_test_cases()
    if not test_cases:
        return False

    print(f"{Fore.CYAN}📋 项目信息:{Style.RESET_ALL}")
    print(f"  名称: {test_cases.get('project', {}).get('name', 'Unknown')}")
    print(f"  版本: {test_cases.get('project', {}).get('version', '1.0.0')}")
    print(f"  描述: {test_cases.get('project', {}).get('description', 'No description')}")

    print(f"\n{Fore.CYAN}🔧 配置信息:{Style.RESET_ALL}")
    print(f"  基础URL: {config.get('server', {}).get('base_url', 'Not configured')}")
    print(f"  超时时间: {config.get('server', {}).get('timeout', 30)}秒")
    print(f"  重试次数: {config.get('server', {}).get('retry_count', 3)}")

    # 检查是否安装了api-test-yh-pro
    try:
        # 尝试导入yh_shell模块
        sys.path.append('..')  # 添加上级目录到路径
        from yh_shell import YHShell

        print(f"\n{Fore.GREEN}✅ 检测到YH API测试框架{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚀 启动测试执行...{Style.RESET_ALL}")

        # 创建shell实例并运行测试
        shell = YHShell()
        shell.do_load("tests/api_tests.yaml")
        shell.do_run("")

        return True

    except ImportError:
        print(f"\n{Fore.YELLOW}⚠️  未检测到YH API测试框架{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📦 请先安装框架: pip install api-test-yh-pro{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 或者将此项目复制到框架目录中运行{Style.RESET_ALL}")

        # 提供手动运行指导
        print(f"\n{Fore.MAGENTA}📋 手动运行步骤:{Style.RESET_ALL}")
        print("1. 安装框架: pip install api-test-yh-pro")
        print("2. 启动框架: python -c \"from yh_shell import YHShell; YHShell().cmdloop()\"")
        print("3. 在框架中运行: load tests/api_tests.yaml")
        print("4. 执行测试: run")

        return False

def main():
    """主函数"""
    print(f"{Fore.MAGENTA + Style.BRIGHT}🌟 YH精神永存！{Style.RESET_ALL}")

    success = run_tests()

    if success:
        print(f"\n{Fore.GREEN + Style.BRIGHT}🎉 测试执行完成！{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 查看报告: reports/目录{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ 测试执行失败{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}\"持续改进，追求卓越！\" - YH精神{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
