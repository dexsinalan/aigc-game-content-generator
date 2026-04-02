# 从各个模型文件导入图像生成函数
from utils.models.ali_generator import generate_image_ali
from utils.models.baidu_generator import generate_image_baidu
from utils.models.zhipu_generator import generate_image_zhipu
from utils.models.xunfei_generator import generate_image_xunfei
from utils.models.claude_generator import generate_image_claude
from utils.models.gpt_generator import generate_image_gpt
from utils.models.deepseek_generator import generate_image_deepseek
from utils.models.silicon_generator import generate_image_silicon

# 图像生成预prompt定义
IMAGE_PROMPT = """请根据以下提示词生成游戏相关的图像：
{prompt}

要求：
1. 图像要与游戏相关，符合提示词的要求
2. 图像要清晰、细节丰富
3. 构图合理，色彩协调
4. 风格统一，符合游戏的整体风格

请生成并返回图像："""

def generate_image_for_model(prompt, model):
    """使用指定的模型生成图像"""
    # 构建完整的prompt
    full_prompt = IMAGE_PROMPT.format(prompt=prompt)
    
    if model == "百度文心一言":
        return generate_image_baidu(full_prompt)
    elif model == "阿里通义千问":
        return generate_image_ali(full_prompt)
    elif model == "智谱AI":
        return generate_image_zhipu(full_prompt)
    elif model == "讯飞星火":
        return generate_image_xunfei(full_prompt)
    elif model == "Claude":
        return generate_image_claude(full_prompt)
    elif model == "ChatGPT":
        return generate_image_gpt(prompt)
    elif model == "DeepSeek":
        return generate_image_deepseek(full_prompt)
    elif model == "硅基流动":
        return generate_image_silicon(full_prompt)
    else:
        return None, "不支持的模型"
