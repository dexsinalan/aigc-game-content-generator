import os
import requests

# 百度文心一言文本生成
def generate_text_baidu(prompt):
    """使用百度文心一言生成文本"""
    api_key = os.getenv('BAIDU_API_KEY')
    secret_key = os.getenv('BAIDU_SECRET_KEY')
    
    if not api_key or not secret_key:
        return "请配置百度文心一言API密钥"
    
    try:
        # 获取access token
        token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
        response = requests.get(token_url)
        access_token = response.json().get('access_token')
        
        if not access_token:
            return "获取百度API访问令牌失败"
        
        # 调用文本生成API
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 8000
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if 'result' in result:
            return result['result']
        else:
            return f"生成失败：{result.get('error_msg', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# 百度文心一言图像生成
def generate_image_baidu(prompt):
    """使用百度文心一言生成图像"""
    api_key = os.getenv('BAIDU_API_KEY')
    secret_key = os.getenv('BAIDU_SECRET_KEY')
    
    if not api_key or not secret_key:
        return "请配置百度文心一言API密钥"
    
    # 获取access token
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    response = requests.get(token_url)
    access_token = response.json().get('access_token')
    
    if not access_token:
        return "获取百度API访问令牌失败"
    
    # 调用图像生成API
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if 'data' in result and len(result['data']) > 0:
        return result['data'][0]['url']
    else:
        return f"生成失败：{result.get('error_msg', '未知错误')}"

# 百度文心一言数据生成
def generate_data_baidu(data_prompt, data_type):
    """使用百度文心一言生成数据"""
    api_key = os.getenv('BAIDU_API_KEY')
    secret_key = os.getenv('BAIDU_SECRET_KEY')
    
    if not api_key or not secret_key:
        return None, "请配置百度文心一言API密钥"
    
    try:
        import json
        import pandas as pd
        from io import BytesIO
        
        # 验证数据类型
        if data_type not in ["JSON", "XLSX", "mindmap"]:
            return None, "不支持的数据类型"
        
        # 调用文本生成
        result = generate_text_baidu(data_prompt)
        
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
                return data, f"generated_data_baidu.json"
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
                    return df, f"generated_data_baidu.xlsx"
                else:
                    return None, "生成的数据格式不正确，应该是一个数组"
            except json.JSONDecodeError as e:
                return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
        elif data_type == "mindmap":
            return result, f"generated_mindmap_baidu.txt"
        else:
            return None, "不支持的数据类型"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"
