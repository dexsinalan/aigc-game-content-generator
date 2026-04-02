# 翻译生成器

from models.ali_generator import translate_text_ali
from models.baidu_generator import translate_text_baidu
from models.zhipu_generator import translate_text_zhipu
from models.xunfei_generator import translate_text_xunfei
from models.claude_generator import translate_text_claude
from models.gpt_generator import translate_text_gpt
from models.deepseek_generator import translate_text_deepseek
from models.silicon_generator import translate_text_silicon

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    "中文": "zh",
    "英文": "en",
    "日文": "ja",
    "韩文": "ko",
    "法文": "fr",
    "德文": "de",
    "西班牙文": "es",
    "葡萄牙文": "pt",
    "意大利文": "it",
    "俄文": "ru",
    "阿拉伯文": "ar",
    "印地文": "hi",
    "越南文": "vi",
    "泰文": "th",
    "印尼文": "id",
    "马来文": "ms",
    "土耳其文": "tr",
    "波兰文": "pl"
}

# 语言代码到语言名称的映射
LANGUAGE_CODES = {v: k for k, v in SUPPORTED_LANGUAGES.items()}

def get_translation_prompt(text, target_language):
    """获取翻译提示词，包含游戏相关的偏向"""
    return f"""请将以下游戏相关文本翻译成{target_language}：
{text}

要求：
1. 准确翻译，保持原文意思
2. 只返回翻译结果，不要包含任何解释文字
3. 翻译结果要流畅自然，符合游戏语境
4. 对于游戏术语和专有名词，保持一致性
5. 考虑游戏本地化的特点，使翻译更符合目标语言玩家的习惯

请直接返回翻译结果："""

def translate_text_for_model(text, target_language, model):
    """使用指定的模型翻译文本"""
    prompt = get_translation_prompt(text, target_language)
    
    if model == "百度文心一言":
        return translate_text_baidu(prompt)
    elif model == "阿里通义千问":
        return translate_text_ali(prompt)
    elif model == "智谱AI":
        return translate_text_zhipu(prompt)
    elif model == "讯飞星火":
        return translate_text_xunfei(prompt)
    elif model == "Claude":
        return translate_text_claude(prompt)
    elif model == "GPT":
        return translate_text_gpt(prompt)
    elif model == "DeepSeek":
        return translate_text_deepseek(prompt)
    elif model == "硅基流动":
        return translate_text_silicon(prompt)
    else:
        return None, "不支持的模型"
