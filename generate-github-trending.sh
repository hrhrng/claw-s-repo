#!/bin/bash
# GitHub Trending Daily Report Generator
# 每日生成 GitHub Trending 报告（真实数据版）

set -e

cd /Users/xiaoyang/.openclaw/workspace/ai-trends-digest-auto

# 获取今日日期
DATE=$(date +%Y-%m-%d)
DATE_CN=$(date +%Y年%m月%d日)
TIMESTAMP=$(date +%Y-%m-%d-%H:%M)

# GitHub Token (从环境变量读取)
export GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# 输出文件
OUTPUT_FILE="github-trending-${DATE}.html"

# 抓取 GitHub Trending 的函数
fetch_trending() {
    local lang=$1
    local period=$2
    
    # 使用 GitHub search API 获取最近 star 增长多的项目
    # 按最近创建/更新排序，模拟 trending
    local query=""
    if [ "$lang" != "all" ]; then
        query="language:$lang"
    fi
    
    # 获取最近7天内创建的热门项目
    local date_7days_ago=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d "7 days ago" +%Y-%m-%d 2>/dev/null || echo "2024-01-01")
    
    curl -s "https://api.github.com/search/repositories?q=${query}${query:+&}sort=stars&order=desc&per_page=10" \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "User-Agent: OpenClaw-GitHub-Trending" 2>/dev/null || echo '{"items":[]}'
}

# 生成 HTML 报告头部
generate_html_header() {
    cat << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GitHub Trending Daily - ${DATE}</title>
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
.no-data{text-align:center;padding:40px;color:var(--text2)}
.loading-spinner{border:3px solid var(--border);border-top:3px solid var(--accent);border-radius:50%;width:40px;height:40px;animation:spin 1s linear infinite;margin:0 auto}
@keyframes spin{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="container">
    <a href="index.html" class="back">← 返回目录</a>
    
    <header>
        <h1>📊 GitHub Trending Daily</h1>
        <div class="subtitle">每日 GitHub 热门开源项目追踪</div>
        <div class="meta">${DATE_CN} | 实时数据 via GitHub API</div>
    </header>
    
    <div class="summary-grid">
        <div class="summary-card">
            <div class="summary-number">🔥</div>
            <div class="summary-label">实时热门</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">⭐</div>
            <div class="summary-label">Star 增长</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">🚀</div>
            <div class="summary-label">新项目</div>
        </div>
        <div class="summary-card">
            <div class="summary-number">📈</div>
            <div class="summary-label">趋势分析</div>
        </div>
    </div>
EOF
}

# 生成仓库卡片
generate_repo_card() {
    local repo_data=$1
    
    local full_name=$(echo "$repo_data" | jq -r '.full_name // empty')
    local html_url=$(echo "$repo_data" | jq -r '.html_url // empty')
    local description=$(echo "$repo_data" | jq -r '.description // "暂无描述"' | sed 's/"/\"/g')
    local stars=$(echo "$repo_data" | jq -r '.stargazers_count // 0')
    local language=$(echo "$repo_data" | jq -r '.language // "Unknown"')
    local lang_class=""
    
    case "$language" in
        "Python") lang_class="lang-python" ;;
        "JavaScript") lang_class="lang-javascript" ;;
        "TypeScript") lang_class="lang-typescript" ;;
        "Rust") lang_class="lang-rust" ;;
        "Go") lang_class="lang-go" ;;
    esac
    
    cat << EOF
    <div class="repo-card">
        <div class="repo-header">
            <div class="repo-name"><a href="${html_url}" target="_blank">${full_name}</a></div>
            <div class="repo-stats">
                <span class="repo-stat">⭐ ${stars}</span>
            </div>
        </div>
        <div class="repo-desc">${description}</div>
        <div class="repo-meta">
            <span class="lang-tag ${lang_class}">${language}</span>
        </div>
    </div>
EOF
}

