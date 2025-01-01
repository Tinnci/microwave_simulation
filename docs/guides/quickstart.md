# 快速入门指南

## 简介

微波阻抗匹配设计工具是一个用于设计和优化微波阻抗匹配网络的软件。本指南将帮助您快速上手使用该工具。

## 安装

### 系统要求
- Python 3.12 或更高版本
- Rust 1.70 或更高版本
- Windows 10/11
- 2GB 以上内存
- 500MB 可用磁盘空间

### 安装步骤

1. 安装Rust工具链(如果未安装):
```bash
# Windows PowerShell
winget install Rustlang.Rust.MSVC
```

2. 克隆仓库：
```bash
git clone https://github.com/Tinnci/microwave_simulation.git
cd microwave_simulation
```

3. 创建虚拟环境并安装依赖：
```bash
uv venv
uv pip install -e .
```

4. 编译GUI程序：
```bash
cd gui_rust
cargo build --release
```

## 基本使用

### 命令行使用

```python
from impedance_matching.core import QuarterWaveTransformer, StubMatcher
from visualization.plotter import plot_s_parameters, plot_smith_chart, plot_vswr
from optimization.calculator import BatchCalculator, CalculationParameters

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
result = quarter_wave.calculate()

# 查看结果
print(f"波长: {result['wavelength']} m")
print(f"VSWR: {result['vswr']}")
print(f"S参数: {result['s_parameters']}")
```

### GUI界面使用

1. 启动程序：
```bash
# 在项目根目录下
./gui_rust/target/release/microwave_gui
```

2. 界面功能区
   - 参数输入区：设置频率、阻抗等参数
   - 匹配方法选择：选择不同的匹配网络类型
   - 结果显示区：查看计算结果和图表
   - 工具栏：保存、导出等操作

3. 参数设置
   - 频率（Hz）：输入工作频率
   - 特征阻抗（Ω）：输入传输线特征阻抗
   - 负载阻抗（Ω）：输入负载阻抗

4. 匹配方法
   - 四分之一波长变换器：适用于纯阻性负载
   - 单枝节匹配器：适用于复阻抗负载
   - L型网络：适用于宽带匹配
   - Pi型网络：适用于双向匹配
   - T型网络：适用于多频段匹配

## 高级功能

### 优化计算

```python
# 创建计算参数
params = CalculationParameters(
    freq=2.4e9,
    z0=50.0,
    z_load_real=75.0,
    z_load_imag=0.0,
    matching_method="quarter_wave",
    optimization_target="vswr"
)

# 创建批量计算器
calculator = BatchCalculator(params)

# 设置参数范围
param_ranges = {
    "freq": (2e9, 3e9),
    "z0": (45, 55)
}

# 执行优化
result = calculator.optimize(param_ranges, num_points=10)
```

### 结果可视化

```python
from visualization.plotter import plot_s_parameters, plot_smith_chart, plot_vswr

# 绘制S参数
fig_s = plot_s_parameters(frequencies, s_parameters)
fig_s.savefig("s_parameters.png")

# 绘制史密斯圆图
fig_smith = plot_smith_chart(s11)
fig_smith.savefig("smith_chart.png")

# 绘制VSWR图
fig_vswr = plot_vswr(frequencies, s11)
fig_vswr.savefig("vswr.png")
```

### 结果保存

```python
from visualization.result_saver import ResultSaver

# 创建结果保存器
saver = ResultSaver(save_dir="results")

# 保存网络数据
saver.save_network_data(network, "network_data")

# 保存图表
saver.save_plots(network, "network_plots")

# 保存优化结果
saver.save_optimization_results(results, "optimization_results")
```

## 常见问题

### 输入验证
- 频率必须为正数
- 特征阻抗必须为正数
- 负载阻抗实部必须为正数

### 计算错误
- 检查输入参数的物理合理性
- 确认选择的匹配方法是否适用
- 验证优化参数设置是否合理

### 程序问题
- 检查Python和Rust环境配置
- 确认所有依赖已正确安装
- 验证GUI程序编译是否成功

## 获取帮助

### 文档资源
- [设计理论](theory.md)
- [API参考](../api/README.md)
- [结果分析](analysis.md)

### 技术支持
- GitHub Issues
- 开发文档
- 示例代码

## 下一步学习

### 进阶主题
- 多级匹配网络设计
- 优化算法原理
- 自定义匹配方法

### 实用技巧
- 参数优化方法
- 结果分析方法
- 批量处理技巧 