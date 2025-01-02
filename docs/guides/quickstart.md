# 快速入门指南

## 环境准备

1. 安装Python 3.12或更高版本
2. 安装Rust 1.76或更高版本
3. 安装uv包管理器
4. 安装cargo包管理器

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/microwave_simulation.git
cd microwave_simulation
```

2. 安装Python依赖：
```bash
uv pip install -r requirements.lock
```

3. 编译Rust组件：
```bash
cd gui_rust
cargo build --release
cd ..
```

## 启动应用

```bash
python main.py
```

## 基本使用

1. 选择电路类型
   - 阻抗匹配网络
   - 滤波器
   - 放大器

2. 输入参数
   - 频率范围
   - 阻抗值
   - 其他电路参数

3. 运行仿真
   - 点击"计算"按钮
   - 等待计算完成

4. 查看结果
   - S参数图
   - 史密斯圆图
   - 其他性能指标

## 常见问题

1. 如果遇到依赖安装问题：
   - 确保Python和Rust版本正确
   - 检查requirements.lock文件是否存在
   - 尝试清理缓存后重新安装

2. 如果GUI无法启动：
   - 检查是否正确编译了Rust组件
   - 查看日志文件中的错误信息
   - 确保所有依赖都已正确安装

## 下一步

- 阅读[理论基础](theory.md)了解更多设计原理
- 查看[示例](../examples/README.md)获取使用灵感
- 参考[API文档](../api/README.md)了解详细功能

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