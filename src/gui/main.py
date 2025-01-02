"""主窗口模块"""
import os
import sys
import numpy as np
from microwave_gui import MicrowaveGUI, start_gui
from src.impedance_matching.quarter_wave import QuarterWaveTransformer
from src.impedance_matching.stub_matching import StubMatcher
from src.optimization.calculator import CalculationParameters
from src.help.help_system import HelpSystem
from src.visualization.result_saver import ResultSaver

class MicrowaveDesignApp:
    def __init__(self):
        """初始化应用"""
        print("初始化应用...")
        self.current_theme = "light"
        self.is_calculating = False
        self.current_parameters = None
        self.gui = MicrowaveGUI(self)
        print("GUI实例已创建")

    def calculate(self):
        """
        执行计算

        返回:
            str, 计算结果的字符串表示
        """
        if not self.current_parameters:
            return "请先输入参数"
            
        self.is_calculating = True
        try:
            if self.current_parameters.matching_method == "quarter_wave":
                transformer = QuarterWaveTransformer(
                    z0=self.current_parameters.z0,
                    zl=self.current_parameters.get_complex_load(),
                    freq=self.current_parameters.freq
                )
                result = transformer.get_results()
                if result:
                    return f"""四分之一波长变换器设计结果:
特征阻抗: {result['z0']:.2f} Ω
负载阻抗: {result['zl']:.2f} Ω
变换器阻抗: {result['z1']:.2f} Ω
变换器长度: {result['length']*1000:.2f} mm"""
            else:
                matcher = StubMatcher(
                    z0=self.current_parameters.z0,
                    zl=self.current_parameters.get_complex_load(),
                    freq=self.current_parameters.freq
                )
                result = matcher.get_results()
                if result:
                    return f"""单枝节匹配设计结果:
特征阻抗: {result['z0']:.2f} Ω
负载阻抗: {result['zl']:.2f} Ω
主线距离: {result['d']*1000:.2f} mm
支节长度: {result['l']*1000:.2f} mm"""
                
            return "计算失败，请检查参数"
        except Exception as e:
            return f"计算错误: {str(e)}"
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
            freq = float(freq)
            z0 = float(z0)
            z_load_real = float(z_load_real)
            z_load_imag = float(z_load_imag)
            
            if freq <= 0:
                return False
            if z0 <= 0:
                return False
            if z_load_real <= 0:
                return False
            if matching_method not in ["quarter_wave", "stub"]:
                return False
                
            self.current_parameters = CalculationParameters(
                freq=freq * 1e9,  # 转换为Hz
                z0=z0,
                z_load_real=z_load_real,
                z_load_imag=z_load_imag,
                matching_method=matching_method
            )
            return True
        except (TypeError, ValueError):
            return False
            
    def run(self):
        """运行GUI应用"""
        print("运行应用...")
        print("启动GUI应用...")
        try:
            start_gui(self.gui)
        except Exception as e:
            print(f"GUI启动错误: {e}")
            raise

if __name__ == "__main__":
    print("程序启动...")
    app = MicrowaveDesignApp()
    print("运行应用...")
    app.run() 