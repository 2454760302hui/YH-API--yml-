#!/usr/bin/env python3
"""
企业微信消息推送模块
支持测试结果通知和报告推送
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging
import base64
import hashlib

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """消息类型枚举"""
    TEXT = "text"
    MARKDOWN = "markdown"
    IMAGE = "image"
    NEWS = "news"
    FILE = "file"

@dataclass
class WeChatConfig:
    """企业微信配置"""
    webhook_url: str
    corp_id: Optional[str] = None
    corp_secret: Optional[str] = None
    agent_id: Optional[str] = None
    mentioned_list: Optional[List[str]] = None
    mentioned_mobile_list: Optional[List[str]] = None

class WeChatNotifier:
    """企业微信通知器"""
    
    def __init__(self, config: WeChatConfig):
        self.config = config
        self.session = requests.Session()
    
    def send_text_message(self, content: str, mentioned_list: Optional[List[str]] = None) -> bool:
        """发送文本消息"""
        message = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or self.config.mentioned_list or [],
                "mentioned_mobile_list": self.config.mentioned_mobile_list or []
            }
        }
        
        return self._send_message(message)
    
    def send_markdown_message(self, content: str) -> bool:
        """发送Markdown消息"""
        message = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        return self._send_message(message)
    
    def send_test_result_summary(self, test_results: List[Dict[str, Any]], 
                               test_name: str = "API接口测试") -> bool:
        """发送测试结果摘要"""
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result.get('success', False))
        failed_tests = total_tests - passed_tests
        
        # 计算成功率
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # 生成状态图标
        status_icon = "✅" if failed_tests == 0 else "❌" if passed_tests == 0 else "⚠️"
        
        # 构建Markdown消息
        content = f"""# {status_icon} {test_name}结果通知

## 📊 测试概览
- **总测试数**: {total_tests}
- **通过数**: {passed_tests} ✅
- **失败数**: {failed_tests} ❌
- **成功率**: {success_rate:.1f}%

## 📅 执行信息
- **执行时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **测试环境**: {self._get_test_environment()}

"""
        
        # 添加失败测试详情
        if failed_tests > 0:
            content += "## ❌ 失败测试详情\n"
            for result in test_results:
                if not result.get('success', False):
                    test_name = result.get('test_name', 'Unknown')
                    error = result.get('error', 'Unknown error')
                    content += f"- **{test_name}**: {error}\n"
            content += "\n"
        
        # 添加性能统计
        if test_results:
            response_times = [r.get('response_time', 0) for r in test_results if 'response_time' in r]
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                max_time = max(response_times)
                content += f"## ⏱️ 性能统计\n"
                content += f"- **平均响应时间**: {avg_time:.3f}s\n"
                content += f"- **最大响应时间**: {max_time:.3f}s\n\n"
        
        content += "---\n*API测试框架自动推送*"
        
        return self.send_markdown_message(content)
    
    def send_test_start_notification(self, test_suite: str, test_count: int) -> bool:
        """发送测试开始通知"""
        content = f"""# 🚀 测试开始通知

## 📋 测试信息
- **测试套件**: {test_suite}
- **测试用例数**: {test_count}
- **开始时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **测试环境**: {self._get_test_environment()}

正在执行测试，请稍候...

---
*API测试框架自动推送*"""
        
        return self.send_markdown_message(content)
    
    def send_critical_error_alert(self, error_message: str, test_name: str = "") -> bool:
        """发送严重错误告警"""
        content = f"""# 🚨 严重错误告警

## ❌ 错误信息
- **测试名称**: {test_name or '未知测试'}
- **错误时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **错误详情**: {error_message}

请立即检查测试环境和配置！

---
*API测试框架自动推送*"""
        
        return self.send_markdown_message(content)
    
    def send_performance_alert(self, slow_tests: List[Dict[str, Any]], threshold: float = 5.0) -> bool:
        """发送性能告警"""
        if not slow_tests:
            return True
        
        content = f"""# ⚠️ 性能告警

检测到响应时间超过 {threshold}s 的测试：

"""
        
        for test in slow_tests:
            test_name = test.get('test_name', 'Unknown')
            response_time = test.get('response_time', 0)
            url = test.get('url', 'Unknown')
            content += f"- **{test_name}**: {response_time:.3f}s ({url})\n"
        
        content += f"""
## 建议
- 检查网络连接
- 优化接口性能
- 调整超时配置

