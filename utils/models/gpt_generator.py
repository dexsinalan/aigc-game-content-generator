import os
import requests

# GPT文本生成
def generate_text_gpt(prompt):
    """使用GPT生成文本"""
    api_key = os.getenv('GPT_API_KEY')
    
    if not api_key:
        return "请配置GPT API密钥"
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 8000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            error_details = response.text
            return f"生成失败：{response.status_code} {response.reason} - {error_details}"
            
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            choice = result['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                return choice['message']['content']
            else:
                return f"生成失败：响应格式错误 - {str(result)}"
        else:
            error_msg = result.get('error', {}).get('message', '未知错误')
            return f"生成失败：{error_msg}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# GPT图像生成
def generate_image_gpt(prompt):
    """使用GPT生成图像"""
    api_key = os.getenv('GPT_API_KEY')
    
    if not api_key:
        return "请配置GPT API密钥"
    
    try:
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            error_details = response.text
            return f"生成失败：{response.status_code} {response.reason} - {error_details}"
            
        result = response.json()
        
        if 'data' in result and len(result['data']) > 0:
            return result['data'][0]['url']
        else:
            error_msg = result.get('error', {}).get('message', '未知错误')
            return f"生成失败：{error_msg}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# GPT数据生成
def generate_data_gpt(prompt, data_type):
    """使用GPT生成数据"""
    api_key = os.getenv('GPT_API_KEY')
    
    if not api_key:
        return None, "请配置GPT API密钥"
    
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
        result = generate_text_gpt(data_prompt)
        
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
                return data, f"generated_data_gpt.json"
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
                    return df, f"generated_data_gpt.xlsx"
                else:
                    return None, "生成的数据格式不正确，应该是一个数组"
            except json.JSONDecodeError as e:
                return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
        elif data_type == "XMind":
            return result, f"generated_mindmap_gpt.txt"
        else:
            return None, "不支持的数据类型"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"
