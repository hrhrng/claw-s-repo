#!/usr/bin/env python3
import os
import re
from datetime import datetime
from html import escape

# 生成文件名
timestamp = datetime.now().strftime("%Y-%m-%d-%H")
html_file = f"deep-dive-{timestamp}.html"

def read_raw_data():
    raw_dir = "raw_data"
    data = {}
    influencers = [
        ("sama", "Sam Altman", "Tier 1"),
        ("openai", "OpenAI", "Tier 1"),
        ("anthropic", "Anthropic", "Tier 1"),
        ("karpathy", "Andrej Karpathy", "Tier 1"),
        ("andrewyng", "Andrew Ng", "Tier 2"),
        ("ylecun", "Yann LeCun", "Tier 2"),
        ("drjimfan", "Jim Fan", "Tier 2"),
        ("ilyasut", "Ilya Sutskever", "Tier 2"),
        ("lilianweng", "Lilian Weng", "Tier 2"),
        ("janleike", "Jan Leike", "Tier 2"),
        ("repligate", "repligate", "Tier 2"),
        ("sebastienbubeck", "Sebastien Bubeck", "Tier 2"),
        ("bindureddy", "Bindu Reddy", "Tier 3"),
        ("gdb", "Greg Brockman", "Tier 3"),
        ("alexandr_wang", "Alexandr Wang", "Tier 3"),
        ("hardmaru", "hardmaru", "Tier 3"),
        ("demishassabis", "Demis Hassabis", "Tier 3"),
        ("sundarpichai", "Sundar Pichai", "Tier 3"),
        ("elonmusk", "Elon Musk", "Tier 3"),
        ("deepseek", "DeepSeek", "Tier 4"),
        ("eladgil", "Elad Gil", "Tier 5"),
        ("paulg", "Paul Graham", "Tier 5"),
        ("nearcyan", "nearcyan", "Tier 6"),
        ("googledeepmind", "Google DeepMind", "公司"),
        ("geminiapp", "Gemini", "公司"),
        ("xai", "xAI", "公司"),
        ("huggingface", "Hugging Face", "公司"),
    ]
    
    for file_key, name, tier in influencers:
        filepath = os.path.join(raw_dir, f"{file_key}.txt")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            data[file_key] = {"name": name, "tier": tier, "content": content}
    return data

