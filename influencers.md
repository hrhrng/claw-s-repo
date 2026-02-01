# AI 大 V 监控列表
# 每小时抓取这些账号的最新推文

# ============ Tier 1: 核心 (OpenAI, Anthropic, 顶级研究员) ============
TIER_1_CORE = [
    "@sama",              # Sam Altman - OpenAI CEO
    "@OpenAI",            # OpenAI 官方
    "@AnthropicAI",       # Anthropic 官方
    "@karpathy",          # Andrej Karpathy - AI 研究员, 前 Tesla AI Director
]

# ============ Tier 2: 研究界 (学者、顶级研究员) ============
TIER_2_RESEARCH = [
    "@AndrewYNg",         # Andrew Ng - DeepLearning.AI 创始人, 斯坦福教授
    "@ylecun",            # Yann LeCun - Meta AI 首席科学家, 图灵奖得主
    "@DrJimFan",          # Jim Fan - NVIDIA 高级研究科学家
    "@ilyasut",           # Ilya Sutskever - SSI (Safe Superintelligence) 创始人, OpenAI 联创
    "@lilianweng",        # Lilian Weng - OpenAI 安全团队负责人
    "@janleike",          # Jan Leike - 前 OpenAI 对齐团队负责人, Anthropic 现员工
    "@repligate",         # Janus - 知名 AI 研究者, 独立研究者
    "@SebastienBubeck",   # Sebastien Bubeck - 微软研究院, Phi 系列模型负责人
]

# ============ Tier 3: 产业界 (创业公司 CEO, 产品负责人) ============
TIER_3_INDUSTRY = [
    "@bindureddy",        # Bindu Reddy - Abacus AI CEO
    "@gdb",               # Greg Brockman - OpenAI 联创, 总裁
    "@alexandr_wang",     # Alexandr Wang - Scale AI 创始人
    "@hardmaru",          # David Ha - 谷歌大脑, 趣味 AI 项目专家
    "@demishassabis",     # Demis Hassabis - Google DeepMind CEO, 诺贝尔奖得主
    "@sundarpichai",      # Sundar Pichai - Google CEO
    "@elonmusk",          # Elon Musk - xAI 创始人, Tesla CEO
]

# ============ Tier 4: 中国 AI (国产模型) ============
TIER_4_CHINA = [
    "@deepseek_ai",       # DeepSeek 官方 - 国产大模型
]

# ============ Tier 5: 投资人 & 分析师 ============
TIER_5_ANALYSTS = [
    "@eladgil",           # Elad Gil - 知名投资人, 投资了 Airbnb, Coinbase, Figma 等
    "@paulg",             # Paul Graham - Y Combinator 联创
]

# ============ Tier 6: AI 安全 & 政策 ============
TIER_6_SAFETY = [
    "@nearcyan",          # Near - AI 安全研究者
]

# ============ 公司官方账号 ============
COMPANY_OFFICIAL = [
    "@GoogleDeepMind",    # Google DeepMind 官方
    "@GeminiApp",         # Google Gemini 官方
    "@xai",               # xAI 官方
    "@huggingface",       # Hugging Face 官方
]

# ============ 合并所有账号 ============
ALL_INFLUENCERS = (
    TIER_1_CORE + 
    TIER_2_RESEARCH + 
    TIER_3_INDUSTRY + 
    TIER_4_CHINA + 
    TIER_5_ANALYSTS +
    TIER_6_SAFETY +
    COMPANY_OFFICIAL
)

# 总共 25+ 位大 V
