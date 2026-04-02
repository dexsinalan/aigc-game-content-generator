import json
import os
import pandas as pd
from io import BytesIO
from utils.text_generator import generate_text_baidu, generate_text_ali, generate_text_zhipu, generate_text_xunfei

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
    else:
        return "不支持的模型"

def generate_json_data(prompt, model):
    """生成JSON格式的数据"""
    try:
        # 构建提示词，要求AI生成JSON格式的数据
        json_prompt = f"""请根据以下描述生成JSON格式的数据：
{prompt}

要求：
1. 只返回JSON数据，不要包含任何解释文字
2. 确保JSON格式正确，可以被Python的json.loads()解析
3. 数据应该包含合理的字段和示例数据
4. 如果是表格数据，使用数组格式，数据量根据用戶要求而定


请直接返回JSON数据："""
        
        # 调用文本生成
        result = generate_text_for_data(json_prompt, model)
        
        # 尝试解析JSON
        try:
            # 清理可能的Markdown代码块标记
            if result.startswith('```json'):
                result = result[7:]
            if result.startswith('```'):
                result = result[3:]
            if result.endswith('```'):
                result = result[:-3]
            
            result = result.strip()
            data = json.loads(result)
            return data, f"generated_data_{model}.json"
        except json.JSONDecodeError as e:
            # 如果解析失败，返回错误信息
            return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"

def generate_xlsx_data(prompt, model):
    """生成Excel格式的数据"""
    try:
        # 构建提示词，要求AI生成表格数据
        xlsx_prompt = f"""请根据以下描述生成表格数据，并返回JSON数组格式：
{prompt}

要求：
1. 返回JSON数组格式，每个元素是一个对象，代表一行数据
2. 确保所有对象具有相同的字段
3. 只返回JSON数组，不要包含任何解释文字
4. 数据量根据用戶要求而定


请直接返回JSON数组："""
        
        # 调用文本生成
        result = generate_text_for_data(xlsx_prompt, model)
        
        # 尝试解析JSON
        try:
            # 清理可能的Markdown代码块标记
            if result.startswith('```json'):
                result = result[7:]
            if result.startswith('```'):
                result = result[3:]
            if result.endswith('```'):
                result = result[:-3]
            
            result = result.strip()
            data_list = json.loads(result)
            
            # 转换为DataFrame
            if isinstance(data_list, list) and len(data_list) > 0:
                df = pd.DataFrame(data_list)
                return df, f"generated_data_{model}.xlsx"
            else:
                return None, "生成的数据格式不正确，应该是一个数组"
                
        except json.JSONDecodeError as e:
            # 如果解析失败，返回错误信息
            return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"

def generate_xmind_data(prompt, model):
    """生成XMind思维导图格式的数据"""
    try:
        # 构建提示词，要求AI生成思维导图数据
        xmind_prompt = f"""请根据以下描述生成思维导图数据，使用Markdown列表格式：
{prompt}

要求：
1. 使用Markdown列表格式（- 和缩进）
2. 第一行是中心主题
3. 使用缩进表示层级关系
4. 包含至少3个主要分支，每个分支有2-3个子节点
5. 只返回思维导图内容，不要包含任何解释文字

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
        
        # 调用文本生成
        result = generate_text_for_data(xmind_prompt, model)
        
        # 返回文本格式的思维导图数据
        # 注意：这里返回的是文本格式，实际使用时可以转换为.xmind文件
        return result, f"generated_mindmap_{model}.txt"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"

# 辅助函数：将文本思维导图转换为XMind文件
def convert_text_to_xmind(text_content, output_path):
    """将文本格式的思维导图转换为XMind文件"""
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
