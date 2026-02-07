#!/bin/bash
# AI Trends Digest 完整工作流脚本
# 正确处理无数据、Git提交等边界情况

set -e

cd /Users/xiaoyang/.openclaw/workspace/ai-trends-digest-auto

# 设置认证
export X_AUTH_TOKEN="${X_AUTH_TOKEN:-cf917b45b964e91156debf72a444a2f237bb46f5}"
export X_CT0_TOKEN="${X_CT0_TOKEN:-a5e8b160594fc409fb0a04f1f9895a5f0f24b8e9f5ec52034ae014e6ca01142e436c069f90810647d7f9b515c99cff55b32008cc18cae4f0c6a9254e1a3c167186b550ab6011ac2f22cdb67ea11f7132}"

TIMESTAMP=$(date +%Y-%m-%d-%H)
DATA_FILE="data.json"

echo "🚀 开始 AI Trends Digest 任务 - ${TIMESTAMP}"

# 1. 抓取数据
echo "📥 抓取推文数据..."
python3 ../skills/ai-trends-digest/scripts/fetch_tweets.py -o "${DATA_FILE}"
FETCH_EXIT=$?

# 检查退出码
if [ $FETCH_EXIT -eq 2 ]; then
    echo "⚠️  本时段无新内容，跳过报告生成"
    exit 0
fi

if [ $FETCH_EXIT -ne 0 ]; then
    echo "❌ 抓取失败，退出码: $FETCH_EXIT"
    exit 1
fi

# 2. 生成报告
echo "📝 生成报告..."
python3 ../skills/ai-trends-digest/scripts/generate_report_v2.py \
    -d "${DATA_FILE}" \
    -o reports/ \
    -t ../skills/ai-trends-digest/templates

# 检查报告是否生成成功
REPORT_EXIT=$?
if [ $REPORT_EXIT -eq 2 ]; then
    echo "⚠️  无有效内容，跳过后续步骤"
    exit 0
fi

if [ $REPORT_EXIT -ne 0 ]; then
    echo "❌ 报告生成失败"
    exit 1
fi

# 3. 更新索引
echo "📇 更新索引..."
python3 ../skills/ai-trends-digest/scripts/generate_index.py \
    -r reports/ \
    -t ../skills/ai-trends-digest/templates \
    -o index.html

# 4. 检查是否有变更需要提交
if git diff --quiet HEAD && git diff --staged --quiet; then
    echo "⚠️  无文件变更，跳过 Git 提交"
    exit 0
fi

# 5. Git 提交和推送
echo "☁️  推送至 Git..."
git add -A
git commit -m "AI Trends: ${TIMESTAMP}" || true
git push

echo "✅ 任务完成: ${TIMESTAMP}"
