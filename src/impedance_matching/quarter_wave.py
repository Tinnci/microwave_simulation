"""四分之一波长变换器模块"""
import numpy as np
from typing import Dict, Optional, List, Union

class QuarterWaveTransformer:
    """四分之一波长变换器类"""
    def __init__(self, freq: float, z0: float, zl: complex):
        """
        初始化四分之一波长变换器

        参数:
            freq: float, 频率 (Hz)
            z0: float, 特征阻抗 (Ω)
            zl: complex, 负载阻抗 (Ω)
        """
        if freq <= 0:
            raise ValueError("频率必须为正数")
        if z0 <= 0:
            raise ValueError("特征阻抗必须为正数")
        if abs(zl) <= 0:
            raise ValueError("负载阻抗的模必须为正数")

        self.freq = freq
        self.z0 = z0
        self.zl = zl
        self.wavelength = self.calculate_wavelength()
        self.zt = self.calculate_transformer_impedance()
        self.s_parameters = self.calculate_s_parameters()
        self.vswr = self.calculate_vswr()

    def calculate_wavelength(self) -> float:
        """
        计算波长

        返回:
            float: 波长 (m)
        """
        c = 3e8  # 光速 (m/s)
        return c / self.freq

    def calculate_transformer_impedance(self) -> float:
        """
        计算变换器特征阻抗

        返回:
            float: 变换器特征阻抗 (Ω)
        """
        return np.sqrt(abs(self.z0 * self.zl))

    def calculate_s_parameters(self) -> List[complex]:
        """
        计算S参数

        返回:
            List[complex]: S参数列表 [S11, S12, S21, S22]
        """
        gamma_in = (self.zt - self.z0) / (self.zt + self.z0)
        gamma_out = (self.zl - self.zt) / (self.zl + self.zt)
        s11 = gamma_in
        s22 = gamma_out
        s12 = s21 = np.sqrt(1 - abs(gamma_in)**2) * np.sqrt(1 - abs(gamma_out)**2)
        return [s11, s12, s21, s22]

    def calculate_vswr(self) -> float:
        """
        计算驻波比

        返回:
            float: 驻波比
        """
        gamma = abs(self.s_parameters[0])  # 使用S11作为反射系数
        return (1 + gamma) / (1 - gamma)

    def get_results(self) -> Dict[str, Union[float, List[complex]]]:
        """
        获取计算结果

        返回:
            Dict[str, Union[float, List[complex]]]: 计算结果字典
        """
        return {
            "wavelength": self.wavelength,
            "transformer_impedance": self.zt,
            "s_parameters": self.s_parameters,
            "vswr": self.vswr
        }

class Network:
    """网络类"""
    
    def __init__(self, frequency, s):
        """
        初始化网络

        参数:
            frequency: ndarray, 频率点
            s: ndarray, S参数矩阵
        """
        self.f = frequency
        self.s = s 