# 翻译生成器

from .models.ali_generator import translate_text_ali
from .models.baidu_generator import translate_text_baidu
from .models.zhipu_generator import translate_text_zhipu
from .models.xunfei_generator import translate_text_xunfei
from .models.claude_generator import translate_text_claude
from .models.gpt_generator import translate_text_gpt
from .models.deepseek_generator import translate_text_deepseek
from .models.silicon_generator import translate_text_silicon
from .prompt_templates import TRANSLATION_PROMPT

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

# 语言名称映射：中文 -> 英文
LANGUAGE_MAP = {
    "中文": "Chinese",
    "英文": "English",
    "日文": "Japanese",
    "韩文": "Korean",
    "法文": "French",
    "德文": "German",
    "西班牙文": "Spanish",
    "葡萄牙文": "Portuguese",
    "意大利文": "Italian",
    "俄文": "Russian",
    "阿拉伯文": "Arabic",
    "印地文": "Hindi",
    "越南文": "Vietnamese",
    "泰文": "Thai",
    "印尼文": "Indonesian",
    "马来文": "Malay",
    "土耳其文": "Turkish",
    "波兰文": "Polish"
}

def translate_text_for_model(text, target_language, model):
    """使用指定的模型翻译文本"""
    # 使用英文语言名称
    en_language = LANGUAGE_MAP.get(target_language, target_language)
    prompt = TRANSLATION_PROMPT.format(target_language=en_language, text=text)
    
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
    elif model == "ChatGPT":
        return translate_text_gpt(prompt)
    elif model == "DeepSeek":
        return translate_text_deepseek(prompt)
    elif model == "硅基流动":
        return translate_text_silicon(prompt)
    else:
        return None, "不支持的模型"
