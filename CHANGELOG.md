# 更新日志

## [Unreleased]

### 依赖更新
- Python依赖更新：
  - numpy 2.2.1
  - scipy 1.14.1
  - matplotlib 3.10.0
  - pillow 11.0.0
  - pytest 8.3.4
  - maturin 1.8.1
  - setuptools_rust 1.10.2

- Rust依赖更新：
  - pyo3 0.21.0
  - iced 0.12.1
  - tokio 1.36.0
  - iced_wgpu 0.12.1
  - iced_winit 0.12.1

### 新增
- GUI模块测试用例
  - 应用初始化测试
  - 参数验证功能测试
  - 复数阻抗解析测试
  - 参数更新功能测试
  - 计算功能测试
  - 主题设置测试
  - 验证消息获取测试

- 帮助系统测试用例
  - 帮助系统初始化测试
  - 工具提示获取功能测试
  - 帮助内容获取功能测试
  - 工具提示内容格式测试
  - 帮助内容格式测试
  - 测试覆盖率达到 100%

### 修复
- 短截线匹配计算问题
  - 修正归一化导纳计算
  - 添加导纳计算异常处理
  - 改进支节长度计算
  - 修复VSWR计算中的反射系数边界检查
  - 处理完全反射情况

### 改进
- 代码健壮性
  - 添加无效参数检查
  - 添加计算错误处理
  - 添加边界条件检查
  - 改进数值计算稳定性
  - 处理除零错误
  - 添加无穷大值处理

### 测试覆盖率
- src/gui/main.py: 94%
- src/impedance_matching/stub_matching.py: 69%
- src/help/help_system.py: 100%
- src/visualization/result_saver.py: 16%
- 整体代码覆盖率: 54%

### 待办事项
1. 可视化模块测试
   - 为 result_saver.py 添加测试用例
   - 提高可视化模块代码覆盖率

2. 优化模块测试
   - 提高 optimization/calculator.py 测试覆盖率
   - 添加边界条件测试

3. 阻抗匹配模块测试
   - 提高 impedance_matching 模块测试覆盖率
   - 添加计算正确性测试

### 修复
- 修复iced库API变化导致的类型错误
  - 更新Size类型的使用方式
- 修复pyo3库API变化导致的警告
  - 更新模块绑定方式
  - 使用新的生命周期标注