# 使用示例

## 基本示例

### 四分之一波长变换器设计

```python
from src.impedance_matching import QuarterWaveTransformer
from src.visualization import ResultSaver

# 创建变换器实例
transformer = QuarterWaveTransformer(
    frequency=5e9,  # 5 GHz
    z0=50,         # 特征阻抗
    zl=100         # 负载阻抗
)

# 计算参数
results = transformer.calculate()

# 保存结果
saver = ResultSaver()
saver.save_network_data(transformer, "quarter_wave")
saver.save_plots(transformer, "quarter_wave")

print(f"变换器特征阻抗: {results['z1']:.2f} Ω")
print(f"变换器长度: {results['length']*1000:.2f} mm")
print(f"VSWR: {results['vswr']:.2f}")
```

### 单枝节匹配器设计

```python
from src.impedance_matching import StubMatcher
from src.visualization import ResultSaver

# 创建匹配器实例
matcher = StubMatcher(
    frequency=5e9,           # 5 GHz
    z0=50,                   # 特征阻抗
    zl=100 + 50j            # 复数负载阻抗
)

# 计算参数
results = matcher.calculate()

# 保存结果
saver = ResultSaver()
saver.save_network_data(matcher, "stub_matching")
saver.save_plots(matcher, "stub_matching")

print(f"支节到负载距离: {results['distance']*1000:.2f} mm")
print(f"支节长度: {results['stub_length']*1000:.2f} mm")
```

### L型匹配网络设计

```python
from src.impedance_matching import LMatcher
from src.visualization import ResultSaver

# 创建匹配网络实例
matcher = LMatcher(
    frequency=5e9,           # 5 GHz
    z0=50,                   # 特征阻抗
    zl=100 + 50j            # 复数负载阻抗
)

# 计算参数
results = matcher.calculate()

# 保存结果
saver = ResultSaver()
saver.save_network_data(matcher, "l_matching")
saver.save_plots(matcher, "l_matching")

print(f"串联元件值: {results['series_element']:.2f}")
print(f"并联元件值: {results['parallel_element']:.2f}")
print(f"品质因数: {results['q_factor']:.2f}")
```

### π型匹配网络设计

```python
from src.impedance_matching import PiMatcher
from src.visualization import ResultSaver

# 创建匹配网络实例
matcher = PiMatcher(
    frequency=5e9,           # 5 GHz
    z0=50,                   # 特征阻抗
    zl=100 + 50j,           # 复数负载阻抗
    q_factor=2.0            # 期望品质因数
)

# 计算参数
results = matcher.calculate()

# 保存结果
saver = ResultSaver()
saver.save_network_data(matcher, "pi_matching")
saver.save_plots(matcher, "pi_matching")

print(f"输入并联元件值: {results['input_parallel']:.2f}")
print(f"串联元件值: {results['series']:.2f}")
print(f"输出并联元件值: {results['output_parallel']:.2f}")
print(f"实际品质因数: {results['q_factor']:.2f}")
```

### T型匹配网络设计

```python
from src.impedance_matching import TMatcher
from src.visualization import ResultSaver

# 创建匹配网络实例
matcher = TMatcher(
    frequency=5e9,           # 5 GHz
    z0=50,                   # 特征阻抗
    zl=100 + 50j,           # 复数负载阻抗
    q_factor=2.0            # 期望品质因数
)

# 计算参数
results = matcher.calculate()

# 保存结果
saver = ResultSaver()
saver.save_network_data(matcher, "t_matching")
saver.save_plots(matcher, "t_matching")

print(f"输入串联元件值: {results['input_series']:.2f}")
print(f"并联元件值: {results['parallel']:.2f}")
print(f"输出串联元件值: {results['output_series']:.2f}")
print(f"实际品质因数: {results['q_factor']:.2f}")
```

## 高级示例

### 参数扫描

```python
from src.impedance_matching import QuarterWaveTransformer
from src.optimization import BatchCalculator
from src.visualization import ResultSaver

# 创建变换器实例
transformer = QuarterWaveTransformer(
    frequency=5e9,
    z0=50,
    zl=100
)

# 创建批量计算器
calculator = BatchCalculator(transformer)

# 执行频率扫描
results = calculator.parameter_sweep(
    parameter="frequency",
    start=4e9,
    stop=6e9,
    steps=101
)

# 保存结果
saver = ResultSaver()
saver.save_optimization_results(results, "frequency_sweep")
```