def extract_key_insights(data):
    insights = []
    highlights = []
    security_alerts = []
    product_launches = []
    
    # 分析 Karpathy 关于 600x 成本下降
    if "karpathy" in data:
        content = data["karpathy"]["content"]
        if "600X" in content or "600x" in content or "$73" in content:
            insights.append({
                "title": "💰 Karpathy: GPT-2 训练成本 7 年下降 600 倍",
                "desc": "Karpathy 的 nanochat 项目现在可以以约 $73（3 小时 8xH100）训练 GPT-2 级别模型，相比 2019 年的 $43K，成本下降约 600 倍。年均成本下降约 2.5 倍。",
                "source": "@karpathy",
                "url": "https://x.com/karpathy/status/2017703360393318587"
            })
            highlights.append("600x 训练成本下降")
        
        if "agent" in content.lower() and "network" in content.lower():
            insights.append({
                "title": "🤖 Karpathy: 大规模 LLM Agent 网络安全警告",
                "desc": "Karpathy 警告称，15 万个 LLM Agent 通过共享 scratchpad 连接是前所未有的规模，可能导致计算机安全噩梦、文本病毒传播、越狱增强等二级效应。",
                "source": "@karpathy",
                "url": "https://x.com/karpathy/status/2017442712388309406",
                "alert": True
            })
            security_alerts.append("大规模 Agent 网络安全风险")
    
    # 分析 Sam Altman
    if "sama" in data:
        content = data["sama"]["content"]
        if "town hall" in content.lower() or "Tomorrow" in content:
            insights.append({
                "title": "📢 OpenAI Town Hall 明天举行",
                "desc": "Sam Altman 宣布明天（1月26日）将举办 AI Builder Town Hall，在 YouTube 直播，收集新一代工具的反馈。",
                "source": "@sama",
                "url": "https://x.com/sama/status/2015548504194654707"
            })
            highlights.append("OpenAI Town Hall 预告")
        
        if "$1B" in content and "ARR" in content:
            insights.append({
                "title": "💵 OpenAI API 业务单月增长 $10 亿 ARR",
                "desc": "Sam Altman 披露仅 API 业务就在过去一个月增加了超过 $10 亿的年化收入。",
                "source": "@sama",
                "url": "https://x.com/sama/status/2014399391025574308"
            })
            highlights.append("API 业务 $1B ARR 增长")
        
        if "Codex" in content:
            insights.append({
                "title": "🚀 Codex 系列产品即将发布",
                "desc": "Sam Altman 预告未来一个月将有一系列 Codex 相关产品发布，下周开始。",
                "source": "@sama",
                "url": "https://x.com/sama/status/2014733975755817267"
            })
            product_launches.append("Codex 系列")
    
    # 分析 Anthropic
    if "anthropic" in data:
        content = data["anthropic"]["content"]
        if "Mars" in content or "Perseverance" in content:
            insights.append({
                "title": "🚀 Claude 首次在火星上规划 AI 驾驶",
                "desc": "Anthropic 宣布 NASA JPL 工程师使用 Claude 为毅力号火星车规划了约 400 米路径的行驶路线，这是首次在其他星球上的 AI 规划驾驶。",
                "source": "@AnthropicAI",
                "url": "https://x.com/AnthropicAI/status/2017313346375004487"
            })
            highlights.append("Claude 火星驾驶")
    
    # 分析 Andrew Ng
    if "andrewyng" in data:
        content = data["andrewyng"]["content"]
        if "Sovereign AI" in content or "sovereign" in content.lower():
            insights.append({
                "title": "🌍 Andrew Ng: 美国政策推动主权 AI 崛起",
                "desc": "Andrew Ng 长文分析美国政策（芯片出口管制、关税、移民政策等）如何推动各国发展主权 AI，DeepSeek、Qwen、Kimi 等中国开源模型因此快速获得全球采用。",
                "source": "@AndrewYNg",
                "url": "https://x.com/AndrewYNg/status/2017283482041651303"
            })
            highlights.append("主权 AI 趋势")
    
    # 分析 xAI
    if "xai" in data:
        content = data["xai"]["content"]
        if "Grok Imagine" in content:
            insights.append({
                "title": "🎬 Grok Imagine 视频生成登顶竞技场",
                "desc": "xAI 的 Grok Imagine 在 Text-to-Video 和 Image-to-Video 竞技场中均排名第一，超越 Runway Gen-4.5、Kling 2.5 Turbo 和 Veo 3.1。",
                "source": "@xAI",
                "url": "https://x.com/ArtificialAnlys/status/2016749756081721561"
            })
            product_launches.append("Grok Imagine API")
    
    # 分析 Jim Fan
    if "drjimfan" in data:
        content = data["drjimfan"]["content"]
        if "robotics" in content.lower() and "lesson" in content.lower():
            insights.append({
                "title": "🦾 Jim Fan: 机器人学的 3 个教训",
                "desc": "1) 硬件领先于软件，但硬件可靠性严重限制软件迭代；2) 机器人基准测试仍是灾难；3) VLM-based VLA 方法存在问题，视频世界模型可能是更好的预训练目标。",
                "source": "@DrJimFan",
                "url": "https://x.com/DrJimFan/status/2005340845055340558"
            })
    
    # 分析 OpenAI
    if "openai" in data:
        content = data["openai"]["content"]
        if "Prism" in content:
            insights.append({
                "title": "🔬 OpenAI 发布 Prism 科研协作平台",
                "desc": "Prism 是面向科学家的免费工作空间，支持 GPT-5.2 驱动的研究写作与协作，消除版本冲突和设置开销。",
                "source": "@OpenAI",
                "url": "https://x.com/OpenAI/status/2016209462621831448"
            })
            product_launches.append("Prism 科研平台")
        
        if "Thinking" in content:
            insights.append({
                "title": "⚙️ GPT-5 Thinking 支持多级调节",
                "desc": "付费用户现在可以在 Web、iOS 和 Android 上调整 GPT-5 的思考级别：Light、Standard、Extended 和 Heavy。",
                "source": "@OpenAI",
                "url": "https://x.com/OpenAI/status/2016972315784061007"
            })
    
    # 分析 Jan Leike
    if "janleike" in data:
        content = data["janleike"]["content"]
        if "aligned" in content.lower() and "2025" in content:
            insights.append({
                "title": "🛡️ 2025 年模型对齐度显著提升",
                "desc": "Jan Leike 指出，2025 年以来模型对齐度显著提高，Anthropic、GDM 和 OpenAI 的自动化审计发现的不对齐行为比例都在下降。",
                "source": "@janleike",
                "url": "https://x.com/janleike/status/2013669924950970781"
            })
    
    # 分析 Google DeepMind
    if "googledeepmind" in data:
        content = data["googledeepmind"]["content"]
        if "Project Genie" in content:
            insights.append({
                "title": "🎮 Google DeepMind 推出 Project Genie",
                "desc": "实验性研究原型，允许用户通过文本和视觉提示创建、编辑和探索虚拟世界，使用 Nano Banana Pro 生成图像预览，Genie 3 世界模型实时生成环境。",
                "source": "@GoogleDeepMind",
                "url": "https://x.com/GoogleDeepMind/status/2016919756440240479"
            })
            product_launches.append("Project Genie")
    
    # 分析 Sebastien Bubeck
    if "sebastienbubeck" in data:
        content = data["sebastienbubeck"]["content"]
        if "Erdos" in content or "Erdős" in content:
            insights.append({
                "title": "🧮 AI 已自主解决 10 个 Erdős 开放问题",
                "desc": "LLM 已完全自主解决了 10 个此前开放的 Erdős 数学问题（#205, 281, 401, 524, 543, 635, 652, 728, 729, 1051）。",
                "source": "@SebastienBubeck",
                "url": "https://x.com/AcerFur/status/2017303947531194398"
            })
            highlights.append("AI 解决 10 个 Erdős 问题")
    
    return insights, highlights, security_alerts, product_launches

