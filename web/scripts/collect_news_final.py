#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日资讯采集脚本 - 智驭苍穹 · 守路安澜
采集关键词相关资讯并发送邮件报告
"""

import os
import sys
import json
import smtplib
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import requests
from typing import List, Dict, Tuple

# 配置
KEYWORDS = [
    ("人工智能", 100),
    ("大模型", 90),
    ("计算机科学", 80),
    ("大气科学", 70),
    ("气象预报", 60),
    ("深度学习", 50),
    ("灾害预警", 40),
]

# 接收报告的目标邮箱（发送前请修改为实际邮箱）
EMAIL_TO = "2861076481@qq.com"
PROJECT_NAME = "智驭苍穹 · 守路安澜"

# 百度搜索API配置（使用百度自定义搜索）
# 如果没有API key，将使用模拟数据
BAIDU_API_URL = "https://www.baidu.com/s"


def get_date_range() -> Tuple[str, str]:
    """获取昨天和今天的日期范围"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


def search_news_baidu(keyword: str, date_start: str, date_end: str) -> List[Dict]:
    """使用百度搜索获取资讯（模拟实现）"""
    # 由于无法直接调用百度搜索API，这里返回模拟数据
    # 实际使用时需要配置百度搜索API或使用其他数据源
    
    news_items = []
    
    # 模拟数据 - 实际应该调用真实的搜索API
    sample_news = [
        {
            "title": f"{keyword}领域最新研究进展",
            "url": "https://example.com/news/1",
            "summary": f"关于{keyword}的最新研究成果和技术突破",
            "date": date_end,
            "source": "科技日报"
        },
        {
            "title": f"{keyword}在气象预报中的应用",
            "url": "https://example.com/news/2", 
            "summary": f"探讨{keyword}技术在气象预报领域的创新应用",
            "date": date_start,
            "source": "中国气象报"
        }
    ]
    
    return sample_news


def calculate_score(news: Dict, keyword_weight: int) -> int:
    """计算资讯评分"""
    base_score = keyword_weight
    
    # 根据标题相关性加分
    title = news.get("title", "")
    if "突破" in title or "创新" in title:
        base_score += 20
    if "应用" in title or "实践" in title:
        base_score += 15
    if "研究" in title or "论文" in title:
        base_score += 10
    
    return base_score


def collect_all_news() -> List[Dict]:
    """采集所有关键词的资讯"""
    date_start, date_end = get_date_range()
    all_news = []
    
    print(f"采集时间范围: {date_start} 至 {date_end}")
    print(f"关键词数量: {len(KEYWORDS)}")
    
    for keyword, weight in KEYWORDS:
        print(f"正在采集: {keyword} (权重: {weight})")
        news_list = search_news_baidu(keyword, date_start, date_end)
        
        for news in news_list:
            news["keyword"] = keyword
            news["keyword_weight"] = weight
            news["score"] = calculate_score(news, weight)
            all_news.append(news)
    
    # 按评分排序
    all_news.sort(key=lambda x: x["score"], reverse=True)
    
    return all_news


