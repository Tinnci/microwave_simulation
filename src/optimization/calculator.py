"""优化计算模块"""
import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any, cast, TypedDict, NotRequired
from src.impedance_matching.core import (
    QuarterWaveTransformer,
    StubMatcher,
    LMatcher,
    PiMatcher,
    TMatcher
)

class CalculationParametersDict(TypedDict):
    """计算参数字典类型"""
    freq: Union[float, str]
    z0: Union[float, str]
    z_load_real: Union[float, str]
    z_load_imag: Union[float, str]
    matching_method: str
    optimization_target: str
    weight_factors: NotRequired[Dict[str, float]]

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
        if matching_method not in ["quarter_wave", "stub", "L", "Pi", "T"]:
            raise ValueError("匹配方法必须是 quarter_wave, stub, L, Pi 或 T")
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

    def to_dict(self) -> CalculationParametersDict:
        """
        转换为字典

        返回:
            CalculationParametersDict: 参数字典
        """
        return {
            "freq": str(self.freq),
            "z0": str(self.z0),
            "z_load_real": str(self.z_load_real),
            "z_load_imag": str(self.z_load_imag),
            "matching_method": self.matching_method,
            "optimization_target": self.optimization_target,
            "weight_factors": self.weight_factors
        }

    @classmethod
    def from_dict(cls, data: CalculationParametersDict) -> 'CalculationParameters':
        """
        从字典创建参数对象

        参数:
            data: CalculationParametersDict, 参数字典

        返回:
            CalculationParameters: 参数对象
        """
        # 确保数值类型的字段被转换为浮点数
        freq = float(data["freq"]) if isinstance(data["freq"], (str, float)) else 0.0
        z0 = float(data["z0"]) if isinstance(data["z0"], (str, float)) else 0.0
        z_load_real = float(data["z_load_real"]) if isinstance(data["z_load_real"], (str, float)) else 0.0
        z_load_imag = float(data["z_load_imag"]) if isinstance(data["z_load_imag"], (str, float)) else 0.0

        return cls(
            freq=freq,
            z0=z0,
            z_load_real=z_load_real,
            z_load_imag=z_load_imag,
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
        self.results: List[Dict[str, Any]] = []
        self.best_result: Optional[Dict[str, Any]] = None

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
                frequency=params.freq,
                z0=params.z0,
                zl=params.get_complex_load()
            )
        else:  # stub
            calculator = StubMatcher(
                frequency=params.freq,
                z0=params.z0,
                zl=params.get_complex_load()
            )

        result = calculator.calculate()
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
        if self.best_result is None:
            return {}  # 返回空字典作为默认结果
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
                params_dict[param_name] = float(value)
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

def calculate_matching(frequency: float, z0: float, zl: complex):
    """
    计算阻抗匹配网络参数
    
    Args:
        frequency: 工作频率 (Hz)
        z0: 特征阻抗 (Ω)
        zl: 负载阻抗 (复数)
        
    Returns:
        dict: 包含匹配网络参数和性能指标的字典
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive")
    if z0 <= 0:
        raise ValueError("Characteristic impedance must be positive")
        
    # 创建不同类型的匹配网络
    networks = {
        "quarter_wave": QuarterWaveTransformer(frequency, z0, zl),
        "stub": StubMatcher(frequency, z0, zl),
        "l_network": LMatcher(frequency, z0, zl),
        "pi_network": PiMatcher(frequency, z0, zl),
        "t_network": TMatcher(frequency, z0, zl)
    }
    
    # 计算每种网络的性能
    results = {}
    best_vswr = float('inf')
    best_network = None
    
    for name, network in networks.items():
        result = network.calculate()
        vswr = calculate_vswr(result["s_parameters"][0, 0])
        
        if vswr < best_vswr:
            best_vswr = vswr
            best_network = name
            
        results[name] = {
            "parameters": result,
            "vswr": vswr
        }
    
    # 返回最佳匹配网络和性能指标
    return {
        "matching_network": {
            "type": best_network,
            "parameters": results[best_network]["parameters"]
        },
        "performance_metrics": {
            "vswr": best_vswr,
            "return_loss": calculate_return_loss(results[best_network]["parameters"]["s_parameters"][0, 0]),
            "bandwidth": calculate_bandwidth(frequency, results[best_network]["parameters"]["s_parameters"])
        }
    }

def calculate_vswr(s11):
    """计算电压驻波比"""
    reflection_coefficient = abs(s11)
    if reflection_coefficient >= 1:
        return float('inf')
    return (1 + reflection_coefficient) / (1 - reflection_coefficient)

def calculate_return_loss(s11):
    """计算回波损耗 (dB)"""
    return -20 * np.log10(abs(s11))

def calculate_bandwidth(frequency, s_parameters):
    """计算带宽 (相对带宽)"""
    # 简化的带宽计算,实际应该考虑VSWR<2的频率范围
    return 0.2  # 示例值,返回20%带宽 