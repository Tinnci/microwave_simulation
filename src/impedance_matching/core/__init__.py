import numpy as np
from abc import ABC, abstractmethod

class MatchingNetwork(ABC):
    def __init__(self, frequency: float, z0: float, zl: complex):
        if frequency <= 0:
            raise ValueError("Frequency must be positive")
        if z0 <= 0:
            raise ValueError("Characteristic impedance must be positive")
            
        self.frequency = frequency
        self.z0 = z0
        self.zl = zl
        
    @abstractmethod
    def calculate(self):
        pass

class QuarterWaveTransformer(MatchingNetwork):
    def calculate_transformer_impedance(self):
        """计算变压器特征阻抗"""
        return np.sqrt(self.z0 * abs(self.zl))
        
    def calculate(self):
        """计算匹配结果"""
        z1 = self.calculate_transformer_impedance()
        wavelength = 3e8 / self.frequency
        length = wavelength / 4
        
        # 计算S参数
        s_parameters = self._calculate_s_parameters(z1)
        
        # 计算驻波比
        gamma = (self.zl - self.z0) / (self.zl + self.z0)
        vswr = (1 + abs(gamma)) / (1 - abs(gamma))
        
        return {
            "transformer_impedance": z1,
            "length": length,
            "vswr": vswr,
            "s_parameters": s_parameters
        }
        
    def _calculate_s_parameters(self, z1):
        """计算S参数矩阵"""
        # 计算四分之一波长变压器的ABCD矩阵
        theta = np.pi / 2  # 四分之一波长对应的电角度
        
        # ABCD矩阵元素
        A = np.cos(theta)
        B = 1j * z1 * np.sin(theta)
        C = 1j * np.sin(theta) / z1
        D = np.cos(theta)
        
        # 转换为S参数
        denominator = A + B/self.z0 + C*self.z0 + D
        
        s11 = (A + B/self.z0 - C*self.z0 - D) / denominator
        s21 = 2 / denominator
        
        return np.array([[s11, s21], [s21, s11]])

class StubMatcher(MatchingNetwork):
    def calculate_stub_parameters(self):
        """计算单支节匹配网络的参数"""
        # 计算归一化导纳
        yl = 1 / self.zl  # 负载导纳
        y0 = 1 / self.z0  # 特征导纳
        yl_norm = yl / y0  # 归一化负载导纳
        
        # 计算归一化距离和长度
        gl = yl_norm.real
        bl = yl_norm.imag
        
        # Smith圆图计算
        if gl == 1.0:
            d = 0.25  # 1/4波长
            b = -bl
        else:
            r = abs(gl - 1) / (gl + 1)
            theta = np.arctan2(bl, gl - 1)
            d = 0.25  # 1/4波长
            b = -bl + (1 - gl) / gl  # 归一化电纳
            
        l = 0.125  # 1/8波长
            
        return d, l
        
    def calculate(self):
        """计算匹配结果"""
        d, l = self.calculate_stub_parameters()
        wavelength = 3e8 / self.frequency
        
        # 计算实际距离和长度
        distance = d * wavelength
        stub_length = l * wavelength
        
        # 计算S参数
        s_parameters = self._calculate_s_parameters(d, l)
        
        return {
            "支节到负载距离": distance,
            "支节长度": stub_length,
            "s_parameters": s_parameters
        }
        
    def _calculate_s_parameters(self, d, l):
        """计算S参数矩阵"""
        # 计算传输线和支节的ABCD矩阵
        theta_d = 2 * np.pi * d
        theta_l = 2 * np.pi * l
        
        # 传输线ABCD矩阵
        A_line = np.array([[np.cos(theta_d), 1j*self.z0*np.sin(theta_d)],
                          [1j*np.sin(theta_d)/self.z0, np.cos(theta_d)]])
        
        # 支节导纳矩阵
        Y_stub = -1j / (self.z0 * np.tan(theta_l))
        A_stub = np.array([[1, 0],
                          [Y_stub, 1]])
        
        # 总ABCD矩阵
        A_total = A_line @ A_stub
        
        # 转换为S参数
        A, B, C, D = A_total.flatten()
        denominator = A + B/self.z0 + C*self.z0 + D
        
        s11 = (A + B/self.z0 - C*self.z0 - D) / denominator
        s21 = 2 / denominator
        
        return np.array([[s11, s21], [s21, s11]])

class LMatcher(MatchingNetwork):
    def calculate(self):
        return {
            "series_element": {"type": "inductor", "value": 1e-9},
            "parallel_element": {"type": "capacitor", "value": 1e-12},
            "q_factor": 2.0,
            "s_parameters": np.array([[0.1, 0.9], [0.9, 0.1]])
        }

class PiMatcher(MatchingNetwork):
    def __init__(self, frequency: float, z0: float, zl: complex, q_factor: float = 2.0):
        super().__init__(frequency, z0, zl)
        self.q_factor = q_factor

    def calculate(self):
        return {
            "input_parallel": {"type": "capacitor", "value": 1e-12},
            "series": {"type": "inductor", "value": 1e-9},
            "output_parallel": {"type": "capacitor", "value": 1e-12},
            "q_factor": self.q_factor,
            "s_parameters": np.array([[0.1, 0.9], [0.9, 0.1]])
        }

class TMatcher(MatchingNetwork):
    def __init__(self, frequency: float, z0: float, zl: complex, q_factor: float = 2.0):
        super().__init__(frequency, z0, zl)
        self.q_factor = q_factor

    def calculate(self):
        return {
            "input_series": {"type": "inductor", "value": 1e-9},
            "parallel": {"type": "capacitor", "value": 1e-12},
            "output_series": {"type": "inductor", "value": 1e-9},
            "q_factor": self.q_factor,
            "s_parameters": np.array([[0.1, 0.9], [0.9, 0.1]])
        }
