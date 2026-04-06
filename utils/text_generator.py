# 从各个模型文件导入文本生成函数
import time
from utils.models.ali_generator import generate_text_ali
from utils.models.baidu_generator import generate_text_baidu
from utils.models.zhipu_generator import generate_text_zhipu
from utils.models.xunfei_generator import generate_text_xunfei
from utils.models.claude_generator import generate_text_claude
from utils.models.gpt_generator import generate_text_gpt
from utils.models.deepseek_generator import generate_text_deepseek
from utils.models.silicon_generator import generate_text_silicon
from utils.prompt_templates import TEXT_PROMPT

def generate_text_for_model(prompt, model):
    """使用指定的模型生成文本"""
    # 构建完整的prompt
    full_prompt = TEXT_PROMPT.format(prompt=prompt)
    
    # 开始计时
    start_time = time.time()
    
    result = None
    tokens = 0
    
    if model == "百度文心一言":
        result = generate_text_baidu(full_prompt)
    elif model == "阿里通义千问":
        result = generate_text_ali(full_prompt)
    elif model == "智谱AI":
        result = generate_text_zhipu(full_prompt)
    elif model == "讯飞星火":
        result = generate_text_xunfei(full_prompt)
    elif model == "Claude":
        result = generate_text_claude(full_prompt)
    elif model == "ChatGPT":
        result = generate_text_gpt(full_prompt)
    elif model == "DeepSeek":
        result = generate_text_deepseek(full_prompt)
    elif model == "硅基流动":
        result = generate_text_silicon(full_prompt)
    else:
        result = "不支持的模型"
    
    # 结束计时
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # 计算Token消耗（简化计算，实际应该根据模型返回的使用情况）
    # 这里使用一个简单的估算：每个中文字符算3个Token，每个英文字符算1.5个Token
    if isinstance(result, str):
        # 计算中文字符数
        chinese_chars = sum(1 for char in result if '\u4e00' <= char <= '\u9fff')
        # 计算英文字符数
        english_chars = sum(1 for char in result if 'a' <= char.lower() <= 'z')
        # 计算其他字符数
        other_chars = len(result) - chinese_chars - english_chars
        # 估算Token数
        tokens = chinese_chars * 3 + int(english_chars * 1.5) + other_chars
    
    return result, elapsed_time, tokens
