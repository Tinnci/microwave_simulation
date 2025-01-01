# 测试规范

本文档详细说明了微波阻抗匹配设计工具的测试规范和流程。

## 测试环境

### 1. 测试工具

1. 测试框架
   - pytest：主要测试框架
   - unittest：标准库测试框架
   - pytest-cov：测试覆盖率工具

2. 辅助工具
   - mock：模拟对象
   - pytest-benchmark：性能测试
   - pytest-xdist：并行测试

### 2. 环境配置

1. 安装测试依赖
```bash
uv pip install pytest pytest-cov pytest-benchmark pytest-xdist
```

2. 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/unit/test_quarter_wave.py

# 运行带覆盖率报告的测试
pytest --cov=src tests/
```

## 测试类型

### 1. 单元测试

1. 测试范围
   - 类方法测试
   - 函数测试
   - 边界条件测试

2. 测试示例
```python
def test_calculate_transformer_impedance():
    """测试变换器特征阻抗计算"""
    transformer = QuarterWaveTransformer(50, 100, 5e9)
    z1 = transformer.calculate_transformer_impedance()
    assert abs(z1 - 70.71) < 0.01

def test_invalid_input():
    """测试无效输入处理"""
    with pytest.raises(ValueError):
        QuarterWaveTransformer(-50, 100, 5e9)
```

### 2. 集成测试

1. 测试范围
   - 模块间交互
   - 完整功能流程
   - 性能测试

2. 测试示例
```python
def test_matching_workflow():
    """测试完整匹配流程"""
    # 设置参数
    z0 = 50
    zl = 25 + 75j
    freq = 5e9
    
    # 创建匹配器
    matcher = StubMatcher(z0, zl, freq)
    
    # 计算参数
    d, l = matcher.calculate_stub_parameters()
    
    # 验证结果
    assert d > 0
    assert l > 0
    
    # 获取网络参数
    network = matcher.get_network((freq*0.8, freq*1.2, 201))
    assert len(network.f) == 201
```

## 测试规范

### 1. 命名规范

1. 测试文件
   - 单元测试：`test_*.py`
   - 集成测试：`test_integration_*.py`
   - 性能测试：`test_perf_*.py`

2. 测试函数
   - 功能测试：`test_function_name`
   - 异常测试：`test_invalid_*`
   - 边界测试：`test_boundary_*`

### 2. 测试结构

1. 测试类组织
```python
class TestQuarterWaveTransformer:
    """四分之一波长变换器测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.z0 = 50
        self.zl = 100
        self.freq = 5e9
        self.transformer = QuarterWaveTransformer(self.z0, self.zl, self.freq)
    
    def test_impedance_calculation(self):
        """测试阻抗计算"""
        pass
    
    def test_wavelength_calculation(self):
        """测试波长计算"""
        pass
```

2. 测试夹具
```python
@pytest.fixture
def sample_network():
    """创建示例网络对象"""
    z0 = 50
    zl = 25 + 75j
    freq = 5e9
    transformer = QuarterWaveTransformer(z0, zl, freq)
    return transformer.get_network((freq*0.8, freq*1.2, 201))
```

## 测试覆盖率

### 1. 覆盖率要求

1. 最低要求
   - 语句覆盖率：90%
   - 分支覆盖率：85%
   - 函数覆盖率：95%

2. 关键模块
   - 阻抗计算：100%
   - 参数验证：100%
   - 异常处理：100%

### 2. 覆盖率报告

1. 生成报告
```bash
pytest --cov=src --cov-report=html tests/
```

2. 报告分析
   - 查看未覆盖代码
   - 识别测试盲点
   - 优化测试用例

## 性能测试

### 1. 基准测试

1. 测试指标
   - 计算时间
   - 内存使用
   - CPU使用率

2. 测试示例
```python
def test_performance(benchmark):
    """性能基准测试"""
    def calc_params():
        transformer = QuarterWaveTransformer(50, 100, 5e9)
        return transformer.calculate_transformer_impedance()
    
    result = benchmark(calc_params)
    assert abs(result - 70.71) < 0.01
```

### 2. 负载测试

1. 测试场景
   - 大规模数据
   - 并发计算
   - 长时间运行

2. 测试指标
   - 响应时间
   - 资源占用
   - 稳定性

## 测试报告

### 1. 报告内容

1. 基本信息
   - 测试时间
   - 测试环境
   - 测试版本

2. 测试结果
   - 通过/失败数
   - 覆盖率数据
   - 性能指标

### 2. 报告格式

1. HTML报告
```bash
pytest --html=report.html tests/
```

2. XML报告
```bash
pytest --junitxml=report.xml tests/
``` 