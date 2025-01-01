"""结果保存模块"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from typing import Any, Dict, List, Optional, Union
from matplotlib import font_manager

class ResultSaver:
    """结果保存器类"""
    def __init__(self, save_dir: str = "results"):
        """
        初始化结果保存器

        参数:
            save_dir: str, 保存目录
        """
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

        # 设置字体
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    def save_network_data(self, network: Any, save_path: str) -> None:
        """
        保存网络数据

        参数:
            network: Any, 网络对象
            save_path: str, 保存路径
        """
        # 检查网络对象类型
        if not hasattr(network, "s_parameters") or not hasattr(network, "vswr"):
            raise ValueError("网络参数未计算")
            
        # 验证网络参数值的有效性
        if not hasattr(network, "reflection_coefficient") or \
           not hasattr(network, "input_impedance") or \
           not hasattr(network, "frequency"):
            raise ValueError("网络参数不完整")
            
        # 验证参数值的范围
        if not np.all(np.isfinite(network.s_parameters)):
            raise ValueError("S参数包含无效值")
            
        if network.vswr < 1.0:
            raise ValueError("VSWR必须大于等于1")
            
        if not np.isfinite(network.reflection_coefficient) or \
           abs(network.reflection_coefficient) > 1.0:
            raise ValueError("反射系数无效")
            
        if not np.isfinite(network.input_impedance.real) or \
           network.input_impedance.real <= 0:
            raise ValueError("输入阻抗实部必须为正数")
            
        if not np.isfinite(network.frequency) or network.frequency <= 0:
            raise ValueError("频率必须为正数")
            
        # 创建保存目录
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir, exist_ok=True)
            except OSError:
                raise OSError("创建保存目录失败")
                
        try:
            # 保存 S 参数数据
            s_data = np.array([
                network.s_parameters[0].real,  # S11 实部
                network.s_parameters[0].imag,  # S11 虚部
                network.vswr,
                network.reflection_coefficient.real,
                network.reflection_coefficient.imag,
                network.input_impedance.real,
                network.input_impedance.imag,
                network.frequency
            ])
            np.save(f"{save_path}_s_parameters.npy", s_data)
        except Exception as e:
            raise OSError(f"保存网络数据失败: {str(e)}")

    def save_plots(self, network: Any, save_path: str) -> None:
        """
        保存图表

        参数:
            network: Any, 网络对象
            save_path: str, 保存路径
        """
        # 检查网络对象类型
        if not hasattr(network, "s_parameters") or not hasattr(network, "vswr"):
            raise ValueError("网络参数未计算")

        # 检查保存路径
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except OSError as e:
                raise OSError(f"创建保存目录失败: {str(e)}")

        try:
            # 绘制S参数图
            plt.figure(figsize=(10, 6))
            s_params = np.array(network.s_parameters)
            plt.plot(abs(s_params[0]), label="S11")
            plt.plot(abs(s_params[1]), label="S12")
            plt.plot(abs(s_params[2]), label="S21")
            plt.plot(abs(s_params[3]), label="S22")
            plt.xlabel("频率点")
            plt.ylabel("幅度 (dB)")
            plt.title("S参数")
            plt.legend()
            plt.grid(True)
            plt.savefig(f"{save_path}_s_parameters.png")
            plt.close()

            # 绘制驻波比图
            plt.figure(figsize=(10, 6))
            plt.plot([network.vswr])
            plt.xlabel("频率点")
            plt.ylabel("VSWR")
            plt.title("驻波比")
            plt.grid(True)
            plt.savefig(f"{save_path}_vswr.png")
            plt.close()
        except (OSError, ValueError) as e:
            raise OSError(f"保存图表失败: {str(e)}")

    def save_optimization_results(self, results: List[Dict[str, float]], save_path: str) -> None:
        """
        保存优化结果

        参数:
            results: List[Dict[str, float]], 优化结果列表
            save_path: str, 保存路径
        """
        # 检查保存路径
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except OSError as e:
                raise OSError(f"创建保存目录失败: {str(e)}")

        try:
            # 保存优化结果
            with open(f"{save_path}_optimization.csv", "w") as f:
                # 写入表头
                headers = list(results[0].keys())
                f.write(",".join(headers) + "\n")

                # 写入数据
                for result in results:
                    values = [str(result[header]) for header in headers]
                    f.write(",".join(values) + "\n")
        except (OSError, ValueError) as e:
            raise OSError(f"保存优化结果失败: {str(e)}")

    def save_parameter_sweep(self, sweep_results: List[Dict[str, float]], save_path: str,
                           param_name: str) -> None:
        """
        保存参数扫描结果

        参数:
            sweep_results: List[Dict[str, float]], 扫描结果列表
            save_path: str, 保存路径
            param_name: str, 扫描参数名
        """
        # 检查保存路径
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except OSError as e:
                raise OSError(f"创建保存目录失败: {str(e)}")

        try:
            # 提取扫描参数值和对应的结果
            param_values = [result[param_name] for result in sweep_results]
            result_values = [result["优化目标值"] for result in sweep_results]

            # 绘制扫描结果图
            plt.figure(figsize=(10, 6))
            plt.plot(param_values, result_values)
            plt.xlabel(param_name)
            plt.ylabel("优化目标值")
            plt.title(f"{param_name}参数扫描结果")
            plt.grid(True)
            plt.savefig(f"{save_path}_sweep_{param_name}.png")
            plt.close()

            # 保存扫描数据
            np.savetxt(f"{save_path}_sweep_{param_name}.csv",
                      np.column_stack((param_values, result_values)),
                      delimiter=",", header=f"{param_name},优化目标值",
                      comments="")
        except (OSError, ValueError) as e:
            raise OSError(f"保存参数扫描结果失败: {str(e)}")

    def save_all_results(self, network: Any, save_path: str) -> None:
        """
        保存所有结果

        参数:
            network: Any, 网络对象
            save_path: str, 保存路径
        """
        # 检查网络对象类型
        if not hasattr(network, "s_parameters") or not hasattr(network, "vswr"):
            raise ValueError("网络参数未计算")
            
        try:
            self.save_network_data(network, save_path)
            self.save_plots(network, save_path)
        except OSError as e:
            raise OSError(f"保存所有结果失败: {str(e)}") 