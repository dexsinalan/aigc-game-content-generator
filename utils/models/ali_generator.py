import os
import requests

# 阿里通义千问文本生成
def generate_text_ali(prompt):
    """使用阿里通义千问生成文本"""
    api_key = os.getenv('ALI_API_KEY')
    
    if not api_key:
        return "请配置阿里通义千问API密钥"
    
    try:
        import dashscope
        dashscope.api_key = api_key
        
        # 调用通义千问的ChatCompletion API
        rsp = dashscope.Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            temperature=0.7,
            max_tokens=8000
        )
        
        if rsp.status_code == 200:
            return rsp.output.text
        else:
            return f"生成失败：{rsp.code} - {rsp.message}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# 阿里通义千问图像生成
def generate_image_ali(prompt):
    """使用阿里通义千问生成图像"""
    api_key = os.getenv('ALI_API_KEY')
    
    if not api_key:
        return "请配置阿里通义千问API密钥"
    
    try:
        import dashscope
        dashscope.api_key = api_key
        
        # 调用阿里专属的 ImageSynthesis API
        rsp = dashscope.ImageSynthesis.call(
            model='wanx-v1',
            prompt=prompt,
            n=1,
            size='1024*1024'  # 阿里的尺寸格式是星号 *，不是 x
        )
        
        if rsp.status_code == 200:
            return rsp.output.results[0].url
        else:
            return f"生成失败：{rsp.code} - {rsp.message}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# 阿里通义千问数据生成
def generate_data_ali(prompt, data_type):
    """使用阿里通义千问生成数据"""
    api_key = os.getenv('ALI_API_KEY')
    
    if not api_key:
        return None, "请配置阿里通义千问API密钥"
    
    try:
        import json
        import pandas as pd
        from io import BytesIO
        
        # 根据数据类型构建提示词
        if data_type == "JSON":
            data_prompt = f"""请根据以下描述生成JSON格式的数据：
{prompt}

要求：
1. 只返回JSON数据，不要包含任何解释文字
2. 确保JSON格式正确，可以被Python的json.loads()解析
3. 数据应该包含合理的字段和示例数据
4. 如果是表格数据，使用数组格式，数据量根据用戶要求而定


请直接返回JSON数据："""
        elif data_type == "XLSX":
            data_prompt = f"""请根据以下描述生成表格数据，并返回JSON数组格式：
{prompt}

要求：
1. 返回JSON数组格式，每个元素是一个对象，代表一行数据
2. 确保所有对象具有相同的字段
3. 只返回JSON数组，不要包含任何解释文字
4. 数据量根据用戶要求而定


请直接返回JSON数组："""
        elif data_type == "mindmap":
            data_prompt = f"""请根据以下描述生成思维导图数据，使用Markdown列表格式：
{prompt}

要求：
1. 使用Markdown列表格式（- 和缩进）
2. 第一行是中心主题
3. 使用缩进表示层级关系
4. 包含多个主要分支，每个分支可以有多个子节点
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
        else:
            return None, "不支持的数据类型"
        
        # 调用文本生成
        result = generate_text_ali(data_prompt)
        
        # 处理生成结果
        if data_type == "JSON":
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
                return data, f"generated_data_ali.json"
            except json.JSONDecodeError as e:
                return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
        elif data_type == "XLSX":
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
                    return df, f"generated_data_ali.xlsx"
                else:
                    return None, "生成的数据格式不正确，应该是一个数组"
            except json.JSONDecodeError as e:
                return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
        elif data_type == "XMind":
            return result, f"generated_mindmap_ali.txt"
        else:
            return None, "不支持的数据类型"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"
