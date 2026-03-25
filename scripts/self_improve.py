#!/usr/bin/env python3
"""
Skill Evaluator 自主改进循环 - 借鉴 Karpathy Loop

用法:
    python self_improve.py --skill-path /path/to/skill --metric accuracy --max-iterations 100
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

# 配置日志
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")


def parse_args():
    parser = argparse.ArgumentParser(description="Skill Evaluator 自主改进循环")
    parser.add_argument("--skill-path", type=str, required=True, help="要改进的 Skill 路径")
    parser.add_argument("--metric", type=str, default="accuracy", choices=["accuracy", "reliability", "efficiency", "cost", "coverage"], help="优化指标")
    parser.add_argument("--max-iterations", type=int, default=100, help="最大迭代次数")
    parser.add_argument("--early-stop", type=int, default=10, help="无改进早期停止的迭代次数")
    parser.add_argument("--output", type=str, default="reports/", help="输出目录")
    parser.add_argument("--verbose", action="store_true", help="输出详细日志")
    return parser.parse_args()


def propose_small_change(skill_path: str) -> dict:
    """
    提出小改动（不破坏性变更）
    
    改动类型:
    1. 优化 prompt 措辞
    2. 调整错误处理逻辑
    3. 添加边界条件检查
    4. 优化资源限制
    """
    import random
    
    change_types = [
        "optimize_prompt",
        "improve_error_handling",
        "add_boundary_check",
        "optimize_resource_limit",
    ]
    
    change_type = random.choice(change_types)
    
    # 这里只是示例，实际实现应该根据 Skill 类型智能提出改动
    change = {
        "type": change_type,
        "timestamp": datetime.now().isoformat(),
        "description": f"Proposed {change_type} change",
    }
    
    logger.info(f"提出改动：{change_type}")
    return change


def backup_skill(skill_path: str) -> str:
    """备份 Skill"""
    backup_path = f"{skill_path}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copytree(skill_path, backup_path)
    return backup_path


def revert_change(skill_path: str, backup_path: str):
    """回滚改动"""
    logger.info(f"回滚改动，恢复到 {backup_path}")
    shutil.rmtree(skill_path)
    shutil.copytree(backup_path, skill_path)


def commit_change(skill_path: str, change: dict):
    """提交改动"""
    logger.info(f"提交改动：{change['type']}")
    # 实际实现应该调用 git commit
    # subprocess.run(["git", "add", "-A"], cwd=skill_path, check=True)
    # subprocess.run(["git", "commit", "-m", f"Auto-improve: {change['type']}"], cwd=skill_path, check=True)


def evaluate_skill(skill_path: str, metric: str) -> float:
    """
    评估 Skill
    
    返回指定指标的得分（0-1）
    """
    # 实际实现应该调用 skill-evaluator
    # result = subprocess.run(
    #     ["python", "scripts/evaluate.py", "--skill-path", skill_path, "--output", "reports/"],
    #     capture_output=True,
    #     text=True,
    #     check=True
    # )
    
    # 这里只是示例
    import random
    score = random.uniform(0.7, 0.95)
    
    logger.info(f"评估结果：{metric} = {score:.2%}")
    return score


def no_improvement_for_n_iterations(history: list, n: int) -> bool:
    """检查是否连续 n 次无改进"""
    if len(history) < n:
        return False
    
    recent = history[-n:]
    best_so_far = max(history[:-n]) if history[:-n] else 0
    
    return all(score <= best_so_far for score in recent)


def calculate_trend(history: list) -> str:
    """计算改进趋势"""
    if len(history) < 5:
        return "insufficient_data"
    
    recent = history[-5:]
    older = history[-10:-5] if len(history) >= 10 else history[:5]
    
    recent_avg = sum(recent) / len(recent)
    older_avg = sum(older) / len(older)
    
    if recent_avg > older_avg * 1.05:  # 5% 提升
        return "improving"
    elif recent_avg < older_avg * 0.95:  # 5% 下降
        return "declining"
    else:
        return "stable"


def generate_suggestions(history: list, trend: str) -> list:
    """生成改进建议"""
    suggestions = []
    
    if trend == "improving":
        suggestions.append("✅ 当前改进方向正确，继续")
    elif trend == "stable":
        suggestions.append("⚠️ 改进停滞，考虑调整策略")
        suggestions.append("尝试更大的改动幅度")
        suggestions.append("检查评估指标是否合理")
    elif trend == "declining":
        suggestions.append("❌ 性能下降，建议回滚到最佳版本")
        suggestions.append("检查是否有破坏性变更")
    
    return suggestions


def self_improve_loop(skill_path: str, metric: str, max_iterations: int, early_stop: int, output_dir: str):
    """
    自主改进循环 - 借鉴 Karpathy Loop
    
    流程:
    1. 修改 Skill 代码（小改动）
    2. 运行评估
    3. 保留或回滚
    4. 重复直到收敛或达到最大迭代次数
    """
    logger.info(f"开始自主改进循环：{skill_path}")
    logger.info(f"优化指标：{metric}, 最大迭代：{max_iterations}, 早期停止：{early_stop}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 备份 Skill
    backup_path = backup_skill(skill_path)
    logger.info(f"已备份 Skill 到：{backup_path}")
    
    # 初始评估
    best_score = evaluate_skill(skill_path, metric)
    logger.info(f"初始得分：{best_score:.2%}")
    
    history = [best_score]
    no_improvement_count = 0
    
    # 改进循环
    for i in range(max_iterations):
        logger.info(f"\n{'='*50}")
        logger.info(f"迭代 {i+1}/{max_iterations}")
        logger.info(f"当前最佳：{best_score:.2%}, 无改进计数：{no_improvement_count}/{early_stop}")
        
        # 1. 提出代码修改（小改动，避免破坏性变更）
        change = propose_small_change(skill_path)
        
        # 2. 运行评估
        score = evaluate_skill(skill_path, metric)
        
        # 3. 保留或回滚
        if score > best_score:
            best_score = score
            commit_change(skill_path, change)
            logger.info(f"✅ 迭代{i+1}: 改进到 {score:.2%}")
            no_improvement_count = 0
        else:
            revert_change(skill_path, backup_path)
            logger.info(f"❌ 迭代{i+1}: 无改进 ({score:.2%})")
            no_improvement_count += 1
        
        history.append(score)
        
        # 4. 早期停止
        if no_improvement_count >= early_stop:
            logger.info(f"\n{early_stop}次无改进，早期停止")
            break
        
        # 5. 检查趋势
        trend = calculate_trend(history)
        if trend == "declining":
            logger.warning("⚠️ 性能下降趋势，建议检查")
            suggestions = generate_suggestions(history, trend)
            for suggestion in suggestions:
                logger.info(f"  {suggestion}")
    
    # 生成报告
    report = {
        "skill_path": skill_path,
        "metric": metric,
        "initial_score": history[0],
        "final_score": best_score,
        "improvement": best_score - history[0],
        "improvement_rate": (best_score - history[0]) / history[0] if history[0] > 0 else 0,
        "total_iterations": len(history) - 1,
        "history": history,
        "trend": calculate_trend(history),
        "timestamp": datetime.now().isoformat(),
    }
    
    # 保存报告
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = Path(output_dir) / f"self-improve-report-{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n{'='*50}")
    logger.info(f"自主改进完成！")
    logger.info(f"初始得分：{history[0]:.2%}")
    logger.info(f"最终得分：{best_score:.2%}")
    logger.info(f"改进幅度：{report['improvement_rate']:.2%}")
    logger.info(f"迭代次数：{report['total_iterations']}")
    logger.info(f"改进趋势：{report['trend']}")
    logger.info(f"报告已保存到：{report_file}")
    
    # 清理备份
    shutil.rmtree(backup_path)
    logger.info(f"已清理备份：{backup_path}")
    
    return report


def main():
    args = parse_args()
    
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
    
    report = self_improve_loop(
        skill_path=args.skill_path,
        metric=args.metric,
        max_iterations=args.max_iterations,
        early_stop=args.early_stop,
        output_dir=args.output,
    )
    
    logger.info(f"\n自主改进循环完成！")


if __name__ == "__main__":
    main()
