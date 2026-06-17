"""
LoongClaw Agent 引擎
基于项目计划的智能任务规划
"""

import os
import yaml
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Task:
    """任务定义"""
    id: str
    name: str
    description: str = ""
    status: str = "pending"
    priority: str = "medium"
    skill: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)


class LoongClawAgent:
    """
    LoongClaw Agent 引擎
    
    基于项目计划书，智能规划每日任务
    """
    
    def __init__(self, dialog, memory):
        self.dialog = dialog
        self.memory = memory
        
        # 项目阶段定义（来自项目计划书）
        self.phases = [
            {
                "name": "数据治理与特征工程构建",
                "start": date(2026, 4, 1),
                "end": date(2026, 5, 31),
                "tasks": [
                    {"name": "铁路雨量数据脱敏接入与清洗", "skill": "quality-control"},
                    {"name": "缺失值智能插补算法开发", "skill": "quality-control"},
                    {"name": "地形强迫因子计算", "skill": "compute-terrain"},
                    {"name": "雷达回波特征提取", "skill": "feature-engineering"},
                    {"name": "基线模型验证", "skill": "train-model"}
                ],
                "tips": [
                    "ERA5数据下载需要CDS API密钥",
                    "地形特征计算可并行进行",
                    "先跑通基线模型验证流程"
                ]
            },
            {
                "name": "模型架构设计与训练迭代",
                "start": date(2026, 5, 1),
                "end": date(2026, 8, 31),
                "tasks": [
                    {"name": "MambaSwin-UNet-STA架构搭建", "skill": "train-model"},
                    {"name": "OpenClaw动态路由调度器开发", "skill": "train-model"},
                    {"name": "大规模GPU训练与超参数调优", "skill": "tune-hyperparams"},
                    {"name": "消融实验验证", "skill": "evaluate-metrics"}
                ],
                "tips": [
                    "先用小数据集验证模型可运行",
                    "注意保存训练checkpoint",
                    "记录每次实验的配置和结果"
                ]
            },
            {
                "name": "风险推演模块耦合与系统集成",
                "start": date(2026, 8, 1),
                "end": date(2026, 11, 30),
                "tasks": [
                    {"name": "SCS-CN水文模型集成", "skill": "risk-inference"},
                    {"name": "风险推演插件开发", "skill": "risk-inference"},
                    {"name": "系统集成与接口设计", "skill": "train-model"},
                    {"name": "端到端流程测试", "skill": "evaluate-metrics"}
                ],
                "tips": [
                    "确保各模块接口一致",
                    "编写单元测试"
                ]
            },
            {
                "name": "典型个例回溯验证与实地调研",
                "start": date(2026, 12, 1),
                "end": date(2027, 1, 31),
                "tasks": [
                    {"name": "22·7甘肃暴雨个例验证", "skill": "evaluate-metrics"},
                    {"name": "25·8榆中山洪个例验证", "skill": "evaluate-metrics"},
                    {"name": "兰州铁路局实地调研", "skill": "generate-report"},
                    {"name": "一线专家可用性评估", "skill": "evaluate-metrics"}
                ],
                "tips": [
                    "选择典型个例详细分析",
                    "对比不同方法优劣"
                ]
            },
            {
                "name": "成果总结、论文撰写与结题验收",
                "start": date(2027, 2, 1),
                "end": date(2027, 4, 30),
                "tasks": [
                    {"name": "代码库整理与开源", "skill": "generate-report"},
                    {"name": "技术验证报告撰写", "skill": "generate-report"},
                    {"name": "核心期刊论文撰写", "skill": "write-paper"},
                    {"name": "结题答辩准备", "skill": "generate-report"}
                ],
                "tips": [
                    "提前准备答辩材料",
                    "整理代码准备开源"
                ]
            }
        ]
        
        # 加载项目配置
        self._load_project_config()
    
    def _load_project_config(self):
        """加载项目配置"""
        config_path = Path(__file__).parent.parent / "configs" / "project.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}
    
    def get_current_phase(self) -> dict:
        """获取当前阶段"""
        today = date.today()
        
        for phase in self.phases:
            if phase["start"] <= today <= phase["end"]:
                return {
                    "name": phase["name"],
                    "start": phase["start"].isoformat(),
                    "end": phase["end"].isoformat(),
                    "progress": self._calculate_progress(phase, today)
                }
        
        # 如果不在任何阶段，返回最近的阶段
        if today < self.phases[0]["start"]:
            return {"name": "项目尚未开始", "start": "", "end": "", "progress": 0}
        else:
            return {"name": "项目已结束", "start": "", "end": "", "progress": 100}
    
    def _calculate_progress(self, phase: dict, today: date) -> int:
        """计算阶段进度"""
        total_days = (phase["end"] - phase["start"]).days
        elapsed_days = (today - phase["start"]).days
        progress = int(elapsed_days / total_days * 100)
        return max(0, min(100, progress))
    
    def get_today_tasks(self) -> dict:
        """
        获取今日任务
        
        Returns:
            今日任务信息
        """
        today = date.today()
        current_phase = self.get_current_phase()
        
        # 找到当前阶段定义
        phase_def = None
        for phase in self.phases:
            if phase["name"] == current_phase["name"]:
                phase_def = phase
                break
        
        if not phase_def:
            return {
                "date": today.isoformat(),
                "phase": current_phase["name"],
                "tasks": [],
                "tips": []
            }
        
        # 生成任务列表
        tasks = []
        for i, task in enumerate(phase_def["tasks"]):
            tasks.append({
                "id": f"task_{i+1}",
                "name": task["name"],
                "skill": task.get("skill"),
                "status": "pending"
            })
        
        return {
            "date": today.isoformat(),
            "phase": current_phase["name"],
            "progress": current_phase.get("progress", 0),
            "tasks": tasks,
            "tips": phase_def.get("tips", [])
        }
    
    def get_phase_overview(self) -> List[dict]:
        """获取所有阶段概览"""
        today = date.today()
        
        overview = []
        for phase in self.phases:
            status = "pending"
            if phase["end"] < today:
                status = "completed"
            elif phase["start"] <= today <= phase["end"]:
                status = "in_progress"
            
            overview.append({
                "name": phase["name"],
                "start": phase["start"].isoformat(),
                "end": phase["end"].isoformat(),
                "status": status,
                "task_count": len(phase["tasks"])
            })
        
        return overview
    
    def get_next_milestone(self) -> dict:
        """获取下一个里程碑"""
        today = date.today()
        
        for phase in self.phases:
            if phase["start"] > today:
                return {
                    "name": phase["name"],
                    "date": phase["start"].isoformat(),
                    "days_remaining": (phase["start"] - today).days
                }
        
        return {"name": "无", "date": "", "days_remaining": 0}
    
    def suggest_next_task(self) -> dict:
        """建议下一个任务"""
        today_tasks = self.get_today_tasks()
        
        if today_tasks["tasks"]:
            # 找到第一个未完成的任务
            for task in today_tasks["tasks"]:
                if task["status"] == "pending":
                    return task
        
        return {"name": "所有任务已完成", "skill": None}
