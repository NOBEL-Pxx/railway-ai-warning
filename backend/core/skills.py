"""
技能管理器 - LoongClaw 气象AI领域定制版
管理气象AI领域专属技能
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Skill:
    """技能定义"""
    name: str
    description: str
    category: str
    func: Callable = None
    command: str = None  # 可以是shell命令或Python函数
    params: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    code_path: str = None  # 关联的代码路径


class SkillManager:
    """
    技能管理器 - LoongClaw 气象AI领域定制

    技能分为两类：
    1. 代码技能：调用项目内 src/ 目录中的代码
    2. 命令技能：执行shell命令
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        # 代码已合并到项目内
        self.code_path = self.project_path
        self.skills: Dict[str, Skill] = {}

        # 加载技能
        self._load_builtin_skills()
        self._load_code_skills()
    
    def _load_builtin_skills(self):
        """加载内置技能"""
        
        # ========== 数据处理技能 ==========
        
        self.register(Skill(
            name="check-data",
            description="检查数据状态（ERA5、DEM、雨量计）",
            category="data",
            func=self._check_data,
            tags=["数据", "状态检查"]
        ))
        
        self.register(Skill(
            name="download-era5",
            description="下载ERA5再分析数据",
            category="data",
            func=self._download_era5,
            tags=["ERA5", "下载", "气象数据"]
        ))
        
        self.register(Skill(
            name="compute-terrain",
            description="计算地形特征（坡度、坡向、汇流面积）",
            category="data",
            func=self._compute_terrain,
            tags=["地形", "DEM", "特征工程"]
        ))
        
        self.register(Skill(
            name="quality-control",
            description="数据质量控制（缺失值、异常值检测）",
            category="data",
            func=self._quality_control,
            tags=["数据", "质量控制"]
        ))
        
        self.register(Skill(
            name="feature-engineering",
            description="特征工程（雷达特征、时序特征）",
            category="data",
            func=self._feature_engineering,
            tags=["特征", "雷达"]
        ))
        
        # ========== 模型技能 ==========
        
        self.register(Skill(
            name="train-model",
            description="训练MambaSwin-UNet-STA模型",
            category="model",
            func=self._train_model,
            tags=["训练", "深度学习", "MambaSwin"],
            code_path="src/training/train.py"
        ))
        
        self.register(Skill(
            name="evaluate-metrics",
            description="计算评估指标（TS、POD、FAR、CSI）",
            category="model",
            func=self._evaluate_metrics,
            tags=["评估", "指标"]
        ))
        
        self.register(Skill(
            name="tune-hyperparams",
            description="超参数调优",
            category="model",
            func=self._tune_hyperparams,
            tags=["调优", "超参数"]
        ))
        
        # ========== 风险推演技能 ==========
        
        self.register(Skill(
            name="risk-inference",
            description="致灾风险推演（路基冲刷、边坡失稳）",
            category="risk",
            func=self._risk_inference,
            tags=["风险", "推演", "水文"]
        ))
        
        self.register(Skill(
            name="plot-forecast",
            description="绑制降水预报图",
            category="viz",
            func=self._plot_forecast,
            tags=["可视化", "预报"]
        ))
        
        self.register(Skill(
            name="plot-risk-map",
            description="绑制风险热力图",
            category="viz",
            func=self._plot_risk_map,
            tags=["可视化", "风险"]
        ))
        
        # ========== 论文技能 ==========
        
        self.register(Skill(
            name="write-paper",
            description="辅助论文写作",
            category="paper",
            func=self._write_paper,
            tags=["论文", "写作"]
        ))
        
        self.register(Skill(
            name="generate-report",
            description="生成技术报告",
            category="paper",
            func=self._generate_report,
            tags=["报告", "文档"]
        ))
    
    def _load_code_skills(self):
        """加载代码项目中的技能"""
        if not self.code_path.exists():
            return

        # 扫描项目内代码模块
        if self.code_path.exists():
            print(f"   已关联代码项目: {self.code_path}")
    
    def register(self, skill: Skill):
        """注册技能"""
        self.skills[skill.name] = skill
    
    def get(self, name: str) -> Optional[Skill]:
        """获取技能"""
        return self.skills.get(name)
    
    def list_skills(self, category: str = None) -> List[Skill]:
        """列出技能"""
        if category:
            return [s for s in self.skills.values() if s.category == category]
        return list(self.skills.values())
    
    def search(self, query: str) -> List[Skill]:
        """搜索技能"""
        results = []
        query_lower = query.lower()
        
        for skill in self.skills.values():
            if (query_lower in skill.name.lower() or
                query_lower in skill.description.lower() or
                any(query_lower in tag.lower() for tag in skill.tags)):
                results.append(skill)
        
        return results
    
    def execute(self, name: str, **kwargs) -> Any:
        """
        执行技能
        
        Args:
            name: 技能名称
            **kwargs: 技能参数
            
        Returns:
            执行结果
        """
        skill = self.get(name)
        if not skill:
            raise ValueError(f"技能 '{name}' 不存在")
        
        print(f"\n🐉 执行技能: {name}")
        print(f"   描述: {skill.description}")
        if skill.code_path:
            print(f"   代码: {skill.code_path}")
        
        try:
            if skill.func:
                result = skill.func(**kwargs)
            elif skill.command:
                result = subprocess.run(skill.command, shell=True, capture_output=True)
                result = result.stdout.decode()
            else:
                result = {"status": "no_action"}
            
            print(f"   状态: 完成 ✓\n")
            return result
            
        except Exception as e:
            print(f"   状态: 失败 ✗")
            print(f"   错误: {e}\n")
            raise
    
    # ============ 技能实现 ============
    
    def _check_data(self, **kwargs) -> dict:
        """检查数据状态"""
        status = {
            "era5": False,
            "dem": False,
            "rainfall": False,
            "processed": False
        }
        
        if self.code_path:
            data_dir = self.code_path / "data"
            status["era5"] = (data_dir / "external" / "era5").exists()
            status["dem"] = (data_dir / "external" / "dem").exists()
            status["rainfall"] = (data_dir / "raw").exists()
            status["processed"] = (data_dir / "processed").exists()
        
        print("\n   数据状态:")
        for key, value in status.items():
            icon = "✓" if value else "✗"
            print(f"     {key}: {icon}")
        
        return status
    
    def _download_era5(self, variables: List[str] = None, 
                       start_date: str = None, end_date: str = None,
                       bbox: List[float] = None, **kwargs) -> dict:
        """下载ERA5数据"""
        print("\n   ERA5下载配置:")
        print(f"     变量: {variables or ['t2m', 'd2m', 'u10', 'v10', 'sp', 'tp']}")
        print(f"     时间: {start_date or '未指定'} 至 {end_date or '未指定'}")
        print(f"     区域: {bbox or '全球'}")
        
        print("\n   提示:")
        print("     1. 安装 cdsapi: pip install cdsapi")
        print("     2. 配置 API密钥: ~/.cdsapirc")
        print("     3. 运行下载脚本")
        
        # 如果有代码项目，生成下载脚本
        if self.code_path:
            script_path = self.code_path / "scripts" / "download_era5.py"
            print(f"\n   下载脚本: {script_path}")
        
        return {"status": "configured", "action": "download_era5"}
    
    def _compute_terrain(self, dem_path: str = None, **kwargs) -> dict:
        """计算地形特征"""
        print("\n   地形特征计算:")
        print("     - 坡度 (Slope)")
        print("     - 坡向 (Aspect)")
        print("     - 汇流面积 (Flow Accumulation)")
        print("     - 曲率 (Curvature)")
        
        if dem_path:
            print(f"\n   DEM文件: {dem_path}")
        elif self.code_path:
            dem_dir = self.code_path / "data" / "external" / "dem"
            print(f"\n   DEM目录: {dem_dir}")
        
        # 关联代码
        if self.code_path:
            code_file = self.code_path / "src" / "data" / "features.py"
            print(f"   代码: {code_file}")
        
        return {"status": "ready", "features": ["slope", "aspect", "flow_acc", "curvature"]}
    
    def _quality_control(self, data_path: str = None, **kwargs) -> dict:
        """数据质量控制"""
        print("\n   质量控制流程:")
        print("     1. 缺失值检测与插补")
        print("     2. 异常值检测与剔除")
        print("     3. 时空一致性检验")
        
        if self.code_path:
            code_file = self.code_path / "src" / "data" / "preprocess.py"
            print(f"\n   代码: {code_file}")
        
        return {"status": "ready"}
    
    def _feature_engineering(self, **kwargs) -> dict:
        """特征工程"""
        print("\n   特征工程:")
        print("     雷达特征: 回波强度、回波顶高、VIL")
        print("     地形特征: 坡度、坡向、汇流面积")
        print("     时序特征: 滑动统计、趋势")
        
        return {"status": "ready"}
    
    def _train_model(self, config_path: str = None, **kwargs) -> dict:
        """训练模型"""
        print("\n   模型: MambaSwin-UNet-STA")
        print("   框架: PyTorch Lightning")
        
        if self.code_path:
            train_script = self.code_path / "src" / "training" / "train.py"
            model_file = self.code_path / "src" / "models" / "mamba_swin_unet.py"
            config_file = self.code_path / "configs" / "model.yaml"
            
            print(f"\n   训练脚本: {train_script}")
            print(f"   模型文件: {model_file}")
            print(f"   配置文件: {config_file}")
            
            print("\n   执行命令:")
            print(f"     cd {self.code_path}")
            print(f"     python src/training/train.py")
        
        return {"status": "ready", "model": "MambaSwin-UNet-STA"}
    
    def _evaluate_metrics(self, **kwargs) -> dict:
        """评估指标"""
        print("\n   评估指标:")
        print("     TS (Threat Score)")
        print("     POD (Probability of Detection)")
        print("     FAR (False Alarm Rate)")
        print("     CSI (Critical Success Index)")
        
        return {"status": "ready"}
    
    def _tune_hyperparams(self, **kwargs) -> dict:
        """超参数调优"""
        print("\n   超参数调优:")
        print("     学习率、batch_size、网络深度...")
        
        return {"status": "ready"}
    
    def _risk_inference(self, **kwargs) -> dict:
        """致灾风险推演"""
        print("\n   风险推演:")
        print("     水文模型: SCS-CN")
        print("     风险类型: 路基冲刷、边坡失稳、积水")
        
        if self.code_path:
            code_file = self.code_path / "src" / "models" / "physics.py"
            print(f"\n   代码: {code_file}")
        
        return {"status": "ready"}
    
    def _plot_forecast(self, **kwargs) -> dict:
        """绑制预报图"""
        print("\n   绑制降水预报图...")
        return {"status": "ready"}
    
    def _plot_risk_map(self, **kwargs) -> dict:
        """绑制风险热力图"""
        print("\n   绑制风险热力图...")
        return {"status": "ready"}
    
    def _write_paper(self, section: str = None, **kwargs) -> dict:
        """辅助论文写作"""
        print("\n   论文写作辅助")
        print("   可用章节: introduction, method, results, discussion")
        
        return {"status": "ready"}
    
    def _generate_report(self, **kwargs) -> dict:
        """生成技术报告"""
        print("\n   生成技术报告...")
        return {"status": "ready"}
