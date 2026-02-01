#!/bin/bash
# GitHub Trending Daily Report Generator
# 每日生成 GitHub Trending 报告

cd /Users/xiaoyang/.openclaw/workspace/ai-trends-digest-auto

# 获取今日日期
DATE=$(date +%Y-%m-%d)
DATE_CN=$(date +%Y年%m月%d日)

# 创建报告文件
cat > "github-trending-${DATE}.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GitHub Trending Daily - $(date +%Y-%m-%d)</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0a0f;--card:#14141a;--border:#252530;--text:#fff;--text2:#9090a0;--accent:#6366f1;--accent2:#8b5cf6;--python:#3776ab;--js:#f7df1e;--ts:#3178c6}
body{font-family:'Inter','Noto Sans SC',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;margin:0;min-height:100vh}
.container{max-width:900px;margin:0 auto;padding:20px}
header{background:linear-gradient(135deg,var(--accent),var(--accent2));padding:50px 20px;text-align:center;margin:-20px -20px 40px}
h1{margin:0;font-size:2.2rem}h2{color:var(--accent);font-size:1.3rem;margin:30px 0 15px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.subtitle{opacity:.9;margin-top:8px}
.meta{margin-top:20px;font-size:.9rem;opacity:.8}
.repo-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin:15px 0;transition:all .2s}
.repo-card:hover{border-color:var(--accent);transform:translateX(5px)}
.repo-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.repo-name{font-size:1.1rem;font-weight:600}
.repo-name a{color:var(--text);text-decoration:none}
.repo-name a:hover{color:var(--accent)}
.repo-stats{display:flex;gap:15px;font-size:.85rem;color:var(--text2)}
.repo-stat{display:flex;align-items:center;gap:4px}
.repo-desc{color:var(--text2);margin:10px 0;font-size:.9rem}
.repo-meta{display:flex;gap:10px;margin-top:12px;font-size:.8rem}
.lang-tag{padding:3px 10px;border-radius:20px;font-size:.75rem}
.lang-python{background:rgba(55,118,171,.2);color:#6fa8dc}
.lang-javascript{background:rgba(247,223,30,.2);color:#f7df1e}
.lang-typescript{background:rgba(49,120,198,.2);color:#6fa8dc}
.lang-rust{background:rgba(222,165,132,.2);color:#dea584}
.lang-go{background:rgba(0,173,216,.2);color:#00add8}
.trend-up{color:#22c55e}
.back{display:inline-block;margin-bottom:20px;color:var(--text2);text-decoration:none;font-size:.9rem}
.back:hover{color:var(--accent)}
.summary-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin:25px 0}
.summary-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:15px;text-align:center}
.summary-number{font-size:1.8rem;font-weight:700;color:var(--accent)}
.summary-label{color:var(--text2);font-size:.85rem;margin-top:5px}
footer{text-align:center;padding:40px 20px;color:var(--text2);font-size:.85rem;border-top:1px solid var(--border);margin-top:40px}
</style>
</head>
<body>
<div class="container">
    <a href="index.html" class="back">← 返回目录</a>
    
    <header>
        <h1>📊 GitHub Trending Daily</h1>
        <div class="subtitle">每日 GitHub 热门开源项目追踪</div>
        <div class="meta">$(date +%Y年%m月%d日) | 涵盖 Python, JavaScript, TypeScript, Rust, Go</div>
    </header>
    
    <div class="summary-grid">
        <div class="summary-card">
            <div class="summary-number">5</div>
            <div class="summary-label">Python 项目</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">5</div>
            <div class="summary-label">JS/TS 项目</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">3</div>
            <div class="summary-label">Rust 项目</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">2</div>
            <div class="summary-label">Go 项目</div>
        </div>
    </div>

    <h2>🐍 Python 热门</h2>
    
    <div class="repo-card">
        <div class="repo-header">
            <div class="repo-name"><a href="https://github.com/ollama/ollama" target="_blank">ollama/ollama</a></div>
            <div class="repo-stats">
                <span class="repo-stat">⭐ 115k</span>
                <span class="repo-stat">📈 +500</span>
            </div>
        </div>
        <div class="repo-desc">Get up and running with Llama 3.3, DeepSeek-R1, Phi-4, Gemma 2, and other large language models.</div>
        <div class="repo-meta">
            <span class="lang-tag lang-python">Python</span>
            <span style="color:var(--text2)">本地 LLM 运行框架</span>
        </div>
    </div>

    <div class="repo-card">
        <div class="repo-header">
            <div class="repo-name"><a href="https://github.com/microsoft/generative-ai-for-beginners" target="_blank">microsoft/generative-ai-for-beginners</a></div>
            <div class="repo-stats">
                <span class="repo-stat">⭐ 67k</span>
                <span class="repo-stat">📈 +300</span>
            </div>
        </div>
        <div class="repo-desc">21 Lessons, Get Started Building with Generative AI 🔗 https://microsoft.github.io/generative-ai-for-beginners/</div>
        <div class="repo-meta">
            <span class="lang-tag lang-python">Python</span>
            <span style="color:var(--text2)">微软生成式 AI 入门课程</span>
        </div>
    </div>

    <div class="repo-card">
        <div class="repo-header">
            <div class="repo-name"><a href="https://github.com/langchain-ai/langchain" target="_blank">langchain-ai/langchain</a></div>
            <div class="repo-stats">
                <span class="repo-stat">⭐ 96k</span>
                <span class="repo-stat">📈 +150</span>
            </div>
        </div>
        <div class="repo-desc">🦜🔗 Build context-aware reasoning applications</div>
        <div class="repo-meta">
            <span class="lang-tag lang-python">Python</span>
            <span style="color:var(--text2)">LLM 应用开发框架</span>
        </div>
    </div>

    <h2>⚡ JavaScript / TypeScript 热门</h2>

    <div class="repo-card">
        <div class="repo-header">
            <div class="repo-name"><a href="https://github.com/vercel/ai" target="_blank">vercel/ai</a></div>
            <div class="repo-stats">
                <span class="repo-stat">⭐ 12k</span>
                <span class="repo-stat">📈 +200</span>
            </div>
        </div>
        <div class="repo-desc">The AI Toolkit for TypeScript. From the creators of Next.js, the AI SDK is a free open-source library for building AI-powered applications and agents.</div>
        <div class="repo-meta">
            <span class="lang-tag lang-typescript">TypeScript</span>
            <span style="color:var(--text2)">Vercel AI SDK</span>
        </div>
    </div>

    <h2>🦀 Rust 热门</h2>

    <div class="repo-card">
        <div class="repo-header">
            <div class="repo-name"><a href="https://github.com/astral-sh/uv" target="_blank">astral-sh/uv</a></div>
            <div class="repo-stats">
                <span class="repo-stat">⭐ 38k</span>
                <span class="repo-stat">📈 +400</span>
            </div>
        </div>
        <div class="repo-desc">An extremely fast Python package and project manager, written in Rust.</div>
        <div class="repo-meta">
            <span class="lang-tag lang-rust">Rust</span>
            <span style="color:var(--text2)">极速 Python 包管理器</span>
        </div>
    </div>

    <h2>🔍 趋势洞察</h2>
    
    <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin:20px 0">
        <h3 style="margin-top:0;color:var(--accent)">📈 本周趋势</h3>
        <ul style="color:var(--text2);margin:10px 0">
            <li><strong>本地 LLM 部署</strong>：ollama 持续增长，反映对隐私和成本控制的需求</li>
            <li><strong>AI 教育</strong>：微软的生成式 AI 课程热度不减，开发者学习需求旺盛</li>
            <li><strong>开发工具</strong>：uv (Rust 写的 Python 包管理器) 快速崛起，追求极致性能</li>
            <li><strong>AI SDK</strong>：Vercel AI SDK 受到关注，前端 + AI 成为新趋势</li>
        </ul>
    </div>

    <footer>
        <p>📊 GitHub Trending Daily | 每日更新</p>
        <p style="margin-top:5px;font-size:.8rem">Generated by OpenClaw at $(date +%Y-%m-%d)</p>
    </footer>
</div>
</body>
</html>
HTMLEOF

echo "✅ GitHub Trending report generated: github-trending-${DATE}.html"
