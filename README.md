# 微波阻抗匹配设计工具

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 项目概述

本项目是一个用于微波阻抗匹配设计的工具软件，提供直观的图形界面和强大的计算功能，帮助工程师快速完成阻抗匹配设计。

## 主要功能

- 复数阻抗输入支持
- 多种匹配方法选择
- 实时参数验证
- 史密斯圆图可视化
- 优化计算支持
- 批量参数扫描
- 结果导出功能

## 安装说明

### 系统要求
- Python 3.12 或更高版本
- Windows 10/11
- Rust工具链（可选，仅用于开发）

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/Tinnci/microwave_simulation.git
cd microwave_simulation
```

2. 使用 uv 安装依赖：
```bash
uv venv
uv pip install -r requirements.txt
```

3. 安装开发依赖（可选）：
```bash
uv pip install -r requirements.txt[dev]
```

## 快速开始

1. 启动程序：
```bash
python src/gui/main.py
```

2. 在界面中输入参数：
   - 工作频率
   - 特征阻抗
   - 负载阻抗（复数形式）

3. 选择匹配方法

4. 点击计算按钮获取结果

## 项目文档

- [项目结构说明](docs/internal/PROJECT_STRUCTURE.md)
- [快速入门指南](docs/guides/quickstart.md)
- [理论基础](docs/guides/theory.md)
- [分析方法](docs/guides/analysis.md)
- [API文档](docs/api/README.md)
- [示例](docs/examples/README.md)
- [开发指南](docs/internal/development/CONTRIBUTING.md)

## 贡献

欢迎贡献代码！请阅读[贡献指南](docs/internal/development/CONTRIBUTING.md)了解如何参与项目开发。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 