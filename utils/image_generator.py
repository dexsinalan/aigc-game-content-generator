import requests
import os
import base64
import json

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

# 讯飞星火图像生成
def generate_image_xunfei(prompt):
    """使用讯飞星火生成图像"""
    api_key = os.getenv('XUNFEI_API_KEY')
    
    if not api_key:
        return "请配置讯飞星火API密钥"
    
    try:
        # 使用新的OpenAI兼容接口
        url = "https://spark-api-open.xf-yun.com/v1/images/generations"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "model": "spark-doubao",  # 使用正确的模型名称
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        
        # 添加超时设置
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()  # 检查HTTP状态码
        result = response.json()
        
        # 检查响应结构
        if 'data' in result and len(result['data']) > 0:
            return result['data'][0]['url']
        else:
            error_msg = result.get('error', {}).get('message', '未知错误')
            return f"生成失败：{error_msg}"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"
