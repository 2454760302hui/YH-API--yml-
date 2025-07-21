"""
测试运行器模块

提供统一的测试执行接口和结果管理功能。
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

from context import TestContext
from config_manager import ConfigManager
from logging_config import get_logger, get_test_logger
from error_handler import handle_test_errors


@dataclass
class TestResult:
    """测试结果数据类"""
    
    name: str
    status: str  # PASSED, FAILED, SKIPPED, ERROR
    duration: float = 0.0
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    test_data: Optional[Dict[str, Any]] = None
    assertions: List[Dict[str, Any]] = field(default_factory=list)
    extractions: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name': self.name,
            'status': self.status,
            'duration': self.duration,
            'error_message': self.error_message,
            'error_traceback': self.error_traceback,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'test_data': self.test_data,
            'assertions': self.assertions,
            'extractions': self.extractions
        }


@dataclass
class TestSuite:
    """测试套件数据类"""
    
    name: str
    tests: List[TestResult] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def duration(self) -> float:
        """计算总耗时"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return sum(test.duration for test in self.tests)
    
    @property
    def passed_count(self) -> int:
        """通过的测试数量"""
        return len([t for t in self.tests if t.status == 'PASSED'])
    
    @property
    def failed_count(self) -> int:
        """失败的测试数量"""
        return len([t for t in self.tests if t.status == 'FAILED'])
    
    @property
    def skipped_count(self) -> int:
        """跳过的测试数量"""
        return len([t for t in self.tests if t.status == 'SKIPPED'])
    
    @property
    def error_count(self) -> int:
        """错误的测试数量"""
        return len([t for t in self.tests if t.status == 'ERROR'])
    
    @property
    def total_count(self) -> int:
        """总测试数量"""
        return len(self.tests)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name': self.name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'total_count': self.total_count,
            'passed_count': self.passed_count,
            'failed_count': self.failed_count,
            'skipped_count': self.skipped_count,
            'error_count': self.error_count,
            'tests': [test.to_dict() for test in self.tests]
        }


class TestRunner:
    """测试运行器"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        初始化测试运行器
        
        Args:
            config_manager: 配置管理器实例
        """
        self.config_manager = config_manager or ConfigManager()
        self.logger = get_logger()
        self.test_logger = get_test_logger()
        self.context = TestContext()
        
        # 测试结果
        self.current_suite: Optional[TestSuite] = None
        self.current_test: Optional[TestResult] = None
        self.suites: List[TestSuite] = []
    
    def start_suite(self, name: str) -> TestSuite:
        """
        开始测试套件
        
        Args:
            name: 套件名称
            
        Returns:
            测试套件对象
        """
        self.current_suite = TestSuite(
            name=name,
            start_time=datetime.now()
        )
        self.suites.append(self.current_suite)
        
        self.logger.info(f"🚀 开始测试套件: {name}")
        return self.current_suite
    
    def end_suite(self) -> Optional[TestSuite]:
        """
        结束当前测试套件
        
        Returns:
            结束的测试套件对象
        """
        if self.current_suite:
            self.current_suite.end_time = datetime.now()
            
            self.logger.info(f"✅ 测试套件完成: {self.current_suite.name}")
            self.logger.info(f"📊 统计信息: 总计 {self.current_suite.total_count}, "
                           f"通过 {self.current_suite.passed_count}, "
                           f"失败 {self.current_suite.failed_count}, "
                           f"跳过 {self.current_suite.skipped_count}, "
                           f"错误 {self.current_suite.error_count}")
            self.logger.info(f"⏱️ 耗时: {self.current_suite.duration:.3f}s")
            
            suite = self.current_suite
            self.current_suite = None
            return suite
        
        return None
    
    @handle_test_errors
    def start_test(self, name: str, test_data: Optional[Dict[str, Any]] = None) -> TestResult:
        """
        开始单个测试
        
        Args:
            name: 测试名称
            test_data: 测试数据
            
        Returns:
            测试结果对象
        """
        if not self.current_suite:
            raise ValueError("必须先开始测试套件")
        
        self.current_test = TestResult(
            name=name,
            status='RUNNING',
            start_time=datetime.now(),
            test_data=test_data
        )
        
        self.current_suite.tests.append(self.current_test)
        self.test_logger.log_test_start(name, test_data)
        
        return self.current_test
    
    @handle_test_errors
    def end_test(self, status: str = 'PASSED', error_message: Optional[str] = None,
                error_traceback: Optional[str] = None) -> Optional[TestResult]:
        """
        结束当前测试
        
        Args:
            status: 测试状态
            error_message: 错误消息
            error_traceback: 错误堆栈
            
        Returns:
            结束的测试结果对象
        """
        if not self.current_test:
            return None
        
        self.current_test.status = status
        self.current_test.end_time = datetime.now()
        self.current_test.error_message = error_message
        self.current_test.error_traceback = error_traceback
        
        if self.current_test.start_time and self.current_test.end_time:
            self.current_test.duration = (
                self.current_test.end_time - self.current_test.start_time
            ).total_seconds()
        
        self.test_logger.log_test_end(
            self.current_test.name, 
            status, 
            self.current_test.duration
        )
        
        test = self.current_test
        self.current_test = None
        return test
    
    def add_assertion(self, expression: str, expected: Any, actual: Any, result: bool):
        """
        添加断言结果
        
        Args:
            expression: 断言表达式
            expected: 期望值
            actual: 实际值
            result: 断言结果
        """
        if self.current_test:
            assertion = {
                'expression': expression,
                'expected': expected,
                'actual': actual,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            self.current_test.assertions.append(assertion)
            
            self.test_logger.log_validation(expression, expected, actual, result)
    
    def add_extraction(self, expression: str, value: Any):
        """
        添加数据提取结果
        
        Args:
            expression: 提取表达式
            value: 提取的值
        """
        if self.current_test:
            extraction = {
                'expression': expression,
                'value': value,
                'timestamp': datetime.now().isoformat()
            }
            self.current_test.extractions.append(extraction)
            
            self.test_logger.log_extraction(expression, value)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取测试总结
        
        Returns:
            测试总结字典
        """
        total_tests = sum(suite.total_count for suite in self.suites)
        total_passed = sum(suite.passed_count for suite in self.suites)
        total_failed = sum(suite.failed_count for suite in self.suites)
        total_skipped = sum(suite.skipped_count for suite in self.suites)
        total_errors = sum(suite.error_count for suite in self.suites)
        total_duration = sum(suite.duration for suite in self.suites)
        
        return {
            'total_suites': len(self.suites),
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'total_skipped': total_skipped,
            'total_errors': total_errors,
            'total_duration': total_duration,
            'success_rate': (total_passed / total_tests * 100) if total_tests > 0 else 0,
            'suites': [suite.to_dict() for suite in self.suites]
        }
    
    def save_results(self, output_path: Optional[Union[str, Path]] = None):
        """
        保存测试结果到文件
        
        Args:
            output_path: 输出文件路径
        """
        import json
        
        if output_path is None:
            output_path = Path("test_results") / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        summary = self.get_summary()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"📄 测试结果已保存到: {output_path}")


# 全局测试运行器实例
_test_runner: Optional[TestRunner] = None


def get_test_runner() -> TestRunner:
    """获取全局测试运行器实例"""
    global _test_runner
    if _test_runner is None:
        _test_runner = TestRunner()
    return _test_runner


def reset_test_runner():
    """重置全局测试运行器实例"""
    global _test_runner
    _test_runner = None
