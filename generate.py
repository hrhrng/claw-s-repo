#!/usr/bin/env python3
"""
AI Trends Report Generator - 实际执行抓取和生成
"""
import json
import os
import re
import socket
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import ssl

# 禁用 SSL 验证
ssl._create_default_https_context = ssl._create_unverified_context
# 设置全局超时
socket.setdefaulttimeout(15)

def fetch_hackernews():
    """从 Hacker News 获取 AI 相关热门"""
    stories = []
    try:
        req = Request(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urlopen(req) as resp:
            top_ids = json.loads(resp.read())[:50]
        
        ai_keywords = ["ai", "artificial intelligence", "llm", "gpt", "claude", "openai", 
                      "chatgpt", "gemini", "anthropic", "model", "neural", "deepseek",
                      "machine learning", "transformer", "reasoning", "agent"]
        
        for story_id in top_ids[:15]:
            try:
                req = Request(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urlopen(req) as resp:
                    story = json.loads(resp.read())
                
                if not story or "title" not in story:
                    continue
                    
                title = story["title"].lower()
                if any(kw in title for kw in ai_keywords):
                    stories.append({
                        "title": story["title"],
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "score": story.get("score", 0),
                        "comments": story.get("descendants", 0),
                        "author": story.get("by", "unknown"),
                        "time": story.get("time", 0),
                        "source": "Hacker News",
                        "type": "讨论"
                    })
                    if len(stories) >= 5:
                        break
            except:
                continue
    except Exception as e:
        print(f"HN Error: {e}")
    return stories

def fetch_github_trending():
    """获取 GitHub 热门 AI 项目"""
    repos = []
    try:
        req = Request(
            "https://api.github.com/search/repositories?q=ai+llm+language:python&sort=stars&order=desc&per_page=10",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        with urlopen(req) as resp:
            data = json.loads(resp.read())
            for item in data.get("items", [])[:5]:
                repos.append({
                    "title": f"⭐ {item['full_name']}: {item['description'] or 'No description'}",
                    "url": item["html_url"],
                    "score": item["stargazers_count"],
                    "comments": item["forks_count"],
                    "author": item["owner"]["login"],
                    "time": 0,
                    "source": "GitHub",
                    "type": "项目"
                })
    except Exception as e:
        print(f"GitHub Error: {e}")
    return repos

def fetch_reddit_ai():
    """从 Reddit r/artificial 获取"""
    posts = []
    try:
        req = Request(
            "https://www.reddit.com/r/artificial/hot.json?limit=20",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urlopen(req) as resp:
            data = json.loads(resp.read())
            for post in data.get("data", {}).get("children", []):
                p = post["data"]
                if p.get("score", 0) > 50:
                    posts.append({
                        "title": p["title"],
                        "url": f"https://reddit.com{p['permalink']}",
                        "score": p["score"],
                        "comments": p["num_comments"],
                        "author": p["author"],
                        "time": p["created_utc"],
                        "source": "Reddit r/artificial",
                        "type": "讨论"
                    })
                    if len(posts) >= 3:
                        break
    except Exception as e:
        print(f"Reddit Error: {e}")
    return posts

def fetch_techcrunch_ai():
    """获取 TechCrunch AI 新闻"""
    articles = []
    try:
        req = Request(
            "https://api.rss2json.com/v1/api.json?rss_url=https://techcrunch.com/category/artificial-intelligence/feed/",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urlopen(req) as resp:
            data = json.loads(resp.read())
            for item in data.get("items", [])[:3]:
                articles.append({
                    "title": item["title"],
                    "url": item["link"],
                    "score": 0,
                    "comments": 0,
                    "author": item.get("author", "TechCrunch"),
                    "time": 0,
                    "source": "TechCrunch AI",
                    "type": "新闻"
                })
    except Exception as e:
        print(f"TechCrunch Error: {e}")
    return articles

def generate_report(items, timestamp):
    """生成报告 HTML"""
    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    time_str = now.strftime("%Y年%m月%d日 %H:%M")
    date_str = now.strftime("%Y-%m-%d")
    hour_str = now.strftime("%H")
    
    # 按类型分组
    by_type = {}
    for item in items:
        t = item.get("type", "其他")
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(item)
    
    # 生成内容
    content_html = ""
    for type_name in ["新闻", "项目", "讨论"]:
        if type_name not in by_type:
            continue
        content_html += f"<h2>📌 {type_name}</h2>\n"
        for item in by_type[type_name]:
            score_display = f"🔥 {item['score']:,}" if item['score'] > 1000 else f"⭐ {item['score']}" if item['score'] > 0 else ""
            comments_display = f"💬 {item['comments']}" if item['comments'] > 0 else ""
            
            content_html += f"""
            <div class="item">
                <div class="item-header">
                    <span class="item-source">{item['source']}</span>
                    <span class="item-meta">{score_display} {comments_display}</span>
                </div>
                <h3 class="item-title"><a href="{item['url']}" target="_blank">{item['title']}</a></h3>
                <div class="item-footer">
                    <span>via {item['author']}</span>
                    <a href="{item['url']}" target="_blank" class="item-link">阅读更多 →</a>
                </div>
            </div>
            """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Trends Report - {date_str} {hour_str}:00</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {{--bg:#0f0f14;--card:#18181f;--border:#2a2a35;--text:#fff;--text2:#a0a0b0;--accent:#6366f1;--accent2:#8b5cf6}}
body{{font-family:'Inter','Noto Sans SC',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;margin:0;min-height:100vh}}
.container{{max-width:900px;margin:0 auto;padding:20px}}
header{{background:linear-gradient(135deg,var(--accent),var(--accent2));padding:40px 20px;text-align:center;margin:-20px -20px 30px}}
h1{{margin:0;font-size:2rem}}.subtitle{{opacity:.9;margin-top:8px}}
.badge{{display:inline-block;background:rgba(255,255,255,.2);padding:4px 12px;border-radius:20px;font-size:.75rem;margin-top:12px}}
h2{{color:var(--accent);font-size:1.25rem;margin:30px 0 15px;padding-bottom:10px;border-bottom:1px solid var(--border)}}
.item{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:15px;transition:transform .2s}}
.item:hover{{transform:translateX(5px)}}
.item-header{{display:flex;justify-content:space-between;margin-bottom:10px;font-size:.85rem}}
.item-source{{color:var(--accent);font-weight:500}}
.item-meta{{color:var(--text2)}}
.item-title{{margin:0 0 10px;font-size:1.1rem;line-height:1.4}}
.item-title a{{color:var(--text);text-decoration:none}}
.item-title a:hover{{color:var(--accent)}}
.item-footer{{display:flex;justify-content:space-between;font-size:.85rem;color:var(--text2);margin-top:15px;padding-top:15px;border-top:1px solid var(--border)}}
.item-link{{color:var(--accent);text-decoration:none}}
.back{{display:inline-block;margin-bottom:20px;color:var(--text2);text-decoration:none}}
.back:hover{{color:var(--accent)}}
.empty{{text-align:center;padding:60px 20px;color:var(--text2)}}
</style>
</head>
<body>
<div class="container">
    <a href="index.html" class="back">← 返回目录</a>
    <header>
        <h1>🤖 AI Trends Report</h1>
        <div class="subtitle">每小时 AI 热点追踪</div>
        <div class="badge">{time_str} 更新</div>
    </header>
    
    {content_html if content_html else '<div class="empty">本时段暂无新热点</div>'}
    
    <footer style="text-align:center;margin-top:40px;padding-top:20px;border-top:1px solid var(--border);color:var(--text2);font-size:.85rem">
        <p>Generated by OpenClaw at {time_str}</p>
    </footer>
</div>
</body>
</html>"""
    
    return html

def update_index(reports_dir):
    """更新主页索引"""
    beijing_tz = timezone(timedelta(hours=8))
    
    # 获取所有报告文件
    reports = []
    for f in sorted(reports_dir.glob("report-*.html"), reverse=True):
        match = re.search(r'report-(\d{4}-\d{2}-\d{2})-(\d{2})', f.name)
        if match:
            date_str, hour = match.groups()
            reports.append({
                "file": f.name,
                "date": date_str,
                "hour": hour,
                "title": f"{date_str} {hour}:00"
            })
    
    # 按日期分组
    by_date = {}
    for r in reports:
        if r["date"] not in by_date:
            by_date[r["date"]] = []
        by_date[r["date"]].append(r)
    
    # 生成索引 HTML
    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Trends Digest | 目录</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {{--bg:#0a0a0f;--card:#14141a;--border:#252530;--text:#fff;--text2:#9090a0;--accent:#6366f1;--accent2:#8b5cf6}}
body{{font-family:'Inter','Noto Sans SC',sans-serif;background:var(--bg);color:var(--text);margin:0;min-height:100vh}}
header{{background:linear-gradient(135deg,var(--accent),var(--accent2));padding:60px 20px;text-align:center}}
h1{{margin:0;font-size:2.5rem}}.subtitle{{opacity:.9;margin-top:8px;font-size:1.1rem}}.meta{{margin-top:20px;font-size:.9rem;opacity:.8}}
.container{{max-width:800px;margin:0 auto;padding:30px 20px}}
.date-group{{margin-bottom:30px}}
.date-title{{font-size:1.1rem;color:var(--text2);margin-bottom:15px;padding-bottom:8px;border-bottom:1px solid var(--border)}}
.report-list{{display:grid;gap:10px}}
.report-item{{display:flex;align-items:center;justify-content:space-between;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:15px 20px;text-decoration:none;color:var(--text);transition:all .2s}}
.report-item:hover{{border-color:var(--accent);transform:translateX(5px)}}
.report-time{{font-size:1.1rem;font-weight:500}}
.report-badge{{background:rgba(99,102,241,.2);color:var(--accent);padding:4px 12px;border-radius:20px;font-size:.75rem}}
.about{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-top:30px}}
.about h3{{margin-top:0;color:var(--accent)}}
.about p{{color:var(--text2);margin:10px 0}}
footer{{text-align:center;padding:30px;color:var(--text2);font-size:.85rem}}
</style>
</head>
<body>
<header>
    <h1>🤖 AI Trends Digest</h1>
    <div class="subtitle">每小时 AI 热点追踪报告</div>
    <div class="meta">已生成 {len(reports)} 份报告 | 最后更新: {datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M')}</div>
</header>

<div class="container">
"""
    
    for date in sorted(by_date.keys(), reverse=True)[:7]:
        index_html += f'<div class="date-group">\n<div class="date-title">📅 {date}</div>\n<div class="report-list">\n'
        for r in by_date[date]:
            index_html += f'<a href="{r["file"]}" class="report-item"><span class="report-time">{r["hour"]}:00</span><span class="report-badge">查看报告</span></a>\n'
        index_html += '</div>\n</div>\n'
    
    index_html += f"""
    <div class="about">
        <h3>关于本项目</h3>
        <p>每小时自动抓取多个平台的 AI 热点，包括 Hacker News、GitHub Trending、Reddit、TechCrunch 等。</p>
        <p>由 OpenClaw 自动更新和维护。</p>
    </div>
</div>

<footer>
    <p>🤖 AI Trends Digest | Powered by OpenClaw</p>
</footer>
</body>
</html>"""
    
    return index_html

def main():
    print("="*50)
    print("🤖 AI Trends Report Generator")
    print("="*50)
    
    work_dir = Path("/Users/xiaoyang/.openclaw/workspace/ai-trends-digest-auto")
    work_dir.mkdir(exist_ok=True)
    
    print("\n🔍 正在抓取数据...")
    all_items = []
    
    print("  📰 Hacker News...")
    hn_items = fetch_hackernews()
    all_items.extend(hn_items)
    print(f"     ✓ {len(hn_items)} items")
    
    print("  ⭐ GitHub...")
    gh_items = fetch_github_trending()
    all_items.extend(gh_items)
    print(f"     ✓ {len(gh_items)} items")
    
    print("  🔴 Reddit...")
    rd_items = fetch_reddit_ai()
    all_items.extend(rd_items)
    print(f"     ✓ {len(rd_items)} items")
    
    print("  📰 TechCrunch...")
    tc_items = fetch_techcrunch_ai()
    all_items.extend(tc_items)
    print(f"     ✓ {len(tc_items)} items")
    
    print(f"\n✅ 共 {len(all_items)} 条热点")
    
    # 生成报告
    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    report_filename = f"report-{now.strftime('%Y-%m-%d-%H')}.html"
    
    print(f"\n📝 生成: {report_filename}")
    report_html = generate_report(all_items, now)
    report_path = work_dir / report_filename
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_html)
    print(f"   ✓ 已保存")
    
    # 更新索引
    print("\n📋 更新主页...")
    index_html = update_index(work_dir)
    with open(work_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"   ✓ 已更新")
    
    # 推送
    print("\n🚀 推送到 GitHub...")
    token = os.environ.get("GITHUB_TOKEN", "")
    
    import subprocess
    try:
        os.chdir(work_dir)
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", 
            f"https://hrhrng:{token}@github.com/hrhrng/claw-s-repo.git"], 
            capture_output=True)
        subprocess.run(["git", "add", "-A"], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Report: {now.strftime('%Y-%m-%d %H:%M')}"], capture_output=True)
        result = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], 
            capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ 推送成功")
        else:
            print(f"   ⚠️ {result.stderr[:100] if result.stderr else 'unknown'}")
    except Exception as e:
        print(f"   ✗ {e}")
    
    print("\n" + "="*50)
    print(f"🎉 完成: {report_filename}")
    print(f"🌐 https://hrhrng.github.io/claw-s-repo/{report_filename}")
    print("="*50)

if __name__ == "__main__":
    main()
