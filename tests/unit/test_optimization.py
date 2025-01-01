"""优化模块测试"""
import pytest
import numpy as np
from src.optimization.calculator import CalculationParameters, BatchCalculator

class TestCalculationParameters:
    """测试计算参数类"""

    def test_init(self):
        """测试初始化"""
        params = CalculationParameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        )
        assert params.freq == 5e9
        assert params.z0 == 50
        assert params.z_load_real == 75
        assert params.z_load_imag == 25
        assert params.matching_method == "quarter_wave"

    def test_get_frequency_hz(self):
        """测试获取频率方法"""
        params = CalculationParameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25
        )
        assert params.get_frequency_hz() == 5e9

    def test_validation(self):
        """测试参数验证"""
        with pytest.raises(ValueError):
            CalculationParameters(
                freq=-1,
                z0=50,
                z_load_real=75,
                z_load_imag=25
            )
        
        with pytest.raises(ValueError):
            CalculationParameters(
                freq=5e9,
                z0=-50,
                z_load_real=75,
                z_load_imag=25
            )

    def test_str_representation(self):
        """测试字符串表示"""
        params = CalculationParameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25
        )
        str_repr = str(params)
        assert "freq" in str_repr
        assert "z0" in str_repr
        assert "z_load_real" in str_repr
        assert "z_load_imag" in str_repr

    def test_valid_parameters(self):
        """测试有效参数"""
        # 测试基本参数
        params = CalculationParameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        )
        assert params.freq == 5e9
        assert params.z0 == 50
        assert params.z_load_real == 75
        assert params.z_load_imag == 25
        assert params.matching_method == "quarter_wave"
        
        # 测试可选参数
        params = CalculationParameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="stub",
            optimization_target="vswr",
            weight_factors={"vswr": 0.7, "length": 0.3}
        )
        assert params.optimization_target == "vswr"
        assert params.weight_factors == {"vswr": 0.7, "length": 0.3}
        
    def test_invalid_parameters(self):
        """测试无效参数"""
        # 测试频率范围
        with pytest.raises(ValueError, match="频率必须为正数"):
            CalculationParameters(
                freq=0,
                z0=50,
                z_load_real=75,
                z_load_imag=25,
                matching_method="quarter_wave"
            )
            
        # 测试特征阻抗范围
        with pytest.raises(ValueError, match="特征阻抗必须为正数"):
            CalculationParameters(
                freq=5e9,
                z0=0,
                z_load_real=75,
                z_load_imag=25,
                matching_method="quarter_wave"
            )
            
        # 测试负载阻抗范围
        with pytest.raises(ValueError, match="负载阻抗实部必须为正数"):
            CalculationParameters(
                freq=5e9,
                z0=50,
                z_load_real=0,
                z_load_imag=25,
                matching_method="quarter_wave"
            )
            
        # 测试匹配方法
        with pytest.raises(ValueError, match="匹配方法必须是"):
            CalculationParameters(
                freq=5e9,
                z0=50,
                z_load_real=75,
                z_load_imag=25,
                matching_method="invalid"
            )
            
        # 测试优化目标
        with pytest.raises(ValueError, match="优化目标必须是"):
            CalculationParameters(
                freq=5e9,
                z0=50,
                z_load_real=75,
                z_load_imag=25,
                matching_method="quarter_wave",
                optimization_target="invalid"
            )
            
        # 测试权重因子
        with pytest.raises(ValueError, match="权重因子必须在"):
            CalculationParameters(
                freq=5e9,
                z0=50,
                z_load_real=75,
                z_load_imag=25,
                matching_method="quarter_wave",
                weight_factors={"vswr": 1.5, "length": -0.5}
            )
            
    def test_parameter_conversion(self):
        """测试参数转换"""
        params = CalculationParameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        )
        # 测试复数阻抗转换
        zl = params.get_complex_load()
        assert zl == complex(75, 25)
        
        # 测试频率转换
        freq_hz = params.get_frequency_hz()
        assert freq_hz == 5e9
        
class TestBatchCalculator:
    """批量计算器测试类"""
    
    @pytest.fixture
    def calculator(self):
        """创建计算器实例"""
        params = CalculationParameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        )
        return BatchCalculator(params)
        
    def test_single_calculation(self, calculator):
        """测试单个计算"""
        result = calculator.calculate()
        assert isinstance(result, dict)
        assert "vswr" in result
        assert result["vswr"] > 1.0
        
    def test_batch_calculation(self, calculator):
        """测试批量计算"""
        params_list = [
            CalculationParameters(freq=5e9, z0=50, z_load_real=75, z_load_imag=25),
            CalculationParameters(freq=5e9, z0=50, z_load_real=100, z_load_imag=0)
        ]
        results = calculator.batch_calculate(params_list)
        assert len(results) == 2
        assert all(isinstance(result, dict) for result in results)
        
    def test_optimization(self, calculator):
        """测试优化计算"""
        param_ranges = {
            "z_load_real": (50, 150),
            "z_load_imag": (-50, 50)
        }
        result = calculator.optimize(param_ranges, num_points=5)
        assert isinstance(result, dict)
        assert "vswr" in result
        
    def test_parameter_sweep(self, calculator):
        """测试参数扫描"""
        values = [50, 75, 100]
        results = calculator.parameter_sweep("z_load_real", values)
        assert len(results) == len(values)
        assert all(isinstance(result, dict) for result in results)
        
    def test_error_handling(self, calculator):
        """测试错误处理"""
        with pytest.raises(ValueError):
            calculator.calculate(CalculationParameters(freq=-1, z0=50, z_load_real=75, z_load_imag=25)) 