# 项目结构说明

## 目录结构

```
microwave_simulation/
├── docs/                    # 文档目录
│   ├── api/                # API文档
│   │   └── README.md      # API文档索引
│   ├── examples/           # 示例文档
│   │   └── README.md      # 示例文档索引
│   ├── guides/            # 用户指南
│   │   ├── analysis.md   # 分析方法指南
│   │   ├── quickstart.md # 快速入门指南
│   │   └── theory.md     # 理论基础
│   └── internal/          # 内部文档
│       ├── development/   # 开发文档
│       │   └── CONTRIBUTING.md # 贡献指南
│       ├── progress/      # 进度追踪
│       └── PROJECT_STRUCTURE.md # 本文档
├── src/                    # 源代码目录
│   ├── impedance_matching/ # 阻抗匹配核心代码
│   │   ├── __init__.py
│   │   ├── quarter_wave.py # 四分之一波长变换器
│   │   └── stub_matching.py # 短截线匹配
│   ├── optimization/      # 优化计算模块
│   │   ├── __init__.py
│   │   └── calculator.py  # 优化计算器
│   ├── help/             # 帮助系统模块
│   │   ├── __init__.py
│   │   └── help_system.py # 帮助系统实现
│   ├── visualization/     # 可视化模块
│   │   ├── __init__.py
│   │   └── result_saver.py # 结果保存
│   └── gui/              # GUI模块
│       ├── __init__.py
│       └── main.py       # GUI主程序
├── gui_rust/              # Rust GUI实现
│   ├── src/              # Rust源代码
│   │   ├── lib.rs       # GUI实现
│   │   └── theme.rs     # 主题配置
│   └── Cargo.toml       # Rust项目配置
├── tests/                 # 测试目录
│   ├── test_gui.py      # GUI测试
│   ├── test_help_system.py # 帮助系统测试
│   ├── test_impedance_matching.py # 阻抗匹配测试
│   ├── test_optimization.py # 优化模块测试
│   └── test_visualization.py # 可视化测试
├── .gitignore            # Git忽略配置
├── CHANGELOG.md          # 更新日志
├── LICENSE              # 许可证文件
├── README.md            # 项目说明
├── pytest.ini           # Pytest配置
├── requirements.txt     # Python依赖
└── setup.py            # 安装配置
```

## 核心模块说明

### 1. GUI模块
- Python后端 (src/gui/)
  - 业务逻辑处理
  - 阻抗匹配计算
  - 结果保存管理

- Rust前端 (gui_rust/)
  - 使用iced库实现GUI
  - 通过PyO3与Python交互
  - 提供用户界面

### 2. 阻抗匹配模块 (src/impedance_matching/)
- 实现阻抗匹配算法
  - 四分之一波长变换器
  - 短截线匹配
- 提供S参数计算
- 支持VSWR分析

### 3. 优化模块 (src/optimization/)
- 参数优化计算
- 性能指标评估
- 多目标优化支持

### 4. 帮助系统 (src/help/)
- 上下文相关帮助
- 工具提示支持
- 理论指导

### 5. 可视化模块 (src/visualization/)
- 结果数据保存
- 图表生成
- 数据导出

## 依赖说明

### 1. Python依赖
- numpy：数值计算
- matplotlib：绘图功能
- scikit-rf：射频计算

### 2. Rust依赖
- iced：GUI框架
- pyo3：Python绑定

### 3. 开发依赖
- pytest：测试框架
- cargo：Rust构建工具
- uv：Python包管理器

## 文档组织

### 1. API文档 (docs/api/)
- 模块API说明
- 函数接口文档
- 类型定义

### 2. 示例文档 (docs/examples/)
- 使用示例
- 最佳实践
- 常见问题解答

### 3. 用户指南 (docs/guides/)
- 快速入门
- 理论基础
- 分析方法

### 4. 内部文档 (docs/internal/)
- 开发指南
- 进度追踪
- 项目结构 