### 优化计算

```python
from src.impedance_matching import StubMatcher
from src.optimization import BatchCalculator
from src.visualization import ResultSaver

# 创建匹配器实例
matcher = StubMatcher(
    frequency=5e9,
    z0=50,
    zl=100 + 50j
)

# 创建批量计算器
calculator = BatchCalculator(matcher)

# 定义目标函数
def target_function(params):
    return abs(matcher.calculate_s11(params))

# 设置参数边界
bounds = [
    (0.001, 0.01),  # 支节距离范围
    (0.001, 0.01)   # 支节长度范围
]

# 执行优化
results = calculator.optimize(
    target_function=target_function,
    bounds=bounds
)

# 保存结果
saver = ResultSaver()
saver.save_optimization_results(results, "optimization")

print(f"优化后支节到负载距离: {results['x'][0]*1000:.2f} mm")
print(f"优化后支节长度: {results['x'][1]*1000:.2f} mm")
print(f"最小反射系数: {results['fun']:.4f}")
```

### 批量处理

```python
from src.impedance_matching import QuarterWaveTransformer
from src.optimization import BatchCalculator
from src.visualization import ResultSaver
import numpy as np

# 创建变换器实例
transformer = QuarterWaveTransformer(
    frequency=5e9,
    z0=50,
    zl=100
)

# 创建批量计算器
calculator = BatchCalculator(transformer)

# 定义负载阻抗范围
zl_values = np.linspace(50, 150, 11)

# 批量计算
results = []
for zl in zl_values:
    transformer.zl = zl
    result = transformer.calculate()
    results.append(result)

# 保存结果
saver = ResultSaver()
saver.save_optimization_results(
    {"zl_values": zl_values, "results": results},
    "batch_processing"
)
```

### 自定义图形

```python
from src.impedance_matching import QuarterWaveTransformer
from src.visualization import ResultSaver
import matplotlib.pyplot as plt

# 创建变换器实例
transformer = QuarterWaveTransformer(
    frequency=5e9,
    z0=50,
    zl=100
)

# 计算参数
results = transformer.calculate()

# 创建自定义图形
plt.figure(figsize=(10, 6))
plt.plot(results['frequencies'], abs(results['s11']), 'b-', label='|S11|')
plt.plot(results['frequencies'], abs(results['s21']), 'r-', label='|S21|')
plt.grid(True)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('S-Parameters vs Frequency')
plt.legend()

# 保存图形
plt.savefig('custom_plot.png', dpi=300, bbox_inches='tight')
plt.close()
```

## 实用技巧

### 错误处理

```python
from src.impedance_matching import QuarterWaveTransformer
from src.exceptions import ParameterError, CalculationError

try:
    # 尝试创建变换器实例
    transformer = QuarterWaveTransformer(
        frequency=-5e9,  # 无效频率
        z0=50,
        zl=100
    )
except ParameterError as e:
    print(f"参数错误: {e}")

try:
    # 尝试计算参数
    transformer = QuarterWaveTransformer(
        frequency=5e9,
        z0=50,
        zl=100
    )
    results = transformer.calculate()
except CalculationError as e:
    print(f"计算错误: {e}")
```

### 结果分析

```python
from src.impedance_matching import QuarterWaveTransformer
from src.utils.network import calculate_vswr, calculate_impedance

# 创建变换器实例
transformer = QuarterWaveTransformer(
    frequency=5e9,
    z0=50,
    zl=100
)

# 计算参数
results = transformer.calculate()

# 分析结果
vswr = calculate_vswr(results['s11'])
z_in = calculate_impedance(results['s_parameters'], z0=50)

print(f"输入VSWR: {vswr:.2f}")
print(f"输入阻抗: {z_in[0]:.2f} + {z_in[1]:.2f}j Ω")
```

### 数据导出

```python
from src.impedance_matching import QuarterWaveTransformer
from src.utils.data import save_to_csv, load_from_csv

# 创建变换器实例并计算
transformer = QuarterWaveTransformer(
    frequency=5e9,
    z0=50,
    zl=100
)
results = transformer.calculate()

# 保存数据到CSV
save_to_csv(results, "transformer_results.csv")

# 加载数据
loaded_results = load_from_csv("transformer_results.csv")
``` 