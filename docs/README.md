# 项目文档

## 文档结构

```
docs/
├── api/           # API文档
├── examples/      # 使用示例
├── guides/        # 用户指南
└── internal/      # 开发文档
```

## 最新更新

- 依赖更新 (2024-03-20)
  - Python 3.12支持
  - Rust 1.76支持
  - 所有依赖包更新到最新版本
  - 修复API兼容性问题

## 快速链接

- [快速入门](guides/quickstart.md)
- [开发指南](internal/development/CONTRIBUTING.md)
- [API参考](api/README.md)
- [示例代码](examples/README.md)

## 文档维护

如需更新文档，请遵循以下步骤：

1. 确保文档内容与最新代码保持同步
2. 使用Markdown格式编写
3. 提交前进行拼写和格式检查
4. 更新相关的版本信息

## 贡献

欢迎提交文档改进建议和Pull Request。详见[贡献指南](internal/development/CONTRIBUTING.md)。

## 依赖要求

### Python环境
- Python 3.12+
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- scikit-rf >= 0.29.0
- scipy >= 1.11.0

### Rust环境（GUI部分）
- Rust 1.70+
- cargo
- eframe = "0.24.1"
- egui = "0.24.1"
- egui_plot = "0.24.1"
- pyo3 = "0.20.0"

## 安装方法

1. 克隆仓库:
```bash
git clone https://github.com/Tinnci/microwave_simulation.git
cd microwave_simulation
```

2. 创建虚拟环境并安装依赖:
```bash
uv venv
uv pip install -e .
```

3. 编译GUI程序:
```bash
cd gui_rust
cargo build --release
```

## 使用示例

```python
from impedance_matching.core import QuarterWaveTransformer, StubMatcher

# 设置参数
frequency = 2.4e9  # 2.4 GHz
z0 = 50.0  # 特征阻抗
z_load = 75.0  # 负载阻抗

# 创建四分之一波长变压器
quarter_wave = QuarterWaveTransformer(
    frequency=frequency,
    z0=z0,
    zl=z_load
)

# 计算匹配网络参数
quarter_wave_result = quarter_wave.calculate()

# 创建短截线匹配器
stub = StubMatcher(
    frequency=frequency,
    z0=z0,
    zl=z_load
)

# 计算短截线匹配网络参数
stub_result = stub.calculate()
```

## 项目结构

```
microwave_simulation/
├── docs/              # 文档
├── gui_rust/          # Rust GUI实现
├── src/               # Python源代码
│   ├── impedance_matching/  # 阻抗匹配核心实现
│   ├── optimization/        # 优化算法
│   └── visualization/       # 可视化模块
└── tests/             # 测试用例
    ├── integration/   # 集成测试
    └── unit/         # 单元测试
```

## 许可证

MIT License 