---
*API测试框架自动推送*"""
        
        return self.send_markdown_message(content)
    
    def send_news_message(self, articles: List[Dict[str, str]]) -> bool:
        """发送图文消息"""
        message = {
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }
        
        return self._send_message(message)
    
    def send_file_message(self, media_id: str) -> bool:
        """发送文件消息"""
        message = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        
        return self._send_message(message)
    
    def _send_message(self, message: Dict[str, Any]) -> bool:
        """发送消息到企业微信"""
        try:
            response = self.session.post(
                self.config.webhook_url,
                json=message,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    logger.info("WeChat message sent successfully")
                    return True
                else:
                    logger.error(f"WeChat API error: {result.get('errmsg', 'Unknown error')}")
                    return False
            else:
                logger.error(f"WeChat HTTP error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send WeChat message: {e}")
            return False
    
    def _get_test_environment(self) -> str:
        """获取测试环境信息"""
        import platform
        import os
        
        env_info = []
        
        # 操作系统
        env_info.append(f"{platform.system()} {platform.release()}")
        
        # Python版本
        env_info.append(f"Python {platform.python_version()}")
        
        # 环境变量中的环境标识
        if 'TEST_ENV' in os.environ:
            env_info.append(f"ENV: {os.environ['TEST_ENV']}")
        
        return " | ".join(env_info)

class WeChatReportSender:
    """企业微信报告发送器"""
    
    def __init__(self, notifier: WeChatNotifier):
        self.notifier = notifier
    
    def send_allure_report_notification(self, report_url: str, test_results: List[Dict[str, Any]]) -> bool:
        """发送Allure报告通知"""
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result.get('success', False))
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # 构建图文消息
        articles = [{
            "title": f"📊 API测试报告 - {time.strftime('%Y-%m-%d %H:%M')}",
            "description": f"总计: {total_tests} | 通过: {passed_tests} | 失败: {failed_tests} | 成功率: {success_rate:.1f}%",
            "url": report_url,
            "picurl": self._get_report_thumbnail_url()
        }]
        
        return self.notifier.send_news_message(articles)
    
    def send_detailed_test_report(self, test_results: List[Dict[str, Any]], 
                                report_path: str = "") -> bool:
        """发送详细测试报告"""
        # 分析测试结果
        analysis = self._analyze_test_results(test_results)
        
        content = f"""# 📋 详细测试报告

## 📊 执行统计
- **总测试数**: {analysis['total']}
- **通过**: {analysis['passed']} ✅
- **失败**: {analysis['failed']} ❌
- **跳过**: {analysis['skipped']} ⏭️
- **成功率**: {analysis['success_rate']:.1f}%

## ⏱️ 性能分析
- **总执行时间**: {analysis['total_time']:.2f}s
- **平均响应时间**: {analysis['avg_response_time']:.3f}s
- **最慢接口**: {analysis['slowest_test']}

## 📈 状态码分布
"""
        
        for status_code, count in analysis['status_codes'].items():
            content += f"- **{status_code}**: {count}次\n"
        
        if analysis['failed_tests']:
            content += "\n## ❌ 失败测试\n"
            for test in analysis['failed_tests'][:5]:  # 只显示前5个失败测试
                content += f"- **{test['name']}**: {test['error']}\n"
            
            if len(analysis['failed_tests']) > 5:
                content += f"- ... 还有 {len(analysis['failed_tests']) - 5} 个失败测试\n"
        
        if report_path:
            content += f"\n## 📄 完整报告\n[点击查看详细报告]({report_path})\n"
        
        content += "\n---\n*API测试框架自动生成*"
        
        return self.notifier.send_markdown_message(content)
    
    def _analyze_test_results(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析测试结果"""
        analysis = {
            'total': len(test_results),
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'total_time': 0,
            'response_times': [],
            'status_codes': {},
            'failed_tests': []
        }
        
        for result in test_results:
            # 统计状态
            if result.get('success', False):
                analysis['passed'] += 1
            elif result.get('skipped', False):
                analysis['skipped'] += 1
            else:
                analysis['failed'] += 1
                analysis['failed_tests'].append({
                    'name': result.get('test_name', 'Unknown'),
                    'error': result.get('error', 'Unknown error')
                })
            
            # 统计时间
            response_time = result.get('response_time', 0)
            analysis['response_times'].append(response_time)
            analysis['total_time'] += response_time
            
            # 统计状态码
            status_code = result.get('status_code')
            if status_code:
                analysis['status_codes'][status_code] = analysis['status_codes'].get(status_code, 0) + 1
        
        # 计算统计值
        analysis['success_rate'] = (analysis['passed'] / analysis['total'] * 100) if analysis['total'] > 0 else 0
        analysis['avg_response_time'] = sum(analysis['response_times']) / len(analysis['response_times']) if analysis['response_times'] else 0
        
        # 找出最慢的测试
        slowest_time = max(analysis['response_times']) if analysis['response_times'] else 0
        analysis['slowest_test'] = 'N/A'
        for result in test_results:
            if result.get('response_time', 0) == slowest_time:
                analysis['slowest_test'] = f"{result.get('test_name', 'Unknown')} ({slowest_time:.3f}s)"
                break
        
        return analysis
    
    def _get_report_thumbnail_url(self) -> str:
        """获取报告缩略图URL"""
        # 这里可以返回一个默认的报告图标URL
        return "https://via.placeholder.com/300x200/4CAF50/FFFFFF?text=Test+Report"

# 便捷函数
def create_wechat_notifier(webhook_url: str, **kwargs) -> WeChatNotifier:
    """创建企业微信通知器"""
    config = WeChatConfig(webhook_url=webhook_url, **kwargs)
    return WeChatNotifier(config)

def send_test_notification(webhook_url: str, test_results: List[Dict[str, Any]], 
                         test_name: str = "API接口测试") -> bool:
    """快速发送测试通知"""
    notifier = create_wechat_notifier(webhook_url)
    return notifier.send_test_result_summary(test_results, test_name)
