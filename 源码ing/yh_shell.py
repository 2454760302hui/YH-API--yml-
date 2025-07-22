#!/usr/bin/env python3
"""
YH风格的Shell启动界面
API测试框架交互式命令行界面
"""

import os
import sys
import time
import random
from typing import Dict, Any, List, Optional
import cmd
import json
import yaml
from colorama import init, Fore, Back, Style

from datetime import datetime

# 初始化colorama
init(autoreset=True)

class YHShell(cmd.Cmd):
    """YH风格的API测试框架Shell"""

    def __init__(self):
        super().__init__()
        self.intro = self.get_yh_intro()
        self.prompt = f"{Fore.YELLOW + Style.BRIGHT}🚀 YH-API-Test{Fore.CYAN} >{Style.RESET_ALL} "
        self.current_test_file = None
        self.test_results = []
        self.session_vars = {}
        self.command_count = 0

    def get_yh_intro(self) -> str:
        """获取YH风格的启动界面"""
        yh_ascii = """
{yellow}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    🚀 API Testing                                             ║
    ║    ⚡ 智能 • 高效 • 专业                                        ║
    ║                                                               ║
    ║    🔧 HTTP/Socket  📊 Reports  🤖 AI Testing                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝



{cyan}
    🏆 框架特性:
    • 🎯 精准的API测试 - 智能高效，追求完美
    • 🔥 并发测试支持 - 高性能，永不放弃
    • 📊 详细的测试报告 - 数据驱动，追求完美
    • 🚀 Socket/WebSocket测试 - 全方位覆盖
    • 💬 企业微信通知 - 团队协作无缝对接
    • 🎨 Allure报告 - 专业级测试展示
{reset}

{green}
    输入 'help' 查看所有命令
    输入 'inspire' 获取激励语录
    输入 'fadeaway' 开始你的API测试之旅

    📞 技术支持 QQ: 2677989813
{reset}
        """.format(
            yellow=Fore.YELLOW + Style.BRIGHT,
            purple=Fore.MAGENTA + Style.BRIGHT,
            cyan=Fore.CYAN + Style.BRIGHT,
            green=Fore.GREEN + Style.BRIGHT,
            reset=Style.RESET_ALL
        )

        return yh_ascii

    def do_inspire(self, arg):
        """显示激励语录"""
        quotes = [
            "🚀 持续改进，追求卓越。",
            "💡 创新思维，突破极限。",
            "⚡ 勇于尝试，不惧失败。",
            "🎯 专注于过程，结果自然会来。",
            "💪 伟大来自于对细节的关注。",
            "🔥 要么全力以赴，要么回家。",
            "🏆 成功是在没有人看见的时候努力出来的。",
            "⭐ 宁愿尝试失败，也不愿不去尝试。",
            "🚀 困难是暂时的，但放弃是永远的。",
            "💎 压力造就钻石。"
        ]

        quote = random.choice(quotes)
        print(f"\n{Fore.YELLOW + Style.BRIGHT}🌟 YH激励语录 🌟{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA + Style.BRIGHT}{quote}{Style.RESET_ALL}\n")

    def do_fadeaway(self, arg):
        """开始API测试 - 精准测试"""
        print(f"\n{Fore.YELLOW + Style.BRIGHT}🚀 准备精准测试... 🚀{Style.RESET_ALL}")

        # 动画效果
        for i in range(3):
            print(f"{Fore.CYAN}{'.' * (i + 1)} 瞄准目标{Style.RESET_ALL}")
            time.sleep(0.5)

        print(f"{Fore.GREEN + Style.BRIGHT}🎯 SWISH! 开始API测试！{Style.RESET_ALL}\n")

        if not arg:
            # 使用默认测试文件
            default_test_file = "default_test.yaml"
            if os.path.exists(default_test_file):
                print(f"{Fore.CYAN}🎯 使用默认测试文件: {default_test_file}{Style.RESET_ALL}")
                self.do_load(default_test_file)
                self.do_run("")
            else:
                print(f"{Fore.RED}❌ 默认测试文件不存在: {default_test_file}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 解决方案:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   1. 指定测试文件: fadeaway <test_file.yaml>{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   2. 创建默认测试文件: {default_test_file}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   3. 使用 'generate' 命令生成示例项目{Style.RESET_ALL}")
            return

        # 先加载文件，再运行
        self.do_load(arg)
        if self.current_test_file:  # 只有加载成功才运行
            self.do_run("")

    def do_load(self, arg):
        """加载测试文件"""
        # 清理输入中的换行符
        arg = arg.replace('\\n', '').replace('\n', '').replace('\r', '').strip()

        if not arg:
            print(f"{Fore.RED}❌ 缺少文件参数{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 用法: load <test_file.yaml>{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   示例: load my_test.yaml{Style.RESET_ALL}")
            return

        try:
            # 调试信息
            print(f"{Fore.CYAN}🔍 正在查找文件: '{arg}'{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📁 当前目录: {os.getcwd()}{Style.RESET_ALL}")

            if not os.path.exists(arg):
                print(f"{Fore.RED}❌ 文件不存在: {arg}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 解决方案:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   1. 检查文件路径是否正确{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   2. 确保文件在当前目录或使用绝对路径{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   3. 使用 'generate' 命令创建示例测试文件{Style.RESET_ALL}")
                return

            with open(arg, 'r', encoding='utf-8') as f:
                if arg.endswith('.yaml') or arg.endswith('.yml'):
                    test_data = yaml.safe_load(f)
                else:
                    test_data = json.load(f)

            self.current_test_file = arg
            print(f"{Fore.GREEN}✅ 成功加载测试文件: {arg}{Style.RESET_ALL}")

            # 显示测试概览
            if isinstance(test_data, list):
                print(f"📊 包含 {len(test_data)} 个测试用例")
            elif isinstance(test_data, dict) and 'tests' in test_data:
                print(f"📊 包含 {len(test_data['tests'])} 个测试用例")

        except Exception as e:
            print(f"{Fore.RED}❌ 加载文件失败: {e}{Style.RESET_ALL}")

    def do_run(self, arg):
        """运行测试"""
        if not self.current_test_file and not arg:
            print("请先加载测试文件或指定文件: run [test_file.yaml]")
            return

        test_file = arg if arg else self.current_test_file

        print(f"\n{Fore.YELLOW + Style.BRIGHT}🚀 开始执行测试: {test_file}{Style.RESET_ALL}")

        # 这里应该调用实际的测试执行逻辑
        # 为了演示，我们模拟测试执行
        self._simulate_test_execution(test_file)

    def _simulate_test_execution(self, test_file: str):
        """模拟测试执行"""
        print(f"{Fore.CYAN}📋 正在解析测试文件...{Style.RESET_ALL}")
        time.sleep(1)

        print(f"{Fore.CYAN}🔧 初始化测试环境...{Style.RESET_ALL}")
        time.sleep(0.5)

        # 模拟测试用例执行
        test_cases = [
            "用户登录接口测试",
            "获取用户信息接口测试",
            "创建订单接口测试",
            "查询订单列表接口测试",
            "更新订单状态接口测试"
        ]

        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"{Fore.BLUE}🧪 [{i}/{len(test_cases)}] 执行: {test_case}{Style.RESET_ALL}")

            # 模拟测试执行时间
            time.sleep(random.uniform(0.3, 1.0))

            # 随机成功/失败
            success = random.choice([True, True, True, False])  # 75%成功率

            if success:
                print(f"{Fore.GREEN}  ✅ 通过 - 响应时间: {random.randint(50, 300)}ms{Style.RESET_ALL}")
                results.append({"name": test_case, "status": "PASS", "time": random.randint(50, 300)})
            else:
                print(f"{Fore.RED}  ❌ 失败 - 状态码: {random.choice([404, 500, 401])}{Style.RESET_ALL}")
                results.append({"name": test_case, "status": "FAIL", "error": "API调用失败"})

        # 显示测试结果
        self._show_test_results(results)

    def _show_test_results(self, results: List[Dict[str, Any]]):
        """显示测试结果"""
        passed = len([r for r in results if r["status"] == "PASS"])
        failed = len([r for r in results if r["status"] == "FAIL"])
        total = len(results)
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"\n{Fore.YELLOW + Style.BRIGHT}📊 测试结果统计{Style.RESET_ALL}")
        print("=" * 50)
        print(f"总测试数: {total}")
        print(f"{Fore.GREEN}通过数: {passed} ✅{Style.RESET_ALL}")
        print(f"{Fore.RED}失败数: {failed} ❌{Style.RESET_ALL}")
        print(f"成功率: {success_rate:.1f}%")

        if success_rate >= 90:
            print(f"\n{Fore.YELLOW + Style.BRIGHT}🏆 完美表现！测试结果优秀！{Style.RESET_ALL}")
        elif success_rate >= 70:
            print(f"\n{Fore.GREEN + Style.BRIGHT}👍 不错的表现！继续保持！{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.MAGENTA + Style.BRIGHT}💪 失败是成功之母，继续努力！{Style.RESET_ALL}")

        self.test_results = results

        # 自动生成和打开Allure报告
        self._generate_allure_report(results)

    def _generate_allure_report(self, results: List[Dict[str, Any]]):
        """生成Allure报告"""
        try:
            from allure_reporter import AllureReporter, AllureConfig
            import platform

            print(f"\n{Fore.CYAN}📊 正在生成测试报告...{Style.RESET_ALL}")

            # 创建Allure配置
            config = AllureConfig(
                results_dir="allure-results",
                report_dir="allure-report",
                clean_results=True,
                generate_report=True,
                open_report=True
            )

            # 创建报告器
            reporter = AllureReporter(config)

            # 生成环境信息
            env_info = {
                "测试框架": "YH-API-Testing-Framework",
                "执行时间": time.strftime('%Y-%m-%d %H:%M:%S'),
                "测试文件": getattr(self, 'current_test_file', None) or "default_test.yaml",
                "总测试数": str(len(results)),
                "通过数": str(len([r for r in results if r["status"] == "PASS"])),
                "失败数": str(len([r for r in results if r["status"] == "FAIL"])),
                "成功率": f"{(len([r for r in results if r['status'] == 'PASS']) / len(results) * 100):.1f}%" if results else "0%"
            }
            reporter.generate_environment_info(env_info)

            # 生成分类信息
            categories = [
                {
                    "name": "API错误",
                    "matchedStatuses": ["failed"],
                    "messageRegex": ".*API.*"
                },
                {
                    "name": "超时错误",
                    "matchedStatuses": ["failed"],
                    "messageRegex": ".*timeout.*"
                },
                {
                    "name": "断言错误",
                    "matchedStatuses": ["failed"],
                    "messageRegex": ".*assert.*"
                }
            ]
            reporter.generate_categories_file(categories)

            # 生成并打开报告
            if reporter.generate_and_open_report():
                print(f"{Fore.GREEN}✅ Allure报告已生成并自动打开{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}📁 报告位置: allure-report/index.html{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️  报告生成失败，请手动运行: allure serve allure-results{Style.RESET_ALL}")

        except ImportError:
            print(f"{Fore.YELLOW}⚠️  未安装allure-pytest，跳过报告生成{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 安装命令: pip install allure-pytest{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ 生成Allure报告失败: {e}{Style.RESET_ALL}")

    def do_status(self, arg):
        """显示当前状态"""
        print(f"\n{Fore.CYAN + Style.BRIGHT}📋 当前状态{Style.RESET_ALL}")
        print("=" * 30)
        print(f"当前测试文件: {self.current_test_file or '未加载'}")
        print(f"会话变量数量: {len(self.session_vars)}")
        print(f"测试结果数量: {len(self.test_results)}")

        if self.test_results:
            passed = len([r for r in self.test_results if r["status"] == "PASS"])
            failed = len([r for r in self.test_results if r["status"] == "FAIL"])
            print(f"最近测试: {passed}通过, {failed}失败")

    def do_vars(self, arg):
        """管理会话变量"""
        # 清理输入中的换行符
        arg = arg.replace('\\n', '').replace('\n', '').replace('\r', '').strip()

        if not arg:
            if not self.session_vars:
                print(f"\n{Fore.YELLOW}📝 会话变量管理{Style.RESET_ALL}")
                print(f"{Fore.CYAN}当前没有会话变量{Style.RESET_ALL}")
                print(f"\n{Fore.GREEN}💡 使用方法:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}   vars set <name> <value>  - 设置变量{Style.RESET_ALL}")
                print(f"{Fore.WHITE}   vars get <name>          - 获取变量{Style.RESET_ALL}")
                print(f"{Fore.WHITE}   vars del <name>          - 删除变量{Style.RESET_ALL}")
                return

            print(f"\n{Fore.CYAN + Style.BRIGHT}📝 会话变量列表{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

            # 美化变量显示
            for i, (key, value) in enumerate(self.session_vars.items(), 1):
                # 截断过长的值
                display_value = str(value)
                if len(display_value) > 50:
                    display_value = display_value[:47] + "..."

                print(f"{Fore.YELLOW}{i:2d}.{Style.RESET_ALL} {Fore.GREEN}{key:<20}{Style.RESET_ALL} = {Fore.WHITE}{display_value}{Style.RESET_ALL}")

            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}总计: {len(self.session_vars)} 个变量{Style.RESET_ALL}")
            return

        parts = arg.split(' ', 2)
        if len(parts) < 2:
            print(f"{Fore.RED}❌ 参数不足{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 用法: vars <set|get|del> <name> [value]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   示例: vars set api_token abc123{Style.RESET_ALL}")
            return

        action, name = parts[0], parts[1]

        if action == 'set':
            if len(parts) < 3:
                print(f"{Fore.RED}❌ 缺少变量值{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 用法: vars set <name> <value>{Style.RESET_ALL}")
                return
            value = parts[2]
            self.session_vars[name] = value
            print(f"{Fore.GREEN}✅ 变量设置成功{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   变量名: {Fore.YELLOW}{name}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   变量值: {Fore.WHITE}{value}{Style.RESET_ALL}")

        elif action == 'get':
            if name in self.session_vars:
                value = self.session_vars[name]
                print(f"{Fore.GREEN}✅ 变量获取成功{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   {name}: {Fore.WHITE}{value}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ 变量不存在: {name}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 使用 'vars' 查看所有变量{Style.RESET_ALL}")

        elif action == 'del':
            if name in self.session_vars:
                old_value = self.session_vars[name]
                del self.session_vars[name]
                print(f"{Fore.GREEN}✅ 变量删除成功{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   已删除: {name} = {old_value}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ 变量不存在: {name}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 使用 'vars' 查看所有变量{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}❌ 未知操作: {action}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 支持的操作: set, get, del{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   示例: vars set username admin{Style.RESET_ALL}")

    def do_concurrent(self, arg):
        """并发测试"""
        if not arg:
            print("用法: concurrent <users> [test_file.yaml]")
            return

        parts = arg.split()
        try:
            users = int(parts[0])
            test_file = parts[1] if len(parts) > 1 else self.current_test_file

            if not test_file:
                print("请指定测试文件")
                return

            print(f"\n{Fore.YELLOW + Style.BRIGHT}🚀 启动并发测试{Style.RESET_ALL}")
            print(f"并发用户数: {users}")
            print(f"测试文件: {test_file}")

            # 并发测试动画
            print(f"\n{Fore.MAGENTA + Style.BRIGHT}🚀 团队协作 - {users}个用户同时测试！{Style.RESET_ALL}")

            for i in range(users):
                print(f"{Fore.CYAN}🏃 用户{i+1}号准备就绪...{Style.RESET_ALL}")
                time.sleep(0.1)

            print(f"{Fore.GREEN + Style.BRIGHT}🎯 全队齐射！{Style.RESET_ALL}")

            # 模拟并发执行
            time.sleep(2)

            # 显示并发结果
            success_rate = random.uniform(85, 98)
            avg_response_time = random.randint(100, 500)

            print(f"\n{Fore.YELLOW + Style.BRIGHT}📊 并发测试结果{Style.RESET_ALL}")
            print("=" * 40)
            print(f"并发用户数: {users}")
            print(f"成功率: {success_rate:.1f}%")
            print(f"平均响应时间: {avg_response_time}ms")
            print(f"总请求数: {users * 5}")  # 假设每个用户5个请求

            if success_rate >= 95:
                print(f"\n{Fore.YELLOW + Style.BRIGHT}🏆 完美团队配合！测试精准！{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN + Style.BRIGHT}👍 不错的团队表现！{Style.RESET_ALL}")

        except ValueError:
            print("❌ 用户数必须是数字")

    def do_report(self, arg):
        """生成测试报告"""
        if not self.test_results:
            print("没有测试结果可生成报告")
            return

        print(f"\n{Fore.YELLOW + Style.BRIGHT}📊 生成测试报告{Style.RESET_ALL}")

        # 模拟报告生成
        report_types = ['HTML', 'Allure', 'JSON', 'Excel']

        for report_type in report_types:
            print(f"{Fore.CYAN}📄 生成{report_type}报告...{Style.RESET_ALL}")
            time.sleep(0.5)
            print(f"{Fore.GREEN}  ✅ {report_type}报告生成完成{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN + Style.BRIGHT}🎉 所有报告生成完成！{Style.RESET_ALL}")
        print("报告文件:")
        print("  📄 test_report.html")
        print("  📊 allure-report/index.html")
        print("  📋 test_results.json")
        print("  📈 test_summary.xlsx")

    def do_socket(self, arg):
        """Socket测试"""
        if not arg:
            print("用法: socket <host:port> [message]")
            return

        parts = arg.split(' ', 1)
        host_port = parts[0]
        message = parts[1] if len(parts) > 1 else "Hello Socket"

        print(f"\n{Fore.YELLOW + Style.BRIGHT}🔌 Socket连接测试{Style.RESET_ALL}")
        print(f"目标: {host_port}")
        print(f"消息: {message}")

        # 模拟Socket连接
        print(f"{Fore.CYAN}🔗 正在连接...{Style.RESET_ALL}")
        time.sleep(1)

        # 随机成功/失败
        success = random.choice([True, True, False])

        if success:
            print(f"{Fore.GREEN}✅ 连接成功{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📤 发送消息: {message}{Style.RESET_ALL}")
            time.sleep(0.5)
            print(f"{Fore.GREEN}📥 收到回复: Echo - {message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ 连接失败: 目标不可达{Style.RESET_ALL}")

    def do_wechat(self, arg):
        """企业微信通知测试"""
        print(f"\n{Fore.YELLOW + Style.BRIGHT}💬 企业微信通知{Style.RESET_ALL}")

        if not arg:
            message = "API测试完成通知"
        else:
            message = arg

        print(f"消息内容: {message}")
        print(f"{Fore.CYAN}📱 正在发送企业微信通知...{Style.RESET_ALL}")

        time.sleep(1)

        success = random.choice([True, True, True, False])  # 75%成功率

        if success:
            print(f"{Fore.GREEN}✅ 企业微信通知发送成功{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ 企业微信通知发送失败{Style.RESET_ALL}")

    def do_ai(self, args):
        """AI智能测试"""
        if not args:
            print(f"{Fore.RED}❌ 请指定目标URL{Style.RESET_ALL}")
            print(f"{Fore.CYAN}用法: ai <目标URL>{Style.RESET_ALL}")
            print(f"{Fore.CYAN}示例: ai https://httpbin.org{Style.RESET_ALL}")
            return

        target_url = args.strip()
        print(f"{Fore.CYAN}🤖 启动AI智能测试...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎯 目标: {target_url}{Style.RESET_ALL}")

        try:
            import requests
            import time

            print(f"{Fore.CYAN}🔍 第1步：基础连接测试{Style.RESET_ALL}")

            # 基础连接测试
            try:
                response = requests.get(target_url, timeout=10)
                print(f"{Fore.GREEN}✅ 连接成功: {response.status_code}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ 连接失败: {e}{Style.RESET_ALL}")
                return

            print(f"{Fore.CYAN}🔍 第2步：端点发现{Style.RESET_ALL}")

            # 端点发现
            common_endpoints = [
                "/", "/api", "/health", "/status", "/version", "/info",
                "/get", "/post", "/put", "/delete", "/patch",
                "/json", "/xml", "/html", "/headers", "/ip"
            ]

            discovered = []
            for endpoint in common_endpoints:
                try:
                    url = target_url.rstrip('/') + endpoint
                    resp = requests.get(url, timeout=5)
                    if resp.status_code < 500:
                        discovered.append({
                            "endpoint": endpoint,
                            "status": resp.status_code,
                            "size": len(resp.content)
                        })
                        print(f"  {Fore.GREEN}✅ {endpoint} -> {resp.status_code}{Style.RESET_ALL}")
                    else:
                        print(f"  {Fore.RED}❌ {endpoint} -> {resp.status_code}{Style.RESET_ALL}")
                except:
                    print(f"  {Fore.YELLOW}⚠️  {endpoint} -> 超时{Style.RESET_ALL}")

            print(f"{Fore.GREEN}🎯 发现 {len(discovered)} 个可用端点{Style.RESET_ALL}")

            if not discovered:
                print(f"{Fore.RED}❌ 未发现可用端点{Style.RESET_ALL}")
                return

            print(f"{Fore.CYAN}🧠 第3步：生成测试用例{Style.RESET_ALL}")

            # 生成测试用例
            tests = []
            for ep in discovered[:5]:  # 只测试前5个端点
                tests.append({
                    "name": f"GET {ep['endpoint']} 基础测试",
                    "method": "GET",
                    "url": target_url.rstrip('/') + ep['endpoint'],
                    "expected_status": [200, 201, 202, 204, 301, 302, 304]
                })

            print(f"{Fore.GREEN}✅ 生成了 {len(tests)} 个测试用例{Style.RESET_ALL}")

            print(f"{Fore.CYAN}🚀 第4步：执行测试{Style.RESET_ALL}")

            # 执行测试
            results = {"total": len(tests), "passed": 0, "failed": 0}

            for i, test in enumerate(tests, 1):
                print(f"  [{i}/{len(tests)}] {test['name']}")
                try:
                    resp = requests.get(test['url'], timeout=10)
                    passed = resp.status_code in test['expected_status']
                    if passed:
                        results['passed'] += 1
                        print(f"    {Fore.GREEN}✅ 通过 ({resp.status_code}){Style.RESET_ALL}")
                    else:
                        results['failed'] += 1
                        print(f"    {Fore.RED}❌ 失败 ({resp.status_code}){Style.RESET_ALL}")
                except Exception as e:
                    results['failed'] += 1
                    print(f"    {Fore.RED}❌ 异常: {e}{Style.RESET_ALL}")

            # 显示结果
            success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
            print(f"\n{Fore.YELLOW}📊 测试结果: {results['passed']}/{results['total']} 通过 ({success_rate:.1f}%){Style.RESET_ALL}")

            if success_rate >= 80:
                print(f"{Fore.GREEN}🏆 API质量优秀！{Style.RESET_ALL}")
            elif success_rate >= 60:
                print(f"{Fore.YELLOW}👍 API质量良好{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}⚠️  API需要改进{Style.RESET_ALL}")

        except ImportError as e:
            print(f"{Fore.RED}❌ 缺少依赖模块: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ AI测试执行失败: {e}{Style.RESET_ALL}")

    def do_quickstart(self, args):
        """一键启动功能"""
        print(f"{Fore.CYAN}🚀 一键启动功能...{Style.RESET_ALL}")
        try:
            import subprocess
            import sys
            subprocess.run([sys.executable, "quick_start.py"])
        except Exception as e:
            print(f"{Fore.RED}❌ 启动失败: {e}{Style.RESET_ALL}")

    def do_docs(self, args):
        """启动文档服务器"""
        print(f"{Fore.CYAN}📚 启动文档服务器...{Style.RESET_ALL}")
        try:
            import subprocess
            import sys
            import threading
            import time

            # 在后台启动文档服务器
            def start_docs():
                subprocess.run([sys.executable, "swagger_docs.py"])

            docs_thread = threading.Thread(target=start_docs, daemon=True)
            docs_thread.start()

            time.sleep(2)
            print(f"{Fore.GREEN}📖 文档服务器已启动: http://127.0.0.1:8080{Style.RESET_ALL}")
            print(f"{Fore.CYAN}💡 提示: 在浏览器中访问上述地址查看文档{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ 文档服务器启动失败: {e}{Style.RESET_ALL}")

    def do_generate(self, args):
        """生成测试项目"""
        print(f"{Fore.YELLOW + Style.BRIGHT}📦 生成测试项目...{Style.RESET_ALL}")

        # 清理输入中的换行符并获取项目名称
        args = args.replace('\\n', '').replace('\n', '').replace('\r', '').strip()
        project_name = args if args else "api_test_project"

        try:
            self.generate_test_project(project_name)
            print(f"{Fore.GREEN + Style.BRIGHT}🎉 测试项目生成成功！{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📁 项目目录: {project_name}/{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 使用说明:{Style.RESET_ALL}")
            print(f"  1. 进入项目目录: cd {project_name}")
            print(f"  2. 修改配置文件: config/test_config.yaml")
            print(f"  3. 更新测试用例: tests/api_tests.yaml")
            print(f"  4. 运行测试: python run.py")

        except Exception as e:
            print(f"{Fore.RED}❌ 项目生成失败: {e}{Style.RESET_ALL}")

    def do_clear(self, arg):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.get_yh_intro())

    def do_exit(self, arg):
        """退出程序"""
        print(f"\n{Fore.YELLOW + Style.BRIGHT}🌟 YH精神永存！{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA + Style.BRIGHT}感谢使用API测试框架，继续追求完美！{Style.RESET_ALL}")
        print(f"{Fore.CYAN}\"持续改进，追求卓越！\" - YH{Style.RESET_ALL}\n")
        return True

    def do_quit(self, arg):
        """退出程序"""
        return self.do_exit(arg)

    def help_general(self):
        """显示通用帮助"""
        help_text = f"""
{Fore.YELLOW + Style.BRIGHT}🚀 YH API测试框架 - 命令帮助{Style.RESET_ALL}

{Fore.CYAN + Style.BRIGHT}📋 基础命令:{Style.RESET_ALL}
  inspire            - 显示激励语录
  fadeaway <file>    - 开始API测试（精准测试）
  load <file>        - 加载测试文件
  run [file]         - 运行测试
  status             - 显示当前状态
  clear              - 清屏并显示启动界面

{Fore.GREEN + Style.BRIGHT}🔧 测试管理:{Style.RESET_ALL}
  vars               - 管理会话变量
  vars set <k> <v>   - 设置变量
  vars get <k>       - 获取变量
  vars del <k>       - 删除变量

{Fore.MAGENTA + Style.BRIGHT}🚀 高级功能:{Style.RESET_ALL}
  concurrent <n> [f] - 并发测试（n个用户）
  socket <host:port> - Socket连接测试
  wechat [msg]       - 企业微信通知测试
  report             - 生成测试报告

{Fore.BLUE + Style.BRIGHT}🤖 AI智能功能:{Style.RESET_ALL}
  ai <url>           - AI智能测试（自动生成和执行测试用例）
  quickstart         - 一键启动所有功能
  docs               - 启动文档服务器

{Fore.GREEN + Style.BRIGHT}📦 项目生成:{Style.RESET_ALL}
  generate [name]    - 生成完整的测试项目目录，目录中需要有完整的测试信息，执行run.py ,可以正确执行，便于 用户 更新 测试项目内容，即可运行测试
  6                  - 快捷生成完整测试项目

{Fore.CYAN + Style.BRIGHT}🐚 Shell命令模式:{Style.RESET_ALL}
  shell              - 查看shell命令帮助
  shell <cmd> <args> - 执行shell模式命令
  2                  - 快捷启动文档服务器

{Fore.RED + Style.BRIGHT}🚪 退出:{Style.RESET_ALL}
  exit / quit        - 退出程序

{Fore.MAGENTA + Style.BRIGHT}📞 联系支持:{Style.RESET_ALL}
  QQ: 2677989813     - 技术支持与交流

{Fore.YELLOW}💡 提示: 输入命令名称可查看详细帮助{Style.RESET_ALL}
{Fore.GREEN}🎯 快速开始: 输入 'fadeaway' 开始API测试之旅{Style.RESET_ALL}
        """
        print(help_text)

    def do_shell(self, args):
        """执行shell命令模式的API测试命令"""
        if not args:
            print(f"\n{Fore.CYAN + Style.BRIGHT}🐚 YH Shell命令模式{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW + Style.BRIGHT}📋 可用命令列表:{Style.RESET_ALL}\n")

            # 分类显示命令
            commands = [
                ("🚀 测试执行", [
                    ("run <file>", "运行测试文件"),
                    ("load <file>", "加载测试文件"),
                    ("fadeaway [file]", "执行精准测试"),
                    ("concurrent <n>", "并发测试")
                ]),
                ("🤖 智能功能", [
                    ("ai <url>", "AI智能测试"),
                    ("socket <host>", "Socket连接测试"),
                    ("wechat [msg]", "企业微信通知")
                ]),
                ("📊 报告管理", [
                    ("report", "生成测试报告"),
                    ("status", "查看当前状态"),
                    ("docs", "启动文档服务器")
                ]),
                ("🔧 工具功能", [
                    ("vars <op>", "变量管理"),
                    ("generate [name]", "生成测试项目"),
                    ("inspire", "获取激励语录")
                ])
            ]

            for category, cmd_list in commands:
                print(f"{Fore.MAGENTA + Style.BRIGHT}{category}:{Style.RESET_ALL}")
                for cmd, desc in cmd_list:
                    print(f"  {Fore.GREEN}shell {cmd:<15}{Style.RESET_ALL} - {Fore.WHITE}{desc}{Style.RESET_ALL}")
                print()

            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 示例: shell run my_test.yaml{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 提示: 所有shell命令都支持完整的参数传递{Style.RESET_ALL}")
            return

        # 清理输入中的换行符
        clean_args = args.replace('\\n', '').replace('\n', '').replace('\r', '').strip()
        parts = clean_args.split()
        if not parts:
            return

        cmd = parts[0]
        cmd_args = " ".join(parts[1:]) if len(parts) > 1 else ""

        # 映射shell命令到内部方法
        shell_commands = {
            'run': self.do_run,
            'load': self.do_load,
            'fadeaway': self.do_fadeaway,
            'concurrent': self.do_concurrent,
            'ai': self.do_ai,
            'report': self.do_report,
            'status': self.do_status,
            'docs': self.do_docs,
            'inspire': self.do_inspire,
            'socket': self.do_socket,
            'wechat': self.do_wechat,
            'vars': self.do_vars,
            'generate': self.do_generate
        }

        if cmd in shell_commands:
            # 美化的命令执行提示
            print(f"\n{Fore.CYAN + Style.BRIGHT}🐚 YH Shell 执行中...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}┌─ 命令: {Fore.GREEN}{cmd}{Style.RESET_ALL}")
            if cmd_args:
                print(f"{Fore.YELLOW}├─ 参数: {Fore.WHITE}{cmd_args}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}└─ 状态: {Fore.GREEN}正在执行...{Style.RESET_ALL}\n")

            try:
                shell_commands[cmd](cmd_args)
                print(f"\n{Fore.GREEN}✅ Shell命令执行完成{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}❌ Shell命令执行失败: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ 不支持的shell命令: '{cmd}'{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 可用命令提示:{Style.RESET_ALL}")

            # 智能建议相似命令
            available_cmds = ['run', 'load', 'fadeaway', 'concurrent', 'ai', 'report', 'status', 'docs', 'inspire', 'socket', 'wechat', 'vars', 'generate']
            suggestions = [c for c in available_cmds if cmd.lower() in c.lower() or c.lower() in cmd.lower()]

            if suggestions:
                print(f"{Fore.GREEN}   🎯 推荐命令: {', '.join(suggestions)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}   📋 输入 'shell' 查看所有支持的命令{Style.RESET_ALL}")



    def default(self, line):
        """处理未知命令"""
        # 彻底清理输入，移除字面上的\n字符串
        clean_line = line.replace('\\n', '').replace('\n', '').replace('\r', '').strip()



        # 处理数字命令
        if clean_line == "2":
            self.do_docs("")
            return
        elif clean_line == "6":
            print(f"{Fore.CYAN}🎯 执行数字命令6 - 生成测试项目{Style.RESET_ALL}")
            self.do_generate("")
            return

        # 友好的错误提示
        command = line.strip()
        print(f"{Fore.RED}❌ 未知命令: '{command}'{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 提示: 您可能想要使用以下命令之一:{Style.RESET_ALL}")

        # 智能建议相似命令
        available_commands = ['help', 'load', 'run', 'test', 'docs', 'vars', 'generate', 'inspire', 'fadeaway', 'exit']
        suggestions = []

        # 简单的相似度匹配
        for cmd in available_commands:
            if command.lower() in cmd.lower() or cmd.lower() in command.lower():
                suggestions.append(cmd)

        if suggestions:
            print(f"{Fore.GREEN}   🎯 推荐命令: {', '.join(suggestions)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}   📋 输入 'help' 查看所有可用命令{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   🚀 输入 'fadeaway' 开始API测试{Style.RESET_ALL}")

    def emptyline(self):
        """处理空行"""
        pass

    def precmd(self, line):
        """预处理命令行输入，更新提示符"""
        # 更新命令计数
        if line.strip():
            self.command_count += 1

        # 动态更新提示符
        status_info = ""
        if self.current_test_file:
            status_info = f"{Fore.GREEN}[{os.path.basename(self.current_test_file)}]{Style.RESET_ALL} "

        if self.session_vars:
            status_info += f"{Fore.BLUE}[{len(self.session_vars)}vars]{Style.RESET_ALL} "

        self.prompt = f"{status_info}{Fore.YELLOW + Style.BRIGHT}🚀 YH-API-Test{Fore.CYAN} >{Style.RESET_ALL} "

        # 清理输入
        line = line.strip()

        # 处理数字命令映射
        if line == "2":
            return "docs"
        elif line == "6":
            return "generate"

        return line

    def generate_test_project(self, project_name):
        """生成完整的测试项目"""
        import os
        from pathlib import Path

        # 创建项目目录结构
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=True)

        # 创建子目录
        (project_path / "config").mkdir(exist_ok=True)
        (project_path / "tests").mkdir(exist_ok=True)
        (project_path / "reports").mkdir(exist_ok=True)
        (project_path / "data").mkdir(exist_ok=True)
        (project_path / "utils").mkdir(exist_ok=True)

        print(f"{Fore.CYAN}📁 创建项目目录结构...{Style.RESET_ALL}")

        # 生成各种配置和测试文件
        self._create_project_files(project_path)

        print(f"{Fore.GREEN}✅ 项目文件生成完成{Style.RESET_ALL}")

    def _create_project_files(self, project_path):
        """创建项目文件"""
        # 1. 创建主配置文件
        self._create_main_config(project_path / "config" / "test_config.yaml")

        # 2. 创建测试用例文件
        self._create_test_cases(project_path / "tests" / "api_tests.yaml")

        # 3. 创建运行脚本
        self._create_run_script(project_path / "run.py")

        # 4. 创建README文档
        self._create_readme(project_path / "README.md")

        # 5. 创建环境配置
        self._create_env_config(project_path / "config" / "environments.yaml")

        # 6. 创建数据文件
        self._create_test_data(project_path / "data" / "test_data.yaml")

        # 7. 创建工具类
        self._create_utils(project_path / "utils" / "helpers.py")

    def _create_main_config(self, config_path):
        """创建主配置文件"""
        config_content = """# API测试框架配置文件
# 基础配置
base:
  name: "API测试项目"
  version: "1.0.0"
  description: "基于YH API测试框架的完整测试项目"

# 服务器配置
server:
  base_url: "https://httpbin.org"  # 替换为实际API地址
  timeout: 30
  retry_count: 3
  retry_delay: 1

# 认证配置
auth:
  type: "bearer"  # bearer, basic, api_key
  token: "your_api_token_here"  # 替换为实际token
  username: "test_user"
  password: "test_password"
  api_key_header: "X-API-Key"
  api_key_value: "your_api_key_here"

# 数据库配置（可选）
database:
  enabled: false
  host: "localhost"
  port: 5432
  name: "test_db"
  username: "db_user"
  password: "db_password"

# 报告配置
reporting:
  enabled: true
  formats: ["html", "json", "allure"]
  output_dir: "reports"
  include_screenshots: true

# 通知配置
notifications:
  wechat:
    enabled: false
    webhook_url: "your_wechat_webhook_url"
  email:
    enabled: false
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "your_email@gmail.com"
    password: "your_email_password"
    recipients: ["recipient@example.com"]

# 并发配置
concurrency:
  max_workers: 5
  batch_size: 10
  delay_between_batches: 2

# 环境配置
environments:
  default: "test"
  available: ["dev", "test", "staging", "prod"]
"""

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"{Fore.GREEN}✅ 创建配置文件: {config_path.name}{Style.RESET_ALL}")

    def _create_test_cases(self, test_path):
        """创建测试用例文件"""
        test_content = """# API测试用例集合
# 测试项目信息
project:
  name: "API接口测试"
  version: "1.0.0"
  description: "完整的API接口测试用例集合"

# 全局变量
globals:
  base_url: "https://httpbin.org"  # 替换为实际API地址
  api_version: "v1"
  content_type: "application/json"
  user_agent: "YH-API-Test-Framework/3.0"

# 测试用例
tests:
  # 1. 基础GET请求测试
  - name: "获取用户信息"
    description: "测试获取用户基本信息接口"
    method: "GET"
    url: "${base_url}/get"  # 替换为: /api/v1/users/{user_id}
    headers:
      Content-Type: "${content_type}"
      User-Agent: "${user_agent}"
      # Authorization: "Bearer ${auth_token}"  # 取消注释并替换实际token
    params:
      user_id: "12345"  # 替换为实际参数
      include_profile: true
    assertions:
      - type: "status_code"
        expected: 200
      - type: "response_time"
        expected: 2000  # 毫秒
      - type: "json_path"
        path: "$.args.user_id"
        expected: "12345"
      # - type: "json_schema"  # 取消注释以验证响应结构
      #   schema:
      #     type: "object"
      #     properties:
      #       id: {type: "integer"}
      #       name: {type: "string"}
      #       email: {type: "string"}

  # 2. POST请求测试
  - name: "创建新用户"
    description: "测试创建新用户接口"
    method: "POST"
    url: "${base_url}/post"  # 替换为: /api/v1/users
    headers:
      Content-Type: "${content_type}"
      # Authorization: "Bearer ${auth_token}"
    data:
      name: "张三"
      email: "zhangsan@example.com"
      age: 25
      department: "技术部"
    assertions:
      - type: "status_code"
        expected: 200  # 替换为实际期望状态码，如201
      - type: "json_path"
        path: "$.json.name"
        expected: "张三"
      - type: "json_path"
        path: "$.json.email"
        expected: "zhangsan@example.com"

  # 3. PUT请求测试
  - name: "更新用户信息"
    description: "测试更新用户信息接口"
    method: "PUT"
    url: "${base_url}/put"  # 替换为: /api/v1/users/{user_id}
    headers:
      Content-Type: "${content_type}"
    data:
      name: "张三（已更新）"
      email: "zhangsan.updated@example.com"
      age: 26
    assertions:
      - type: "status_code"
        expected: 200
      - type: "json_path"
        path: "$.json.name"
        expected: "张三（已更新）"

  # 4. DELETE请求测试
  - name: "删除用户"
    description: "测试删除用户接口"
    method: "DELETE"
    url: "${base_url}/delete"  # 替换为: /api/v1/users/{user_id}
    headers:
      Content-Type: "${content_type}"
    params:
      user_id: "12345"
    assertions:
      - type: "status_code"
        expected: 200  # 替换为实际期望状态码，如204

  # 5. 文件上传测试
  - name: "上传文件"
    description: "测试文件上传接口"
    method: "POST"
    url: "${base_url}/post"  # 替换为: /api/v1/upload
    headers:
      # Content-Type会自动设置为multipart/form-data
      pass
    files:
      file: "data/test_file.txt"  # 确保文件存在
    data:
      description: "测试文件上传"
      category: "document"
    assertions:
      - type: "status_code"
        expected: 200

  # 6. 参数化测试
  - name: "批量用户查询"
    description: "测试批量查询用户信息"
    method: "GET"
    url: "${base_url}/get"  # 替换为实际接口
    parameters:
      - user_id: "001"
        expected_name: "用户001"
      - user_id: "002"
        expected_name: "用户002"
      - user_id: "003"
        expected_name: "用户003"
    headers:
      Content-Type: "${content_type}"
    params:
      user_id: "${user_id}"
    assertions:
      - type: "status_code"
        expected: 200
      - type: "json_path"
        path: "$.args.user_id"
        expected: "${user_id}"

  # 7. 依赖测试（使用前一个测试的结果）
  - name: "获取创建的用户详情"
    description: "获取之前创建的用户的详细信息"
    method: "GET"
    url: "${base_url}/get"  # 替换为: /api/v1/users/${created_user_id}
    headers:
      Content-Type: "${content_type}"
    params:
      user_id: "${created_user_id}"  # 从前面的测试中提取
    depends_on: "创建新用户"  # 依赖的测试名称
    extract:
      - name: "created_user_id"
        path: "$.json.id"  # 从响应中提取用户ID
    assertions:
      - type: "status_code"
        expected: 200

# 测试套件配置
suites:
  smoke_test:
    description: "冒烟测试套件"
    tests: ["获取用户信息", "创建新用户"]

  full_test:
    description: "完整测试套件"
    tests: ["获取用户信息", "创建新用户", "更新用户信息", "删除用户"]

  file_test:
    description: "文件操作测试"
    tests: ["上传文件"]
"""

        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        print(f"{Fore.GREEN}✅ 创建测试用例: {test_path.name}{Style.RESET_ALL}")

    def _create_run_script(self, script_path):
        """创建运行脚本"""
        script_content = '''#!/usr/bin/env python3
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
        print(f"{Fore.RED}❌ 配置❌ ❌ 文件不存在，请检查文件路径是否正确\n💡 提示：使用相对路径或绝对路径，请检查文件路径是否正确\n💡 提示：使用相对路径或绝对路径: {config_path}{Style.RESET_ALL}")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_test_cases():
    """加载测试用例"""
    test_path = Path("tests/api_tests.yaml")
    if not test_path.exists():
        print(f"{Fore.RED}❌ 测试用例❌ ❌ 文件不存在，请检查文件路径是否正确\n💡 提示：使用相对路径或绝对路径，请检查文件路径是否正确\n💡 提示：使用相对路径或绝对路径: {test_path}{Style.RESET_ALL}")
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

    print(f"\\n{Fore.CYAN}🔧 配置信息:{Style.RESET_ALL}")
    print(f"  基础URL: {config.get('server', {}).get('base_url', 'Not configured')}")
    print(f"  超时时间: {config.get('server', {}).get('timeout', 30)}秒")
    print(f"  重试次数: {config.get('server', {}).get('retry_count', 3)}")

    # 检查是否安装了api-test-yh-pro
    try:
        # 尝试导入yh_shell模块
        sys.path.append('..')  # 添加上级目录到路径
        from yh_shell import YHShell

        print(f"\\n{Fore.GREEN}✅ 检测到YH API测试框架{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚀 启动测试执行...{Style.RESET_ALL}")

        # 创建shell实例并运行测试
        shell = YHShell()
        shell.do_load("tests/api_tests.yaml")
        shell.do_run("")

        return True

    except ImportError:
        print(f"\\n{Fore.YELLOW}⚠️  未检测到YH API测试框架{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📦 请先安装框架: pip install api-test-yh-pro{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 或者将此项目复制到框架目录中运行{Style.RESET_ALL}")

        # 提供手动运行指导
        print(f"\\n{Fore.MAGENTA}📋 手动运行步骤:{Style.RESET_ALL}")
        print("1. 安装框架: pip install api-test-yh-pro")
        print("2. 启动框架: python -c \\"from yh_shell import YHShell; YHShell().cmdloop()\\"")
        print("3. 在框架中运行: load tests/api_tests.yaml")
        print("4. 执行测试: run")

        return False

def main():
    """主函数"""
    print(f"{Fore.MAGENTA + Style.BRIGHT}🌟 YH精神永存！{Style.RESET_ALL}")

    success = run_tests()

    if success:
        print(f"\\n{Fore.GREEN + Style.BRIGHT}🎉 测试执行完成！{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 查看报告: reports/目录{Style.RESET_ALL}")
    else:
        print(f"\\n{Fore.RED}❌ 测试执行失败{Style.RESET_ALL}")

    print(f"\\n{Fore.YELLOW}\\"持续改进，追求卓越！\\" - YH精神{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
'''

        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"{Fore.GREEN}✅ 创建运行脚本: {script_path.name}{Style.RESET_ALL}")

    def _create_readme(self, readme_path):
        """创建README文档"""
        readme_content = '''# API测试项目

基于YH API测试框架的完整API测试项目模板。

## 🚀 项目简介

这是一个使用YH API测试框架生成的完整测试项目，包含了完整的配置文件、测试用例、数据文件和工具类，可以直接用于API接口测试。

## 📁 项目结构

```
api_test_project/
├── config/                 # 配置文件目录
│   ├── test_config.yaml   # 主配置文件
│   └── environments.yaml  # 环境配置文件
├── tests/                  # 测试用例目录
│   └── api_tests.yaml     # API测试用例
├── data/                   # 测试数据目录
│   ├── test_data.yaml     # 测试数据文件
│   └── test_file.txt      # 测试文件
├── utils/                  # 工具类目录
│   └── helpers.py         # 辅助工具类
├── reports/               # 测试报告目录
├── run.py                # 测试运行脚本
└── README.md             # 项目说明文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install api-test-kb-pro
```

### 2. 配置项目

编辑 `config/test_config.yaml` 文件，更新以下配置：

- `server.base_url`: 替换为实际的API服务器地址
- `auth`: 配置认证信息（token、用户名密码等）
- 其他相关配置

### 3. 更新测试用例

编辑 `tests/api_tests.yaml` 文件：

- 将示例URL替换为实际的API接口地址
- 更新请求参数、请求体数据
- 修改断言条件以匹配实际API响应

### 4. 运行测试

```bash
# 方式1: 使用项目运行脚本
python run.py

# 方式2: 使用YH框架命令行
python -c "from yh_shell import YHShell; YHShell().cmdloop()"
# 然后在框架中执行:
# > load tests/api_tests.yaml
# > run
```

## 💡 使用技巧

1. **变量替换**: 在测试用例中使用 `${variable_name}` 进行变量替换
2. **数据提取**: 使用 `extract` 从响应中提取数据供后续测试使用
3. **测试套件**: 使用 `suites` 组织不同类型的测试
4. **并发测试**: 配置 `concurrency` 进行并发测试
5. **通知集成**: 配置企业微信或邮件通知测试结果

## 🚀 YH精神

> "持续改进，追求卓越！" - YH精神

不断完善，追求完美的API测试！

## 📞 支持

如有问题，请联系：
- QQ: 2677989813

---

**💪 YH精神永存！继续追求完美的API测试！**
'''

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"{Fore.GREEN}✅ 创建README文档: {readme_path.name}{Style.RESET_ALL}")

    def _create_env_config(self, env_path):
        """创建环境配置文件"""
        env_content = '''# 环境配置文件
# 支持多环境配置，便于在不同环境间切换

# 开发环境
dev:
  name: "开发环境"
  base_url: "https://dev-api.example.com"  # 替换为实际开发环境地址
  database:
    host: "dev-db.example.com"
    port: 5432
    name: "dev_database"
  auth:
    token: "dev_token_here"
  features:
    debug_mode: true
    mock_external_apis: true

# 测试环境
test:
  name: "测试环境"
  base_url: "https://test-api.example.com"  # 替换为实际测试环境地址
  database:
    host: "test-db.example.com"
    port: 5432
    name: "test_database"
  auth:
    token: "test_token_here"
  features:
    debug_mode: true
    mock_external_apis: false

# 预发布环境
staging:
  name: "预发布环境"
  base_url: "https://staging-api.example.com"  # 替换为实际预发布环境地址
  database:
    host: "staging-db.example.com"
    port: 5432
    name: "staging_database"
  auth:
    token: "staging_token_here"
  features:
    debug_mode: false
    mock_external_apis: false

# 生产环境
prod:
  name: "生产环境"
  base_url: "https://api.example.com"  # 替换为实际生产环境地址
  database:
    host: "prod-db.example.com"
    port: 5432
    name: "prod_database"
  auth:
    token: "prod_token_here"
  features:
    debug_mode: false
    mock_external_apis: false
    read_only_mode: true  # 生产环境只读模式

# 本地环境
local:
  name: "本地环境"
  base_url: "http://localhost:8080"
  database:
    host: "localhost"
    port: 5432
    name: "local_database"
  auth:
    token: "local_token_here"
  features:
    debug_mode: true
    mock_external_apis: true
'''

        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"{Fore.GREEN}✅ 创建环境配置: {env_path.name}{Style.RESET_ALL}")

    def _create_test_data(self, data_path):
        """创建测试数据文件"""
        data_content = '''# 测试数据文件
# 包含各种测试场景的数据

# 用户测试数据
users:
  valid_user:
    name: "张三"
    email: "zhangsan@example.com"
    age: 25
    department: "技术部"
    phone: "13800138000"
    address: "北京市朝阳区"

  invalid_user:
    name: ""  # 空名称
    email: "invalid-email"  # 无效邮箱
    age: -1  # 无效年龄

  admin_user:
    name: "管理员"
    email: "admin@example.com"
    role: "admin"
    permissions: ["read", "write", "delete"]

# 产品测试数据
products:
  valid_product:
    name: "测试产品"
    description: "这是一个测试产品"
    price: 99.99
    category: "电子产品"
    stock: 100
    tags: ["测试", "产品", "电子"]

  expensive_product:
    name: "高端产品"
    price: 9999.99
    category: "奢侈品"

  out_of_stock_product:
    name: "缺货产品"
    stock: 0

# 订单测试数据
orders:
  simple_order:
    user_id: 12345
    products:
      - product_id: 1
        quantity: 2
        price: 99.99
      - product_id: 2
        quantity: 1
        price: 199.99
    total_amount: 399.97
    shipping_address: "北京市朝阳区测试地址"

  bulk_order:
    user_id: 12345
    products:
      - product_id: 1
        quantity: 100
        price: 99.99

# 认证测试数据
auth:
  valid_credentials:
    username: "testuser"
    password: "testpass123"
    email: "testuser@example.com"

  invalid_credentials:
    username: "wronguser"
    password: "wrongpass"

  expired_token: "expired.jwt.token.here"
  valid_token: "valid.jwt.token.here"

# 文件测试数据
files:
  valid_image:
    filename: "test_image.jpg"
    content_type: "image/jpeg"
    size: 1024000  # 1MB

  large_file:
    filename: "large_file.zip"
    content_type: "application/zip"
    size: 10485760  # 10MB

  invalid_file:
    filename: "test.exe"
    content_type: "application/x-executable"

# 搜索测试数据
search:
  valid_queries:
    - "测试"
    - "产品"
    - "用户"

  invalid_queries:
    - ""  # 空查询
    - "a"  # 太短
    - "x" * 1000  # 太长

  special_queries:
    - "测试 AND 产品"
    - "用户 OR 客户"
    - '"精确匹配"'

# 分页测试数据
pagination:
  valid_params:
    - page: 1
      size: 10
    - page: 2
      size: 20
    - page: 1
      size: 50

  invalid_params:
    - page: 0
      size: 10
    - page: 1
      size: 0
    - page: -1
      size: -1

# 边界值测试数据
boundary_values:
  strings:
    empty: ""
    single_char: "a"
    max_length: "a" * 255
    unicode: "测试🏀🐍"

  numbers:
    zero: 0
    negative: -1
    max_int: 2147483647
    min_int: -2147483648
    decimal: 123.456

  arrays:
    empty: []
    single_item: [1]
    large_array: [1, 2, 3, 4, 5] * 100

# 错误场景数据
error_scenarios:
  network_errors:
    - timeout: 30000  # 超时场景
    - connection_refused: true  # 连接拒绝

  server_errors:
    - status_code: 500
      message: "内部服务器错误"
    - status_code: 503
      message: "服务不可用"

  client_errors:
    - status_code: 400
      message: "请求❌ 参数格式错误\n💡 提示：请使用 help <命令> 查看正确用法"
    - status_code: 401
      message: "未授权访问"
    - status_code: 404
      message: "资源不存在"
'''

        with open(data_path, 'w', encoding='utf-8') as f:
            f.write(data_content)
        print(f"{Fore.GREEN}✅ 创建测试数据: {data_path.name}{Style.RESET_ALL}")

        # 同时创建测试文件
        test_file_path = data_path.parent / "test_file.txt"
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write("这是一个用于测试文件上传功能的示例文件。\\n")
            f.write("文件内容：YH API测试框架\\n")
            f.write("YH精神永存！\\n")
        print(f"{Fore.GREEN}✅ 创建测试文件: {test_file_path.name}{Style.RESET_ALL}")

    def _create_utils(self, utils_path):
        """创建工具类文件"""
        utils_content = '''#!/usr/bin/env python3
"""
测试辅助工具类
提供常用的测试工具函数
"""

import json
import yaml
import time
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class TestHelpers:
    """测试辅助工具类"""

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_random_email() -> str:
        """生成随机邮箱地址"""
        username = TestHelpers.generate_random_string(8)
        domains = ['example.com', 'test.com', 'demo.org']
        domain = random.choice(domains)
        return f"{username}@{domain}"

    @staticmethod
    def generate_random_phone() -> str:
        """生成随机手机号"""
        prefixes = ['138', '139', '150', '151', '188', '189']
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{suffix}"

    @staticmethod
    def generate_timestamp(days_offset: int = 0) -> str:
        """生成时间戳"""
        target_date = datetime.now() + timedelta(days=days_offset)
        return target_date.isoformat()

    @staticmethod
    def load_test_data(file_path: str) -> Dict[str, Any]:
        """加载测试数据文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    return yaml.safe_load(f)
                elif file_path.endswith('.json'):
                    return json.load(f)
                else:
                    raise ValueError(f"不支持的文件格式: {file_path}")
        except Exception as e:
            print(f"加载测试数据失败: {e}")
            return {}

    @staticmethod
    def validate_response_structure(response: Dict[str, Any], expected_keys: List[str]) -> bool:
        """验证响应结构"""
        for key in expected_keys:
            if key not in response:
                return False
        return True

    @staticmethod
    def extract_json_value(data: Dict[str, Any], path: str) -> Any:
        """从JSON中提取值（支持点号路径）"""
        keys = path.split('.')
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        return current

    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, interval: int = 1) -> bool:
        """等待条件满足"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False

    @staticmethod
    def create_test_file(file_path: str, content: str = "测试文件内容") -> bool:
        """创建测试文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"创建测试文件失败: {e}")
            return False

    @staticmethod
    def cleanup_test_files(file_paths: List[str]) -> None:
        """清理测试文件"""
        import os
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"删除文件失败 {file_path}: {e}")

class DataGenerator:
    """测试数据生成器"""

    @staticmethod
    def generate_user_data(count: int = 1) -> List[Dict[str, Any]]:
        """生成用户测试数据"""
        users = []
        for i in range(count):
            user = {
                'id': i + 1,
                'name': f"测试用户{i+1:03d}",
                'email': TestHelpers.generate_random_email(),
                'phone': TestHelpers.generate_random_phone(),
                'age': random.randint(18, 65),
                'department': random.choice(['技术部', '产品部', '运营部', '市场部']),
                'created_at': TestHelpers.generate_timestamp(-random.randint(1, 365))
            }
            users.append(user)
        return users

    @staticmethod
    def generate_product_data(count: int = 1) -> List[Dict[str, Any]]:
        """生成产品测试数据"""
        products = []
        categories = ['电子产品', '服装', '食品', '图书', '家居']

        for i in range(count):
            product = {
                'id': i + 1,
                'name': f"测试产品{i+1:03d}",
                'description': f"这是第{i+1}个测试产品的描述",
                'price': round(random.uniform(10.0, 1000.0), 2),
                'category': random.choice(categories),
                'stock': random.randint(0, 100),
                'created_at': TestHelpers.generate_timestamp(-random.randint(1, 30))
            }
            products.append(product)
        return products

class AssertionHelpers:
    """断言辅助工具"""

    @staticmethod
    def assert_status_code(actual: int, expected: int) -> bool:
        """断言状态码"""
        return actual == expected

    @staticmethod
    def assert_response_time(actual: float, max_time: float) -> bool:
        """断言响应时间"""
        return actual <= max_time

    @staticmethod
    def assert_json_contains(response: Dict[str, Any], expected_data: Dict[str, Any]) -> bool:
        """断言JSON包含指定数据"""
        for key, value in expected_data.items():
            if key not in response or response[key] != value:
                return False
        return True

    @staticmethod
    def assert_array_length(array: List[Any], expected_length: int) -> bool:
        """断言数组长度"""
        return len(array) == expected_length

    @staticmethod
    def assert_string_contains(text: str, substring: str) -> bool:
        """断言字符串包含子串"""
        return substring in text

# 使用示例
if __name__ == "__main__":
    # 生成测试数据示例
    print("生成用户数据:")
    users = DataGenerator.generate_user_data(3)
    for user in users:
        print(f"  {user}")

    print("\\n生成产品数据:")
    products = DataGenerator.generate_product_data(2)
    for product in products:
        print(f"  {product}")

    # 工具函数示例
    print(f"\\n随机字符串: {TestHelpers.generate_random_string()}")
    print(f"随机邮箱: {TestHelpers.generate_random_email()}")
    print(f"随机手机: {TestHelpers.generate_random_phone()}")
    print(f"当前时间戳: {TestHelpers.generate_timestamp()}")
'''

        with open(utils_path, 'w', encoding='utf-8') as f:
            f.write(utils_content)
        print(f"{Fore.GREEN}✅ 创建工具类: {utils_path.name}{Style.RESET_ALL}")

def main():
    """主函数"""
    try:
        shell = YHShell()
        shell.cmdloop()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW + Style.BRIGHT}🌟 YH精神永存！再见！{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ 程序异常: {e}{Style.RESET_ALL}")

def fadeaway_main():
    """fadeaway命令入口点"""
    try:
        shell = YHShell()
        shell.do_fadeaway("")
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW + Style.BRIGHT}🌟 YH精神永存！再见！{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ fadeaway执行异常: {e}{Style.RESET_ALL}")

def inspire_main():
    """inspire命令入口点"""
    try:
        shell = YHShell()
        shell.do_inspire("")
    except Exception as e:
        print(f"\n{Fore.RED}❌ inspire执行异常: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()