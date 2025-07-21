"""
并发测试运行器模块

提供多线程和异步测试执行支持，提高测试执行效率。
"""

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from queue import Queue, Empty

from test_runner import TestRunner, TestResult, TestSuite
from logging_config import get_logger
from error_handler import handle_concurrent_errors


@dataclass
class ConcurrentConfig:
    """并发配置"""
    
    max_workers: int = 4  # 最大工作线程数
    timeout: Optional[float] = None  # 超时时间（秒）
    retry_count: int = 0  # 重试次数
    retry_delay: float = 1.0  # 重试延迟（秒）
    fail_fast: bool = False  # 遇到失败时是否立即停止
    thread_local_session: bool = True  # 是否使用线程本地会话


@dataclass
class ConcurrentTask:
    """并发任务"""
    
    id: str
    name: str
    test_function: Callable
    test_data: Dict[str, Any]
    priority: int = 0  # 优先级，数字越大优先级越高
    dependencies: List[str] = field(default_factory=list)  # 依赖的任务ID
    retry_count: int = 0
    max_retries: int = 0
    
    def __lt__(self, other):
        """支持优先级队列排序"""
        return self.priority > other.priority


class ConcurrentTestRunner:
    """并发测试运行器"""
    
    def __init__(self, config: Optional[ConcurrentConfig] = None):
        """
        初始化并发测试运行器
        
        Args:
            config: 并发配置
        """
        self.config = config or ConcurrentConfig()
        self.logger = get_logger()
        self.test_runner = TestRunner()
        
        # 任务管理
        self.tasks: Dict[str, ConcurrentTask] = {}
        self.completed_tasks: Dict[str, TestResult] = {}
        self.failed_tasks: Dict[str, Exception] = {}
        self.task_queue = Queue()
        
        # 线程本地存储
        self.thread_local = threading.local()
        
        # 统计信息
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_tasks = 0
        self.completed_count = 0
        self.failed_count = 0
    
    def add_task(self, task: ConcurrentTask):
        """
        添加并发任务
        
        Args:
            task: 并发任务
        """
        self.tasks[task.id] = task
        self.logger.debug(f"添加并发任务: {task.name} (ID: {task.id})")
    
    def add_simple_task(self, task_id: str, name: str, test_function: Callable, 
                       test_data: Dict[str, Any], **kwargs):
        """
        添加简单任务的便捷方法
        
        Args:
            task_id: 任务ID
            name: 任务名称
            test_function: 测试函数
            test_data: 测试数据
            **kwargs: 其他任务配置
        """
        task = ConcurrentTask(
            id=task_id,
            name=name,
            test_function=test_function,
            test_data=test_data,
            **kwargs
        )
        self.add_task(task)
    
    @handle_concurrent_errors
    def run_concurrent(self) -> Dict[str, Any]:
        """
        运行并发测试
        
        Returns:
            测试结果摘要
        """
        if not self.tasks:
            self.logger.warning("没有要执行的任务")
            return self._get_summary()
        
        self.start_time = datetime.now()
        self.total_tasks = len(self.tasks)
        
        self.logger.info(f"🚀 开始并发测试执行，任务数: {self.total_tasks}, 工作线程: {self.config.max_workers}")
        
        # 开始测试套件
        suite_name = f"ConcurrentTest_{self.start_time.strftime('%Y%m%d_%H%M%S')}"
        self.test_runner.start_suite(suite_name)
        
        try:
            # 使用线程池执行任务
            with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                # 提交所有可执行的任务
                futures = self._submit_ready_tasks(executor)
                
                # 处理完成的任务
                self._process_completed_tasks(executor, futures)
            
        except Exception as e:
            self.logger.error(f"并发测试执行出错: {e}")
            raise
        finally:
            self.end_time = datetime.now()
            self.test_runner.end_suite()
        
        return self._get_summary()
    
    def _submit_ready_tasks(self, executor: ThreadPoolExecutor) -> Dict[str, Future]:
        """
        提交准备就绪的任务
        
        Args:
            executor: 线程池执行器
            
        Returns:
            Future对象字典
        """
        futures = {}
        
        for task_id, task in self.tasks.items():
            if self._is_task_ready(task):
                future = executor.submit(self._execute_task, task)
                futures[task_id] = future
                self.logger.debug(f"提交任务: {task.name}")
        
        return futures
    
    def _is_task_ready(self, task: ConcurrentTask) -> bool:
        """
        检查任务是否准备就绪
        
        Args:
            task: 任务对象
            
        Returns:
            是否准备就绪
        """
        # 检查依赖是否完成
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        # 检查是否已经完成或失败
        if task.id in self.completed_tasks or task.id in self.failed_tasks:
            return False
        
        return True
    
    def _process_completed_tasks(self, executor: ThreadPoolExecutor, futures: Dict[str, Future]):
        """
        处理完成的任务
        
        Args:
            executor: 线程池执行器
            futures: Future对象字典
        """
        while futures or (self.completed_count + self.failed_count < self.total_tasks):
            # 等待任务完成
            completed_futures = []
            for task_id, future in list(futures.items()):
                if future.done():
                    completed_futures.append((task_id, future))
                    del futures[task_id]
            
            # 处理完成的任务
            for task_id, future in completed_futures:
                try:
                    result = future.result(timeout=1.0)
                    self.completed_tasks[task_id] = result
                    self.completed_count += 1
                    
                    self.logger.info(f"✅ 任务完成: {self.tasks[task_id].name}")
                    
                    # 检查是否有新的任务可以执行
                    new_futures = self._submit_ready_tasks(executor)
                    futures.update(new_futures)
                    
                except Exception as e:
                    task = self.tasks[task_id]
                    
                    # 检查是否需要重试
                    if task.retry_count < task.max_retries:
                        task.retry_count += 1
                        self.logger.warning(f"⚠️ 任务失败，准备重试 ({task.retry_count}/{task.max_retries}): {task.name}")
                        
                        # 延迟后重新提交
                        time.sleep(self.config.retry_delay)
                        future = executor.submit(self._execute_task, task)
                        futures[task_id] = future
                    else:
                        self.failed_tasks[task_id] = e
                        self.failed_count += 1
                        
                        self.logger.error(f"❌ 任务失败: {task.name}, 错误: {e}")
                        
                        if self.config.fail_fast:
                            self.logger.error("启用了快速失败模式，停止执行")
                            # 取消所有未完成的任务
                            for remaining_future in futures.values():
                                remaining_future.cancel()
                            return
            
            # 短暂休眠避免忙等待
            if futures:
                time.sleep(0.1)
    
    @handle_concurrent_errors
    def _execute_task(self, task: ConcurrentTask) -> TestResult:
        """
        执行单个任务
        
        Args:
            task: 任务对象
            
        Returns:
            测试结果
        """
        # 设置线程本地存储
        if self.config.thread_local_session:
            self._setup_thread_local()
        
        # 开始测试
        test_result = self.test_runner.start_test(task.name, task.test_data)
        
        try:
            # 执行测试函数
            start_time = time.time()
            
            if self.config.timeout:
                # 使用超时执行
                result = self._execute_with_timeout(task.test_function, task.test_data, self.config.timeout)
            else:
                result = task.test_function(task.test_data)
            
            duration = time.time() - start_time
            
            # 结束测试
            self.test_runner.end_test('PASSED')
            
            self.logger.debug(f"任务执行成功: {task.name}, 耗时: {duration:.3f}s")
            return test_result
            
        except Exception as e:
            # 结束测试并记录错误
            self.test_runner.end_test('FAILED', str(e))
            raise e
    
    def _setup_thread_local(self):
        """设置线程本地存储"""
        if not hasattr(self.thread_local, 'session'):
            from http_session import HttpSession
            self.thread_local.session = HttpSession()
            self.logger.debug(f"为线程 {threading.current_thread().name} 创建会话")
    
    def _execute_with_timeout(self, func: Callable, data: Dict[str, Any], timeout: float) -> Any:
        """
        带超时的函数执行
        
        Args:
            func: 要执行的函数
            data: 函数参数
            timeout: 超时时间
            
        Returns:
            函数执行结果
        """
        result_queue = Queue()
        exception_queue = Queue()
        
        def target():
            try:
                result = func(data)
                result_queue.put(result)
            except Exception as e:
                exception_queue.put(e)
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # 超时了，但无法强制终止线程
            self.logger.warning(f"任务执行超时: {timeout}s")
            raise TimeoutError(f"任务执行超时: {timeout}s")
        
        # 检查是否有异常
        try:
            exception = exception_queue.get_nowait()
            raise exception
        except Empty:
            pass
        
        # 获取结果
        try:
            return result_queue.get_nowait()
        except Empty:
            raise RuntimeError("任务执行完成但没有返回结果")
    
    def _get_summary(self) -> Dict[str, Any]:
        """
        获取执行摘要
        
        Returns:
            执行摘要字典
        """
        duration = 0.0
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            'total_tasks': self.total_tasks,
            'completed_count': self.completed_count,
            'failed_count': self.failed_count,
            'success_rate': (self.completed_count / self.total_tasks * 100) if self.total_tasks > 0 else 0,
            'duration': duration,
            'max_workers': self.config.max_workers,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'completed_tasks': list(self.completed_tasks.keys()),
            'failed_tasks': {task_id: str(error) for task_id, error in self.failed_tasks.items()}
        }


