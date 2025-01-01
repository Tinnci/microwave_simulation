# API 文档

## 核心模块

### 阻抗匹配模块 (`src.impedance_matching`)

#### QuarterWaveTransformer

四分之一波长变换器类。

```python
class QuarterWaveTransformer:
    def __init__(self, frequency: float, z0: float, zl: complex):
        """
        初始化四分之一波长变换器。

        Args:
            frequency: 工作频率（Hz）
            z0: 特征阻抗（Ω）
            zl: 负载阻抗（Ω）
        """
        pass

    def calculate(self) -> Dict[str, Any]:
        """
        计算变换器参数。

        Returns:
            Dict[str, Any]: 包含以下键值对：
                - z1: 变换器特征阻抗
                - length: 变换器长度
                - vswr: 电压驻波比
                - s_parameters: S参数
        """
        pass
```

#### StubMatcher

单枝节匹配器类。

```python
class StubMatcher:
    def __init__(self, frequency: float, z0: float, zl: complex):
        """
        初始化单枝节匹配器。

        Args:
            frequency: 工作频率（Hz）
            z0: 特征阻抗（Ω）
            zl: 负载阻抗（Ω）
        """
        pass

    def calculate(self) -> Dict[str, Any]:
        """
        计算匹配器参数。

        Returns:
            Dict[str, Any]: 包含以下键值对：
                - distance: 支节到负载距离
                - stub_length: 支节长度
                - s_parameters: S参数
        """
        pass
```

### 优化模块 (`src.optimization`)

#### BatchCalculator

批量计算类。

```python
class BatchCalculator:
    def __init__(self, matcher: Union[QuarterWaveTransformer, StubMatcher]):
        """
        初始化批量计算器。

        Args:
            matcher: 匹配器实例
        """
        pass

    def parameter_sweep(self, parameter: str, start: float, stop: float, steps: int) -> Dict[str, Any]:
        """
        执行参数扫描。

        Args:
            parameter: 要扫描的参数名
            start: 起始值
            stop: 终止值
            steps: 步数

        Returns:
            Dict[str, Any]: 扫描结果
        """
        pass

    def optimize(self, target_function: Callable, bounds: List[Tuple[float, float]]) -> Dict[str, Any]:
        """
        执行优化计算。

        Args:
            target_function: 目标函数
            bounds: 参数边界

        Returns:
            Dict[str, Any]: 优化结果
        """
        pass
```

### 可视化模块 (`src.visualization`)

#### ResultSaver

结果保存类。

```python
class ResultSaver:
    def __init__(self, base_path: str = "results"):
        """
        初始化结果保存器。

        Args:
            base_path: 基础保存路径
        """
        pass

    def save_network_data(self, network: Any, filename: str) -> None:
        """
        保存网络数据。

        Args:
            network: 网络对象
            filename: 文件名
        """
        pass

    def save_plots(self, network: Any, filename: str) -> None:
        """
        保存图形。

        Args:
            network: 网络对象
            filename: 文件名
        """
        pass

    def save_optimization_results(self, results: Dict[str, Any], filename: str) -> None:
        """
        保存优化结果。

        Args:
            results: 优化结果
            filename: 文件名
        """
        pass
```

### 帮助系统模块 (`src.help`)

#### HelpSystem

帮助系统类。

```python
class HelpSystem:
    def __init__(self):
        """初始化帮助系统。"""
        pass

    def get_topic_help(self, topic: str) -> str:
        """
        获取主题帮助。

        Args:
            topic: 主题名称

        Returns:
            str: 帮助内容
        """
        pass

    def get_parameter_help(self, parameter: str) -> str:
        """
        获取参数帮助。

        Args:
            parameter: 参数名称

        Returns:
            str: 帮助内容
        """
        pass
```

### GUI模块 (`src.gui`)

#### MicrowaveDesignApp

主应用类。

```python
class MicrowaveDesignApp:
    def __init__(self):
        """初始化应用。"""
        pass

    def run(self) -> None:
        """运行应用。"""
        pass

    def calculate(self) -> None:
        """执行计算。"""
        pass

    def save_results(self) -> None:
        """保存结果。"""
        pass
```

## 工具函数

### 网络分析 (`src.utils.network`)

```python
def calculate_vswr(s11: complex) -> float:
    """
    计算VSWR。

    Args:
        s11: 反射系数

    Returns:
        float: VSWR值
    """
    pass

def calculate_impedance(s_parameters: np.ndarray, z0: float) -> np.ndarray:
    """
    计算阻抗。

    Args:
        s_parameters: S参数矩阵
        z0: 参考阻抗

    Returns:
        np.ndarray: 阻抗矩阵
    """
    pass
```

### 数据处理 (`src.utils.data`)

```python
def save_to_csv(data: Dict[str, Any], filename: str) -> None:
    """
    保存数据到CSV文件。

    Args:
        data: 要保存的数据
        filename: 文件名
    """
    pass

def load_from_csv(filename: str) -> Dict[str, Any]:
    """
    从CSV文件加载数据。

    Args:
        filename: 文件名

    Returns:
        Dict[str, Any]: 加载的数据
    """
    pass
```

## 异常类

### 参数异常

```python
class ParameterError(Exception):
    """参数错误异常。"""
    pass
```

### 计算异常

```python
class CalculationError(Exception):
    """计算错误异常。"""
    pass
```

### 保存异常

```python
class SaveError(Exception):
    """保存错误异常。"""
    pass
```

## 常量定义

### 物理常量

```python
SPEED_OF_LIGHT = 299792458  # 光速（m/s）
EPSILON_0 = 8.854e-12      # 真空介电常数
MU_0 = 1.257e-6           # 真空磁导率
```

### 默认参数

```python
DEFAULT_FREQUENCY = 1e9    # 默认频率（1 GHz）
DEFAULT_Z0 = 50.0         # 默认特征阻抗
DEFAULT_STEPS = 101       # 默认步数
```

## 配置选项

### 全局配置

```python
CONFIG = {
    'save_path': 'results',
    'plot_dpi': 300,
    'csv_delimiter': ',',
    'decimal_places': 3
}
```

### 优化配置

```python
OPTIMIZATION_CONFIG = {
    'max_iterations': 1000,
    'tolerance': 1e-6,
    'population_size': 50,
    'mutation_rate': 0.1
}
``` 