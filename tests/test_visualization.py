import pytest
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from src.visualization.plotter import plot_s_parameters, plot_smith_chart, plot_vswr

def test_plot_s_parameters():
    """测试S参数绘图函数"""
    # 准备测试数据
    frequencies = np.linspace(1e9, 3e9, 101)
    s_parameters = np.zeros((101, 2), dtype=complex)
    s_parameters[:, 0] = 0.1 + 0.1j  # S11
    s_parameters[:, 1] = 0.9 + 0.1j  # S21

    # 调用绘图函数
    fig = plot_s_parameters(frequencies, s_parameters)

    # 验证返回值类型
    assert isinstance(fig, Figure)

    # 验证图形属性
    ax = fig.axes[0]
    assert isinstance(ax, Axes)
    assert ax.get_title() == "S-Parameters"
    assert ax.get_xlabel() == "Frequency (Hz)"
    assert ax.get_ylabel() == "Magnitude (dB)"

def test_plot_smith_chart():
    """测试史密斯圆图绘制函数"""
    # 准备测试数据
    s11 = np.array([0.1 + 0.1j, 0.2 + 0.2j, 0.3 + 0.3j])

    # 调用绘图函数
    fig = plot_smith_chart(s11)

    # 验证返回值类型
    assert isinstance(fig, Figure)

    # 验证图形属性
    ax = fig.axes[0]
    assert isinstance(ax, Axes)
    assert ax.get_title() == "Smith Chart"
    assert ax.get_aspect() == "equal"

def test_plot_vswr():
    """测试驻波比绘图函数"""
    # 准备测试数据
    frequencies = np.linspace(1e9, 3e9, 101)
    s11 = np.full(101, 0.1 + 0.1j)

    # 调用绘图函数
    fig = plot_vswr(frequencies, s11)

    # 验证返回值类型
    assert isinstance(fig, Figure)

    # 验证图形属性
    ax = fig.axes[0]
    assert isinstance(ax, Axes)
    assert ax.get_title() == "VSWR"
    assert ax.get_xlabel() == "Frequency (Hz)"
    assert ax.get_ylabel() == "VSWR" 