def generate_html(data, insights, highlights, security_alerts, product_launches):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:00")
    date_str = datetime.now().strftime("%Y-%m-%d-%H")
    
    # 提取各 tier 内容
    tier1_content = []
    tier2_content = []
    tier3_content = []
    others_content = []
    
    for key, info in data.items():
        tier = info["tier"]
        name = info["name"]
        content = info["content"]
        
        # 清理内容，只保留有用的推文
        lines = content.split('\n')
        tweets = []
        current_tweet = []
        
        for line in lines:
            if line.startswith('@') and '(' in line:
                if current_tweet:
                    tweets.append('\n'.join(current_tweet))
                current_tweet = [line]
            elif line.startswith('date:') or line.startswith('url:') or line.startswith('─'):
                current_tweet.append(line)
            elif line and not line.startswith('[info]'):
                current_tweet.append(line)
        
        if current_tweet:
            tweets.append('\n'.join(current_tweet))
        
        # 只保留该用户的推文（过滤掉转推）
        user_tweets = []
        for t in tweets:
            if f'@{key}' in t.lower() or f'@{name.lower().replace(" ", "")}' in t.lower():
                user_tweets.append(t)
        
        if user_tweets:
            entry = {"name": name, "handle": f"@{key}", "tweets": user_tweets[:3]}
            if tier == "Tier 1":
                tier1_content.append(entry)
            elif tier == "Tier 2":
                tier2_content.append(entry)
            elif tier == "Tier 3":
                tier3_content.append(entry)
            else:
                others_content.append(entry)
    
    # 生成分类内容 HTML
    def generate_tier_html(entries, tier_name):
        if not entries:
            return ""
        html = f'<div class="tier-section"><h3>🔹 {tier_name}</h3>'
        for entry in entries:
            html += f'<div class="influencer-block"><h4>{entry["name"]} <span class="handle">{entry["handle"]}</span></h4>'
            for i, tweet in enumerate(entry["tweets"]):
                # 提取日期和 URL
                date_match = re.search(r'date: (.+)', tweet)
                url_match = re.search(r'url: (.+)', tweet)
                
                # 清理推文文本
                text = tweet
                text = re.sub(r'^@[^\n]+\n', '', text)  # 移除用户名行
                text = re.sub(r'date: .+\n?', '', text)  # 移除日期
                text = re.sub(r'url: .+\n?', '', text)  # 移除 URL
                text = re.sub(r'─+\n?', '', text)  # 移除分隔线
                text = re.sub(r'PHOTO: .+\n?', '[图片]', text)  # 替换图片
                text = re.sub(r'GIF: .+\n?', '[GIF]', text)  # 替换 GIF
                text = re.sub(r'VIDEO: .+\n?', '[视频]', text)  # 替换视频
                text = text.strip()
                
                if text and len(text) > 20:  # 只保留有意义的推文
                    html += f'<div class="tweet"><p>{escape(text[:500])}</p>'
                    if url_match:
                        html += f'<a href="{url_match.group(1)}" class="tweet-link" target="_blank">查看原文 →</a>'
                    html += '</div>'
            html += '</div>'
        html += '</div>'
        return html
    
    tier1_html = generate_tier_html(tier1_content, "Tier 1 - 核心人物")
    tier2_html = generate_tier_html(tier2_content, "Tier 2 - 研究界")
    tier3_html = generate_tier_html(tier3_content, "Tier 3 - 产业界")
    others_html = generate_tier_html(others_content, "其他")
    
    # 生成关键洞察 HTML
    insights_html = ""
    for insight in insights:
        alert_class = "alert" if insight.get("alert") else ""
        insights_html += f'''
        <div class="insight-card {alert_class}">
            <h4>{insight["title"]}</h4>
            <p>{insight["desc"]}</p>
            <div class="insight-source">来源: <a href="{insight.get("url", "#")}" target="_blank">{insight["source"]}</a></div>
        </div>
        '''
    
    # 生成 Highlights
    highlights_html = ""
    for h in highlights:
        highlights_html += f'<span class="highlight-tag">{h}</span>'
    
    # 生成安全警报
    alerts_html = ""
    for alert in security_alerts:
        alerts_html += f'<div class="security-alert">🚨 {alert}</div>'
    
    # 生成产品发布
    launches_html = ""
    for launch in product_launches:
        launches_html += f'<div class="product-launch">🚀 {launch}</div>'
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Trends 深度报告 - {timestamp}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0a0a0f;--card:#14141a;--border:#252530;--text:#fff;--text2:#9090a0;--accent:#6366f1;--accent2:#8b5cf6;--alert:#ef4444;--success:#22c55e}}
body{{font-family:'Inter','Noto Sans SC',sans-serif;background:var(--bg);color:var(--text);margin:0;min-height:100vh;line-height:1.6}}
header{{background:linear-gradient(135deg,var(--accent),var(--accent2));padding:50px 20px;text-align:center}}
h1{{margin:0;font-size:2rem}}.meta{{opacity:.9;margin-top:10px;font-size:.9rem}}
.container{{max-width:1000px;margin:0 auto;padding:30px 20px}}
.section-title{{font-size:1.3rem;color:var(--accent);margin:40px 0 20px;padding-bottom:10px;border-bottom:2px solid var(--border)}}
.highlights{{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}}
.highlight-tag{{background:rgba(99,102,241,.2);color:var(--accent);padding:6px 14px;border-radius:20px;font-size:.85rem;font-weight:500}}
.security-alert{{background:rgba(239,68,68,.15);color:#fca5a5;padding:12px 16px;border-radius:8px;margin:8px 0;border-left:3px solid var(--alert)}}
.product-launch{{background:rgba(34,197,94,.15);color:#86efac;padding:12px 16px;border-radius:8px;margin:8px 0;border-left:3px solid var(--success)}}
.insight-card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:15px;transition:all .2s}}
.insight-card:hover{{border-color:var(--accent)}}
.insight-card.alert{{border-color:var(--alert);background:rgba(239,68,68,.05)}}
.insight-card h4{{margin:0 0 10px;color:var(--accent);font-size:1.1rem}}
.insight-card.alert h4{{color:var(--alert)}}
.insight-card p{{margin:0;color:var(--text2);font-size:.95rem}}
.insight-source{{margin-top:10px;font-size:.8rem;color:var(--text2)}}
.insight-source a{{color:var(--accent);text-decoration:none}}
.tier-section{{margin:30px 0}}
.tier-section h3{{color:var(--accent2);margin-bottom:15px}}
.influencer-block{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;margin-bottom:15px}}
.influencer-block h4{{margin:0 0 15px;display:flex;align-items:center;gap:10px}}
.handle{{color:var(--text2);font-weight:normal;font-size:.9rem}}
.tweet{{padding:15px;background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:10px}}
.tweet p{{margin:0 0 8px;color:var(--text)}}
.tweet-link{{color:var(--accent);font-size:.8rem;text-decoration:none}}
.tweet-link:hover{{text-decoration:underline}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin:30px 0}}
.stat-card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;text-align:center}}
.stat-number{{font-size:2rem;font-weight:700;color:var(--accent)}}
.stat-label{{color:var(--text2);font-size:.85rem;margin-top:5px}}
footer{{text-align:center;padding:40px 20px;color:var(--text2);font-size:.85rem;border-top:1px solid var(--border);margin-top:40px}}
</style>
</head>
<body>
<header>
    <h1>🤖 AI Trends 深度报告</h1>
    <div class="meta">生成时间: {timestamp} CST | 监控 27 位大 V</div>
