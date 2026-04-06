# 从各个模型文件导入图像生成函数
import time
from utils.models.ali_generator import generate_image_ali
from utils.models.baidu_generator import generate_image_baidu
from utils.models.zhipu_generator import generate_image_zhipu
from utils.models.xunfei_generator import generate_image_xunfei
from utils.models.claude_generator import generate_image_claude
from utils.models.gpt_generator import generate_image_gpt
from utils.models.deepseek_generator import generate_image_deepseek
from utils.models.silicon_generator import generate_image_silicon
from utils.prompt_templates import IMAGE_PROMPT

def generate_image_for_model(prompt, model):
    """使用指定的模型生成图像"""
    # 构建完整的prompt
    full_prompt = IMAGE_PROMPT.format(prompt=prompt)
    
    # 开始计时
    start_time = time.time()
    
    result = None
    tokens = 0
    
    if model == "百度文心一言":
        result = generate_image_baidu(full_prompt)
    elif model == "阿里通义千问":
        result = generate_image_ali(full_prompt)
    elif model == "智谱AI":
        result = generate_image_zhipu(full_prompt)
    elif model == "讯飞星火":
        result = generate_image_xunfei(full_prompt)
    elif model == "Claude":
        result = generate_image_claude(full_prompt)
    elif model == "ChatGPT":
        result = generate_image_gpt(full_prompt)
    elif model == "DeepSeek":
        result = generate_image_deepseek(full_prompt)
    elif model == "硅基流动":
        result = generate_image_silicon(full_prompt)
    else:
        result = "不支持的模型"
    
    # 结束计时
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # 计算Token消耗（简化计算，实际应该根据模型返回的使用情况）
    # 对于图像生成，我们使用一个固定的估算值
    tokens = 2000  # 假设图像生成消耗约2000个Token
    
    return result, elapsed_time, tokens
