# 贡献指南

感谢您对电商数据分析系统的关注！我们欢迎任何形式的贡献，包括但不限于：

- 代码贡献
- 文档改进
- Bug报告
- 功能建议

## 开发流程

1. Fork 项目到您的GitHub账号
2. 克隆项目到本地
```bash
git clone https://github.com/your-username/ecommerce-analysis.git
cd ecommerce-analysis
```

3. 创建新的分支
```bash
git checkout -b feature/your-feature-name
```

4. 进行开发和测试
- 遵循代码规范
- 添加必要的测试
- 确保所有测试通过

5. 提交变更
```bash
git add .
git commit -m "feat: add your feature description"
```

6. 推送到GitHub
```bash
git push origin feature/your-feature-name
```

7. 创建Pull Request

## 代码规范

1. Python代码规范
- 遵循PEP 8规范
- 使用类型注解
- 编写详细的文档字符串
- 变量和函数使用有意义的名称

2. Git提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

3. 文档规范
- 保持文档的及时更新
- 使用清晰的语言
- 提供必要的示例

## 开发环境设置

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置开发环境
- 复制config.yaml.example为config.yaml
- 修改必要的配置项

3. 运行测试
```bash
python -m pytest
```

## 提交Pull Request前的检查清单

- [ ] 代码符合规范
- [ ] 添加了必要的测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 提交信息符合规范

## 问题反馈

如果您发现了bug或有新的功能建议，请：

1. 检查是否已存在相关的Issue
2. 创建新的Issue，并提供：
   - 问题的详细描述
   - 复现步骤（如果是bug）
   - 预期行为
   - 实际行为
   - 系统环境信息

## 联系方式

如有任何问题，请通过以下方式联系我们：

- 提交Issue
- 发送邮件至：[项目维护者邮箱]

感谢您的贡献！ 