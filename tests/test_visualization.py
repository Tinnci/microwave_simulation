"""可视化模块测试"""
import os
import pytest
import numpy as np
from unittest.mock import patch
from src.visualization.result_saver import ResultSaver

class MockNetwork:
    """模拟网络类"""
    def __init__(self):
        """初始化模拟网络"""
        self.s_parameters = np.array([
            complex(0.1, 0.2),  # S11
            complex(0.3, 0.4),  # S12
            complex(0.3, 0.4),  # S21
            complex(0.5, 0.6)   # S22
        ])
        self.vswr = 1.5
        self.reflection_coefficient = complex(0.2, 0.3)
        self.input_impedance = complex(50.0, 10.0)
        self.frequency = 1e9

class TestResultSaver:
    """测试结果保存器类"""
    
    @pytest.fixture
    def result_saver(self, tmp_path):
        """创建结果保存器实例"""
        save_dir = tmp_path / "test_results"
        return ResultSaver(str(save_dir))
        
    @pytest.fixture
    def mock_network(self):
        """创建模拟网络实例"""
        return MockNetwork()
        
    def test_init(self, result_saver, tmp_path):
        """测试初始化"""
        # 测试保存目录创建
        save_dir = tmp_path / "test_results"
        assert os.path.exists(save_dir)
        
        # 测试字体设置
        import matplotlib.pyplot as plt
        assert plt.rcParams['font.family'] == ['sans-serif']
        assert all(font in plt.rcParams['font.sans-serif'] for font in ['Microsoft YaHei', 'SimHei', 'Arial'])
        assert not plt.rcParams['axes.unicode_minus']
        
    def test_save_network_data(self, result_saver, mock_network, tmp_path):
        """测试保存网络数据"""
        save_path = str(tmp_path / "test_results/network")
        result_saver.save_network_data(mock_network, save_path)
        
        # 测试 S 参数数据文件
        s_params_file = f"{save_path}_s_parameters.npy"
        assert os.path.exists(s_params_file)
        data = np.load(s_params_file)
        
        # 验证数据形状和类型
        assert isinstance(data, np.ndarray)
        assert data.dtype == np.float64
        assert data.shape == (8,)
        
        # 验证数据内容和范围
        assert np.all(np.isfinite(data))  # 检查是否有无穷大或 NaN 值
        assert -1 <= data[0] <= 1  # S11 实部应在 [-1, 1] 范围内
        assert -1 <= data[1] <= 1  # S11 虚部应在 [-1, 1] 范围内
        assert data[2] >= 1.0  # VSWR 应大于等于 1
        assert -1 <= data[3] <= 1  # 反射系数实部应在 [-1, 1] 范围内
        assert -1 <= data[4] <= 1  # 反射系数虚部应在 [-1, 1] 范围内
        assert data[5] > 0  # 输入阻抗实部应为正数
        assert data[7] > 0  # 频率应为正数
        
        # 验证具体数值
        assert np.allclose(data[0], mock_network.s_parameters[0].real)
        assert np.allclose(data[1], mock_network.s_parameters[0].imag)
        assert np.allclose(data[2], mock_network.vswr)
        assert np.allclose(data[3], mock_network.reflection_coefficient.real)
        assert np.allclose(data[4], mock_network.reflection_coefficient.imag)
        assert np.allclose(data[5], mock_network.input_impedance.real)
        assert np.allclose(data[6], mock_network.input_impedance.imag)
        assert np.allclose(data[7], mock_network.frequency)
        
    def test_save_plots(self, result_saver, mock_network, tmp_path):
        """测试保存图表"""
        save_path = str(tmp_path / "test_results/network")
        result_saver.save_plots(mock_network, save_path)
        
        # 测试S参数图
        s_params_plot = f"{save_path}_s_parameters.png"
        assert os.path.exists(s_params_plot)
        
        # 测试驻波比图
        vswr_plot = f"{save_path}_vswr.png"
        assert os.path.exists(vswr_plot)
        
    def test_save_optimization_results(self, result_saver, tmp_path):
        """测试保存优化结果"""
        results = [
            {"param1": 1.0, "param2": 2.0, "result": 3.0},
            {"param1": 1.5, "param2": 2.5, "result": 3.5}
        ]
        save_path = str(tmp_path / "test_results/optimization")
        result_saver.save_optimization_results(results, save_path)
        
        # 测试优化结果文件
        opt_file = f"{save_path}_optimization.csv"
        assert os.path.exists(opt_file)
        
        # 读取并验证数据
        with open(opt_file, "r") as f:
            lines = f.readlines()
            assert len(lines) == 3  # 表头 + 2行数据
            assert "param1,param2,result" in lines[0]
            
    def test_save_parameter_sweep(self, result_saver, tmp_path):
        """测试保存参数扫描结果"""
        sweep_results = [
            {"freq": 1e9, "优化目标值": 1.0},
            {"freq": 2e9, "优化目标值": 1.5},
            {"freq": 3e9, "优化目标值": 2.0}
        ]
        save_path = str(tmp_path / "test_results/sweep")
        result_saver.save_parameter_sweep(sweep_results, save_path, "freq")
        
        # 测试扫描结果图
        sweep_plot = f"{save_path}_sweep_freq.png"
        assert os.path.exists(sweep_plot)
        
        # 测试扫描数据文件
        sweep_file = f"{save_path}_sweep_freq.csv"
        assert os.path.exists(sweep_file)
        data = np.loadtxt(sweep_file, delimiter=",", skiprows=1)
        assert data.shape == (3, 2)
        
    def test_save_all_results(self, result_saver, mock_network, tmp_path):
        """测试保存所有结果"""
        save_path = str(tmp_path / "test_results/all")
        result_saver.save_all_results(mock_network, save_path)
        
        # 测试网络数据文件
        assert os.path.exists(f"{save_path}_s_parameters.npy")
        
        # 测试图表文件
        assert os.path.exists(f"{save_path}_s_parameters.png")
        assert os.path.exists(f"{save_path}_vswr.png")
        
    def test_invalid_network(self, result_saver, mock_network, tmp_path):
        """测试无效网络对象"""
        save_path = str(tmp_path / "test_results/invalid")
        
        # 测试完全无效的网络对象
        class InvalidNetwork:
            pass
        invalid_network = InvalidNetwork()
        with pytest.raises(ValueError, match="网络参数未计算"):
            result_saver.save_network_data(invalid_network, save_path)
            
        # 测试部分属性缺失的网络对象
        class PartialNetwork:
            def __init__(self):
                self.s_parameters = np.array([complex(0.1, 0.2)])
                # 缺少 vswr 属性
        partial_network = PartialNetwork()
        with pytest.raises(ValueError, match="网络参数未计算"):
            result_saver.save_network_data(partial_network, save_path)
            
        # 测试属性值无效的网络对象
        class InvalidValueNetwork:
            def __init__(self):
                self.s_parameters = np.array([complex(np.inf, np.nan)])
                self.vswr = -1.0  # 无效的 VSWR 值
                self.reflection_coefficient = complex(2.0, 2.0)  # 无效的反射系数
                self.input_impedance = complex(-50.0, np.inf)  # 无效的输入阻抗
                self.frequency = -1e9  # 无效的频率
        invalid_value_network = InvalidValueNetwork()
        with pytest.raises(ValueError):
            result_saver.save_network_data(invalid_value_network, save_path)
            
        # 测试文件系统错误
        with patch('os.makedirs') as mock_makedirs:
            mock_makedirs.side_effect = OSError("模拟的文件系统错误")
            with pytest.raises(OSError, match="创建保存目录失败"):
                result_saver.save_network_data(mock_network, os.path.join(tmp_path, "nonexistent", "test"))

    def test_invalid_save_path(self, result_saver, mock_network, tmp_path):
        """测试无效保存路径"""
        # 使用不存在的目录
        invalid_path = str(tmp_path / "nonexistent/test")
        
        # 测试保存网络数据
        result_saver.save_network_data(mock_network, invalid_path)
        assert os.path.exists(f"{invalid_path}_s_parameters.npy")
        
        # 测试保存图表
        result_saver.save_plots(mock_network, invalid_path)
        assert os.path.exists(f"{invalid_path}_s_parameters.png")
        
        # 测试保存优化结果
        results = [{"param": 1.0, "result": 2.0}]
        result_saver.save_optimization_results(results, invalid_path)
        assert os.path.exists(f"{invalid_path}_optimization.csv")
        
        # 测试保存参数扫描结果
        sweep_results = [{"freq": 1e9, "优化目标值": 1.0}]
        result_saver.save_parameter_sweep(sweep_results, invalid_path, "freq")
        assert os.path.exists(f"{invalid_path}_sweep_freq.png")
        
    def test_matplotlib_config(self, result_saver):
        """测试 matplotlib 配置"""
        import matplotlib.pyplot as plt
        
        # 测试字体配置
        assert 'sans-serif' in plt.rcParams['font.family']
        assert all(font in plt.rcParams['font.sans-serif'] 
                  for font in ['Microsoft YaHei', 'SimHei', 'Arial'])
        
        # 测试负号显示配置
        assert not plt.rcParams['axes.unicode_minus']
        
        # 测试后端配置
        assert plt.get_backend() == 'Agg'
        
        # 测试图表样式配置
        fig, ax = plt.subplots()
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)
        
        # 测试中文字体渲染
        fig, ax = plt.subplots()
        ax.set_title('测试中文标题')
        ax.set_xlabel('测试中文标签')
        plt.close(fig)