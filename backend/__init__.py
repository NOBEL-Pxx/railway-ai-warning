"""
LoongClaw - 气象AI科研助手
基于项目计划的智能任务规划与执行框架

使用方法:
    from loongclaw import Dragon

    dragon = Dragon()
    dragon.chat("今天该做什么？")
    dragon.run("train-model")
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from core.agent import LoongClawAgent
from core.skills import SkillManager
from core.workflow import WorkflowEngine
from core.memory import MemorySystem
from core.dialog import DialogManager


class Dragon:
    """
    LoongClaw 主入口类

    提供统一的交互接口:
    - chat(): 对话交互
    - run(): 执行技能
    - status(): 查看状态
    - today(): 今日任务
    - remember(): 记录记忆
    - recall(): 检索记忆
    """

    def __init__(self,
                 project_path: str = None,
                 name: str = "LoongClaw"):
        """
        初始化 LoongClaw

        Args:
            project_path: 项目路径 (默认使用脚本所在目录)
            name: 助手名称
        """
        self.name = name

        # 项目路径：默认使用脚本所在目录（合并后只有一个项目）
        self.project_path = Path(project_path).resolve() if project_path else PROJECT_ROOT

        # 初始化组件
        self._init_components()

        # 打印欢迎信息
        self._welcome()
    
    def _init_components(self):
        """初始化组件"""
        # 记忆系统
        self.memory = MemorySystem(str(self.project_path))

        # 技能管理器（合并后代码在项目内 src/ 目录）
        self.skills = SkillManager(project_path=str(self.project_path))

        # 工作流引擎
        self.workflow = WorkflowEngine(self.skills, self.memory)

        # 对话管理器
        self.dialog = DialogManager(self.skills, self.workflow, self.memory)

        # Agent
        self.agent = LoongClawAgent(self.dialog, self.memory)

    def _welcome(self):
        """打印欢迎信息"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🐉 LoongClaw - 气象AI科研助手                              ║
║                                                              ║
║   项目: 气候暖湿化背景下铁路沿线小流域短临降水智能预测        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

        # 显示当前状态
        phase = self.agent.get_current_phase()
        print(f"📍 当前阶段: {phase['name']}")

        print(f"📁 项目路径: {self.project_path}")
        print(f"💾 记忆条目: {self.memory.count()}")
        print(f"🔧 可用技能: {len(self.skills.list_skills())}")
        print()
    
    def chat(self, message: str) -> str:
        """
        对话交互
        
        Args:
            message: 用户消息
            
        Returns:
            助手响应
        """
        return self.dialog.process(message)
    
    def run(self, skill_name: str, **kwargs) -> Any:
        """
        执行技能
        
        Args:
            skill_name: 技能名称
            **kwargs: 技能参数
            
        Returns:
            执行结果
        """
        return self.skills.execute(skill_name, **kwargs)
    
    def status(self) -> Dict[str, Any]:
        """
        获取项目状态

        Returns:
            状态信息
        """
        phase = self.agent.get_current_phase()
        overview = self.agent.get_phase_overview()
        memory_summary = self.memory.summary()

        return {
            "current_phase": phase,
            "phases": overview,
            "memory": memory_summary,
            "skills_count": len(self.skills.list_skills()),
            "project_path": str(self.project_path)
        }
    
    def today(self) -> Dict[str, Any]:
        """
        获取今日任务
        
        Returns:
            今日任务信息
        """
        return self.agent.get_today_tasks()
    
    def remember(self, content: str, 
                 entry_type: str = "note",
                 tags: List[str] = None,
                 importance: int = 1) -> str:
        """
        记录记忆
        
        Args:
            content: 内容
            entry_type: 类型 (task, experiment, note, lesson, decision)
            tags: 标签
            importance: 重要性 (1-5)
            
        Returns:
            记忆ID
        """
        return self.memory.save({
            "type": entry_type,
            "content": content,
            "tags": tags or [],
            "importance": importance
        })
    
    def recall(self, query: str, limit: int = 10) -> List:
        """
        检索记忆
        
        Args:
            query: 查询字符串
            limit: 返回数量
            
        Returns:
            匹配的记忆列表
        """
        return self.memory.search(query, limit)
    
    def run_workflow(self, workflow_name: str, **kwargs) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            workflow_name: 工作流名称
            **kwargs: 参数
            
        Returns:
            执行结果
        """
        return self.workflow.run(workflow_name, **kwargs)
    
    def list_skills(self, category: str = None) -> List:
        """
        列出技能
        
        Args:
            category: 类别过滤
            
        Returns:
            技能列表
        """
        return self.skills.list_skills(category)
    
    def list_workflows(self) -> List[str]:
        """列出工作流"""
        return self.workflow.list_workflows()
    
    def suggest_next_task(self) -> Dict[str, Any]:
        """建议下一个任务"""
        return self.agent.suggest_next_task()
    
    def daily_summary(self) -> str:
        """生成每日总结"""
        return self.memory.daily_summary()
    
    def __repr__(self):
        return f"<Dragon: {self.name}>"


def create_dragon(project_path: str = None) -> Dragon:
    """
    创建 Dragon 实例的便捷函数

    Args:
        project_path: 项目路径（默认使用当前目录）

    Returns:
        Dragon 实例
    """
    return Dragon(project_path=project_path)


# 命令行入口
def main():
    """命令行交互模式"""
    import argparse

    parser = argparse.ArgumentParser(description='LoongClaw 气象AI科研助手')
    parser.add_argument('--project', type=str, help='项目路径（默认当前目录）')
    parser.add_argument('--cmd', type=str, help='直接执行命令')
    args = parser.parse_args()

    # 创建实例
    dragon = Dragon(project_path=args.project)
    
    if args.cmd:
        # 直接执行命令
        print(dragon.chat(args.cmd))
        return
    
    # 交互模式
    print("\n输入消息开始对话，输入 'quit' 退出\n")
    
    while True:
        try:
            user_input = input("你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n再见! 🐉")
                break
            
            if not user_input:
                continue
            
            response = dragon.chat(user_input)
            print(f"\n🐉 {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n再见! 🐉")
            break
        except Exception as e:
            print(f"\n错误: {e}\n")


if __name__ == "__main__":
    main()
