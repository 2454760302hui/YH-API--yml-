"""
增强功能使用示例

展示如何使用新的增强功能进行接口测试
"""

import pytest
from pathlib import Path

# 导入增强功能模块
from config_manager import ConfigManager
from context import TestContext
from test_runner import TestRunner
from data_driven import DataProvider, create_data_source
from concurrent_runner import ConcurrentTestRunner, ConcurrentConfig
from parametrize import ParametrizedTestCase, create_parameter_spec
from enhanced_validation import EnhancedValidator, EnhancedExtractor, create_validation_rule, create_extraction_rule


class TestEnhancedFeatures:
    """增强功能测试示例"""
    
    def setup_class(self):
        """测试类初始化"""
        self.config_manager = ConfigManager()
        self.test_runner = TestRunner(self.config_manager)
        self.context = TestContext()
        
    def test_config_management(self):
        """配置管理示例"""
        # 加载配置
        config = self.config_manager.load_config('test')
        
        # 验证配置
        assert config is not None
        assert hasattr(config, 'base_url')
        
        print(f"✅ 配置加载成功: {config.base_url}")
    
    def test_context_management(self):
        """上下文管理示例"""
        # 设置全局变量
        self.context.set_variable('api_key', 'test-api-key-123', scope='global')
        self.context.set_variable('user_id', 12345, scope='module')
        
        # 获取变量
        api_key = self.context.get_variable('api_key')
        user_id = self.context.get_variable('user_id')
        
        assert api_key == 'test-api-key-123'
        assert user_id == 12345
        
        print(f"✅ 上下文管理成功: API Key={api_key}, User ID={user_id}")
    
    def test_enhanced_validation(self):
        """增强验证示例"""
        # 模拟API响应数据
        response_data = {
            'status': 'success',
            'data': {
                'user': {
                    'id': 123,
                    'name': 'John Doe',
                    'email': 'john@example.com',
                    'age': 30
                },
                'permissions': ['read', 'write']
            },
            'meta': {
                'total': 1,
                'page': 1
            }
        }
        
        # 创建验证规则
        validation_rules = [
            create_validation_rule('status_check', 'status', 'success'),
            create_validation_rule('user_id_check', 'data.user.id', 123),
            create_validation_rule('user_name_check', 'data.user.name', 'John Doe'),
            create_validation_rule('age_range_check', 'data.user.age', 18, 'ge'),
            create_validation_rule('permissions_check', 'read', 'data.permissions', 'in'),
            create_validation_rule('total_count_check', 'meta.total', 0, 'gt')
        ]
        
        # 执行验证
        validator = EnhancedValidator()
        results = validator.validate(response_data, validation_rules)
        
        assert results['success'] == True
        assert results['passed'] == 6
        assert results['failed'] == 0
        
        print(f"✅ 验证成功: 通过 {results['passed']} 个规则")
    
    def test_enhanced_extraction(self):
        """增强提取示例"""
        # 模拟API响应数据
        response_data = {
            'data': {
                'users': [
                    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
                    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
                ],
                'pagination': {
                    'total': 2,
                    'page': 1,
                    'per_page': 10
                }
            }
        }
        
        # 创建提取规则
        extraction_rules = [
            create_extraction_rule('first_user_id', 'data.users.0.id'),
            create_extraction_rule('first_user_name', 'data.users.0.name'),
            create_extraction_rule('user_count', 'data.pagination.total'),
            create_extraction_rule('all_user_names', 'data.users', post_processor=lambda users: [u['name'] for u in users])
        ]
        
        # 执行提取
        extractor = EnhancedExtractor()
        results = extractor.extract(response_data, extraction_rules)
        
        assert results['first_user_id'] == 1
        assert results['first_user_name'] == 'Alice'
        assert results['user_count'] == 2
        assert results['all_user_names'] == ['Alice', 'Bob']
        
        print(f"✅ 提取成功: {results}")
    
    def test_data_driven_testing(self):
        """数据驱动测试示例"""
        # 创建内联数据源
        test_data = [
            {'user_id': 1, 'expected_name': 'Alice'},
            {'user_id': 2, 'expected_name': 'Bob'},
            {'user_id': 3, 'expected_name': 'Charlie'}
        ]
        
        data_source = create_data_source('inline', test_data)
        provider = DataProvider(data_source)
        
        # 加载数据
        loaded_data = provider.load_data()
        
        assert len(loaded_data) == 3
        assert loaded_data[0]['user_id'] == 1
        assert loaded_data[0]['expected_name'] == 'Alice'
        
        print(f"✅ 数据驱动测试数据加载成功: {len(loaded_data)} 条记录")
    
    def test_parametrized_testing(self):
        """参数化测试示例"""
        # 定义测试函数
        def validate_user_data(params):
            user_id = params['user_id']
            name = params['name']
            age = params['age']
            
            # 模拟验证逻辑
            assert isinstance(user_id, int)
            assert isinstance(name, str)
            assert isinstance(age, int)
            assert age > 0
            
            return {'user_id': user_id, 'name': name, 'age': age, 'valid': True}
        
        # 创建参数规格
        parameter_specs = [
            create_parameter_spec('user_id', 'int', range_config={'min': 1, 'max': 100}),
            create_parameter_spec('name', 'string', range_config={'min_length': 2, 'max_length': 20}),
            create_parameter_spec('age', 'int', range_config={'min': 18, 'max': 80})
        ]
        
        # 创建参数化测试用例
        test_case = ParametrizedTestCase(
            'user_validation_test',
            validate_user_data,
            parameter_specs,
            strategy='random',
            strategy_config={'combination_count': 5}
        )
        
        # 运行测试
        results = test_case.run()
        
        assert len(results) == 5
        assert all(result['status'] == 'PASSED' for result in results)
        
        print(f"✅ 参数化测试成功: 执行了 {len(results)} 个测试用例")
    
    def test_concurrent_execution(self):
        """并发执行示例"""
        # 定义测试任务
        def mock_api_test(data):
            import time
            import random
            
            # 模拟API调用延迟
            time.sleep(random.uniform(0.1, 0.3))
            
            user_id = data['user_id']
            return {
                'user_id': user_id,
                'status': 'success',
                'response_time': random.uniform(0.1, 0.3)
            }
        
        # 创建并发配置
        config = ConcurrentConfig(
            max_workers=3,
            timeout=5.0,
            retry_count=1
        )
        
        # 创建并发运行器
        concurrent_runner = ConcurrentTestRunner(config)
        
        # 添加并发任务
        for i in range(10):
            concurrent_runner.add_simple_task(
                f'api_test_{i}',
                f'API测试 {i}',
                mock_api_test,
                {'user_id': i + 1}
            )
        
        # 执行并发测试
        summary = concurrent_runner.run_concurrent()
        
        assert summary['total_tasks'] == 10
        assert summary['completed_count'] == 10
        assert summary['failed_count'] == 0
        assert summary['success_rate'] == 100.0
        
        print(f"✅ 并发测试成功: 完成 {summary['completed_count']}/{summary['total_tasks']} 个任务")
    
    def test_test_runner_integration(self):
        """测试运行器集成示例"""
        # 开始测试套件
        suite = self.test_runner.start_suite('集成测试套件')
        
        # 执行多个测试
        test_cases = [
            {'name': '用户登录测试', 'data': {'username': 'test', 'password': 'pass'}},
            {'name': '获取用户信息测试', 'data': {'user_id': 123}},
            {'name': '更新用户信息测试', 'data': {'user_id': 123, 'name': 'New Name'}}
        ]
        
        for test_case in test_cases:
            # 开始单个测试
            test_result = self.test_runner.start_test(test_case['name'], test_case['data'])
            
            # 模拟测试执行
            try:
                # 这里可以放实际的测试逻辑
                assert test_case['data'] is not None
                
                # 添加验证结果
                self.test_runner.add_assertion(
                    'data_not_null',
                    'not null',
                    test_case['data'],
                    test_case['data'] is not None
                )
                
                # 添加提取结果
                if 'user_id' in test_case['data']:
                    self.test_runner.add_extraction('user_id', test_case['data']['user_id'])
                
                # 结束测试
                self.test_runner.end_test('PASSED')
                
            except Exception as e:
                # 测试失败
                self.test_runner.end_test('FAILED', str(e))
        
        # 结束测试套件
        completed_suite = self.test_runner.end_suite()
        
        assert completed_suite.total_count == 3
        assert completed_suite.passed_count == 3
        assert completed_suite.failed_count == 0
        
        # 获取测试总结
        summary = self.test_runner.get_summary()
        
        print(f"✅ 测试套件执行成功:")
        print(f"   - 总测试数: {summary['total_tests']}")
        print(f"   - 通过数: {summary['total_passed']}")
        print(f"   - 成功率: {summary['success_rate']:.1f}%")
        print(f"   - 总耗时: {summary['total_duration']:.3f}s")


if __name__ == '__main__':
    # 运行示例测试
    pytest.main([__file__, '-v', '-s'])
