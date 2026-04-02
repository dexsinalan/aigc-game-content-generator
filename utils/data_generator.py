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

# 预prompt定义
JSON_PROMPT = """请根据以下描述生成JSON数据：
{prompt}

要求：
1. 只返回JSON数据，不要包含任何解释文字
2. 确保JSON格式正确，可以被Python的json.loads()解析
3. 数据应该包含合理的字段和示例数据
4. 如果是表格数据，使用数组格式，数据量根据用戶要求而定

请直接返回JSON数据："""

XLSX_PROMPT = """请根据以下描述生成表格数据，并返回JSON数组格式：
{prompt}

要求：
1. 返回JSON数组格式，每个元素是一个对象，代表一行数据
2. 确保所有对象具有相同的字段
3. 只返回JSON数组，不要包含任何解释文字
4. 数据量根据用戶要求而定

请直接返回JSON数组："""

MINDMAP_PROMPT = """请根据以下描述生成思维导图数据，使用Markdown列表格式：
{prompt}

要求：
1. 使用Markdown列表格式（- 和缩进）
2. 第一行是中心主题
3. 使用2个空格作为缩进表示层级关系
4. 包含多个主要分支，每个分支可以有多个子节点
5. 只返回思维导图内容，不要包含任何解释文字
6. 确保格式干净，没有多余的空行或注释

示例格式：
游戏设计
- 角色系统
  - 战士
  - 法师
  - 弓箭手
- 战斗系统
  - 回合制
  - 实时战斗
- 任务系统
  - 主线任务
  - 支线任务

请直接返回思维导图内容："""

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
    # 根据数据类型选择对应的预prompt
    if data_type == "JSON":
        data_prompt = JSON_PROMPT.format(prompt=prompt)
    elif data_type == "XLSX":
        data_prompt = XLSX_PROMPT.format(prompt=prompt)
    elif data_type == "mindmap":
        data_prompt = MINDMAP_PROMPT.format(prompt=prompt)
    else:
        return None, "不支持的数据类型"
    
    if model == "百度文心一言":
        return generate_data_baidu(data_prompt, data_type)
    elif model == "阿里通义千问":
        return generate_data_ali(data_prompt, data_type)
    elif model == "智谱AI":
        return generate_data_zhipu(data_prompt, data_type)
    elif model == "讯飞星火":
        return generate_data_xunfei(data_prompt, data_type)
    elif model == "Claude":
        return generate_data_claude(data_prompt, data_type)
    elif model == "GPT":
        return generate_data_gpt(data_prompt, data_type)
    elif model == "DeepSeek":
        return generate_data_deepseek(data_prompt, data_type)
    elif model == "硅基流动":
        return generate_data_silicon(data_prompt, data_type)
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
