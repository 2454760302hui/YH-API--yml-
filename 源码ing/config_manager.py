"""
配置管理器模块
Configuration Manager Module

提供统一的配置管理功能，支持多环境配置和动态配置加载。
"""

import os
import yaml
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field

# 内置环境配置
class TestEnv:
    """测试环境配置"""
    BASE_URL = "https://httpbin.org"
    TIMEOUT = 30
    RETRY_COUNT = 3

class ProdEnv:
    """生产环境配置"""
    BASE_URL = "https://api.production.com"
    TIMEOUT = 60
    RETRY_COUNT = 5

class LocalEnv:
    """本地环境配置"""
    BASE_URL = "http://localhost:8000"
    TIMEOUT = 10
    RETRY_COUNT = 1


@dataclass
class ConfigManager:
    """配置管理器"""
    
    def __init__(self, env: str = "test", config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            env: 环境名称 (test, prod, local)
            config_file: 配置文件路径
        """
        self.env = env
        self.config_file = config_file
        self._config_cache = {}
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        # 加载环境配置
        if self.env == "test":
            self._env_config = TestEnv
        elif self.env == "prod":
            self._env_config = ProdEnv
        elif self.env == "local":
            self._env_config = LocalEnv
        else:
            self._env_config = TestEnv  # 默认使用测试环境
        
        # 如果指定了配置文件，加载文件配置
        if self.config_file and os.path.exists(self.config_file):
            self._load_config_file()
    
    def _load_config_file(self):
        """从文件加载配置"""
        try:
            config_path = Path(self.config_file)
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
            elif config_path.suffix.lower() == '.json':
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")
            
            self._config_cache.update(file_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值
            
        Returns:
            配置值
        """
        # 首先从缓存中查找
        if key in self._config_cache:
            return self._config_cache[key]
        
        # 支持嵌套键查找
        if '.' in key:
            return self._get_nested_value(key, default)
        
        # 从环境配置中查找
        if hasattr(self._env_config, key.upper()):
            return getattr(self._env_config, key.upper())
        
        return default
    
    def _get_nested_value(self, key: str, default: Any = None) -> Any:
        """获取嵌套配置值"""
        keys = key.split('.')
        current = self._config_cache
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        self._config_cache[key] = value
    
    def get_base_url(self) -> str:
        """获取基础URL"""
        return self.get('base_url', getattr(self._env_config, 'BASE_URL', 'https://httpbin.org'))
    
    def get_timeout(self) -> int:
        """获取超时时间"""
        return self.get('timeout', getattr(self._env_config, 'TIMEOUT', 30))
    
    def get_retry_count(self) -> int:
        """获取重试次数"""
        return self.get('retry_count', getattr(self._env_config, 'RETRY_COUNT', 3))
    
    def get_database_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return self.get('database', getattr(self._env_config, 'DATABASE', {}))
    
    def get_redis_config(self) -> Dict[str, Any]:
        """获取Redis配置"""
        return self.get('redis', getattr(self._env_config, 'REDIS', {}))
    
    def get_notification_config(self) -> Dict[str, Any]:
        """获取通知配置"""
        return self.get('notifications', {})
    
    def get_auth_config(self) -> Dict[str, Any]:
        """获取认证配置"""
        return self.get('auth', {})
    
    def get_reporting_config(self) -> Dict[str, Any]:
        """获取报告配置"""
        return self.get('reporting', {})
    
    def get_concurrency_config(self) -> Dict[str, Any]:
        """获取并发配置"""
        return self.get('concurrency', {})
    
    def update_from_dict(self, config_dict: Dict[str, Any]):
        """
        从字典更新配置
        
        Args:
            config_dict: 配置字典
        """
        self._config_cache.update(config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转换为字典
        
        Returns:
            配置字典
        """
        result = dict(self._config_cache)
        
        # 添加环境配置
        env_attrs = [attr for attr in dir(self._env_config) if not attr.startswith('_')]
        for attr in env_attrs:
            key = attr.lower()
            if key not in result:
                result[key] = getattr(self._env_config, attr)
        
        return result
    
    def reload(self):
        """重新加载配置"""
        self._config_cache.clear()
        self._load_config()
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"ConfigManager(env={self.env}, config_file={self.config_file})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return self.__str__()


# 全局配置管理器实例
_global_config_manager = None


def get_config_manager(env: str = "test", config_file: Optional[str] = None) -> ConfigManager:
    """
    获取全局配置管理器实例
    
    Args:
        env: 环境名称
        config_file: 配置文件路径
        
    Returns:
        ConfigManager实例
    """
    global _global_config_manager
    
    if _global_config_manager is None:
        _global_config_manager = ConfigManager(env=env, config_file=config_file)
    
    return _global_config_manager


def reset_config_manager():
    """重置全局配置管理器"""
    global _global_config_manager
    _global_config_manager = None
