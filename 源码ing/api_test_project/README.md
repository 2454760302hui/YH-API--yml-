# API测试项目

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
