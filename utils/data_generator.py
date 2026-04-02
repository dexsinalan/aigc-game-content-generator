import json
import os
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
    elif model == "GPT":
        return generate_text_gpt(prompt)
    elif model == "DeepSeek":
        return generate_text_deepseek(prompt)
    elif model == "硅基流动":
        return generate_text_silicon(prompt)
    else:
        return "不支持的模型"

def generate_data_for_model(prompt, model, data_type):
    """使用指定的模型生成数据"""
    if model == "百度文心一言":
        return generate_data_baidu(prompt, data_type)
    elif model == "阿里通义千问":
        return generate_data_ali(prompt, data_type)
    elif model == "智谱AI":
        return generate_data_zhipu(prompt, data_type)
    elif model == "讯飞星火":
        return generate_data_xunfei(prompt, data_type)
    elif model == "Claude":
        return generate_data_claude(prompt, data_type)
    elif model == "GPT":
        return generate_data_gpt(prompt, data_type)
    elif model == "DeepSeek":
        return generate_data_deepseek(prompt, data_type)
    elif model == "硅基流动":
        return generate_data_silicon(prompt, data_type)
    else:
        return None, "不支持的模型"

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
