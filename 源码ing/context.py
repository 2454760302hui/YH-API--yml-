"""
上下文管理模块

提供测试执行上下文管理，替代全局变量，支持变量作用域和依赖注入。
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from threading import local
import copy
from logging_config import get_logger
log = get_logger()
from exceptions import VariableError


@dataclass
class VariableScope:
    """变量作用域"""
    name: str
    variables: Dict[str, Any] = field(default_factory=dict)
    parent: Optional['VariableScope'] = None
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取变量值"""
        if key in self.variables:
            return self.variables[key]
        elif self.parent:
            return self.parent.get(key, default)
        else:
            return default
    
    def set(self, key: str, value: Any) -> None:
        """设置变量值"""
        self.variables[key] = value
    
    def update(self, variables: Dict[str, Any]) -> None:
        """批量更新变量"""
        self.variables.update(variables)
    
    def has(self, key: str) -> bool:
        """检查变量是否存在"""
        if key in self.variables:
            return True
        elif self.parent:
            return self.parent.has(key)
        else:
            return False
    
    def list_variables(self) -> Dict[str, Any]:
        """列出所有可用变量"""
        all_vars = {}
        if self.parent:
            all_vars.update(self.parent.list_variables())
        all_vars.update(self.variables)
        return all_vars
    
    def create_child(self, name: str) -> 'VariableScope':
        """创建子作用域"""
        return VariableScope(name=name, parent=self)


class TestContext:
    """测试执行上下文"""
    
    def __init__(self, test_name: str = "default"):
        """
        初始化测试上下文
        
        Args:
            test_name: 测试名称
        """
        self.test_name = test_name
        self.global_scope = VariableScope("global")
        self.module_scope = VariableScope("module", parent=self.global_scope)
        self.function_scope = VariableScope("function", parent=self.module_scope)
        self.step_scope = VariableScope("step", parent=self.function_scope)
        
        # 当前作用域
        self.current_scope = self.step_scope
        
        # 导出变量列表
        self.exported_variables: List[str] = []
        
        # 钩子函数
        self.hooks: Dict[str, List[Callable]] = {
            "before_request": [],
            "after_request": [],
            "before_validation": [],
            "after_validation": [],
            "before_extraction": [],
            "after_extraction": []
        }
        
        # 上下文数据
        self.context_data: Dict[str, Any] = {}
        
        log.debug(f"创建测试上下文: {test_name}")
    
    def set_variable(self, key: str, value: Any, scope: str = "step") -> None:
        """
        设置变量
        
        Args:
            key: 变量名
            value: 变量值
            scope: 作用域 (global, module, function, step)
        """
        scope_map = {
            "global": self.global_scope,
            "module": self.module_scope,
            "function": self.function_scope,
            "step": self.step_scope
        }
        
        target_scope = scope_map.get(scope)
        if not target_scope:
            raise VariableError(f"无效的变量作用域: {scope}", variable_name=key)
        
        target_scope.set(key, value)
        log.debug(f"设置变量 {key}={value} (作用域: {scope})")
    
    def get_variable(self, key: str, default: Any = None) -> Any:
        """
        获取变量值
        
        Args:
            key: 变量名
            default: 默认值
            
        Returns:
            变量值
        """
        value = self.current_scope.get(key, default)
        if value is default and default is None:
            available_vars = list(self.current_scope.list_variables().keys())
            raise VariableError(
                f"变量 '{key}' 未定义",
                variable_name=key,
                variable_scope=self.current_scope.name,
                available_variables=available_vars
            )
        return value
    
    def has_variable(self, key: str) -> bool:
        """检查变量是否存在"""
        return self.current_scope.has(key)
    
    def update_variables(self, variables: Dict[str, Any], scope: str = "step") -> None:
        """
        批量更新变量
        
        Args:
            variables: 变量字典
            scope: 作用域
        """
        scope_map = {
            "global": self.global_scope,
            "module": self.module_scope,
            "function": self.function_scope,
            "step": self.step_scope
        }
        
        target_scope = scope_map.get(scope)
        if not target_scope:
            raise VariableError(f"无效的变量作用域: {scope}")
        
        target_scope.update(variables)
        log.debug(f"批量更新变量 (作用域: {scope}): {list(variables.keys())}")
    
    def list_all_variables(self) -> Dict[str, Any]:
        """列出所有可用变量"""
        return self.current_scope.list_variables()
    
    def export_variables(self, variable_names: List[str]) -> None:
        """
        导出变量到全局作用域
        
        Args:
            variable_names: 要导出的变量名列表
        """
        for var_name in variable_names:
            if self.has_variable(var_name):
                value = self.get_variable(var_name)
                self.global_scope.set(var_name, value)
                self.exported_variables.append(var_name)
                log.debug(f"导出变量到全局作用域: {var_name}={value}")
            else:
                log.warning(f"尝试导出不存在的变量: {var_name}")
    
    def create_step_context(self, step_name: str) -> 'StepContext':
        """
        创建步骤上下文
        
        Args:
            step_name: 步骤名称
            
        Returns:
            步骤上下文管理器
        """
        return StepContext(self, step_name)
    
    def add_hook(self, hook_type: str, func: Callable) -> None:
        """
        添加钩子函数
        
        Args:
            hook_type: 钩子类型
            func: 钩子函数
        """
        if hook_type in self.hooks:
            self.hooks[hook_type].append(func)
            log.debug(f"添加钩子函数: {hook_type}")
        else:
            log.warning(f"无效的钩子类型: {hook_type}")
    
    def execute_hooks(self, hook_type: str, *args, **kwargs) -> None:
        """
        执行钩子函数
        
        Args:
            hook_type: 钩子类型
            *args: 位置参数
            **kwargs: 关键字参数
        """
        hooks = self.hooks.get(hook_type, [])
        for hook in hooks:
            try:
                hook(*args, **kwargs)
                log.debug(f"执行钩子函数: {hook_type}")
            except Exception as e:
                log.error(f"钩子函数执行失败 {hook_type}: {e}")
    
    def set_context_data(self, key: str, value: Any) -> None:
        """设置上下文数据"""
        self.context_data[key] = value
    
    def get_context_data(self, key: str, default: Any = None) -> Any:
        """获取上下文数据"""
        return self.context_data.get(key, default)
    
    def clear_step_scope(self) -> None:
        """清空步骤作用域"""
        self.step_scope.variables.clear()
        log.debug("清空步骤作用域变量")
    
    def copy(self) -> 'TestContext':
        """创建上下文副本"""
        new_context = TestContext(self.test_name)
        
        # 复制变量作用域
        new_context.global_scope.variables = copy.deepcopy(self.global_scope.variables)
        new_context.module_scope.variables = copy.deepcopy(self.module_scope.variables)
        new_context.function_scope.variables = copy.deepcopy(self.function_scope.variables)
        new_context.step_scope.variables = copy.deepcopy(self.step_scope.variables)
        
        # 复制其他数据
        new_context.exported_variables = self.exported_variables.copy()
        new_context.context_data = copy.deepcopy(self.context_data)
        
        return new_context


