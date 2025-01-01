"""优化计算模块"""
import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any
from src.impedance_matching.quarter_wave import QuarterWaveTransformer
from src.impedance_matching.stub_matching import StubMatcher

class CalculationParameters:
    """计算参数类"""
    def __init__(self, freq: float = 5e9, z0: float = 50, z_load_real: float = 75,
                 z_load_imag: float = 25, matching_method: str = "quarter_wave",
                 optimization_target: str = "vswr", weight_factors: Optional[Dict[str, float]] = None):
        """
        初始化计算参数

        参数:
            freq: float, 频率 (Hz)
            z0: float, 特征阻抗 (Ω)
            z_load_real: float, 负载阻抗实部 (Ω)
            z_load_imag: float, 负载阻抗虚部 (Ω)
            matching_method: str, 匹配方法
            optimization_target: str, 优化目标
            weight_factors: dict, 权重因子
        """
        if freq <= 0:
            raise ValueError("频率必须为正数")
        if z0 <= 0:
            raise ValueError("特征阻抗必须为正数")
        if z_load_real <= 0:
            raise ValueError("负载阻抗实部必须为正数")
        if matching_method not in ["quarter_wave", "stub"]:
            raise ValueError("匹配方法必须是quarter_wave或stub")
        if optimization_target not in ["vswr", "length"]:
            raise ValueError("优化目标必须是vswr或length")
        if weight_factors is not None:
            if not all(0 <= v <= 1 for v in weight_factors.values()):
                raise ValueError("权重因子必须在0到1之间")
            if abs(sum(weight_factors.values()) - 1) > 1e-6:
                raise ValueError("权重因子之和必须为1")

        self.freq = freq
        self.z0 = z0
        self.z_load_real = z_load_real
        self.z_load_imag = z_load_imag
        self.matching_method = matching_method
        self.optimization_target = optimization_target
        self.weight_factors = weight_factors or {"vswr": 0.7, "length": 0.3}

    def get_complex_load(self) -> complex:
        """
        获取复数形式的负载阻抗

        返回:
            complex: 负载阻抗
        """
        return complex(self.z_load_real, self.z_load_imag)

    def get_frequency_hz(self) -> float:
        """
        获取频率值

        返回:
            float: 频率 (Hz)
        """
        return self.freq

    def to_dict(self) -> Dict[str, Union[float, str, Dict[str, float]]]:
        """
        转换为字典

        返回:
            Dict[str, Union[float, str, Dict[str, float]]]: 参数字典
        """
        return {
            "freq": self.freq,
            "z0": self.z0,
            "z_load_real": self.z_load_real,
            "z_load_imag": self.z_load_imag,
            "matching_method": self.matching_method,
            "optimization_target": self.optimization_target,
            "weight_factors": self.weight_factors
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[float, str, Dict[str, float]]]) -> 'CalculationParameters':
        """
        从字典创建参数对象

        参数:
            data: Dict[str, Union[float, str, Dict[str, float]]], 参数字典

        返回:
            CalculationParameters: 参数对象
        """
        return cls(
            freq=float(data["freq"]),
            z0=float(data["z0"]),
            z_load_real=float(data["z_load_real"]),
            z_load_imag=float(data["z_load_imag"]),
            matching_method=str(data["matching_method"]),
            optimization_target=str(data["optimization_target"]),
            weight_factors=data.get("weight_factors")
        )

    def __str__(self):
        """返回参数的字符串表示"""
        return (
            f"CalculationParameters(freq={self.freq}, "
            f"z0={self.z0}, "
            f"z_load_real={self.z_load_real}, "
            f"z_load_imag={self.z_load_imag}, "
            f"matching_method={self.matching_method})"
        )