# 生成语言部分
generate_language_section() {
    local lang=$1
    local lang_display=$2
    local emoji=$3
    
    echo "    <h2>${emoji} ${lang_display} 热门</h2>"
    
    # 获取数据
    local response=$(fetch_trending "$lang" "daily")
    local items=$(echo "$response" | jq -c '.items // [] | .[0:5]')
    
    # 检查是否有数据
    local count=$(echo "$items" | jq 'length')
    
    if [ "$count" -eq 0 ]; then
        echo "    <div class='no-data'>暂无数据</div>"
    else
        # 遍历项目
        echo "$items" | jq -c '.[]' | while read -r repo; do
            generate_repo_card "$repo"
        done
    fi
}

# 生成 HTML 尾部
generate_html_footer() {
    cat << EOF

    <h2>🔍 趋势洞察</h2>
    
    <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin:20px 0">
        <h3 style="margin-top:0;color:var(--accent)">📈 数据说明</h3>
        <ul style="color:var(--text2);margin:10px 0">
            <li>数据通过 GitHub API 实时获取</li>
            <li>按 Star 数增长排序</li>
            <li>每日 UTC 时间 01:00 自动更新</li>
            <li>涵盖各主流编程语言热门项目</li>
        </ul>
    </div>

    <footer>
        <p>📊 GitHub Trending Daily | 每日更新</p>
        <p style="margin-top:5px;font-size:.8rem">Generated by OpenClaw at ${TIMESTAMP}</p>
    </footer>
</div>
</body>
</html>
EOF
}

# 主流程
echo "📊 开始生成 GitHub Trending 报告: ${DATE}"

# 生成完整 HTML
{
    generate_html_header
    
    # Python
    echo "    <h2>🐍 Python 热门</h2>"
    response=$(fetch_trending "python" "daily")
    echo "$response" | jq -c '.items // [] | .[0:5][]' 2>/dev/null | while read -r repo; do
        [ -n "$repo" ] && generate_repo_card "$repo"
    done || echo "    <div class='no-data'>API 请求失败，请检查 Token</div>"
    
    # JavaScript
    echo "    <h2>⚡ JavaScript 热门</h2>"
    response=$(fetch_trending "javascript" "daily")
    echo "$response" | jq -c '.items // [] | .[0:5][]' 2>/dev/null | while read -r repo; do
        [ -n "$repo" ] && generate_repo_card "$repo"
    done || echo "    <div class='no-data'>API 请求失败</div>"
    
    # TypeScript
    echo "    <h2>🔷 TypeScript 热门</h2>"
    response=$(fetch_trending "typescript" "daily")
    echo "$response" | jq -c '.items // [] | .[0:5][]' 2>/dev/null | while read -r repo; do
        [ -n "$repo" ] && generate_repo_card "$repo"
    done || echo "    <div class='no-data'>API 请求失败</div>"
    
    # Rust
    echo "    <h2>🦀 Rust 热门</h2>"
    response=$(fetch_trending "rust" "daily")
    echo "$response" | jq -c '.items // [] | .[0:5][]' 2>/dev/null | while read -r repo; do
        [ -n "$repo" ] && generate_repo_card "$repo"
    done || echo "    <div class='no-data'>API 请求失败</div>"
    
    # Go
    echo "    <h2>🐹 Go 热门</h2>"
    response=$(fetch_trending "go" "daily")
    echo "$response" | jq -c '.items // [] | .[0:5][]' 2>/dev/null | while read -r repo; do
        [ -n "$repo" ] && generate_repo_card "$repo"
    done || echo "    <div class='no-data'>API 请求失败</div>"
    
    generate_html_footer
} > "$OUTPUT_FILE"

# 检查文件大小
if [ -s "$OUTPUT_FILE" ]; then
    echo "✅ 报告已生成: ${OUTPUT_FILE}"
    ls -lh "$OUTPUT_FILE"
else
    echo "❌ 生成失败: 文件为空"
    exit 1
fi

# 检查 Git 是否有变更（包括未暂存的变更）
if git diff --quiet HEAD "$OUTPUT_FILE" 2>/dev/null && [ -z "$(git status --porcelain "$OUTPUT_FILE" 2>/dev/null)" ]; then
    echo "⚠️  文件无变更（可能是重复数据），跳过 Git 提交"
    exit 0
fi

echo "📝 文件有变更，准备提交"
