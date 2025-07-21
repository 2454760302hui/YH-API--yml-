"""
数据驱动测试模块

提供增强的数据驱动测试功能，支持多种数据源和参数化方式。
"""

import csv
import json
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Iterator, Callable
from dataclasses import dataclass
from itertools import product

from logging_config import get_logger
from error_handler import handle_data_errors


@dataclass
class DataSource:
    """数据源配置"""
    
    type: str  # file, database, api, inline
    source: Union[str, Path, List[Dict], Dict]
    format: Optional[str] = None  # json, yaml, csv, excel
    query: Optional[str] = None  # SQL查询或API路径
    parameters: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """后处理初始化"""
        if isinstance(self.source, str):
            self.source = Path(self.source)


class DataProvider:
    """数据提供器基类"""
    
    def __init__(self, data_source: DataSource):
        """
        初始化数据提供器
        
        Args:
            data_source: 数据源配置
        """
        self.data_source = data_source
        self.logger = get_logger()
    
    @handle_data_errors
    def load_data(self) -> List[Dict[str, Any]]:
        """
        加载数据
        
        Returns:
            数据列表
            
        Raises:
            DataLoadError: 数据加载失败时抛出
        """
        if self.data_source.type == 'file':
            return self._load_from_file()
        elif self.data_source.type == 'database':
            return self._load_from_database()
        elif self.data_source.type == 'api':
            return self._load_from_api()
        elif self.data_source.type == 'inline':
            return self._load_from_inline()
        else:
            raise ValueError(f"不支持的数据源类型: {self.data_source.type}")
    
    def _load_from_file(self) -> List[Dict[str, Any]]:
        """从文件加载数据"""
        file_path = self.data_source.source
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"数据文件不存在: {file_path}")
        
        # 根据文件扩展名或指定格式确定加载方式
        format_type = self.data_source.format or file_path.suffix.lower().lstrip('.')
        
        if format_type in ['json']:
            return self._load_json(file_path)
        elif format_type in ['yaml', 'yml']:
            return self._load_yaml(file_path)
        elif format_type in ['csv']:
            return self._load_csv(file_path)
        elif format_type in ['xlsx', 'xls', 'excel']:
            return self._load_excel(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {format_type}")
    
    def _load_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """加载JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            raise ValueError("JSON数据必须是字典或字典列表")
    
    def _load_yaml(self, file_path: Path) -> List[Dict[str, Any]]:
        """加载YAML文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            raise ValueError("YAML数据必须是字典或字典列表")
    
    def _load_csv(self, file_path: Path) -> List[Dict[str, Any]]:
        """加载CSV文件"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data
    
    def _load_excel(self, file_path: Path) -> List[Dict[str, Any]]:
        """加载Excel文件"""
        try:
            import pandas as pd
            df = pd.read_excel(file_path)
            return df.to_dict('records')
        except ImportError:
            raise ImportError("需要安装pandas和openpyxl来支持Excel文件: pip install pandas openpyxl")
    
    def _load_from_database(self) -> List[Dict[str, Any]]:
        """从数据库加载数据"""
        from db import ConnectMysql
        
        if not self.data_source.query:
            raise ValueError("数据库数据源必须提供查询语句")
        
        # 从配置中获取数据库连接信息
        db_config = self.data_source.parameters or {}
        db = ConnectMysql(**db_config)
        
        result = db.query_sql(self.data_source.query)
        if isinstance(result, dict):
            return [result]
        elif isinstance(result, list):
            return result
        else:
            return []
    
    def _load_from_api(self) -> List[Dict[str, Any]]:
        """从API加载数据"""
        from http_client import HttpClient

        client = HttpClient()
        url = str(self.data_source.source)

        # 支持GET和POST请求
        method = self.data_source.parameters.get('method', 'GET') if self.data_source.parameters else 'GET'

        if method.upper() == 'GET':
            response = client.get(url, params=self.data_source.parameters)
        else:
            response = client.post(url, json=self.data_source.parameters)

        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            return []
    
    def _load_from_inline(self) -> List[Dict[str, Any]]:
        """从内联数据加载"""
        data = self.data_source.source
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            raise ValueError("内联数据必须是字典或字典列表")


class ParameterGenerator:
    """参数生成器"""
    
    def __init__(self):
        """初始化参数生成器"""
        self.logger = get_logger()
    
    @handle_data_errors
    def generate_combinations(self, parameters: Dict[str, List[Any]]) -> Iterator[Dict[str, Any]]:
        """
        生成参数组合
        
        Args:
            parameters: 参数字典，每个键对应一个值列表
            
        Yields:
            参数组合字典
        """
        if not parameters:
            yield {}
            return
        
        keys = list(parameters.keys())
        values = list(parameters.values())
        
        for combination in product(*values):
            yield dict(zip(keys, combination))
    
    @handle_data_errors
    def generate_pairwise(self, parameters: Dict[str, List[Any]]) -> Iterator[Dict[str, Any]]:
        """
        生成成对参数组合（减少测试用例数量）
        
        Args:
            parameters: 参数字典
            
        Yields:
            参数组合字典
        """
        try:
            from allpairspy import AllPairs
            
            keys = list(parameters.keys())
            values = list(parameters.values())
            
            for combination in AllPairs(values):
                yield dict(zip(keys, combination))
                
        except ImportError:
            self.logger.warning("allpairspy未安装，使用全组合方式。安装命令: pip install allpairspy")
            yield from self.generate_combinations(parameters)
    
    @handle_data_errors
    def generate_boundary_values(self, parameter_ranges: Dict[str, Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        """
        生成边界值测试数据
        
        Args:
            parameter_ranges: 参数范围配置
                格式: {
                    'param1': {'type': 'int', 'min': 1, 'max': 100},
                    'param2': {'type': 'string', 'min_length': 1, 'max_length': 50}
                }
                
        Yields:
            边界值参数组合
        """
        boundary_values = {}
        
        for param_name, config in parameter_ranges.items():
            param_type = config.get('type', 'int')
            
            if param_type == 'int':
                min_val = config.get('min', 0)
                max_val = config.get('max', 100)
                boundary_values[param_name] = [
                    min_val - 1,  # 下边界外
                    min_val,      # 下边界
                    min_val + 1,  # 下边界内
                    max_val - 1,  # 上边界内
                    max_val,      # 上边界
                    max_val + 1   # 上边界外
                ]
            elif param_type == 'string':
                min_len = config.get('min_length', 0)
                max_len = config.get('max_length', 100)
                boundary_values[param_name] = [
                    '',                    # 空字符串
                    'a' * (min_len - 1),   # 最小长度-1
                    'a' * min_len,         # 最小长度
                    'a' * (min_len + 1),   # 最小长度+1
                    'a' * (max_len - 1),   # 最大长度-1
                    'a' * max_len,         # 最大长度
                    'a' * (max_len + 1)    # 最大长度+1
                ]
        
        yield from self.generate_combinations(boundary_values)


class DataDrivenTestCase:
    """数据驱动测试用例"""
    
    def __init__(self, name: str, data_sources: List[DataSource], 
                 test_function: Callable, parameters: Optional[Dict[str, List[Any]]] = None):
        """
        初始化数据驱动测试用例
        
        Args:
            name: 测试用例名称
            data_sources: 数据源列表
            test_function: 测试函数
            parameters: 参数化配置
        """
        self.name = name
        self.data_sources = data_sources
        self.test_function = test_function
        self.parameters = parameters or {}
        self.logger = get_logger()
    
    @handle_data_errors
    def generate_test_data(self) -> Iterator[Dict[str, Any]]:
        """
        生成测试数据
        
        Yields:
            测试数据字典
        """
        # 从数据源加载数据
        all_data = []
        for data_source in self.data_sources:
            provider = DataProvider(data_source)
            data = provider.load_data()
            all_data.extend(data)
        
        # 如果有参数化配置，生成参数组合
        if self.parameters:
            generator = ParameterGenerator()
            for base_data in all_data:
                for param_combination in generator.generate_combinations(self.parameters):
                    # 合并基础数据和参数组合
                    combined_data = {**base_data, **param_combination}
                    yield combined_data
        else:
            # 直接使用数据源数据
            for data in all_data:
                yield data
    
    def run(self) -> List[Dict[str, Any]]:
        """
        运行数据驱动测试
        
        Returns:
            测试结果列表
        """
        results = []
        
        for i, test_data in enumerate(self.generate_test_data()):
            test_name = f"{self.name}[{i}]"
            self.logger.info(f"执行测试: {test_name}")
            
            try:
                result = self.test_function(test_data)
                results.append({
                    'name': test_name,
                    'data': test_data,
                    'result': result,
                    'status': 'PASSED'
                })
            except Exception as e:
                self.logger.error(f"测试失败: {test_name}, 错误: {e}")
                results.append({
                    'name': test_name,
                    'data': test_data,
                    'error': str(e),
                    'status': 'FAILED'
                })
        
        return results


def create_data_source(source_type: str, source: Union[str, Path, List, Dict], 
                      **kwargs) -> DataSource:
    """
    创建数据源配置的便捷函数
    
    Args:
        source_type: 数据源类型
        source: 数据源
        **kwargs: 其他配置参数
        
    Returns:
        数据源配置对象
    """
    return DataSource(
        type=source_type,
        source=source,
        format=kwargs.get('format'),
        query=kwargs.get('query'),
        parameters=kwargs.get('parameters')
    )