class BatchCalculator:
    """批量计算器类"""
    def __init__(self, params: CalculationParameters):
        """
        初始化批量计算器

        参数:
            params: CalculationParameters, 计算参数
        """
        self.params = params
        self.results = []
        self.best_result = None

    def calculate(self, params: Optional[CalculationParameters] = None) -> Dict[str, Any]:
        """
        执行单次计算

        参数:
            params: Optional[CalculationParameters], 计算参数，如果为None则使用初始化时的参数

        返回:
            Dict[str, Any]: 计算结果
        """
        if params is None:
            params = self.params

        if params.matching_method == "quarter_wave":
            calculator = QuarterWaveTransformer(
                freq=params.freq,
                z0=params.z0,
                zl=params.get_complex_load()
            )
        else:  # stub
            calculator = StubMatcher(
                freq=params.freq,
                z0=params.z0,
                zl=params.get_complex_load()
            )

        result = calculator.get_results()
        result["params"] = params.to_dict()
        return result

    def batch_calculate(self, param_list: List[CalculationParameters]) -> List[Dict[str, Any]]:
        """
        执行批量计算

        参数:
            param_list: List[CalculationParameters], 参数列表

        返回:
            List[Dict[str, Any]]: 计算结果列表
        """
        self.results = []
        for params in param_list:
            result = self.calculate(params)
            self.results.append(result)
            if self._is_better_result(result):
                self.best_result = result
        return self.results

    def _is_better_result(self, result: Dict[str, Any]) -> bool:
        """
        判断结果是否更优

        参数:
            result: Dict[str, Any], 计算结果

        返回:
            bool: 是否更优
        """
        if not self.best_result:
            return True

        if self.params.optimization_target == "vswr":
            return result["vswr"] < self.best_result["vswr"]
        else:  # length
            current_length = result["distance"] + result["stub_length"]
            best_length = self.best_result["distance"] + self.best_result["stub_length"]
            return current_length < best_length

    def optimize(self, param_ranges: Dict[str, Tuple[float, float]], num_points: int = 10) -> Dict[str, Any]:
        """
        执行参数优化

        参数:
            param_ranges: Dict[str, Tuple[float, float]], 参数范围
            num_points: int, 每个参数的采样点数

        返回:
            Dict[str, Any]: 最优结果
        """
        param_list = self._generate_param_combinations(param_ranges, num_points)
        self.batch_calculate(param_list)
        return self.best_result

    def _generate_param_combinations(self, param_ranges: Dict[str, Tuple[float, float]], 
                                  num_points: int) -> List[CalculationParameters]:
        """
        生成参数组合

        参数:
            param_ranges: Dict[str, Tuple[float, float]], 参数范围
            num_points: int, 每个参数的采样点数

        返回:
            List[CalculationParameters]: 参数组合列表
        """
        param_list = []
        base_params = self.params.to_dict()

        for param_name, (min_val, max_val) in param_ranges.items():
            values = np.linspace(min_val, max_val, num_points)
            for value in values:
                params_dict = base_params.copy()
                params_dict[param_name] = value
                param_list.append(CalculationParameters.from_dict(params_dict))

        return param_list

    def parameter_sweep(self, param_name: str, values: List[float]) -> List[Dict[str, Any]]:
        """
        执行参数扫描

        参数:
            param_name: str, 参数名称
            values: List[float], 参数值列表

        返回:
            List[Dict[str, Any]]: 计算结果列表
        """
        param_list = []
        base_params = self.params.to_dict()

        for value in values:
            params_dict = base_params.copy()
            params_dict[param_name] = value
            param_list.append(CalculationParameters.from_dict(params_dict))

        return self.batch_calculate(param_list)

    def get_best_result(self) -> Optional[Dict[str, Any]]:
        """
        获取最优结果

        返回:
            Optional[Dict[str, Any]]: 最优结果
        """
        return self.best_result

    def get_all_results(self) -> List[Dict[str, Any]]:
        """
        获取所有结果

        返回:
            List[Dict[str, Any]]: 所有计算结果
        """
        return self.results 