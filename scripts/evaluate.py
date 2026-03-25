#!/usr/bin/env python3
"""
Skill Evaluator — 评估和提升其他 Skill 的能力

用法:
    python evaluate.py --skill-path /path/to/skill --output reports/
    python evaluate.py --skill-path /path/to/skill --output reports/ --verbose
    python evaluate.py --skill-path /path/to/skill --output reports/ --format json
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml
from loguru import logger

# 配置日志
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")


def parse_args():
    parser = argparse.ArgumentParser(description="Skill Evaluator — 评估 Skill 能力")
    parser.add_argument("--skill-path", type=str, required=True, help="要评估的 Skill 路径")
    parser.add_argument("--output", type=str, default="reports/", help="输出目录")
    parser.add_argument("--verbose", action="store_true", help="输出详细日志")
    parser.add_argument("--format", type=str, choices=["markdown", "json"], default="markdown", help="输出格式")
    parser.add_argument("--red-team", action="store_true", help="运行红队测试")
    return parser.parse_args()


def check_skill_structure(skill_path: str) -> dict:
    """检查 Skill 目录结构"""
    result = {
        "has_skill_md": False,
        "has_scripts": False,
        "has_evals": False,
        "has_tests": False,
        "has_readme": False,
    }
    
    skill_dir = Path(skill_path)
    
    if (skill_dir / "SKILL.md").exists():
        result["has_skill_md"] = True
    
    if (skill_dir / "scripts").exists():
        result["has_scripts"] = True
    
    if (skill_dir / "evals").exists() or (skill_dir / "tests").exists():
        result["has_evals"] = True
    
    if (skill_dir / "tests").exists():
        result["has_tests"] = True
    
    if (skill_dir / "README.md").exists():
        result["has_readme"] = True
    
    return result


def parse_skill_md(skill_path: str) -> dict:
    """解析 SKILL.md 文件"""
    skill_file = Path(skill_path) / "SKILL.md"
    
    if not skill_file.exists():
        return {}
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单的 YAML frontmatter 解析
    skill_info = {}
    lines = content.split('\n')
    in_frontmatter = False
    frontmatter_lines = []
    
    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
                try:
                    skill_info = yaml.safe_load('\n'.join(frontmatter_lines))
                except:
                    pass
                break
        elif in_frontmatter:
            frontmatter_lines.append(line)
    
    return skill_info


def run_promptfoo_eval(skill_path: str, eval_config: str) -> dict:
    """运行 Promptfoo 评估"""
    try:
        result = subprocess.run(
            ["promptfoo", "eval", "-c", eval_config, "--output", "json"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            logger.warning(f"Promptfoo 评估失败：{result.stderr}")
            return {}
    except subprocess.TimeoutExpired:
        logger.error("Promptfoo 评估超时")
        return {}
    except Exception as e:
        logger.error(f"Promptfoo 评估错误：{e}")
        return {}


def calculate_skill_level(structure: dict, eval_result: dict) -> str:
    """计算 Skill 能力等级"""
    # 安全获取字典值，避免 KeyError
    has_skill_md = structure.get("has_skill_md", False)
    has_scripts = structure.get("has_scripts", False)
    has_evals = structure.get("has_evals", False)
    has_tests = structure.get("has_tests", False)
    has_readme = structure.get("has_readme", False)
    
    # Level 3: 生产就绪
    if (has_skill_md and has_scripts and has_evals and has_tests and has_readme):
        return "Level 3"
    
    # Level 2: 稳定可靠
    if (has_skill_md and has_scripts and has_evals):
        return "Level 2"
    
    # Level 1: 基础可用
    if has_skill_md:
        return "Level 1"
    
    return "未评级"


def generate_markdown_report(skill_info: dict, structure: dict, eval_result: dict, timestamp: str) -> str:
    """生成 Markdown 格式报告"""
    skill_level = calculate_skill_level(structure, eval_result)
    
    # 安全获取字典值
    check_mark = lambda key: '✅' if structure.get(key, False) else '❌'
    
    report = f"""# Skill 评估报告