</header>

<div class="container">

<div class="section-title">📊 核心发现</div>
<div class="stats">
    <div class="stat-card">
        <div class="stat-number">{len(insights)}</div>
        <div class="stat-label">关键洞察</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{len(security_alerts)}</div>
        <div class="stat-label">安全警报</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{len(product_launches)}</div>
        <div class="stat-label">产品发布</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">27</div>
        <div class="stat-label">监控账号</div>
    </div>
</div>

<div class="highlights">
    {highlights_html}
</div>

{alerts_html if alerts_html else '<div style="color:var(--text2);font-style:italic">本期无新增安全警报</div>'}

{launches_html if launches_html else ''}

<div class="section-title">🔍 深度洞察</div>
{insights_html}

<div class="section-title">📝 大 V 动态原文</div>
{tier1_html}
{tier2_html}
{tier3_html}
{others_html}

</div>

<footer>
    <p>🤖 AI Trends Digest | 每小时自动更新</p>
    <p>数据来源: X (Twitter) | 由 OpenClaw 自动生成</p>
</footer>
</body>
</html>'''
    
    return html_content, html_file

# 主程序
data = read_raw_data()
insights, highlights, security_alerts, product_launches = extract_key_insights(data)
html_content, html_file = generate_html(data, insights, highlights, security_alerts, product_launches)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"报告已生成: {html_file}")
print(f"关键洞察数: {len(insights)}")
print(f"安全警报数: {len(security_alerts)}")
print(f"产品发布数: {len(product_launches)}")
print(f"成功抓取账号: {len(data)}/27")
