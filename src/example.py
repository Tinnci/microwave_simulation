"""
示例脚本：演示如何使用阻抗匹配模块
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 设置后端为Agg，禁止图形窗口显示
import matplotlib.pyplot as plt
from impedance_matching.core import QuarterWaveTransformer, StubMatcher
from visualization.result_saver import ResultSaver
import skrf as rf

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题 