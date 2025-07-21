try:
    from . import create_funtion
    from . import validate
    from . import extract
    from . import my_builtins
    from . import render_template_obj
    from . import exceptions
except ImportError:
    import create_funtion
    import validate
    import extract
    import my_builtins
    import render_template_obj
    import exceptions
import types
from inspect import Parameter
import copy
import yaml
from pathlib import Path
import inspect
import allure
from logging_config import get_logger
log = get_logger()
from db import ConnectMysql
import mimetypes
from requests_toolbelt import MultipartEncoder
import time
import json
import pytest
import re
import sys
import platform
from websocket import create_connection
import websocket


class RunYaml(object):
    """ 运行yaml """

    def __init__(self, raw: dict, module: types.ModuleType, g: dict):
        self.raw = raw  # 读取yaml 原始数据
        self.module = module  # 动态创建的 module 模型
        self.module_variable = {}  # 模块变量
        self.context = {}
        self.hooks = {}  # 全局hooks
        self.g = g  # 全局配置

    def run(self):
        if not self.raw.get('config'):
            self.raw['config'] = {}
        # config 获取用例名称 name 和 base_url
        # config_name = self.raw.get('config').get('name', '')
        base_url = self.raw.get('config').get('base_url', None)
        config_variables = self.raw.get('config').get('variables', {})
        config_fixtures = self.raw.get('config').get('fixtures', [])
        config_params = self.raw.get('config').get('parameters', [])
        config_hooks = self.raw.get('config').get('hooks', {})
        config_exports: list = self.raw.get('config').get('export', [])
        config_allure: dict = self.raw.get('config').get('allure', {})
        if not isinstance(config_exports, list):
            config_exports = []
            log.error("export must be type of list")
        # 模块变量渲染
        self.context.update(__builtins__)  # noqa 内置函数加载
        self.context.update(my_builtins.__dict__)  # 自定义函数对象
        db_obj = self.execute_mysql()
        self.context.update(**self.g)  # 加载全局配置
        self.context.update(**db_obj)  # 加载操作mysql 内置函数
        self.module_variable = render_template_obj.rend_template_any(config_variables, **self.context)
        # 模块变量 添加到模块全局变量
        if isinstance(self.module_variable, dict):
            self.context.update(self.module_variable)
        # 支持 2 种参数化格式数据
        config_params = render_template_obj.rend_template_any(config_params, **self.context)
        config_fixtures = render_template_obj.rend_template_any(config_fixtures, **self.context)
        config_fixtures, config_params = self.parameters_date(config_fixtures, config_params)
        # ---------------------config 中 模块参数化---------------------
        if config_fixtures:
            # 向 module 中加参数化数据的属性
            setattr(self.module, 'module_params_data', config_params)
            setattr(self.module, 'module_params_fixtures', config_fixtures)
        # ---------------------config 中 模块参数化 end---------------------
        case = {}   # 收集用例名称和执行内容
        # -------------mark 标记config 下整个yaml 中全部标记--------------#
        config_mark = self.raw.get('config').get('mark')
        if isinstance(config_mark, str):
            config_mark = [item.strip(" ") for item in config_mark.split(',')]
        elif isinstance(config_mark, int):
            config_mark = [str(config_mark)]
        if config_mark:
            pytest_m = [
                pytest.Mark(
                    name=re.sub('\((.+)\)', "", mark_name),
                    args=(re.sub('.+\(', "", mark_name).rstrip(")"),),
                    kwargs={}) for mark_name in config_mark
            ]
            setattr(self.module, "pytestmark", pytest_m)
        # ---------mark end---------------#

        for case_name, case_value in self.raw.items():
            case_fixtures = []
            case_params = []
            case_mark = []  # 用例 mark 标记
            if case_name == 'config':
                continue  # 跳过config 非用例部分
            # case_name 必须 test 开头
            if not str(case_name).startswith('test'):
                case_name = 'test_' + str(case_name)
            if isinstance(case_value, list):
                case[case_name] = case_value
            else:
                case[case_name] = [case_value]
            # 用例参数获取
            if len(case[case_name]) < 1:
                log.debug('test case not item to run !')
            else:
                if 'mark' in case[case_name][0]:
                    # 用例 mark 标记
                    case_mark = case[case_name][0].get('mark', [])
                    if isinstance(case_mark, str):
                        case_mark = [item.strip(" ") for item in str(case_mark).split(',')]
                    elif isinstance(case_mark, int):
                        case_mark = [str(case_mark)]
                if 'fixtures' in case[case_name][0]:
                    case_raw_fixtures = case[case_name][0].get('fixtures', [])
                    case_fixtures = render_template_obj.rend_template_any(case_raw_fixtures, **self.context)
                if "parameters" in case[case_name][0]:
                    case_raw_parameters = case[case_name][0].get('parameters', [])
                    # 支持 2 种参数化格式数据
                    case_params = render_template_obj.rend_template_any(case_raw_parameters, **self.context)
                    # case 中的参数化 覆盖 config 的参数化
                case_fixtures, case_params = self.parameters_date(case_fixtures, case_params)
                # ----------------- case 用例参数化 parameters ------------
                if case_params:
                    # 向 module 中加参数化数据的属性
                    setattr(self.module, f'{case_name}_params_data', case_params)
                    setattr(self.module, f'{case_name}_params_fixtures', case_fixtures)
                # ------------------------case 用例参数化 parameters  end ---------------
                # -------------v1.4.0 添加  allure 报告-----------------
                if 'allure' not in case[case_name][0]:
                    case[case_name][0]['allure'] = {}
                    # ------------- allure 报告 end-----------------

            def execute_yaml_case(args):
                # 获取被调用函数名称
                log.info(f'执行文件-> {self.module.__name__}.yml')
                log.info(f'base_url-> {base_url or args.get("request").config.option.base_url}')
                log.info(f'config variables-> {self.module_variable}')
                call_function_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
                log.info(f'运行用例-> {call_function_name}')

                # 更新 fixture 的值 到context
                self.context.update(args)
                # ----------- 通过 config 获取 export 变量 ------
                request_config = args.get('request').config
                if not hasattr(request_config, 'export'):
                    request_config.export = {}
                self.context.update(request_config.export)
                case_exports = []  # 用例中需要导出的变量收集
                # 模块变量优先级高
                self.context.update(self.module_variable)
                # ----------- export end ---------
                ws = None
                for step in case[call_function_name]:
                    response = None
                    api_validate = []
                    step_context = self.context.copy()  # 步骤变量
                    step_name = step.get('name')
                    if step_name:
                        # 添加 allure 报告--> step
                        with allure.step(step_name):
                            pass
                    if 'validate' not in step.keys():
                        step['validate'] = []
                    for item, value in step.items():
                        # 执行用例里面的方法
                        if item == 'name':
                            pass  # noqa
                        elif item == 'ws':
                            value = render_template_obj.rend_template_any(value, **step_context)
                            ws_base_url = base_url or args.get("request").config.option.base_url
                            if 'ws' in ws_base_url:
                                ws_url = value.get('url')
                                if 'ws://' in ws_url or 'wss://' in ws_url:
                                    pass
                                else:
                                    value['url'] = f"{base_url.rstrip('/')}/{ws_url.lstrip('/')}"
                            ws = create_connection(**value)  # 创建链接
                            log.info(f"创建 websocket 链接: {value.get('url')}")
                        elif item == "send":
                            value = render_template_obj.rend_template_any(value, **step_context)
                            log.info(f"websocket send: {value}")
                            if not isinstance(value, str):
                                value = json.dumps(value)
                            ws.send(value)     # 发送请求
                            response = {
                                "status": ws.getstatus(),
                                "recv": ws.recv()
                            }
                            log.info(f'websocket recv: {response.get("recv")}')
                        elif item == 'mark':
                            pass
                        elif item == 'parameters':
                            pass
                        elif item == 'fixtures':
                            pass
                        elif item == 'variables':  # step 步骤变量获取
                            copy_value = copy.deepcopy(value)
                            if not isinstance(copy_value, dict):
                                log.error('step variables->variables must be dict type!')
                            else:
                                step_variables_value = render_template_obj.rend_template_any(
                                    copy_value, **self.context
                                )
                                step_context.update(step_variables_value)
                        elif item == 'api':
                            root_dir = args.get('request').config.rootdir  # 内置request 获取root_dir
                            api_path = Path(root_dir).joinpath(value)
                            raw_api = yaml.safe_load(api_path.open(encoding='utf-8'))
                            api_validate = raw_api.get('validate', [])
                            copy_value = copy.deepcopy(raw_api.get('request'))  # 深拷贝一份新的value
                            response = self.run_request(args, copy_value, config_hooks, base_url, context=step_context)
                            step_context.update(response=response)
                        elif item == 'request':
                            copy_value = copy.deepcopy(value)  # 深拷贝一份新的value
                            copy_config_hooks = copy.deepcopy(config_hooks)
                            response = self.run_request(args, copy_value, copy_config_hooks, base_url,
                                                        context=step_context)
                            step_context.update(response=response)
                        elif item == 'extract':
                            # 提取变量
                            copy_value = copy.deepcopy(value)
                            extract_value = render_template_obj.rend_template_any(copy_value, **step_context)
                            extract_result = self.extract_response(response, extract_value)
                            log.info(f'extract  提取变量-> {extract_result}')
                            # 添加到模块变量
                            self.module_variable.update(extract_result)
                            # 添加到步骤变量
                            step_context.update(extract_result)
                            if isinstance(self.module_variable, dict):
                                self.context.update(self.module_variable)  # 加载模块变量
                        elif item == 'export':
                            if isinstance(value, list):
                                for _export in value:
                                    if _export not in case_exports:
                                        case_exports.append(_export)
                                    # 支持局部 variables 变量提升为全局变量 v1.3.6 版本更新
                                    if step_context.get(_export):
                                        export_dict = {}
                                        export_dict[_export] = step_context.get(_export)
                                        self.context.update(export_dict)
                                    # -------------------v1.3.6 版本更新-----------
                            else:
                                log.error("export must be list type")
                        elif item == 'validate':
                            copy_value = copy.deepcopy(value)
                            # 合并校验
                            copy_value.extend([v for v in api_validate if v not in copy_value])
                            validate_value = render_template_obj.rend_template_any(copy_value, **step_context)
                            if validate_value:
                                log.info(f'validate 校验内容-> {validate_value}')
                                self.validate_response(response, validate_value)
                        elif item == 'sleep':
                            sleep_value = render_template_obj.rend_template_any(value, **step_context)
                            try:
                                log.info(f'sleep time: {sleep_value}')
                                time.sleep(sleep_value)
                            except Exception as msg:
                                log.error(f'Run error: sleep value must be int or float, error msg: {msg}')
                        elif item == 'skip':
                            skip_reason = render_template_obj.rend_template_any(value, **step_context)
                            pytest.skip(skip_reason)
                        elif item == 'skipif':  # noqa
                            if_exp = render_template_obj.rend_template_any(value, **step_context)
                            log.info(f'skipif : {eval(str(if_exp))}')  # noqa
                            if eval(str(if_exp)):
                                pytest.skip(str(if_exp))
                        elif item == 'allure':
                            value = render_template_obj.rend_template_any(value, **step_context)
                            # 合并config_allure
                            value.update(config_allure)
                            if not value.get('feature'):
                                # 给默认feature
                                value.update(feature=f'{self.module.__name__}.yml: {value.get("feature", "")}')
                            if not value.get('title'):
                                value.update(title=call_function_name)
                            for allure_key, allure_value in value.items():
                                try:
                                    getattr(allure.dynamic, allure_key)(allure_value)
                                except Exception as msg:
                                    log.error(f"error msg: {msg}. allure.dynamic has not attribute: {allure_key} ")
                        else:
                            value = render_template_obj.rend_template_any(value, **step_context)
                            try:
                                eval(item)(value)
                            except Exception as msg:
                                raise exceptions.ParserError(f'Parsers error: {msg}') from None
                #  ---------用例结束，更新 export 变量到全局 ------
                for export_key in config_exports:
                    request_config.export[export_key] = self.context.get(export_key)
                for export_key in case_exports:
                    request_config.export[export_key] = self.context.get(export_key)
                if request_config.export:
                    log.info(f"export 导出全局变量：{request_config.export}")
                #  ---------更新export end ------
            fun_fixtures = []
            # 合并 config 和 case 用例 fixtures
            fun_fixtures.extend(config_fixtures)
            [fun_fixtures.append(fixt) for fixt in case_fixtures if fixt not in fun_fixtures]

            f = create_funtion.create_function_from_parameters(
                func=execute_yaml_case,
                # parameters 传内置fixture 和 用例fixture
                parameters=self.function_parameters(fun_fixtures),
                documentation=case_name,
                func_name=case_name,
                func_filename=f"{self.module.__name__}.py",
            )
            if case_mark:
                f.pytestmark = [
                    pytest.Mark(
                        name=re.sub('\((.+)\)', "", mark_name),
                        args=(re.sub('.+\(', "", mark_name).rstrip(")"),),
                        kwargs={}) for mark_name in case_mark
                ]
            # ---------------为用例添加mark 标记示例 end--------
            # 向 module 中加入用例
            setattr(self.module, str(case_name), f)

    def run_request(self, args, copy_value, config_hooks, base_url, context=None):
        """运行request请求"""
        request_session = args.get('requests_function') or args.get('requests_module') or args.get('requests_session')
        # 加载参数化的值和fixture的值
        if context is None:
            request_value = render_template_obj.rend_template_any(copy_value, **self.context)
        else:
            request_value = render_template_obj.rend_template_any(copy_value, **context)
        # request 请求参数预处理
        request_pre = self.request_hooks(config_hooks, request_value)
        if request_pre:
            # 执行 pre request 预处理
            if context:
                context.update({"req": request_value})
            else:
                self.context.update({"req": request_value})
            self.run_request_hooks(request_pre, request_value, context=context)
        # request请求 带上hooks "response"参数
        self.response_hooks(config_hooks, request_value)

        # multipart/form-data 文件上传支持
        root_dir = args.get('request').config.rootdir  # 内置request 获取root_dir
        request_value = self.multipart_encoder_request(request_value, root_dir)
        log.info(f'--------  request info ----------')
        log.info(f'yml raw  -->: {request_value}')
        log.info(f'method   -->: {request_value.get("method", "")}')
        log.info(f'url      -->: {request_value.get("url", "")}')
        request_headers = {}
        request_headers.update(request_session.headers)
        if request_value.get("headers", {}):
            request_headers.update(request_value.get("headers", {}))
        log.info(f'headers  -->: {request_headers}')
        if request_value.get('json'):
            log.info(f'json     -->: {json.dumps(request_value.get("json", {}), ensure_ascii=False)}')
        else:
            log.info(f'data     -->: {request_value.get("data", {})}')
        response = request_session.send_request(
            base_url=base_url,
            **request_value
        )
        log.info(f'------  response info  {getattr(response, "status_code")} {getattr(response, "reason", "")} ------ ')
        log.info(f'耗时     <--: {getattr(response, "elapsed", "").total_seconds() if getattr(response, "elapsed", "") else ""}s')
        log.info(f'url      <--: {getattr(response, "url", "")}')
        log.info(f'headers  <--: {getattr(response, "headers", "")}')
        log.info(f'cookies  <--: {dict(getattr(response, "cookies", {}))}')
        log.info(f'raw text <--: {getattr(response, "text", "")}')
        return response

    @staticmethod
    def function_parameters(config_fixtures) -> list:
        """ 测试函数传 fixture """
        # 测试函数的默认请求参数
        function_parameters = [
            Parameter('request', Parameter.POSITIONAL_OR_KEYWORD)  # 内置request fixture
        ]
        # 获取传给用例的 fixtures
        if isinstance(config_fixtures, str):
            config_fixtures = [item.strip(" ") for item in config_fixtures.split(',')]
        if not config_fixtures:
            function_parameters.append(
                Parameter('requests_session', Parameter.POSITIONAL_OR_KEYWORD),
            )
        else:
            if 'requests_function' in config_fixtures:
                function_parameters.append(
                    Parameter('requests_function', Parameter.POSITIONAL_OR_KEYWORD),
                )
            elif 'requests_module' in config_fixtures:
                function_parameters.append(
                    Parameter('requests_module', Parameter.POSITIONAL_OR_KEYWORD),
                )
            else:
                function_parameters.append(
                    Parameter('requests_session', Parameter.POSITIONAL_OR_KEYWORD),
                )
            for fixture in config_fixtures:
                if fixture not in ['requests_function', 'requests_module']:
                    function_parameters.append(
                        Parameter(fixture, Parameter.POSITIONAL_OR_KEYWORD),
                    )
        return function_parameters

    @staticmethod
    def parameters_date(fixtures, parameters):
        """
            参数化实现2种方式：
        方式1：
            config:
               name: post示例
               fixtures: username, password
               parameters:
                 - [test1, '123456']
                 - [test2, '123456']
        方式2：
            config:
               name: post示例
               parameters:
                 - {"username": "test1", "password": "123456"}
                 - {"username": "test2", "password": "1234562"}
        :returns
        fixtures: 用例需要用到的fixtures:  ['username', 'password']
        parameters: 参数化的数据list of list : [['test1', '123456'], ['test2', '123456']]
        """
        if isinstance(fixtures, str):
            # 字符串切成list
            fixtures = [item.strip(" ") for item in fixtures.split(',')]
        if isinstance(parameters, list) and len(parameters) >= 1:
            if isinstance(parameters[0], dict):
                # list of dict
                params = list(parameters[0].keys())
                new_parameters = []
                for item in parameters:
                    new_parameters.append(list(item.values()))
                # fixtures 追加参数化的参数
                for param in params:
                    if param not in fixtures:
                        fixtures.append(param)
                return fixtures, new_parameters
            else:
                # list of list
                return fixtures, parameters
        elif isinstance(parameters, dict):
            # -----v1.3.8 兼容name: ["user1", "user2"] 格式参数化---
            parameters_args = parameters.keys()
            for args in parameters_args:
                if ',' in args:
                    args = str(args).split(',')
                elif '-' in args:
                    args = str(args).split('-')
                else:
                    args = [args]
                fixtures.extend(args)
            return fixtures, parameters
            # --------- end -----------------
        else:
            return fixtures, []

    def hooks_event(self, hooks):
        """
        获取 requests 请求执行钩子, 仅支持2个事件，request 和 response
        :param hooks: yml 文件中读取的原始数据
           hooks = {
                "response": ['fun1', 'fun2'],
                "request": ['fun3', 'fun4']
            }
        :return: 返回结果示例:
            hooks = {
                "response": [fun1, fun2],
                "request": [fun3, fun4]
            }
        """
        # response hook事件
        hooks_response = hooks.get('response', [])
        if isinstance(hooks_response, str):
            # 字符串切成list
            hooks_response = [item.strip(" ") for item in hooks_response.split(',')]
        # 获取 my_builtins 模块函数对象
        hooks_response = [self.context.get(func) for func in hooks_response if self.context.get(func)]
        hooks['response'] = hooks_response
        # request  hook事件
        hooks_request = hooks.get('request', [])
        if isinstance(hooks_request, str):
            # 字符串切成list
            hooks_request = [item.strip(" ") for item in hooks_request.split(',')]
        # 获取 my_builtins 模块函数对象
        hooks_request = [self.context.get(func) for func in hooks_request if self.context.get(func)]
        hooks['request'] = hooks_request
        return hooks

    def request_hooks(self, config_hooks: dict, request_value: dict) -> dict:
        """ 合并全局config_hooks 和 单个请求 hooks 参数
            config_hooks = {
                "response": ['fun1', 'fun2'],
                "request": ['fun3', 'fun4']
            }
            request_value = {
                "method": "GET",
                "hooks": {"response": ['fun5']}
            }
            发送请求，request上带上hooks参数
            :return {"request": ['fun3', 'fun4']} 合并后的request 预处理函数
        """
        # request hooks 事件 (requests 库只有response 事件)
        config_request_hooks = []
        if 'request' in config_hooks.keys():
            config_request_hooks = config_hooks.get('request')
            if isinstance(config_request_hooks, str):
                # 字符串切成list
                config_request_hooks = [item.strip(" ") for item in config_request_hooks.split(',')]
        req_request_hooks = request_value.get('hooks', {})
        if 'request' in req_request_hooks.keys():
            req_hooks = req_request_hooks.pop('request')
            if isinstance(req_hooks, str):
                # 字符串切成list
                req_hooks = [item.strip(" ") for item in req_hooks.split(',')]
            for h in req_hooks:
                config_request_hooks.append(h)
        # 更新 request_value
        if config_request_hooks:
            hooks = self.hooks_event({'request': config_request_hooks})
            # 去掉值为空的response 事件
            new_hooks = {key: value for key, value in hooks.items() if value}
            return new_hooks
        return {'request': []}

    def run_request_hooks(self, request_pre: dict, request_value, context=None):
        """执行请求预处理hooks内容
        request_pre: 待执行的预处理函数
        """
        funcs = request_pre.get('request', [])
        if not funcs:
            return request_value
        import inspect
        for fun in funcs:
            # 获取函数对象的入参
            ars = [arg_name for arg_name, v in inspect.signature(fun).parameters.items()]
            if 'req' in ars:
                if context:
                    fun(*[context.get(arg) for arg in ars])
                else:
                    fun(*[self.context.get(arg) for arg in ars])
            else:
                fun()
        return request_value

    def response_hooks(self, config_hooks: dict, request_value: dict) -> dict:
        """
            合并全局config_hooks 和 单个请求 hooks 参数
        config_hooks = {
            "response": ['fun1', 'fun2'],
            "request": ['fun3', 'fun4']
        }
        request_value = {
            "method": "GET",
            "hooks": {"response": ['fun5']}
        }
        发送请求，request上带上hooks参数
        :return request_value  合并后的request请求
        """
        # request hooks 事件 (requests 库只有response 事件)
        if 'response' in config_hooks.keys():
            config_response_hooks = config_hooks.get('response')
            if isinstance(config_response_hooks, str):
                # 字符串切成list
                config_response_hooks = [item.strip(" ") for item in config_response_hooks.split(',')]
        else:
            config_response_hooks = []
        req_response_hooks = request_value.get('hooks', {})
        if 'response' in req_response_hooks.keys():
            resp_hooks = req_response_hooks.get('response')
            if isinstance(resp_hooks, str):
                # 字符串切成list
                resp_hooks = [item.strip(" ") for item in resp_hooks.split(',')]
            for h in resp_hooks:
                config_response_hooks.append(h)
        # 更新 request_value
        if config_response_hooks:
            hooks = self.hooks_event({'response': config_response_hooks})
            # 去掉值为空的response 事件
            new_hooks = {key: value for key, value in hooks.items() if value}
            request_value['hooks'] = new_hooks
        return request_value

    @staticmethod
    def extract_response(response, extract_obj: dict):
        """extract 提取返回结果"""
        extract_result = {}
        if isinstance(extract_obj, dict):
            for extract_var, extract_expression in extract_obj.items():
                extract_var_value = extract.extract_by_object(response, extract_expression)  # 实际结果
                extract_result[extract_var] = extract_var_value
            return extract_result
        else:
            return extract_result

    @staticmethod
    def validate_response(response, validate_check: list) -> None:
        """校验结果"""
        for check in validate_check:
            for check_type, check_value in check.items():
                actual_value = extract.extract_by_object(response, check_value[0])  # 实际结果
                expect_value = check_value[1]  # 期望结果
                log.info(f'validate 校验结果-> {check_type}: [{actual_value}, {expect_value}]')
                if check_type in ["eq", "equals", "equal"]:
                    validate.equals(actual_value, expect_value)
                elif check_type in ["lt", "less_than"]:
                    validate.less_than(actual_value, expect_value)
                elif check_type in ["le", "less_or_equals"]:
                    validate.less_than_or_equals(actual_value, expect_value)
                elif check_type in ["gt", "greater_than"]:
                    validate.greater_than(actual_value, expect_value)
                elif check_type in ["ne", "not_equal", "not_equal"]:
                    validate.not_equals(actual_value, expect_value)
                elif check_type in ["str_eq", "str_equals", "string_equals", "string_equal"]:
                    validate.string_equals(actual_value, expect_value)
                elif check_type in ["len_eq", "length_equal", "length_equals"]:
                    validate.length_equals(actual_value, expect_value)
                elif check_type in ["len_gt", "length_greater_than"]:
                    validate.length_greater_than(actual_value, expect_value)
                elif check_type in ["len_ge", "length_greater_or_equals"]:
                    validate.length_greater_than_or_equals(actual_value, expect_value)
                elif check_type in ["len_lt", "length_less_than"]:
                    validate.length_less_than(actual_value, expect_value)
                elif check_type in ["len_le", "length_less_or_equals"]:
                    validate.length_less_than_or_equals(actual_value, expect_value)
                elif check_type in ["contains", "contain"]:
                    validate.contains(actual_value, expect_value)
                elif check_type in ["bool_eq", "bool_equal", "bool_equals"]:
                    validate.bool_equals(actual_value, expect_value)
                else:
                    if hasattr(validate, check_type):
                        getattr(validate, check_type)(actual_value, expect_value)
                    else:
                        log.error(f'{check_type}  not valid check type')

    def execute_mysql(self):
        """执行 mysql 操作"""
        env_obj = self.g.get('env')  # 获取环境配置
        if not hasattr(env_obj, 'MYSQL_HOST') and not hasattr(env_obj, 'DB_INFO'):
            return {
                "query_sql": lambda x: log.error("MYSQL_HOST or DB_INFO  not found in config.py"),
                "execute_sql": lambda x: log.error("MYSQL_HOST or DB_INFO not found in config.py")
            }
        try:
            if hasattr(env_obj, 'DB_INFO'):
                db = ConnectMysql(**env_obj.DB_INFO)
            else:
                db = ConnectMysql(
                    host=env_obj.MYSQL_HOST,
                    user=env_obj.MYSQL_USER,
                    password=env_obj.MYSQL_PASSWORD,
                    port=env_obj.MYSQL_PORT,
                    database=env_obj.MYSQL_DATABASE,
                )
            return {
                "query_sql": db.query_sql,
                "execute_sql": db.execute_sql
            }
        except Exception as msg:
            log.error(f'mysql init error: {msg}')
            return {
                "query_sql": lambda x: log.error("MYSQL connect error in config.py"),
                "execute_sql": lambda x: log.error("MYSQL connect error in config.py")
            }

    @staticmethod
    def upload_file(filepath: Path):
        """根据文件路径，自动获取文件名称和文件mime类型"""
        if not filepath.exists():
            log.error(f"文件路径不存在：{filepath}")
            return
        mime_type = mimetypes.guess_type(filepath)[0]
        return (
            filepath.name, filepath.open("rb"), mime_type
        )

    def multipart_encoder_request(self, request_value: dict, root_dir):
        """判断请求头部 Content-Type: multipart/form-data 格式支持"""
        if 'files' in request_value.keys():
            fields = []
            data = request_value.get('data', {})
            fields.extend(data.items())  # 添加data数据
            for key, value in request_value.get('files', {}).items():
                if Path(root_dir).joinpath(value).is_file():
                    fields.append(
                        (key, self.upload_file(Path(root_dir).joinpath(value).resolve()))
                    )
                else:
                    fields.append((key, value))
            m = MultipartEncoder(
                fields=fields
            )
            request_value.pop('files')  # 去掉 files 参数
            request_value['data'] = m
            new_headers = request_value.get('headers', {})
            new_headers.update({'Content-Type': m.content_type})
            request_value['headers'] = new_headers
            return request_value
        else:
            return request_value

    def finalize_test_run(self):
        """完成测试运行后的处理"""
        try:
            # 尝试导入并使用Allure报告器
            from allure_reporter import AllureReporter, AllureConfig

            # 创建Allure配置，设置自动打开报告
            config = AllureConfig(
                results_dir="allure-results",
                report_dir="allure-report",
                clean_results=True,
                generate_report=True,
                open_report=True
            )

            # 创建报告器并生成报告
            reporter = AllureReporter(config)

            # 生成环境信息
            env_info = {
                "测试框架": "API-Test-KB-Pro",
                "执行时间": time.strftime('%Y-%m-%d %H:%M:%S'),
                "Python版本": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "操作系统": f"{platform.system()} {platform.release()}"
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
            reporter.generate_and_open_report()

            log.info("✅ 测试完成，Allure报告已生成并打开")

        except ImportError:
            log.warning("⚠️  未安装allure-pytest，跳过报告生成")
        except Exception as e:
            log.error(f"❌ 生成Allure报告失败: {e}")

        # 打印测试总结
        self.print_test_summary()

    def print_test_summary(self):
        """打印测试总结"""
        print("\n" + "="*60)
        print("🎯 测试执行完成")
        print("="*60)
        print(f"📊 执行时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 结果目录: allure-results/")
        print(f"📋 报告目录: allure-report/")
        print("🚀 如需重新查看报告，请运行: allure serve allure-results")
        print("="*60)