**评估时间**: {timestamp}

---

## Skill 信息

| 字段 | 值 |
|------|-----|
| 名称 | {skill_info.get('name', 'N/A')} |
| 版本 | {skill_info.get('version', 'N/A')} |
| 描述 | {skill_info.get('description', 'N/A')} |
| 作者 | {skill_info.get('author', 'N/A')} |
| 标签 | {', '.join(skill_info.get('tags', []))} |

---

## 能力等级：**{skill_level}**

---

## 目录结构检查

| 检查项 | 状态 |
|--------|------|
| SKILL.md | {check_mark('has_skill_md')} |
| scripts/ | {check_mark('has_scripts')} |
| evals/ | {check_mark('has_evals')} |
| tests/ | {check_mark('has_tests')} |
| README.md | {check_mark('has_readme')} |

---

## 评估结果

{json.dumps(eval_result, ensure_ascii=False, indent=2) if eval_result else '暂无评估数据'}

---

## 改进建议

"""
    
    # 根据检查结果生成建议
    suggestions = []
    
    if not structure.get("has_skill_md", False):
        suggestions.append("1. **【高优先级】** 添加 SKILL.md 文件，定义 Skill 职责和工作流程")
    
    if not structure.get("has_scripts", False):
        suggestions.append("2. **【高优先级】** 添加 scripts/ 目录，实现 Skill 核心功能")
    
    if not structure.get("has_evals", False):
        suggestions.append("3. **【中优先级】** 添加 evals/ 目录，配置基准测试")
    
    if not structure.get("has_tests", False):
        suggestions.append("4. **【中优先级】** 添加 tests/ 目录，编写测试用例")
    
    if not structure.get("has_readme", False):
        suggestions.append("5. **【低优先级】** 添加 README.md 文件，完善使用说明")
    
    if suggestions:
        report += "\n".join(suggestions)
    else:
        report += "✅ Skill 结构完整，无需改进"
    
    return report


def generate_report(skill_path: str, structure: dict, skill_info: dict, eval_result: dict, output_dir: str, output_format: str):
    """生成评估报告"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    skill_name = skill_info.get("name", "unknown-skill")
    
    if output_format == "json":
        report_file = Path(output_dir) / f"{skill_name}-eval-{timestamp}.json"
        report = {
            "skill_info": skill_info,
            "structure": structure,
            "eval_result": eval_result,
            "skill_level": calculate_skill_level(structure, eval_result),
            "timestamp": timestamp,
        }
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    else:
        report_file = Path(output_dir) / f"{skill_name}-eval-{timestamp}.md"
        report = generate_markdown_report(skill_info, structure, eval_result, timestamp)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
    
    logger.info(f"评估报告已保存到：{report_file}")
    return report_file


def main():
    args = parse_args()
    
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
    
    logger.info(f"开始评估 Skill: {args.skill_path}")
    
    # 检查 Skill 结构
    logger.info("检查 Skill 目录结构...")
    structure = check_skill_structure(args.skill_path)
    logger.info(f"结构检查结果：{structure}")
    
    # 解析 SKILL.md
    logger.info("解析 SKILL.md...")
    skill_info = parse_skill_md(args.skill_path)
    logger.info(f"Skill 信息：{skill_info}")
    
    # 运行 Promptfoo 评估
    eval_config = str(Path(args.skill_path) / "evals" / "skill-eval-config.yaml")
    if os.path.exists(eval_config):
        logger.info("运行 Promptfoo 评估...")
        eval_result = run_promptfoo_eval(args.skill_path, eval_config)
    else:
        logger.warning(f"未找到评估配置：{eval_config}")
        eval_result = {}
    
    # 生成报告
    logger.info("生成评估报告...")
    report_file = generate_report(args.skill_path, structure, skill_info, eval_result, args.output, args.format)
    
    logger.info(f"评估完成！报告：{report_file}")


if __name__ == "__main__":
    main()