class StepContext:
    """步骤上下文管理器"""
    
    def __init__(self, test_context: TestContext, step_name: str):
        """
        初始化步骤上下文
        
        Args:
            test_context: 测试上下文
            step_name: 步骤名称
        """
        self.test_context = test_context
        self.step_name = step_name
        self.original_scope = None
    
    def __enter__(self) -> TestContext:
        """进入步骤上下文"""
        # 保存原始作用域
        self.original_scope = self.test_context.current_scope
        
        # 创建新的步骤作用域
        self.test_context.step_scope = VariableScope(
            f"step_{self.step_name}",
            parent=self.test_context.function_scope
        )
        self.test_context.current_scope = self.test_context.step_scope
        
        log.debug(f"进入步骤上下文: {self.step_name}")
        return self.test_context
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出步骤上下文"""
        # 恢复原始作用域
        if self.original_scope:
            self.test_context.current_scope = self.original_scope
        
        log.debug(f"退出步骤上下文: {self.step_name}")


# 线程本地存储
_thread_local = local()


def get_current_context() -> Optional[TestContext]:
    """获取当前线程的测试上下文"""
    return getattr(_thread_local, 'context', None)


def set_current_context(context: TestContext) -> None:
    """设置当前线程的测试上下文"""
    _thread_local.context = context


def create_test_context(test_name: str) -> TestContext:
    """
    创建并设置测试上下文
    
    Args:
        test_name: 测试名称
        
    Returns:
        测试上下文
    """
    context = TestContext(test_name)
    set_current_context(context)
    return context


def clear_current_context() -> None:
    """清除当前线程的测试上下文"""
    if hasattr(_thread_local, 'context'):
        delattr(_thread_local, 'context')
