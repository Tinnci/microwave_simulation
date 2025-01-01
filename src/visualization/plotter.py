import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from typing import Optional, Dict, Any, Tuple, cast

def plot_s_parameters(frequencies: np.ndarray,
                     s_parameters: np.ndarray,
                     title: str = "S-Parameters",
                     xlabel: str = "Frequency (Hz)",
                     ylabel: str = "Magnitude (dB)",
                     grid: bool = True) -> Figure:
    """
    绘制S参数
    
    Args:
        frequencies: 频率点数组
        s_parameters: S参数矩阵
        title: 图标题
        xlabel: x轴标签
        ylabel: y轴标签
        grid: 是否显示网格
        
    Returns:
        matplotlib.figure.Figure: 图形对象
    """
    fig = plt.figure(figsize=(10, 6))
    ax = cast(Axes, fig.add_subplot(111))
    
    # 计算dB值
    s11_db = 20 * np.log10(np.abs(s_parameters[:, 0]))
    s21_db = 20 * np.log10(np.abs(s_parameters[:, 1]))
    
    # 绘制S参数
    ax.plot(frequencies, s11_db, label='S11')
    ax.plot(frequencies, s21_db, label='S21')
    
    # 设置图形属性
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(grid)
    ax.legend()
    
    return fig

def plot_smith_chart(s11: np.ndarray,
                    title: str = "Smith Chart",
                    grid: bool = True) -> Figure:
    """
    绘制史密斯圆图
    
    Args:
        s11: 反射系数
        title: 图标题
        grid: 是否显示网格
        
    Returns:
        matplotlib.figure.Figure: 图形对象
    """
    fig = plt.figure(figsize=(8, 8))
    ax = cast(Axes, fig.add_subplot(111))
    
    # 绘制单位圆
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.5)
    
    # 绘制反射系数轨迹
    ax.plot(np.real(s11), np.imag(s11), 'b-')
    
    # 设置图形属性
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(grid)
    ax.set_xlim((-1.2, 1.2))
    ax.set_ylim((-1.2, 1.2))
    
    return fig

def plot_vswr(frequencies: np.ndarray,
              s11: np.ndarray,
              title: str = "VSWR",
              xlabel: str = "Frequency (Hz)",
              ylabel: str = "VSWR",
              grid: bool = True) -> Figure:
    """
    绘制驻波比
    
    Args:
        frequencies: 频率点数组
        s11: 反射系数
        title: 图标题
        xlabel: x轴标签
        ylabel: y轴标签
        grid: 是否显示网格
        
    Returns:
        matplotlib.figure.Figure: 图形对象
    """
    fig = plt.figure(figsize=(10, 6))
    ax = cast(Axes, fig.add_subplot(111))
    
    # 计算VSWR
    reflection_coefficient = np.abs(s11)
    vswr = (1 + reflection_coefficient) / (1 - reflection_coefficient)
    
    # 绘制VSWR
    ax.plot(frequencies, vswr)
    
    # 设置图形属性
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(grid)
    
    return fig 