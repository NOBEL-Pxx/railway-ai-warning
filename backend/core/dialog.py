"""
对话管理器 - 项目任务导向
理解用户意图，返回项目相关建议
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import date
from enum import Enum


class Intent(Enum):
    """用户意图"""
    ASK_TODAY = "ask_today"           # 今天该做什么
    ASK_STATUS = "ask_status"         # 项目状态
    ASK_PHASE = "ask_phase"           # 当前阶段
    RUN_SKILL = "run_skill"           # 执行技能
    ASK_MEMORY = "ask_memory"         # 查询记忆
    RECORD_NOTE = "record_note"       # 记录笔记
    ASK_HELP = "ask_help"             # 帮助
    ASK_CODE = "ask_code"             # 查看代码
    UNKNOWN = "unknown"


class DialogManager:
    """
    对话管理器 - 项目任务导向
    
    理解用户关于项目的查询，返回相关建议
    """
    
    def __init__(self, skill_manager, workflow_engine, memory):
        self.skills = skill_manager
        self.workflow = workflow_engine
        self.memory = memory
        
        # 意图识别模式
        self.intent_patterns = {
            Intent.ASK_TODAY: [
                r"今天.*做",
                r"今日.*任务",
                r"接下来.*做",
                r"现在.*做",
                r"下一步",
                r"该做.*什么"
            ],
            Intent.ASK_STATUS: [
                r"项目.*状态",
                r"进度.*怎样",
                r"当前.*情况",
                r"状态$"
            ],
            Intent.ASK_PHASE: [
                r"当前.*阶段",
                r"什么阶段",
                r"阶段.*进度"
            ],
            Intent.RUN_SKILL: [
                r"帮我(.+)",
                r"执行(.+)",
                r"运行(.+)",
                r"开始(.+)",
                r"下载(.+)",
                r"训练(.+)",
                r"计算(.+)"
            ],
            Intent.ASK_MEMORY: [
                r"记得(.+)",
                r"上次(.+)",
                r"查询.*记忆",
                r"历史.*记录"
            ],
            Intent.RECORD_NOTE: [
                r"记录(.+)",
                r"记住(.+)",
                r"保存(.+)"
            ],
            Intent.ASK_CODE: [
                r"代码.*在哪",
                r"查看.*代码",
                r"代码.*位置"
            ],
            Intent.ASK_HELP: [
                r"帮助",
                r"help",
                r"怎么用",
                r"能做什么"
            ]
        }
    
    def process(self, user_input: str) -> str:
        """处理用户输入"""
        intent, entities = self._recognize_intent(user_input)
        response = self._generate_response(intent, entities, user_input)
        
        # 记录对话
        self.memory.save({
            "type": "dialog",
            "content": f"用户: {user_input}",
            "metadata": {"intent": intent.value},
            "tags": ["对话"]
        })
        
        return response
    
    def _recognize_intent(self, text: str) -> Tuple[Intent, Dict[str, Any]]:
        """识别意图"""
        text_lower = text.lower().strip()
        entities = {}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    if match.groups():
                        entities["target"] = match.group(1).strip()
                    return intent, entities
        
        return Intent.UNKNOWN, entities
    
    def _generate_response(self, intent: Intent, entities: Dict[str, Any],
                           original_input: str) -> str:
        """生成响应"""
        
        if intent == Intent.ASK_TODAY:
            return self._handle_ask_today()
        
        elif intent == Intent.ASK_STATUS:
            return self._handle_ask_status()
        
        elif intent == Intent.ASK_PHASE:
            return self._handle_ask_phase()
        
        elif intent == Intent.RUN_SKILL:
            target = entities.get("target", "")
            return self._handle_run_skill(target)
        
        elif intent == Intent.ASK_MEMORY:
            target = entities.get("target", original_input)
            return self._handle_ask_memory(target)
        
        elif intent == Intent.RECORD_NOTE:
            content = entities.get("target", "")
            return self._handle_record_note(content)
        
        elif intent == Intent.ASK_CODE:
            return self._handle_ask_code()
        
        elif intent == Intent.ASK_HELP:
            return self._handle_help()
        
        else:
            return self._handle_unknown(original_input)
    
    def _handle_ask_today(self) -> str:
        """处理'今天该做什么'"""
        today = date.today()
        
        # 获取Agent的任务建议
        from .agent import LoongClawAgent
        agent = LoongClawAgent(self, self.memory)
        task_info = agent.get_today_tasks()
        
        response = f"📅 {today.isoformat()}\n"
        response += f"📍 当前阶段: {task_info['phase']}"
        
        if task_info.get('progress'):
            response += f" ({task_info['progress']}%)"
        response += "\n\n"
        
        if task_info["tasks"]:
            response += "📋 今日任务:\n"
            for i, task in enumerate(task_info["tasks"], 1):
                response += f"  {i}. {task['name']}\n"
                if task.get('skill'):
                    response += f"     → dragon.run(\"{task['skill']}\")\n"
        else:
            response += "暂无待办任务\n"
        
        if task_info.get("tips"):
            response += "\n💡 提示:\n"
            for tip in task_info["tips"][:2]:
                response += f"  - {tip}\n"
        
        return response
    
    def _handle_ask_status(self) -> str:
        """处理项目状态查询"""
        from .agent import LoongClawAgent
        agent = LoongClawAgent(self, self.memory)
        
        overview = agent.get_phase_overview()
        memory_summary = self.memory.summary()
        
        response = "📊 项目状态\n\n"
        
        # 阶段进度
        response += "阶段进度:\n"
        for phase in overview:
            icon = {"completed": "✓", "in_progress": "▶", "pending": "○"}[phase["status"]]
            response += f"  {icon} {phase['name']}\n"
        
        # 统计信息
        response += f"\n记忆条目: {memory_summary['total']}\n"
        response += f"可用技能: {len(self.skills.list_skills())}\n"
        
        # 代码项目
        if self.skills.code_path:
            response += f"代码项目: {self.skills.code_path}\n"
        
        return response
    
    def _handle_ask_phase(self) -> str:
        """处理阶段查询"""
        from .agent import LoongClawAgent
        agent = LoongClawAgent(self, self.memory)
        
        current = agent.get_current_phase()
        next_milestone = agent.get_next_milestone()
        
        response = f"📍 当前阶段: {current['name']}\n"
        
        if current.get('progress'):
            response += f"   进度: {current['progress']}%\n"
            response += f"   结束: {current['end']}\n"
        
        if next_milestone['name'] != "无":
            response += f"\n🎯 下一里程碑: {next_milestone['name']}\n"
            response += f"   剩余: {next_milestone['days_remaining']} 天\n"
        
        return response
    
    def _handle_run_skill(self, target: str) -> str:
        """处理执行技能"""
        # 技能关键词映射
        skill_keywords = {
            "era5": "download-era5",
            "数据": "check-data",
            "地形": "compute-terrain",
            "训练": "train-model",
            "模型": "train-model",
            "评估": "evaluate-metrics",
            "风险": "risk-inference",
            "预报": "plot-forecast",
            "论文": "write-paper"
        }
        
        # 匹配技能
        matched_skill = None
        for keyword, skill_name in skill_keywords.items():
            if keyword in target:
                matched_skill = skill_name
                break
        
        if matched_skill:
            skill = self.skills.get(matched_skill)
            if skill:
                return f"找到技能: {skill.name}\n描述: {skill.description}\n\n执行: dragon.run(\"{skill.name}\")"
        
        # 搜索技能
        results = self.skills.search(target)
        if results:
            response = f"找到 {len(results)} 个相关技能:\n\n"
            for skill in results[:5]:
                response += f"  - {skill.name}: {skill.description}\n"
            return response
        
        return f"未找到匹配的技能: {target}\n\n使用 dragon.skills.list_skills() 查看所有技能"
    
    def _handle_ask_memory(self, query: str) -> str:
        """处理记忆查询"""
        entries = self.memory.search(query)
        
        if not entries:
            return f"未找到相关记忆: {query}"
        
        response = f"找到 {len(entries)} 条相关记忆:\n\n"
        for entry in entries[:5]:
            response += f"【{entry.type}】{entry.content[:80]}\n"
            response += f"  时间: {entry.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        
        return response
    
    def _handle_record_note(self, content: str) -> str:
        """处理记录笔记"""
        entry_id = self.memory.save({
            "type": "note",
            "content": content,
            "tags": ["笔记"]
        })
        return f"✓ 已记录 (ID: {entry_id})"
    
    def _handle_ask_code(self) -> str:
        """处理代码查询"""
        if self.skills.code_path:
            return f"""代码项目位置: {self.skills.code_path}

主要文件:
  - 模型: src/models/mamba_swin_unet.py
  - 训练: src/training/train.py
  - 数据: src/data/preprocess.py
  - 配置: configs/config.yaml

执行训练:
  cd {self.skills.code_path}
  python src/training/train.py
"""
        return "未关联代码项目"
    
    def _handle_help(self) -> str:
        """处理帮助"""
        return """
🐉 LoongClaw 帮助

对话示例:
  "今天该做什么？"     → 查看今日任务
  "项目状态"           → 查看项目进度
  "当前阶段"           → 查看阶段信息
  "帮我下载ERA5数据"   → 执行下载技能
  "训练模型"           → 执行训练技能
  "代码在哪"           → 查看代码位置

技能执行:
  dragon.run("train-model")
  dragon.run("download-era5")

记忆管理:
  dragon.remember("完成了数据清洗")
  dragon.recall("上次训练参数")

项目状态:
  dragon.status()
  dragon.today()
"""
    
    def _handle_unknown(self, text: str) -> str:
        """处理未知输入"""
        return f"不太理解: \"{text}\"\n\n试试说:\n  - \"今天该做什么？\"\n  - \"项目状态\"\n  - \"帮助\""
