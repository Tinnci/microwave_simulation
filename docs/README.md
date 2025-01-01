# 微波阻抗匹配设计工具

这是一个用于微波电路阻抗匹配设计的Python工具包。它提供了两种常用的阻抗匹配方法实现：四分之一波长变换器和单枝节匹配。

## 功能特点

- 四分之一波长变换器设计
  - 计算变换器特征阻抗
  - 计算物理长度
  - 生成S参数
  - VSWR分析

- 单枝节匹配器设计
  - 计算支节位置
  - 计算支节长度
  - 生成S参数
  - VSWR分析

- 可视化与分析
  - S参数幅度/相位图
  - 史密斯圆图
  - VSWR图
  - 性能对比分析

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
- pandas >= 2.0.0

### Rust环境
- Rust 1.70+
- cargo
- iced = "0.10"
- pyo3 = "0.19"

## 安装方法

1. 克隆仓库:
```bash
git clone https://github.com/Tinnci/microwave_simulation.git
cd microwave_simulation
```

2. 安装Python依赖:
```bash
uv venv
uv pip install -r requirements.txt
```

3. 编译GUI程序:
```bash
cd gui_rust
cargo build --release
```

## 使用示例

```python
from src.impedance_matching import QuarterWaveTransformer, StubMatcher

# 设置参数
z0 = 50  # 特征阻抗
zl = 25 + 75j  # 负载阻抗
freq = 5e9  # 中心频率

# 创建匹配器实例
quarter_wave = QuarterWaveTransformer(z0, zl, freq)
stub = StubMatcher(z0, zl, freq)

# 计算参数
z1 = quarter_wave.calculate_transformer_impedance()
d, l = stub.calculate_stub_parameters()
```

## 许可证

MIT License 