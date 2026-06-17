"""
工作流引擎
自动化科研流程
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class StepStatus(Enum):
    """步骤状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowStep:
    """工作流步骤"""
    name: str
    skill: str
    params: Dict[str, Any] = field(default_factory=dict)
    condition: Optional[str] = None
    on_failure: str = "stop"  # stop, skip, continue
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: Optional[str] = None


@dataclass
class Workflow:
    """工作流定义"""
    name: str
    description: str
    steps: List[WorkflowStep]
    schedule: Optional[str] = None  # cron表达式
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    last_status: Optional[str] = None


class WorkflowEngine:
    """
    工作流引擎
    
    负责：
    - 工作流加载
    - 工作流执行
    - 进度追踪
    """
    
    def __init__(self, skill_manager, memory):
        self.skill_manager = skill_manager
        self.memory = memory
        self.workflows: Dict[str, Workflow] = {}
        
        # 加载预定义工作流
        self._load_workflows()
    
    def _load_workflows(self):
        """加载工作流"""
        # 内置工作流
        self._register_builtin_workflows()

        # 从文件加载
        workflows_dir = Path(__file__).parent.parent / "workflows"
        if workflows_dir.exists():
            for file in os.listdir(str(workflows_dir)):
                if file.endswith(".yaml") or file.endswith(".yml"):
                    self._load_workflow_file(str(workflows_dir / file))
    
    def _register_builtin_workflows(self):
        """注册内置工作流"""
        
        # 每日科研流程
        daily_workflow = Workflow(
            name="daily_research",
            description="每日科研流程",
            steps=[
                WorkflowStep(name="检查数据状态", skill="check_data"),
                WorkflowStep(name="质量检查", skill="quality_control"),
                WorkflowStep(name="更新记忆", skill="update_memory")
            ],
            schedule="0 9 * * *"  # 每天9点
        )
        self.workflows["daily_research"] = daily_workflow
        
        # 数据处理流程
        data_workflow = Workflow(
            name="data_pipeline",
            description="数据处理流程",
            steps=[
                WorkflowStep(name="下载数据", skill="download_era5"),
                WorkflowStep(name="质量控制", skill="quality_control"),
                WorkflowStep(name="特征工程", skill="compute_terrain")
            ]
        )
        self.workflows["data_pipeline"] = data_workflow
        
        # 模型训练流程
        train_workflow = Workflow(
            name="training_pipeline",
            description="模型训练流程",
            steps=[
                WorkflowStep(name="检查数据", skill="check_data"),
                WorkflowStep(name="训练模型", skill="train_model"),
                WorkflowStep(name="评估指标", skill="evaluate_metrics"),
                WorkflowStep(name="保存结果", skill="save_results")
            ]
        )
        self.workflows["training_pipeline"] = train_workflow
        
        # 完整科研流程
        full_workflow = Workflow(
            name="full_research",
            description="完整科研流程",
            steps=[
                WorkflowStep(name="数据处理", skill="check_data"),
                WorkflowStep(name="特征工程", skill="compute_terrain"),
                WorkflowStep(name="模型训练", skill="train_model"),
                WorkflowStep(name="模型评估", skill="evaluate_metrics"),
                WorkflowStep(name="可视化", skill="plot_forecast")
            ]
        )
        self.workflows["full_research"] = full_workflow
    
    def _load_workflow_file(self, filepath: str):
        """从文件加载工作流"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            steps = [
                WorkflowStep(
                    name=step.get('name', f"step_{i}"),
                    skill=step.get('skill', ''),
                    params=step.get('params', {}),
                    condition=step.get('condition')
                )
                for i, step in enumerate(data.get('steps', []))
            ]
            
            workflow = Workflow(
                name=data.get('name', 'unnamed'),
                description=data.get('description', ''),
                steps=steps,
                schedule=data.get('schedule')
            )
            
            self.workflows[workflow.name] = workflow
            
        except Exception as e:
            print(f"加载工作流失败: {filepath}, 错误: {e}")
    
    def list_workflows(self) -> List[str]:
        """列出所有工作流"""
        return list(self.workflows.keys())
    
    def get(self, name: str) -> Optional[Workflow]:
        """获取工作流"""
        return self.workflows.get(name)
    
    def run(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            name: 工作流名称
            **kwargs: 传递给步骤的参数
            
        Returns:
            执行结果
        """
        workflow = self.get(name)
        if not workflow:
            raise ValueError(f"工作流 '{name}' 不存在")
        
        print(f"\n🐉 执行工作流: {name}")
        print(f"   描述: {workflow.description}")
        print(f"   步骤数: {len(workflow.steps)}")
        print("-" * 50)
        
        results = {
            "workflow": name,
            "status": "running",
            "steps": [],
            "started_at": datetime.now().isoformat()
        }
        
        for i, step in enumerate(workflow.steps):
            print(f"\n[{i+1}/{len(workflow.steps)}] {step.name}")
            step.status = StepStatus.RUNNING
            
            try:
                # 检查条件
                if step.condition and not self._check_condition(step.condition, results):
                    print(f"   跳过 (条件不满足)")
                    step.status = StepStatus.SKIPPED
                    results["steps"].append({
                        "name": step.name,
                        "status": "skipped"
                    })
                    continue
                
                # 执行技能
                result = self.skill_manager.execute(step.skill, **step.params, **kwargs)
                
                step.status = StepStatus.COMPLETED
                step.result = result
                
                results["steps"].append({
                    "name": step.name,
                    "status": "completed",
                    "result": result
                })
                
            except Exception as e:
                step.status = StepStatus.FAILED
                step.error = str(e)
                
                results["steps"].append({
                    "name": step.name,
                    "status": "failed",
                    "error": str(e)
                })
                
                if step.on_failure == "stop":
                    results["status"] = "failed"
                    print(f"   失败: {e}")
                    print(f"\n工作流终止")
                    break
                elif step.on_failure == "skip":
                    print(f"   失败，跳过: {e}")
                    continue
                else:
                    print(f"   失败，继续: {e}")
                    continue
        
        # 更新工作流状态
        workflow.last_run = datetime.now()
        workflow.last_status = results["status"]
        
        # 保存到记忆
        self.memory.save({
            "type": "workflow_run",
            "workflow": name,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
        print("-" * 50)
        print(f"工作流完成: {results['status']}")
        
        results["completed_at"] = datetime.now().isoformat()
        return results
    
    def _check_condition(self, condition: str, results: dict) -> bool:
        """检查条件"""
        # TODO: 实现条件检查逻辑
        return True
    
    def create(self, name: str, steps: List[dict], 
               description: str = "", schedule: str = None) -> Workflow:
        """
        创建新工作流
        
        Args:
            name: 工作流名称
            steps: 步骤列表
            description: 描述
            schedule: 定时计划
            
        Returns:
            创建的工作流
        """
        workflow_steps = [
            WorkflowStep(
                name=step.get('name', f"step_{i}"),
                skill=step.get('skill', ''),
                params=step.get('params', {})
            )
            for i, step in enumerate(steps)
        ]
        
        workflow = Workflow(
            name=name,
            description=description,
            steps=workflow_steps,
            schedule=schedule
        )
        
        self.workflows[name] = workflow
        return workflow
    
    def save(self, name: str, filepath: str = None):
        """保存工作流到文件"""
        workflow = self.get(name)
        if not workflow:
            raise ValueError(f"工作流 '{name}' 不存在")
        
        data = {
            "name": workflow.name,
            "description": workflow.description,
            "schedule": workflow.schedule,
            "steps": [
                {
                    "name": step.name,
                    "skill": step.skill,
                    "params": step.params
                }
                for step in workflow.steps
            ]
        }
        
        filepath = filepath or f"workflows/{name}.yaml"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        print(f"工作流已保存: {filepath}")
