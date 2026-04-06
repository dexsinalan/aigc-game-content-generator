import os
import requests

# Claude文本生成
def generate_text_claude(prompt):
    """使用Claude生成文本"""
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        return "请配置Claude API密钥"
    
    try:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
        data = {
            "model": "claude-3-opus-20240229",
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
        
        if 'content' in result and len(result['content']) > 0:
            return result['content'][0]['text']
        else:
            error_msg = result.get('error', {}).get('message', '未知错误')
            return f"生成失败：{error_msg}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# Claude图像生成
def generate_image_claude(prompt):
    """使用Claude生成图像"""
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        return "请配置Claude API密钥"
    
    try:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
        data = {
            "model": "claude-3-opus-20240229",
            "messages": [
                {
                    "role": "user",
                    "content": f"生成一张关于'{prompt}'的图像，详细描述图像内容"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            error_details = response.text
            return f"生成失败：{response.status_code} {response.reason} - {error_details}"
            
        result = response.json()
        
        if 'content' in result and len(result['content']) > 0:
            return result['content'][0]['text']
        else:
            error_msg = result.get('error', {}).get('message', '未知错误')
            return f"生成失败：{error_msg}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# Claude数据生成
def generate_data_claude(data_prompt, data_type):
    """使用Claude生成数据"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        return None, "请配置Claude API密钥"
    
    try:
        import json
        import pandas as pd
        from io import BytesIO
        
        # 验证数据类型
        if data_type not in ["JSON", "XLSX", "mindmap"]:
            return None, "不支持的数据类型"
        
        # 调用文本生成
        result = generate_text_claude(data_prompt)
        
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
                return data, f"generated_json_claude.json"
            except json.JSONDecodeError as e:
                # 增加更详细的错误信息
                error_pos = min(e.pos + 50, len(result))
                error_context = result[max(0, e.pos - 50):error_pos]
                return None, f"""JSON解析失败：{str(e)}
错误位置上下文：...{error_context}...
完整生成内容：{result}"""
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
                    return df, f"generated_xlsx_claude.xlsx"
                else:
                    return None, "生成的数据格式不正确，应该是一个数组"
            except json.JSONDecodeError as e:
                # 增加更详细的错误信息
                error_pos = min(e.pos + 50, len(result))
                error_context = result[max(0, e.pos - 50):error_pos]
                return None, f"""JSON解析失败：{str(e)}
错误位置上下文：...{error_context}...
完整生成内容：{result}"""
        elif data_type == "mindmap":
            return result, f"generated_mindmap_claude.txt"
        else:
            return None, "不支持的数据类型"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"

def translate_text_claude(prompt):
    """使用Claude翻译文本"""
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        return None, "请配置Claude API密钥"
    
    try:
        result = generate_text_claude(prompt)
        return result, "翻译成功"
    except Exception as e:
        return None, f"翻译失败：{str(e)}"

