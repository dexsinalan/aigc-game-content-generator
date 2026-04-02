import requests
import os
import time
import hmac
import hashlib
import base64
import json
from urllib.parse import urlencode

# 百度文心一言文本生成
def generate_text_baidu(prompt):
    """使用百度文心一言生成文本"""
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
    
    # 调用文本生成API
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "messages": [
            {"role": "user", "content": prompt}
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

# 阿里通义千问文本生成
def generate_text_ali(prompt):
    """使用阿里通义千问生成文本"""
    api_key = os.getenv('ALI_API_KEY')
    
    if not api_key:
        return "请配置阿里通义千问API密钥"
    
    # 千问API的正确端点
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": "qwen-turbo",  # 千问基础模型
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 8000
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if 'output' in result and 'text' in result['output']:
        return result['output']['text']
    else:
        return f"生成失败：{result.get('message', '未知错误')}"

# 智谱AI文本生成
def generate_text_zhipu(prompt):
    """使用智谱AI生成文本"""
    api_key = os.getenv('ZHIPU_API_KEY')
    
    if not api_key:
        return "请配置智谱AI API密钥"
    
    # 智谱AI最新的API端点
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": "glm-4",  # 使用最新的GLM-4模型
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 8000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)  # 增加超时时间到60秒
        response.raise_for_status()  # 检查HTTP状态码
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return f"生成失败：{result.get('error', {}).get('message', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"

# 讯飞星火文本生成
def generate_text_xunfei(prompt):
    """使用讯飞星火生成文本"""
    app_id = os.getenv('XUNFEI_APP_ID')
    api_key = os.getenv('XUNFEI_API_KEY')
    api_secret = os.getenv('XUNFEI_API_SECRET')
    
    if not app_id or not api_key or not api_secret:
        return "请配置讯飞星火API密钥"
    
    try:
        # 计算签名
        import time
        import hmac
        import hashlib
        import base64
        
        timestamp = str(int(time.time()))
        host = "spark-api.xf-yun.com"
        request_uri = "/v3.1/chat"
        
        # 拼接待签名字符串
        signature_origin = f"host: {host}\n"
        signature_origin += f"date: {timestamp}\n"
        signature_origin += f"POST {request_uri} HTTP/1.1\n"
        signature_origin += f"content-type:application/json\n"
        signature_origin += f"app_id:{app_id}\n"
        signature_origin += f"sign_type:SIGN_TYPE_HMAC_SHA256"
        
        # 生成签名
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(signature_sha).decode('utf-8')
        
        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line content-type app_id sign_type", signature="{signature}"',
            'Host': host,
            'Date': timestamp,
            'app_id': app_id
        }
        
        # 构建请求数据
        data = {
            "model": "x1.5",  # 使用x1.5模型
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 8000
        }
        
        # 发送请求
        url = f"https://{host}{request_uri}"
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        # 捕获详细的错误信息
        if response.status_code != 200:
            error_details = response.text
            return f"生成失败：{response.status_code} {response.reason} - {error_details}"
            
        result = response.json()
        
        # 检查响应结构
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
