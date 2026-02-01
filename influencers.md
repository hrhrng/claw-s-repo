# AI 大 V 监控列表
# 每小时抓取这些账号的最新推文

TIER_1_CORE = [
    "@sama",           # Sam Altman - OpenAI CEO
    "@OpenAI",         # OpenAI 官方
    "@AnthropicAI",    # Anthropic 官方
    "@karpathy",       # Andrej Karpathy - AI 研究员
]

TIER_2_RESEARCH = [
    "@AndrewYNg",      # Andrew Ng - DeepLearning.AI 创始人
    "@ylecun",         # Yann LeCun - Meta AI 首席科学家
    "@DrJimFan",       # Jim Fan - NVIDIA 研究员
    "@ilyasut",        # Ilya Sutskever - SSI 创始人
]

TIER_3_INDUSTRY = [
    "@bindureddy",     # Bindu Reddy - Abacus AI CEO
    "@gdb",            # Greg Brockman - OpenAI 联创
    "@goodside",       # Riley Goodside - Prompt 工程专家
    "@mtfriese",       # Matthias Friese - AI 研究员
]

TIER_4_CHINA = [
    "@deepseek_ai",    # DeepSeek 官方
]

ALL_INFLUENCERS = TIER_1_CORE + TIER_2_RESEARCH + TIER_3_INDUSTRY + TIER_4_CHINA
