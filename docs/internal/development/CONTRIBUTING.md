# 贡献指南

## 开发环境设置

1. 安装必要工具：
   - Python 3.12+
   - Rust 1.76+
   - uv包管理器
   - cargo包管理器
   - Git

2. 克隆仓库：
```bash
git clone https://github.com/yourusername/microwave_simulation.git
cd microwave_simulation
```

3. 安装开发依赖：
```bash
uv pip install -r requirements-dev.txt
```

4. 编译Rust组件：
```bash
cd gui_rust
cargo build
cd ..
```

## 代码规范

### Python代码规范
- 使用black进行代码格式化
- 使用flake8进行代码检查
- 使用mypy进行类型检查
- 使用pytest进行单元测试

### Rust代码规范
- 使用rustfmt进行代码格式化
- 使用clippy进行代码检查
- 使用cargo test进行单元测试

## 提交规范

1. 创建分支：
```bash
git checkout -b feature/your-feature
```

2. 提交代码：
```bash
git add .
git commit -m "feat: add new feature"
```

3. 推送分支：
```bash
git push origin feature/your-feature
```

4. 创建Pull Request

## 版本发布

1. 更新版本号：
   - 修改setup.py
   - 修改Cargo.toml
   - 更新CHANGELOG.md

2. 创建标签：
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## 文档维护

1. 更新API文档：
   - 使用docstrings记录Python函数
   - 使用rustdoc记录Rust函数
   - 保持文档与代码同步

2. 更新用户指南：
   - 添加新功能说明
   - 更新安装说明
   - 添加使用示例

## 测试

1. 运行Python测试：
```bash
pytest tests/
```

2. 运行Rust测试：
```bash
cd gui_rust
cargo test
cd ..
```

3. 运行集成测试：
```bash
pytest tests/integration/
```

## 问题反馈

- 使用GitHub Issues报告问题
- 提供详细的复现步骤
- 附上相关的日志信息
- 标注问题的严重程度

## 许可证

贡献的代码将使用MIT许可证。 