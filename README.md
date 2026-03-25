# Skill Evaluator — Skill 评估与提升专家

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill Level: Level 3](https://img.shields.io/badge/Skill%20Level-Level%203-green)](https://github.com/openclaw/skill-evaluator)
[![Promptfoo Eval](https://img.shields.io/badge/Promptfoo-Eval%20Ready-blue)](https://github.com/promptfoo/promptfoo)

**评估和提升其他 Skill 的能力，提供基准测试、红队测试和改进建议。**

---

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/openclaw/skill-evaluator.git
cd skill-evaluator

# 安装依赖
pip install -r requirements.txt

# 验证安装
python scripts/evaluate.py --help
```

### 使用

#### 评估单个 Skill

```bash
# 评估一个 Skill
python scripts/evaluate.py --skill-path /path/to/skill --output reports/

# 评估并生成详细报告
python scripts/evaluate.py --skill-path /path/to/skill --output reports/ --verbose

# 评估并导出 JSON 格式
python scripts/evaluate.py --skill-path /path/to/skill --output reports/ --format json
```

#### 对比多个 Skill

```bash
# 对比多个 Skill
python scripts/compare.py --skills /path/to/skill1 /path/to/skill2 --output reports/
```

#### 运行基准测试

```bash
# 运行 Promptfoo 评估
promptfoo eval -c evals/skill-eval-config.yaml

# 运行红队测试
python scripts/red_team.py --skill-path /path/to/skill
```

---

## 功能特性

### 1. 能力等级评估

自动判定 Skill 的能力等级：

| 等级 | 名称 | 标准 |
|------|------|------|
| **Level 1** | 基础可用 | ✅ 能完成核心任务<br>✅ 有基本错误处理<br>⚠️ 测试覆盖率 < 50% |
| **Level 2** | 稳定可靠 | ✅ 能完成核心任务<br>✅ 有完整的错误处理<br>✅ 测试覆盖率 > 80%<br>✅ 有基准测试 |
| **Level 3** | 生产就绪 | ✅ 能完成核心任务<br>✅ 有完整的错误处理<br>✅ 测试覆盖率 > 95%<br>✅ 有基准测试和红队测试<br>✅ 有用户反馈循环<br>✅ 有版本管理和迭代记录 |

### 2. 六维度评估

| 维度 | 权重 | 评估指标 |
|------|------|---------|
| **准确性** | 25% | 任务完成率 |
| **可靠性** | 20% | 错误率 |
| **效率** | 20% | 平均执行时间 |
| **成本** | 15% | 平均 Token 消耗 |
| **覆盖率** | 10% | 测试用例通过率 |
| **安全性** | 10% | 红队测试通过率 |

### 3. 红队测试

内置红队测试用例：
- SQL 注入测试
- 提示词注入测试
- 资源限制测试
- 恶意输入测试
- 边界条件测试

### 4. 改进建议

根据评估结果生成改进建议：
- 代码质量改进
- 测试覆盖率提升
- 性能优化建议
- 安全加固建议
- 文档完善建议

---

## 评估报告示例

```markdown
# Skill 评估报告

## Skill 信息
- 名称：csv-summarizer
- 版本：1.2.0
- 作者：John Doe

## 能力等级：Level 2（稳定可靠）

## 各维度得分
| 维度 | 得分 | 目标值 | 状态 |
|------|------|--------|------|
| 准确性 | 92% | > 90% | ✅ |
| 可靠性 | 88% | > 95% | ⚠️ |
| 效率 | 95% | < 30 秒 | ✅ |
| 成本 | 90% | < $0.50 | ✅ |
| 覆盖率 | 75% | > 95% | ❌ |
| 安全性 | 85% | > 90% | ⚠️ |

## 发现的问题
1. 测试覆盖率不足（75% < 95%）
2. 错误处理不完整（可靠性 88%）
3. 红队测试有 2 个用例未通过

## 改进建议
1. 【高优先级】添加边界条件测试用例
2. 【高优先级】完善错误处理逻辑
3. 【中优先级】优化 Token 使用效率
4. 【低优先级】添加更多使用示例

## 测试详情
- 总测试用例：20
- 通过：17
- 失败：3
- 执行时间：45 秒
- Token 消耗：$0.35
```

---

## 目录结构

```
skill-evaluator/
├── SKILL.md                 # Skill 定义文件
├── README.md                # 使用说明
├── requirements.txt         # Python 依赖
├── scripts/
│   ├── evaluate.py          # 评估主脚本
│   ├── compare.py           # 对比脚本
│   ├── red_team.py          # 红队测试脚本
│   └── report_generator.py  # 报告生成脚本
├── evals/
│   ├── skill-eval-config.yaml  # Promptfoo 评估配置
│   └── test-cases.yaml         # 测试用例库
├── tests/
│   ├── test_normal.py       # 正常场景测试
│   ├── test_edge_cases.py   # 边界场景测试
│   └── test_security.py     # 安全测试
├── red_team/
│   └── adversarial_tests.py # 对抗性测试
├── .feedback/               # 评估报告输出目录
├── .github/
│   └── workflows/
│       └── eval.yml         # CI/CD 评估工作流
└── reports/                 # 评估报告缓存
```

---

## CI/CD 集成

Skill Evaluator 支持 GitHub Actions 自动评估：

```yaml
# .github/workflows/eval.yml
name: Skill Evaluation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          npm install -g promptfoo
      
      - name: Run Skill Evaluation
        run: |
          python scripts/evaluate.py --skill-path ./ --output reports/
      
      - name: Run Promptfoo Eval
        run: |
          promptfoo eval -c evals/skill-eval-config.yaml
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: skill-eval-report
          path: reports/
```

---

## 贡献指南

欢迎贡献！请参考以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 相关链接

- [Skill 开发最佳实践](https://github.com/openclaw/skill-evaluator/blob/main/docs/skill-development-best-practices.md)
- [Promptfoo 评估指南](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/)
- [OpenAI Eval Skills](https://developers.openai.com/blog/eval-skills/)
- [ClawHub Skill 市场](https://clawhub.com)

---

## 维护者

- OpenClaw Team <team@openclaw.ai>

---

*最后更新：2026-03-25*
