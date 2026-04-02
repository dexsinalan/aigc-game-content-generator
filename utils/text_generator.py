# 从各个模型文件导入文本生成函数
from utils.models.ali_generator import generate_text_ali
from utils.models.baidu_generator import generate_text_baidu
from utils.models.zhipu_generator import generate_text_zhipu
from utils.models.xunfei_generator import generate_text_xunfei
from utils.models.claude_generator import generate_text_claude
from utils.models.gpt_generator import generate_text_gpt
from utils.models.deepseek_generator import generate_text_deepseek
from utils.models.silicon_generator import generate_text_silicon

# 文本生成预prompt定义
TEXT_PROMPT = """请根据以下提示词生成游戏相关的文本内容：
{prompt}

要求：
1. 内容要与游戏相关，符合提示词的要求
2. 生成的内容要详细、丰富、有创意
3. 语言表达要流畅、自然
4. 不要包含任何无关的内容

请直接返回生成的文本内容："""

def generate_text_for_model(prompt, model):
    """使用指定的模型生成文本"""
    # 构建完整的prompt
    full_prompt = TEXT_PROMPT.format(prompt=prompt)
    
    if model == "百度文心一言":
        return generate_text_baidu(full_prompt)
    elif model == "阿里通义千问":
        return generate_text_ali(full_prompt)
    elif model == "智谱AI":
        return generate_text_zhipu(full_prompt)
    elif model == "讯飞星火":
        return generate_text_xunfei(full_prompt)
    elif model == "Claude":
        return generate_text_claude(full_prompt)
    elif model == "ChatGPT":
        return generate_text_gpt(full_prompt)
    elif model == "DeepSeek":
        return generate_text_deepseek(full_prompt)
    elif model == "硅基流动":
        return generate_text_silicon(full_prompt)
    else:
        return "不支持的模型"
