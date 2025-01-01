# 贡献指南

感谢您对微波阻抗匹配设计工具的关注！我们欢迎各种形式的贡献，包括但不限于：

- 报告问题
- 提交功能请求
- 提交代码修复
- 改进文档
- 添加测试用例

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/Tinnci/microwave_simulation.git
cd microwave_simulation
```

2. 创建虚拟环境并安装依赖：
```bash
uv venv
uv pip install -r requirements.txt
uv pip install .[dev]
```

3. 安装Rust工具链（如果需要修改GUI）：
   - 访问 https://rustup.rs/ 并按照说明安装

## 代码风格

- Python代码使用black格式化
- 使用ruff进行代码检查
- 使用mypy进行类型检查
- Rust代码使用rustfmt格式化

## 提交代码

1. 创建新分支：
```bash
git checkout -b feature/your-feature-name
```

2. 进行修改并提交：
```bash
git add .
git commit -m "feat: 添加新功能"
```

3. 推送到GitHub：
```bash
git push origin feature/your-feature-name
```

4. 创建Pull Request

## 提交信息规范

使用约定式提交规范：

- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式修改
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 测试

- 所有新代码都需要添加测试
- 运行测试：`pytest tests/`
- 检查覆盖率：`pytest --cov=src tests/`

## 文档

- 所有新功能都需要添加文档
- 更新API文档
- 添加使用示例

## 许可证

贡献的代码将使用MIT许可证。 