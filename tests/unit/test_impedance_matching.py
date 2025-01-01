"""阻抗匹配模块测试"""
import pytest
import numpy as np
from src.impedance_matching.core import (
    QuarterWaveTransformer,
    StubMatcher
)

class TestQuarterWaveTransformer:
    """四分之一波长变换器测试类"""
    
    def test_valid_parameters(self):
        """测试有效参数"""
        # 测试纯实数负载
        transformer = QuarterWaveTransformer(
            frequency=5e9,
            z0=50,
            zl=complex(75, 0)
        )
        assert transformer.frequency == 5e9
        assert transformer.z0 == 50
        assert transformer.zl == complex(75, 0)
        
        # 测试复数负载
        transformer = QuarterWaveTransformer(
            frequency=5e9,
            z0=50,
            zl=complex(75, 25)
        )
        assert transformer.frequency == 5e9
        assert transformer.z0 == 50
        assert transformer.zl == complex(75, 25)
        
    def test_invalid_parameters(self):
        """测试无效参数"""
        # 测试频率范围
        with pytest.raises(ValueError, match="Frequency must be positive"):
            QuarterWaveTransformer(
                frequency=0,
                z0=50,
                zl=complex(75, 0)
            )
            
        # 测试特征阻抗范围
        with pytest.raises(ValueError, match="Characteristic impedance must be positive"):
            QuarterWaveTransformer(
                frequency=5e9,
                z0=0,
                zl=complex(75, 0)
            )
            
    def test_vswr_calculation(self):
        """测试驻波比计算"""
        transformer = QuarterWaveTransformer(
            frequency=5e9,
            z0=50,
            zl=complex(75, 0)
        )
        result = transformer.calculate()
        vswr = result["vswr"]
        assert vswr == pytest.approx(1.5, rel=1e-3)
        
    def test_wavelength_calculation(self):
        """测试波长计算"""
        transformer = QuarterWaveTransformer(
            frequency=5e9,
            z0=50,
            zl=complex(75, 0)
        )
        result = transformer.calculate()
        length = result["length"]
        wavelength = length * 4
        assert wavelength == pytest.approx(0.06, rel=1e-3)
        
class TestStubMatcher:
    """单枝节匹配器测试类"""
    
    def test_valid_parameters(self):
        """测试有效参数"""
        # 测试纯实数负载
        matcher = StubMatcher(
            frequency=5e9,
            z0=50,
            zl=complex(75, 0)
        )
        assert matcher.frequency == 5e9
        assert matcher.z0 == 50
        assert matcher.zl == complex(75, 0)
        
        # 测试复数负载
        matcher = StubMatcher(
            frequency=5e9,
            z0=50,
            zl=complex(75, 25)
        )
        assert matcher.frequency == 5e9
        assert matcher.z0 == 50
        assert matcher.zl == complex(75, 25)
        
    def test_invalid_parameters(self):
        """测试无效参数"""
        # 测试频率范围
        with pytest.raises(ValueError, match="Frequency must be positive"):
            StubMatcher(
                frequency=0,
                z0=50,
                zl=complex(75, 0)
            )
            
        # 测试特征阻抗范围
        with pytest.raises(ValueError, match="Characteristic impedance must be positive"):
            StubMatcher(
                frequency=5e9,
                z0=0,
                zl=complex(75, 0)
            )
            
    def test_distance_calculation(self):
        """测试支节到负载距离计算"""
        matcher = StubMatcher(
            frequency=5e9,
            z0=50,
            zl=complex(75, 0)
        )
        result = matcher.calculate()
        distance = result["支节到负载距离"]
        assert distance == pytest.approx(0.015, rel=1e-3)
        
    def test_stub_length_calculation(self):
        """测试支节长度计算"""
        matcher = StubMatcher(
            frequency=5e9,
            z0=50,
            zl=complex(75, 0)
        )
        result = matcher.calculate()
        length = result["支节长度"]
        assert length == pytest.approx(0.0075, rel=1e-3)
        
    def test_multiple_solutions(self):
        """测试多解情况"""
        matcher = StubMatcher(
            frequency=5e9,
            z0=50,
            zl=complex(75, 25)
        )
        result = matcher.calculate()
        assert "支节到负载距离" in result
        assert "支节长度" in result