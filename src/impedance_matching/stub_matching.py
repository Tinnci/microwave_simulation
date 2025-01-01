"""单支节匹配器模块"""
import numpy as np
from typing import Dict, List, Tuple, Union

class StubMatcher:
    """单支节匹配器类"""
    def __init__(self, freq: float, z0: float, zl: complex):
        """
        初始化单支节匹配器

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
        self._calculate_parameters()

    def calculate_wavelength(self) -> float:
        """
        计算波长

        返回:
            float: 波长 (m)
        """
        c = 3e8  # 光速 (m/s)
        return c / self.freq

    def _calculate_parameters(self) -> None:
        """计算匹配器参数"""
        # 归一化负载阻抗
        zl_norm = self.zl / self.z0
        yl_norm = 1 / zl_norm
        gl_norm = yl_norm.real
        bl_norm = yl_norm.imag

        # 计算支节导纳
        try:
            b_stub = np.sqrt(abs((gl_norm - 1)**2 + bl_norm**2 - 1))
            if not np.isfinite(b_stub):
                raise ValueError("无法找到有效的短截线解")
        except (ValueError, RuntimeWarning):
            raise ValueError("无法找到有效的短截线解")

        self.b_stub = b_stub

        # 计算支节到负载的距离
        theta = np.arctan2(bl_norm, gl_norm - 1)
        if theta < 0:
            theta += np.pi
        self.distance = theta * self.wavelength / (4 * np.pi)

        # 计算支节长度
        stub_angle = -np.arctan(1 / b_stub)
        if stub_angle < 0:
            stub_angle += np.pi
        self.stub_length = stub_angle * self.wavelength / (2 * np.pi)

        # 计算S参数
        self.s_parameters = self._calculate_s_parameters()
        self.vswr = self._calculate_vswr()

    def _calculate_s_parameters(self) -> List[complex]:
        """
        计算S参数

        返回:
            List[complex]: S参数列表 [S11, S12, S21, S22]
        """
        # 计算归一化导纳
        y_stub = 1j * self.b_stub
        y_load = 1 / (self.zl / self.z0)

        # 计算反射系数
        gamma_in = (y_stub - 1) / (y_stub + 1)
        gamma_out = (y_load - 1) / (y_load + 1)

        # 计算S参数
        s11 = gamma_in
        s22 = gamma_out
        s12 = s21 = np.sqrt(1 - abs(gamma_in)**2) * np.sqrt(1 - abs(gamma_out)**2)
        return [s11, s12, s21, s22]

    def _calculate_vswr(self) -> float:
        """
        计算驻波比

        返回:
            float: 驻波比
        """
        gamma = abs(self.s_parameters[0])  # 使用S11作为反射系数
        if gamma >= 1:
            return float('inf')  # 完全反射时返回无穷大
        return (1 + gamma) / (1 - gamma)

    def calculate_distance(self) -> float:
        """
        计算支节到负载的距离

        返回:
            float: 支节到负载的距离 (m)
        """
        return self.distance

    def calculate_stub_length(self) -> float:
        """
        计算支节长度

        返回:
            float: 支节长度 (m)
        """
        return self.stub_length

    def get_all_solutions(self) -> List[Dict[str, float]]:
        """
        获取所有可能的解

        返回:
            List[Dict[str, float]]: 解的列表
        """
        solutions = []
        # 基本解
        solutions.append({
            "distance": self.distance,
            "stub_length": self.stub_length
        })
        # 半波长周期解
        for i in range(1, 3):  # 添加两个周期解
            solutions.append({
                "distance": self.distance + i * self.wavelength / 2,
                "stub_length": self.stub_length
            })
        return solutions

    def get_results(self) -> Dict[str, Union[float, List[complex], List[Dict[str, float]]]]:
        """
        获取计算结果

        返回:
            Dict[str, Union[float, List[complex], List[Dict[str, float]]]]: 计算结果字典
        """
        return {
            "wavelength": self.wavelength,
            "distance": self.distance,
            "stub_length": self.stub_length,
            "s_parameters": self.s_parameters,
            "vswr": self.vswr,
            "solutions": self.get_all_solutions()
        }

    def _calculate_stub_parameters(self):
        """计算短截线参数"""
        # 归一化负载导纳
        yl_norm = 1 / self.zl_norm
        gl_norm = yl_norm.real
        bl_norm = yl_norm.imag
        
        # 计算短截线导纳
        try:
            b_stub = np.sqrt(abs((gl_norm - 1)**2 + bl_norm**2 - 1))  # 添加 abs 避免负数平方根
            if not np.isfinite(b_stub):
                raise ValueError("无法找到有效的短截线解")
        except (ValueError, RuntimeWarning):
            raise ValueError("无法找到有效的短截线解")
            
        # 计算短截线到负载的距离
        theta = np.arctan2(bl_norm, gl_norm - 1)
        if theta < 0:
            theta += np.pi
            
        # 计算短截线长度
        stub_length = -np.arctan(1 / b_stub) / (2 * np.pi)
        if stub_length < 0:
            stub_length += 0.5
            
        return b_stub, theta, stub_length

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