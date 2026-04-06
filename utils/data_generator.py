import json
import os
import time
import pandas as pd
from io import BytesIO
# 从各个模型文件导入文本生成和数据生成函数
from utils.models.ali_generator import generate_text_ali, generate_data_ali
from utils.models.baidu_generator import generate_text_baidu, generate_data_baidu
from utils.models.zhipu_generator import generate_text_zhipu, generate_data_zhipu
from utils.models.xunfei_generator import generate_text_xunfei, generate_data_xunfei
from utils.models.claude_generator import generate_text_claude, generate_data_claude
from utils.models.gpt_generator import generate_text_gpt, generate_data_gpt
from utils.models.deepseek_generator import generate_text_deepseek, generate_data_deepseek
from utils.models.silicon_generator import generate_text_silicon, generate_data_silicon
from utils.prompt_templates import JSON_PROMPT, XLSX_PROMPT, MINDMAP_PROMPT

def generate_text_for_data(prompt, model):
    """使用指定的模型生成文本数据"""
    if model == "百度文心一言":
        return generate_text_baidu(prompt)
    elif model == "阿里通义千问":
        return generate_text_ali(prompt)
    elif model == "智谱AI":
        return generate_text_zhipu(prompt)
    elif model == "讯飞星火":
        return generate_text_xunfei(prompt)
    elif model == "Claude":
        return generate_text_claude(prompt)
    elif model == "ChatGPT":
        return generate_text_gpt(prompt)
    elif model == "DeepSeek":
        return generate_text_deepseek(prompt)
    elif model == "硅基流动":
        return generate_text_silicon(prompt)
    else:
        return "不支持的模型"

def generate_data_for_model(prompt, model, data_type):
    """使用指定的模型生成数据"""
    # 根据数据类型选择对应的预prompt
    if data_type == "JSON":
        data_prompt = JSON_PROMPT.format(prompt=prompt)
    elif data_type == "XLSX":
        data_prompt = XLSX_PROMPT.format(prompt=prompt)
    elif data_type == "mindmap":
        data_prompt = MINDMAP_PROMPT.format(prompt=prompt)
    else:
        return None, "不支持的数据类型", 0, 0
    
    # 开始计时
    start_time = time.time()
    
    result = None
    filename = None
    tokens = 0
    
    if model == "百度文心一言":
        result, filename = generate_data_baidu(data_prompt, data_type)
    elif model == "阿里通义千问":
        result, filename = generate_data_ali(data_prompt, data_type)
    elif model == "智谱AI":
        result, filename = generate_data_zhipu(data_prompt, data_type)
    elif model == "讯飞星火":
        result, filename = generate_data_xunfei(data_prompt, data_type)
    elif model == "Claude":
        result, filename = generate_data_claude(data_prompt, data_type)
    elif model == "ChatGPT":
        result, filename = generate_data_gpt(data_prompt, data_type)
    elif model == "DeepSeek":
        result, filename = generate_data_deepseek(data_prompt, data_type)
    elif model == "硅基流动":
        result, filename = generate_data_silicon(data_prompt, data_type)
    else:
        return None, "不支持的模型", 0, 0
    
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
    elif isinstance(result, dict) or isinstance(result, list):
        # 对于JSON数据，将其转换为字符串后计算
        result_str = json.dumps(result, ensure_ascii=False)
        chinese_chars = sum(1 for char in result_str if '\u4e00' <= char <= '\u9fff')
        english_chars = sum(1 for char in result_str if 'a' <= char.lower() <= 'z')
        other_chars = len(result_str) - chinese_chars - english_chars
        tokens = chinese_chars * 3 + int(english_chars * 1.5) + other_chars
    elif isinstance(result, pd.DataFrame):
        # 对于DataFrame，将其转换为字符串后计算
        result_str = result.to_string()
        chinese_chars = sum(1 for char in result_str if '\u4e00' <= char <= '\u9fff')
        english_chars = sum(1 for char in result_str if 'a' <= char.lower() <= 'z')
        other_chars = len(result_str) - chinese_chars - english_chars
        tokens = chinese_chars * 3 + int(english_chars * 1.5) + other_chars
    
    return result, filename, elapsed_time, tokens

def generate_json_data(prompt, model):
    """生成JSON格式的数据"""
    return generate_data_for_model(prompt, model, "JSON")

def generate_xlsx_data(prompt, model):
    """生成Excel格式的数据"""
    return generate_data_for_model(prompt, model, "XLSX")

def generate_mindmap_data(prompt, model):
    """生成mindmap思维导图格式的数据"""
    return generate_data_for_model(prompt, model, "mindmap")

# 辅助函数：将文本思维导图转换为mindmap文件
def convert_text_to_mindmap(text_content, output_path):
    """将文本格式的思维导图转换为mindmap文件"""
    try:
        # 这里需要安装xmind库
        # pip install xmind
        try:
            import xmind
        except ImportError:
            return False, "请先安装xmind库：pip install xmind"
        
        # 创建工作簿
        workbook = xmind.load(output_path)
        sheet = workbook.getPrimarySheet()
        sheet.setTitle("生成的思维导图")
        
        # 解析文本并构建思维导图
        root_topic = sheet.getRootTopic()
        lines = text_content.strip().split('\n')
        
        if lines:
            root_topic.setTitle(lines[0].strip('- '))
            
            current_topic = root_topic
            previous_level = 0
            topic_stack = [root_topic]
            
            for line in lines[1:]:
                if not line.strip():
                    continue
                
                # 计算缩进级别
                stripped_line = line.lstrip()
                indent = len(line) - len(stripped_line)
                level = indent // 2
                
                # 添加子主题
                if level > previous_level:
                    # 添加为当前主题的子主题
                    sub_topic = current_topic.addSubTopic()
                    sub_topic.setTitle(stripped_line.strip('- '))
                    topic_stack.append(sub_topic)
                    current_topic = sub_topic
                elif level == previous_level:
                    # 添加为同级主题
                    if len(topic_stack) > 1:
                        topic_stack.pop()
                    parent = topic_stack[-1]
                    sub_topic = parent.addSubTopic()
                    sub_topic.setTitle(stripped_line.strip('- '))
                    topic_stack.append(sub_topic)
                    current_topic = sub_topic
                else:
                    # 回到上级
                    while len(topic_stack) > level + 1:
                        topic_stack.pop()
                    parent = topic_stack[-1]
                    sub_topic = parent.addSubTopic()
                    sub_topic.setTitle(stripped_line.strip('- '))
                    topic_stack.append(sub_topic)
                    current_topic = sub_topic
                
                previous_level = level
        
        # 保存文件
        xmind.save(workbook, output_path)
        return True, output_path
        
    except Exception as e:
        return False, f"转换失败：{str(e)}"
