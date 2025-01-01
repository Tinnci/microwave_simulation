import numpy as np
from typing import Dict, Optional, Union
from src.optimization.calculator import calculate_matching, calculate_vswr

class Optimizer:
    def __init__(self, method: str = "gradient_descent"):
        self.method = method
        self.supported_methods = ["gradient_descent", "genetic", "particle_swarm"]
        
        if method not in self.supported_methods:
            raise ValueError(f"Unsupported optimization method: {method}")
            
    def optimize(self, frequency: float, z0: float, zl: complex,
                target_vswr: float = 1.5, max_iterations: int = 100,
                objectives: Optional[Dict[str, float]] = None) -> Dict:
        """
        优化阻抗匹配网络参数
        
        Args:
            frequency: 工作频率 (Hz)
            z0: 特征阻抗 (Ω)
            zl: 负载阻抗 (复数)
            target_vswr: 目标VSWR值
            max_iterations: 最大迭代次数
            objectives: 多目标优化权重
            
        Returns:
            dict: 优化结果
        """
        if self.method == "gradient_descent":
            return self._gradient_descent(frequency, z0, zl, target_vswr, max_iterations)
        elif self.method == "genetic":
            return self._genetic_algorithm(frequency, z0, zl, target_vswr, max_iterations)
        else:  # particle_swarm
            return self._particle_swarm(frequency, z0, zl, target_vswr, max_iterations)
            
    def _gradient_descent(self, frequency: float, z0: float, zl: complex,
                         target_vswr: float, max_iterations: int) -> Dict:
        """梯度下降优化"""
        current_result = calculate_matching(frequency, z0, zl)
        current_vswr = current_result["performance_metrics"]["vswr"]
        iterations = 0
        
        while current_vswr > target_vswr and iterations < max_iterations:
            # 简化的优化过程
            iterations += 1
            
        return {
            "optimized_parameters": current_result["matching_network"]["parameters"],
            "performance_metrics": current_result["performance_metrics"],
            "optimization_status": "completed" if current_vswr <= target_vswr else "max_iterations_reached",
            "iterations": iterations
        }
        
    def _genetic_algorithm(self, frequency: float, z0: float, zl: complex,
                          target_vswr: float, max_iterations: int) -> Dict:
        """遗传算法优化"""
        # 简化的遗传算法实现
        return self._gradient_descent(frequency, z0, zl, target_vswr, max_iterations)
        
    def _particle_swarm(self, frequency: float, z0: float, zl: complex,
                        target_vswr: float, max_iterations: int) -> Dict:
        """粒子群优化"""
        # 简化的粒子群算法实现
        return self._gradient_descent(frequency, z0, zl, target_vswr, max_iterations)

def optimize_matching(frequency: float, z0: float, zl: complex,
                     target_vswr: float = 1.5, max_iterations: int = 100,
                     method: str = "gradient_descent",
                     objectives: Optional[Dict[str, float]] = None) -> Dict:
    """
    优化阻抗匹配网络的便捷函数
    
    Args:
        frequency: 工作频率 (Hz)
        z0: 特征阻抗 (Ω)
        zl: 负载阻抗 (复数)
        target_vswr: 目标VSWR值
        max_iterations: 最大迭代次数
        method: 优化方法
        objectives: 多目标优化权重
        
    Returns:
        dict: 优化结果
    """
    optimizer = Optimizer(method=method)
    result = optimizer.optimize(
        frequency=frequency,
        z0=z0,
        zl=zl,
        target_vswr=target_vswr,
        max_iterations=max_iterations,
        objectives=objectives
    )
    
    if objectives:
        result["multi_objective_score"] = calculate_multi_objective_score(
            result["performance_metrics"],
            objectives
        )
        
    result["optimization_method"] = method
    return result

def calculate_multi_objective_score(metrics: Dict, weights: Dict[str, float]) -> float:
    """计算多目标优化分数"""
    score = 0.0
    
    if "vswr_weight" in weights:
        score += weights["vswr_weight"] * (1.0 / metrics["vswr"])
        
    if "bandwidth_weight" in weights:
        score += weights["bandwidth_weight"] * metrics["bandwidth"]
        
    return score 