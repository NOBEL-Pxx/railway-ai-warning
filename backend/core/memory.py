"""
记忆系统
记录科研进展、实验结果、经验教训
"""

import os
import json
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
import hashlib


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    type: str  # task, experiment, note, lesson, decision
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    importance: int = 1  # 1-5, 5最重要


class MemorySystem:
    """
    记忆系统
    
    负责：
    - 记录科研进展
    - 存储实验结果
    - 保存经验教训
    - 智能检索
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.memory_dir = os.path.join(project_path, "memory")
        self.entries: Dict[str, MemoryEntry] = {}
        
        # 确保目录存在
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # 加载已有记忆
        self._load_memories()
    
    def _load_memories(self):
        """加载已有记忆"""
        # 加载每日记忆
        today = date.today()
        daily_file = os.path.join(self.memory_dir, f"{today.isoformat()}.json")
        
        if os.path.exists(daily_file):
            with open(daily_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry_data in data.get("entries", []):
                    entry = MemoryEntry(**entry_data)
                    self.entries[entry.id] = entry
        
        # 加载长期记忆
        longterm_file = os.path.join(self.memory_dir, "MEMORY.json")
        if os.path.exists(longterm_file):
            with open(longterm_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry_data in data.get("entries", []):
                    entry = MemoryEntry(**entry_data)
                    self.entries[entry.id] = entry
    
    def save(self, data: Dict[str, Any]) -> str:
        """
        保存记忆
        
        Args:
            data: 记忆数据，包含 type, content, metadata 等
            
        Returns:
            记忆ID
        """
        # 生成ID
        content_str = json.dumps(data, sort_keys=True)
        entry_id = hashlib.md5((content_str + datetime.now().isoformat()).encode()).hexdigest()[:8]
        
        # 创建条目
        entry = MemoryEntry(
            id=entry_id,
            type=data.get("type", "note"),
            content=data.get("content", ""),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            importance=data.get("importance", 1)
        )
        
        self.entries[entry_id] = entry
        
        # 保存到文件
        self._save_to_file(entry)
        
        print(f"💾 记忆已保存: [{entry.type}] {entry.content[:50]}...")
        
        return entry_id
    
    def _save_to_file(self, entry: MemoryEntry):
        """保存到文件"""
        today = date.today()
        
        if entry.importance >= 4:
            # 重要记忆保存到长期记忆
            filepath = os.path.join(self.memory_dir, "MEMORY.json")
        else:
            # 普通记忆保存到每日记忆
            filepath = os.path.join(self.memory_dir, f"{today.isoformat()}.json")
        
        # 读取现有数据
        data = {"entries": []}
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # 添加新条目
        entry_dict = asdict(entry)
        entry_dict["created_at"] = entry.created_at.isoformat()
        data["entries"].append(entry_dict)
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """
        搜索记忆
        
        Args:
            query: 查询字符串
            limit: 返回数量限制
            
        Returns:
            匹配的记忆列表
        """
        results = []
        query_lower = query.lower()
        
        for entry in self.entries.values():
            score = 0
            
            # 内容匹配
            if query_lower in entry.content.lower():
                score += 10
            
            # 类型匹配
            if query_lower in entry.type.lower():
                score += 5
            
            # 标签匹配
            for tag in entry.tags:
                if query_lower in tag.lower():
                    score += 3
            
            # 元数据匹配
            for key, value in entry.metadata.items():
                if isinstance(value, str) and query_lower in value.lower():
                    score += 2
            
            if score > 0:
                results.append((score, entry))
        
        # 按分数排序
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [entry for _, entry in results[:limit]]
    
    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取指定记忆"""
        return self.entries.get(entry_id)
    
    def get_recent(self, days: int = 7, entry_type: str = None) -> List[MemoryEntry]:
        """
        获取最近记忆
        
        Args:
            days: 天数
            entry_type: 类型过滤
            
        Returns:
            记忆列表
        """
        cutoff = datetime.now().timestamp() - days * 24 * 3600
        
        results = []
        for entry in self.entries.values():
            if entry.created_at.timestamp() >= cutoff:
                if entry_type is None or entry.type == entry_type:
                    results.append(entry)
        
        # 按时间排序
        results.sort(key=lambda x: x.created_at, reverse=True)
        
        return results
    
    def count(self) -> int:
        """记忆总数"""
        return len(self.entries)
    
    def summary(self) -> Dict[str, Any]:
        """
        记忆摘要
        
        Returns:
            摘要信息
        """
        type_counts = {}
        for entry in self.entries.values():
            type_counts[entry.type] = type_counts.get(entry.type, 0) + 1
        
        return {
            "total": len(self.entries),
            "by_type": type_counts,
            "recent_7_days": len(self.get_recent(7))
        }
    
    def record_task(self, task_name: str, status: str, details: str = ""):
        """记录任务"""
        self.save({
            "type": "task",
            "content": f"{task_name}: {status}",
            "metadata": {
                "task_name": task_name,
                "status": status,
                "details": details
            },
            "tags": ["任务"]
        })
    
    def record_experiment(self, name: str, config: dict, results: dict):
        """记录实验"""
        self.save({
            "type": "experiment",
            "content": f"实验: {name}",
            "metadata": {
                "name": name,
                "config": config,
                "results": results
            },
            "tags": ["实验"],
            "importance": 3
        })
    
    def record_lesson(self, problem: str, solution: str, context: str = ""):
        """记录经验教训"""
        self.save({
            "type": "lesson",
            "content": f"问题: {problem}\n解决: {solution}",
            "metadata": {
                "problem": problem,
                "solution": solution,
                "context": context
            },
            "tags": ["经验教训"],
            "importance": 4
        })
    
    def record_decision(self, decision: str, reason: str, alternatives: List[str] = None):
        """记录决策"""
        self.save({
            "type": "decision",
            "content": f"决策: {decision}",
            "metadata": {
                "decision": decision,
                "reason": reason,
                "alternatives": alternatives or []
            },
            "tags": ["决策"],
            "importance": 4
        })
    
    def daily_summary(self) -> str:
        """生成每日总结"""
        today = date.today()
        today_entries = [
            e for e in self.entries.values()
            if e.created_at.date() == today
        ]
        
        if not today_entries:
            return "今天还没有记录任何内容。"
        
        summary = f"📅 {today.isoformat()} 总结\n\n"
        
        # 按类型分组
        by_type = {}
        for entry in today_entries:
            by_type.setdefault(entry.type, []).append(entry)
        
        for entry_type, entries in by_type.items():
            summary += f"【{entry_type}】\n"
            for entry in entries:
                summary += f"  - {entry.content}\n"
            summary += "\n"
        
        return summary
