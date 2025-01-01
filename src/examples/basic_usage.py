"""
示例脚本：演示如何使用阻抗匹配模块
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 设置后端为Agg，禁止图形窗口显示
import matplotlib.pyplot as plt
from src.impedance_matching import QuarterWaveTransformer, StubMatcher
from src.visualization.result_saver import ResultSaver
from skrf import plotting

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def main():
    # 设置参数
    z0 = 50  # 特征阻抗
    zl = 25 + 75j  # 负载阻抗
    freq = 5e9  # 中心频率
    
    # 创建结果保存器
    saver = ResultSaver()
    
    # 保存初始参数
    initial_params = {
        "特征阻抗": z0,
        "负载阻抗": zl,
        "中心频率": f"{freq/1e9:.2f} GHz"  # 转换为GHz
    }
    saver.save_parameters(initial_params, "initial_parameters.json")
    
    # 创建四分之一波长变换器
    quarter_wave = QuarterWaveTransformer(z0, zl, freq)
    z1 = quarter_wave.calculate_transformer_impedance()
    quarter_wave_params = {
        "变换器特征阻抗": f"{z1:.2f} Ω",
        "四分之一波长": f"{quarter_wave.calculate_quarter_wavelength()*1000:.2f} mm",
        "VSWR": f"{quarter_wave.calculate_vswr():.2f}"
    }
    print("\n四分之一波长变换器参数:")
    for key, value in quarter_wave_params.items():
        print(f"{key}: {value}")
    
    # 创建单枝节匹配器
    stub = StubMatcher(z0, zl, freq)
    d, l = stub.calculate_stub_parameters()
    stub_params = {
        "从负载到支节的距离": f"{d*1000:.2f} mm",
        "支节长度": f"{l*1000:.2f} mm"
    }
    print("\n单枝节匹配参数:")
    for key, value in stub_params.items():
        print(f"{key}: {value}")
    
    # 获取网络参数并绘图
    freq_range = (freq * 0.8, freq * 1.2, 201)
    
    # 获取并保存四分之一波长变换器结果
    network_quarter = quarter_wave.get_network(freq_range)
    saver.save_network_data(network_quarter, "quarter_wave", freq_range)
    saver.save_plots(network_quarter, "四分之一波长变换器", "quarter_wave")
    
    # 获取并保存单枝节匹配结果
    network_stub = stub.get_network(freq_range)
    saver.save_network_data(network_stub, "stub_matching", freq_range)
    saver.save_plots(network_stub, "单枝节匹配", "stub_matching")
    
    # 比较两种匹配方案
    networks = [network_quarter, network_stub]
    titles = ["四分之一波长变换器", "单枝节匹配"]
    
    # 生成比较图
    for plot_type in ['magnitude', 'vswr', 'smith']:
        saver.plot_comparison(networks, titles, plot_type)
    
    # 保存结果摘要
    saver.save_summary(quarter_wave_params, stub_params)

if __name__ == '__main__':
    main() 