"""主窗口模块"""
import os
import numpy as np
from microwave_gui import MicrowaveGUI
from src.impedance_matching.quarter_wave import QuarterWaveTransformer
from src.impedance_matching.stub_matching import StubMatcher
from src.optimization.calculator import CalculationParameters
from src.help.help_system import HelpSystem
from src.visualization.result_saver import ResultSaver

class MicrowaveDesignApp:
    """微波设计应用类"""
    
    def __init__(self):
        """初始化应用"""
        self.help_system = HelpSystem()
        self.result_saver = ResultSaver()
        self.current_parameters = None
        self.is_calculating = False
        self.current_theme = "light"
        self.gui = MicrowaveGUI(self)
        
    def validate_parameters(self, freq, z0, z_load_real, z_load_imag, matching_method):
        """
        验证参数

        参数:
            freq: float, 频率 (Hz)
            z0: float, 特征阻抗 (Ω)
            z_load_real: float, 负载阻抗实部 (Ω)
            z_load_imag: float, 负载阻抗虚部 (Ω)
            matching_method: str, 匹配方法

        返回:
            bool, 参数是否有效
        """
        try:
            if freq <= 0:
                return False
            if z0 <= 0:
                return False
            if z_load_real <= 0:
                return False
            if matching_method not in ["quarter_wave", "stub"]:
                return False
            return True
        except (TypeError, ValueError):
            return False
            
    def parse_complex_impedance(self, impedance_str):
        """
        解析复数阻抗

        参数:
            impedance_str: str, 复数阻抗字符串

        返回:
            complex, 复数阻抗
        """
        try:
            if "j" in impedance_str:
                real_str, imag_str = impedance_str.split("+j")
                return complex(float(real_str), float(imag_str))
            else:
                return complex(float(impedance_str), 0)
        except (ValueError, TypeError):
            raise ValueError("无效的复数阻抗格式")
            
    def set_frequency(self, value: str) -> None:
        """设置频率"""
        try:
            freq = float(value)
            if self.validate_parameters(freq, 50, 75, 0, "quarter_wave"):
                if self.current_parameters:
                    self.current_parameters.freq = freq
        except ValueError:
            pass
            
    def set_z0(self, value: str) -> None:
        """设置特征阻抗"""
        try:
            z0 = float(value)
            if self.validate_parameters(1e9, z0, 75, 0, "quarter_wave"):
                if self.current_parameters:
                    self.current_parameters.z0 = z0
        except ValueError:
            pass
            
    def set_z_load_real(self, value: str) -> None:
        """设置负载阻抗实部"""
        try:
            z_load_real = float(value)
            if self.validate_parameters(1e9, 50, z_load_real, 0, "quarter_wave"):
                if self.current_parameters:
                    self.current_parameters.z_load_real = z_load_real
        except ValueError:
            pass
            
    def set_z_load_imag(self, value: str) -> None:
        """设置负载阻抗虚部"""
        try:
            z_load_imag = float(value)
            if self.current_parameters:
                self.current_parameters.z_load_imag = z_load_imag
        except ValueError:
            pass
            
    def set_matching_method(self, method: str) -> None:
        """设置匹配方法"""
        if method in ["quarter_wave", "stub"]:
            if self.current_parameters:
                self.current_parameters.matching_method = method
            
    def update_parameters(self, freq, z0, z_load_real, z_load_imag, matching_method):
        """
        更新参数

        参数:
            freq: float, 频率 (Hz)
            z0: float, 特征阻抗 (Ω)
            z_load_real: float, 负载阻抗实部 (Ω)
            z_load_imag: float, 负载阻抗虚部 (Ω)
            matching_method: str, 匹配方法
        """
        self.current_parameters = CalculationParameters(
            freq=freq,
            z0=z0,
            z_load_real=z_load_real,
            z_load_imag=z_load_imag,
            matching_method=matching_method
        )
        # 同步更新GUI状态
        self.gui.begin_update()
        self.gui.set_frequency(str(freq))
        self.gui.set_z0(str(z0))
        self.gui.set_z_load_real(str(z_load_real))
        self.gui.set_z_load_imag(str(z_load_imag))
        self.gui.set_matching_method(matching_method)
        self.gui.end_update()
        
    def calculate(self):
        """
        执行计算

        返回:
            dict, 计算结果
        """
        if not self.current_parameters:
            return None
            
        self.is_calculating = True
        try:
            if self.current_parameters.matching_method == "quarter_wave":
                transformer = QuarterWaveTransformer(
                    z0=self.current_parameters.z0,
                    zl=self.current_parameters.get_complex_load(),
                    freq=self.current_parameters.freq
                )
                result = transformer.get_results()
            else:
                matcher = StubMatcher(
                    z0=self.current_parameters.z0,
                    zl=self.current_parameters.get_complex_load(),
                    freq=self.current_parameters.freq
                )
                result = matcher.get_results()
                
            # 更新GUI结果
            if result:
                self.gui.set_result(str(result))
            return result
        finally:
            self.is_calculating = False
            
    def set_theme(self, theme):
        """
        设置主题

        参数:
            theme: str, 主题名称
        """
        if theme in ["light", "dark"]:
            self.current_theme = theme
            self.gui.set_theme(theme)
            
    def get_validation_message(self, freq, z0, z_load_real, z_load_imag, matching_method):
        """
        获取验证消息

        参数:
            freq: float, 频率 (Hz)
            z0: float, 特征阻抗 (Ω)
            z_load_real: float, 负载阻抗实部 (Ω)
            z_load_imag: float, 负载阻抗虚部 (Ω)
            matching_method: str, 匹配方法

        返回:
            str, 验证消息，如果参数有效则返回None
        """
        try:
            if freq <= 0:
                return "频率必须为正数"
            if z0 <= 0:
                return "特征阻抗必须为正数"
            if z_load_real <= 0:
                return "负载阻抗实部必须为正数"
            if matching_method not in ["quarter_wave", "stub"]:
                return "匹配方法必须是quarter_wave或stub"
            return None
        except (TypeError, ValueError):
            return "参数类型错误"
            
    def run(self):
        """运行GUI应用"""
        # 启动Rust GUI
        self.gui.view() 