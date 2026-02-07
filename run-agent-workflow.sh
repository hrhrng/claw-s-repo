#!/bin/bash
# AI Trends Digest - Agent 驱动工作流
# Agent 收到任务后执行此脚本，但也可以自主决定流程

set -e

cd /Users/xiaoyang/.openclaw/workspace/ai-trends-digest-auto

TIMESTAMP=$(date +%Y-%m-%d-%H)
DATA_FILE="data/raw_${TIMESTAMP}.json"
REPORT_FILE="reports/ai-trends-${TIMESTAMP}.html"

echo "🚀 AI Trends 任务开始: ${TIMESTAMP}"

# 1. 抓取数据
echo "📥 抓取 X 平台数据..."
python3 ../skills/ai-trends-digest/scripts/fetch_tweets.py \
    --output "${DATA_FILE}" \
    --hours 3

if [ ! -f "${DATA_FILE}" ]; then
    echo "❌ 数据抓取失败"
    exit 1
fi

TWEET_COUNT=$(cat "${DATA_FILE}" | python3 -c "import json,sys; print(json.load(sys.stdin).get('total_tweets',0))")
echo "✅ 抓取完成: ${TWEET_COUNT} 条推文"

if [ "$TWEET_COUNT" -eq 0 ]; then
    echo "⚠️  无新数据，任务结束"
    exit 0
fi

# 2. Agent 分析并生成报告
echo "🤖 等待 Agent 分析数据并生成报告..."
echo "   提示: Agent 应读取 ${DATA_FILE} 和 ../skills/ai-trends-digest/templates/report_framework.html"
echo "   生成报告保存到: ${REPORT_FILE}"

# 注意：实际报告生成由 Agent 完成，不在这里自动化
# Agent 应该：
# - 读取抓取的 JSON 数据
# - 分析推文内容
# - 基于 report_framework.html 生成 HTML
# - 填充 hot_topics, key_insights, trend_analysis, highlights

# 3. 检查报告是否生成
if [ ! -f "${REPORT_FILE}" ]; then
    echo "⏳ 报告尚未生成，请 Agent 完成生成后继续"
    exit 0
fi

echo "✅ 报告已生成: ${REPORT_FILE}"

# 4. Agent 更新索引
echo "📇 等待 Agent 更新索引页..."
echo "   提示: Agent 应基于 ../skills/ai-trends-digest/templates/index_framework.html 生成 index.html"

# 5. Git 提交（如果有变更）
if git diff --quiet HEAD 2>/dev/null && git diff --staged --quiet 2>/dev/null; then
    echo "⚠️  无文件变更，跳过 Git 提交"
else
    echo "☁️  推送至 Git..."
    git add -A
    git commit -m "AI Trends: ${TIMESTAMP}" || true
    git push
    echo "✅ 已推送"
fi

echo "✅ 工作流完成: ${TIMESTAMP}"
