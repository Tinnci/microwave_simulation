"""GUI单元测试模块"""
import pytest
from src.gui.main import MicrowaveDesignApp

@pytest.fixture
def app():
    """创建应用实例"""
    return MicrowaveDesignApp()

def test_validate_parameters(app):
    """测试参数验证"""
    # 有效参数
    assert app.validate_parameters(1e9, 50, 75, 25, "quarter_wave") is True
    assert app.validate_parameters(2e9, 75, 100, 0, "stub") is True
    
    # 无效参数
    assert app.validate_parameters(-1e9, 50, 75, 25, "quarter_wave") is False
    assert app.validate_parameters(1e9, -50, 75, 25, "quarter_wave") is False
    assert app.validate_parameters(1e9, 50, -75, 25, "quarter_wave") is False
    assert app.validate_parameters(1e9, 50, 75, 25, "invalid_method") is False

def test_parse_complex_impedance(app):
    """测试复数阻抗解析"""
    # 有效输入
    assert app.parse_complex_impedance("50+j25") == complex(50, 25)
    assert app.parse_complex_impedance("75") == complex(75, 0)
    
    # 无效输入
    with pytest.raises(ValueError):
        app.parse_complex_impedance("invalid")
    with pytest.raises(ValueError):
        app.parse_complex_impedance("50+25")

def test_update_parameters(app):
    """测试参数更新"""
    app.update_parameters(1e9, 50, 75, 25, "quarter_wave")
    params = app.current_parameters
    assert params.freq == 1e9
    assert params.z0 == 50
    assert params.z_load_real == 75
    assert params.z_load_imag == 25
    assert params.matching_method == "quarter_wave"

def test_calculate(app):
    """测试计算功能"""
    # 未设置参数时
    assert app.calculate() is None
    
    # 设置参数后
    app.update_parameters(1e9, 50, 75, 25, "quarter_wave")
    result = app.calculate()
    assert result is not None
    assert "wavelength" in result
    assert "transformer_impedance" in result
    assert "vswr" in result

def test_set_theme(app):
    """测试主题设置"""
    # 默认主题
    assert app.current_theme == "light"
    
    # 设置有效主题
    app.set_theme("dark")
    assert app.current_theme == "dark"
    
    # 设置无效主题
    app.set_theme("invalid")
    assert app.current_theme == "dark"  # 保持原主题不变

def test_get_validation_message(app):
    """测试验证消息获取"""
    # 有效参数
    assert app.get_validation_message(1e9, 50, 75, 25, "quarter_wave") is None
    
    # 无效参数
    assert "频率" in app.get_validation_message(-1e9, 50, 75, 25, "quarter_wave")
    assert "特征阻抗" in app.get_validation_message(1e9, -50, 75, 25, "quarter_wave")
    assert "负载阻抗" in app.get_validation_message(1e9, 50, -75, 25, "quarter_wave")
    assert "匹配方法" in app.get_validation_message(1e9, 50, 75, 25, "invalid_method") 