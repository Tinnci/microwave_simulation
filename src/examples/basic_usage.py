"""
示例脚本：演示如何使用阻抗匹配模块
"""

import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from impedance_matching.core import QuarterWaveTransformer, StubMatcher
from visualization.result_saver import ResultSaver

# 设置参数
frequency = 2.4e9  # 2.4 GHz
z0 = 50.0  # 特征阻抗
z_load = 75.0  # 负载阻抗

# 创建结果保存器
result_saver = ResultSaver(save_dir="results")

# 创建四分之一波长变压器
quarter_wave = QuarterWaveTransformer(
    frequency=frequency,
    z0=z0,
    zl=z_load
)

# 计算匹配网络参数
quarter_wave_result = quarter_wave.calculate()

# 保存四分之一波长变压器的结果
result_saver.save_network_data(quarter_wave, "results/quarter_wave")
result_saver.save_plots(quarter_wave, "results/quarter_wave")

# 创建短截线匹配器
stub = StubMatcher(
    frequency=frequency,
    z0=z0,
    zl=z_load
)

# 计算短截线匹配网络参数
stub_result = stub.calculate()

# 保存短截线匹配器的结果
result_saver.save_network_data(stub, "results/stub")
result_saver.save_plots(stub, "results/stub")

# 保存所有结果的比较
result_saver.save_all_results(quarter_wave, "results/comparison_quarter_wave")
result_saver.save_all_results(stub, "results/comparison_stub") 