# 微波阻抗匹配设计工具

这是一个用于微波电路阻抗匹配设计的Python工具包。它提供了多种阻抗匹配方法的实现，包括四分之一波长变换器、单枝节匹配、L型网络、Pi型网络和T型网络。

## 功能特点

- 多种匹配网络设计
  - 四分之一波长变换器
  - 单枝节匹配器
  - L型网络
  - Pi型网络
  - T型网络

- 网络分析功能
  - S参数计算
  - VSWR分析
  - 输入阻抗计算
  - 反射系数分析

- 优化功能
  - 参数扫描
  - 多目标优化
  - 性能评估

- 可视化与分析
  - S参数幅度/相位图
  - 史密斯圆图
  - VSWR图
  - 性能对比分析

- 结果保存与导出
  - 网络参数保存
  - 图表导出
  - 优化结果记录
  - 参数扫描数据保存

## 文档导航

- [快速开始](guides/quickstart.md)
- [设计理论](guides/theory.md)
- [API参考](api/README.md)
- [使用示例](examples/README.md)
- [结果分析](guides/analysis.md)

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