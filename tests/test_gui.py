"""GUI模块测试"""
import pytest
from src.gui.main import MicrowaveDesignApp

class TestMicrowaveDesignApp:
    """测试微波设计应用类"""
    
    @pytest.fixture
    def app(self):
        """创建应用实例"""
        return MicrowaveDesignApp()
        
    def test_init(self, app):
        """测试初始化"""
        assert app.current_parameters is None
        assert app.is_calculating is False
        assert app.current_theme == "light"
        
    def test_validate_parameters(self, app):
        """测试参数验证"""
        # 测试有效参数
        assert app.validate_parameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) is True
        
        # 测试无效频率
        assert app.validate_parameters(
            freq=-1,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) is False
        
        # 测试无效特征阻抗
        assert app.validate_parameters(
            freq=5e9,
            z0=0,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) is False
        
        # 测试无效负载阻抗
        assert app.validate_parameters(
            freq=5e9,
            z0=50,
            z_load_real=0,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) is False
        
        # 测试无效匹配方法
        assert app.validate_parameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="invalid"
        ) is False
        
    def test_parse_complex_impedance(self, app):
        """测试复数阻抗解析"""
        # 测试实部+虚部
        assert app.parse_complex_impedance("75+j25") == complex(75, 25)
        
        # 测试仅实部
        assert app.parse_complex_impedance("50") == complex(50, 0)
        
        # 测试无效格式
        with pytest.raises(ValueError, match="无效的复数阻抗格式"):
            app.parse_complex_impedance("invalid")
            
    def test_update_parameters(self, app):
        """测试参数更新"""
        app.update_parameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        )
        assert app.current_parameters is not None
        assert app.current_parameters.freq == 5e9
        assert app.current_parameters.z0 == 50
        assert app.current_parameters.z_load_real == 75
        assert app.current_parameters.z_load_imag == 25
        assert app.current_parameters.matching_method == "quarter_wave"
        
    def test_calculate(self, app):
        """测试计算"""
        # 测试无参数时的计算
        assert app.calculate() is None
        
        # 测试四分之一波长变换器计算
        app.update_parameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        )
        result = app.calculate()
        assert result is not None
        assert "vswr" in result
        assert result["vswr"] > 1.0
        
        # 测试短截线计算
        app.update_parameters(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="stub"
        )
        result = app.calculate()
        assert result is not None
        assert "vswr" in result
        assert result["vswr"] > 1.0
        
    def test_set_theme(self, app):
        """测试主题设置"""
        # 测试有效主题
        app.set_theme("dark")
        assert app.current_theme == "dark"
        
        app.set_theme("light")
        assert app.current_theme == "light"
        
        # 测试无效主题
        app.set_theme("invalid")
        assert app.current_theme == "light"  # 保持原主题不变
        
    def test_get_validation_message(self, app):
        """测试验证消息获取"""
        # 测试有效参数
        assert app.get_validation_message(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) is None
        
        # 测试无效频率
        assert app.get_validation_message(
            freq=-1,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) == "频率必须为正数"
        
        # 测试无效特征阻抗
        assert app.get_validation_message(
            freq=5e9,
            z0=0,
            z_load_real=75,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) == "特征阻抗必须为正数"
        
        # 测试无效负载阻抗
        assert app.get_validation_message(
            freq=5e9,
            z0=50,
            z_load_real=0,
            z_load_imag=25,
            matching_method="quarter_wave"
        ) == "负载阻抗实部必须为正数"
        
        # 测试无效匹配方法
        assert app.get_validation_message(
            freq=5e9,
            z0=50,
            z_load_real=75,
            z_load_imag=25,
            matching_method="invalid"
        ) == "匹配方法必须是quarter_wave或stub" 