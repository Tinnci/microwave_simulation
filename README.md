# 微波电路仿真工具

基于Python和Rust开发的微波电路仿真工具，提供图形化界面进行电路设计和分析。

## 环境要求

- Python 3.12+
- Rust 1.76+
- uv 包管理器
- cargo 包管理器

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/microwave_simulation.git
cd microwave_simulation
```

2. 安装Python依赖：
```bash
uv pip install -r requirements.lock
```

3. 编译Rust组件：
```bash
cd gui_rust
cargo build --release
cd ..
```

## 使用说明

1. 启动应用：
```bash
python main.py
```

2. 在GUI界面中：
   - 选择电路类型
   - 输入参数
   - 点击"计算"按钮进行仿真
   - 查看结果图表

## 开发

1. 安装开发依赖：
```bash
uv pip install -r requirements-dev.txt
```

2. 运行测试：
```bash
pytest tests/
```

## 许可证

MIT License 