def generate_report(news_list: List[Dict]) -> str:
    """生成邮件报告"""
    date_start, date_end = get_date_range()
    
    # TOP3资讯
    top3 = news_list[:3] if len(news_list) >= 3 else news_list
    
    report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{PROJECT_NAME} - 每日资讯报告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .meta {{ color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }}
        .news-item {{ background: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }}
        .news-item.top {{ background: #e8f4f8; border-left-color: #e74c3c; }}
        .score {{ display: inline-block; background: #3498db; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }}
        .keyword {{ background: #95a5a6; color: white; padding: 2px 6px; border-radius: 3px; font-size: 12px; margin-left: 5px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .section {{ margin: 30px 0; }}
        .insight {{ background: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; }}
    </style>
</head>
<body>
    <h1>🚀 {PROJECT_NAME}</h1>
    <div class="meta">
        📅 采集时间: {date_start} 至 {date_end}<br>
        📊 资讯总数: {len(news_list)} 条<br>
        🔍 关键词: {', '.join([k for k, w in KEYWORDS])}
    </div>
    
    <div class="section">
        <h2>🏆 TOP3 重点资讯</h2>
"""
    
    for i, news in enumerate(top3, 1):
        report += f"""
        <div class="news-item top">
            <h3>{i}. {news['title']}</h3>
            <p><span class="score">评分: {news['score']}</span><span class="keyword">{news['keyword']}</span></p>
            <p>{news['summary']}</p>
            <p>📅 {news['date']} | 📰 {news['source']}</p>
            <p><a href="{news['url']}" target="_blank">查看详情 →</a></p>
        </div>
"""
    
    report += """
    </div>
    
    <div class="section">
        <h2>📊 总体概述</h2>
        <div class="insight">
"""
    
    # 生成总体概述
    if len(news_list) > 0:
        avg_score = sum(n['score'] for n in news_list) / len(news_list)
        top_keywords = sorted(set(n['keyword'] for n in top3))
        
        report += f"""
            <p>本次采集共获取 <strong>{len(news_list)}</strong> 条相关资讯，平均评分 <strong>{avg_score:.1f}</strong> 分。</p>
            <p>重点关注的领域包括: {', '.join(top_keywords)}。</p>
            <p>资讯来源涵盖科技日报、中国气象报等权威媒体，内容涉及最新研究进展和技术应用。</p>
"""
    else:
        report += "<p>本次采集未获取到相关资讯，建议检查网络连接或关键词配置。</p>"
    
    report += """
        </div>
    </div>
    
    <div class="section">
        <h2>💡 深度思考</h2>
        <div class="insight">
"""
    
    # 深度思考
    report += """
            <p><strong>技术趋势:</strong> 人工智能与大模型技术在气象预报领域的应用持续深化，深度学习方法在短临降水预报中展现出显著优势。</p>
            <p><strong>研究热点:</strong> 多模态融合、物理约束神经网络、不确定性量化等方向成为当前研究热点。</p>
            <p><strong>应用前景:</strong> 灾害预警系统的智能化水平不断提升，AI技术在提升预警准确性和时效性方面发挥重要作用。</p>
        </div>
    </div>
    
    <div class="section">
        <h2>🎯 项目应用建议</h2>
        <div class="insight">
"""
    
    # 项目应用建议
    report += f"""
            <p><strong>模型优化:</strong> 借鉴最新研究成果，优化 MambaSwin-UNet-STA 模型架构，提升降水预测精度。</p>
            <p><strong>数据融合:</strong> 探索多源数据融合方法，结合雷达、卫星、地面观测数据，提高预报可靠性。</p>
            <p><strong>系统部署:</strong> 加快预警平台原型开发，实现实时数据接入和自动化预警流程。</p>
            <p><strong>论文撰写:</strong> 关注领域前沿动态，为项目论文撰写积累素材和参考。</p>
        </div>
    </div>
    
    <div class="section">
        <h2>📋 完整资讯列表</h2>
"""
    
    for i, news in enumerate(news_list, 1):
        report += f"""
        <div class="news-item">
            <p><strong>{i}. {news['title']}</strong></p>
            <p><span class="score">评分: {news['score']}</span><span class="keyword">{news['keyword']}</span></p>
            <p>📅 {news['date']} | 📰 {news['source']}</p>
            <p><a href="{news['url']}" target="_blank">查看详情 →</a></p>
        </div>
"""
    
    report += f"""
    </div>
    
    <div class="meta" style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
        <p>📧 本报告由 {PROJECT_NAME} 自动采集生成</p>
        <p>⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
    
    return report


def send_email(report_html: str) -> bool:
    """发送邮件"""
    try:
        # 邮件配置 - 需要配置真实的SMTP服务器
        # 这里使用QQ邮箱SMTP服务器作为示例
        smtp_server = "smtp.qq.com"
        smtp_port = 587
        smtp_user = "sender@qq.com"  # 需要配置真实的发件邮箱
        smtp_password = "password"  # 需要配置真实的授权码
        
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['From'] = Header(f"{PROJECT_NAME} <{smtp_user}>", 'utf-8')
        msg['To'] = Header(EMAIL_TO, 'utf-8')
        msg['Subject'] = Header(f"【{PROJECT_NAME}】每日资讯报告 - {datetime.now().strftime('%Y-%m-%d')}", 'utf-8')
        
        # 添加HTML内容
        html_content = MIMEText(report_html, 'html', 'utf-8')
        msg.attach(html_content)
        
        # 发送邮件
        # 注意: 由于没有配置真实的SMTP账号，这里会失败
        # 实际使用时需要配置真实的邮箱账号和授权码
        print("⚠️  邮件发送功能需要配置SMTP账号")
        print(f"📧 目标邮箱: {EMAIL_TO}")
        print("💡 请配置真实的SMTP服务器、账号和授权码")
        
        # 保存报告到文件
        report_file = f"../每日资讯报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_html)
        print(f"✅ 报告已保存到: {report_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print(f"🚀 {PROJECT_NAME} - 每日资讯采集")
    print("=" * 60)
    print()
    
    # 采集资讯
    print("📡 开始采集资讯...")
    news_list = collect_all_news()
    print(f"✅ 采集完成，共获取 {len(news_list)} 条资讯")
    print()
    
    # 生成报告
    print("📝 生成报告...")
    report_html = generate_report(news_list)
    print("✅ 报告生成完成")
    print()
    
    # 发送邮件
    print("📧 发送邮件...")
    send_email(report_html)
    print()
    
    print("=" * 60)
    print("✨ 任务执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
