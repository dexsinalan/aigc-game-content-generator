import os
import requests

# 智谱AI文本生成
def generate_text_zhipu(prompt):
    """使用智谱AI生成文本"""
    api_key = os.getenv('ZHIPU_API_KEY')
    
    if not api_key:
        return "请配置智谱AI API密钥"
    
    try:
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "model": "glm-4",
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
        response.raise_for_status()
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

# 智谱AI图像生成
def generate_image_zhipu(prompt):
    """使用智谱AI生成图像"""
    api_key = os.getenv('ZHIPU_API_KEY')
    
    if not api_key:
        return "请配置智谱AI API密钥"
    
    try:
        url = "https://open.bigmodel.cn/api/paas/v4/images/generations"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "model": "glm-image",
            "prompt": prompt,
            "size": "1280x1280",
            "quality": "hd"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if 'data' in result and len(result['data']) > 0:
            return result['data'][0]['url']
        else:
            return f"生成失败：{result.get('error', {}).get('message', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# 智谱AI数据生成
def generate_data_zhipu(data_prompt, data_type):
    """使用智谱AI生成数据"""
    api_key = os.getenv('ZHIPU_API_KEY')
    
    if not api_key:
        return None, "请配置智谱AI API密钥"
    
    try:
        import json
        import pandas as pd
        from io import BytesIO
        
        # 验证数据类型
        if data_type not in ["JSON", "XLSX", "mindmap"]:
            return None, "不支持的数据类型"
        
        # 调用文本生成
        result = generate_text_zhipu(data_prompt)
        
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
                return data, f"generated_data_zhipu.json"
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
                    return df, f"generated_data_zhipu.xlsx"
                else:
                    return None, "生成的数据格式不正确，应该是一个数组"
            except json.JSONDecodeError as e:
                return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
        elif data_type == "mindmap":
            return result, f"generated_mindmap_zhipu.txt"
        else:
            return None, "不支持的数据类型"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"

def translate_text_zhipu(prompt):
    """使用智谱AI翻译文本"""
    api_key = os.getenv('ZHIPU_API_KEY')
    
    if not api_key:
        return None, "请配置智谱AI API密钥"
    
    try:
        result = generate_text_zhipu(prompt)
        return result, "翻译成功"
    except Exception as e:
        return None, f"翻译失败：{str(e)}"