class AsyncTestRunner:
    """异步测试运行器"""
    
    def __init__(self, config: Optional[ConcurrentConfig] = None):
        """
        初始化异步测试运行器
        
        Args:
            config: 并发配置
        """
        self.config = config or ConcurrentConfig()
        self.logger = get_logger()
        self.test_runner = TestRunner()
        
        # 任务管理
        self.tasks: List[Callable] = []
        self.semaphore: Optional[asyncio.Semaphore] = None
    
    def add_async_task(self, coro: Callable):
        """
        添加异步任务
        
        Args:
            coro: 协程函数
        """
        self.tasks.append(coro)
    
    async def run_async(self) -> Dict[str, Any]:
        """
        运行异步测试
        
        Returns:
            测试结果摘要
        """
        if not self.tasks:
            self.logger.warning("没有要执行的异步任务")
            return {'total_tasks': 0, 'completed_count': 0, 'failed_count': 0}
        
        # 创建信号量限制并发数
        self.semaphore = asyncio.Semaphore(self.config.max_workers)
        
        start_time = datetime.now()
        self.logger.info(f"🚀 开始异步测试执行，任务数: {len(self.tasks)}")
        
        # 开始测试套件
        suite_name = f"AsyncTest_{start_time.strftime('%Y%m%d_%H%M%S')}"
        self.test_runner.start_suite(suite_name)
        
        try:
            # 执行所有异步任务
            results = await asyncio.gather(*[self._execute_async_task(task) for task in self.tasks], 
                                         return_exceptions=True)
            
            # 统计结果
            completed_count = sum(1 for r in results if not isinstance(r, Exception))
            failed_count = sum(1 for r in results if isinstance(r, Exception))
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.info(f"✅ 异步测试完成，成功: {completed_count}, 失败: {failed_count}, 耗时: {duration:.3f}s")
            
            return {
                'total_tasks': len(self.tasks),
                'completed_count': completed_count,
                'failed_count': failed_count,
                'success_rate': (completed_count / len(self.tasks) * 100) if self.tasks else 0,
                'duration': duration,
                'results': results
            }
            
        finally:
            self.test_runner.end_suite()
    
    async def _execute_async_task(self, task: Callable) -> Any:
        """
        执行异步任务
        
        Args:
            task: 异步任务
            
        Returns:
            任务执行结果
        """
        async with self.semaphore:
            try:
                if self.config.timeout:
                    return await asyncio.wait_for(task(), timeout=self.config.timeout)
                else:
                    return await task()
            except Exception as e:
                self.logger.error(f"异步任务执行失败: {e}")
                raise


def create_concurrent_config(max_workers: int = 4, timeout: Optional[float] = None, 
                           **kwargs) -> ConcurrentConfig:
    """
    创建并发配置的便捷函数
    
    Args:
        max_workers: 最大工作线程数
        timeout: 超时时间
        **kwargs: 其他配置参数
        
    Returns:
        并发配置对象
    """
    return ConcurrentConfig(
        max_workers=max_workers,
        timeout=timeout,
        **kwargs
    )
