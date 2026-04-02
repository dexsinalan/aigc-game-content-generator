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
        host = "spark-api.cn-huabei-1.xf-yun.com"
        request_uri = "/v2.1/tti"
        
        # 拼接待签名字符串（严格按照讯飞官方文档格式）
        signature_origin = f"host: {host}\n"
        signature_origin += f"date: {timestamp}\n"
        signature_origin += f"POST {request_uri} HTTP/1.1"        
        # 生成签名
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(signature_sha).decode('utf-8')
        
        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"',
            'Host': host,
            'Date': timestamp
        }
        
        # 构建请求数据（任务创建）
        task_data = {
            "header": {
                "app_id": app_id,
                "status": 3,
                "channel": "default"
            },
            "parameter": {
                "oig": {
                    "result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "oig": {
                    "text": {
                        "prompt": prompt,
                        "aspect_ratio": "1:1",
                        "img_count": 1,
                        "resolution": "2k"
                    }
                }
            }
        }
        
        # 发送任务创建请求
        create_url = f"https://{host}{request_uri}"
        response = requests.post(create_url, headers=headers, json=task_data, timeout=60)
        response.raise_for_status()
        create_result = response.json()
        
        # 检查任务创建是否成功
        if 'header' not in create_result or create_result['header'].get('code') != 0:
            error_msg = create_result.get('header', {}).get('message', '任务创建失败')
            return f"生成失败：{error_msg}"
        
        # 获取task_id
        task_id = create_result.get('payload', {}).get('oig', {}).get('task_id')
        if not task_id:
            return "生成失败：获取任务ID失败"
        
        # 轮询任务状态
        import time
        max_retries = 30  # 最多轮询30次
        retry_interval = 2  # 每2秒轮询一次
        
        for _ in range(max_retries):
            # 构建任务查询请求
            query_data = {
                "header": {
                    "app_id": app_id,
                    "task_id": task_id
                }
            }
            
            # 发送任务查询请求
            query_response = requests.post(create_url, headers=headers, json=query_data, timeout=60)
            query_response.raise_for_status()
            query_result = query_response.json()
            
            # 检查任务状态
            task_status = query_result.get('header', {}).get('task_status')
            
            if task_status == 3:  # 任务完成
                # 获取图片数据
                text_data = query_result.get('payload', {}).get('oig', {}).get('text')
                if text_data and 'images' in text_data:
                    images = text_data['images']
                    if images and len(images) > 0:
                        image_url = images[0].get('image_url')
                        if image_url:
                            return image_url
                        else:
                            return "生成失败：获取图片URL失败"
                return "生成失败：获取图片数据失败"
            elif task_status == 4:  # 回调完成
                return "生成失败：任务回调完成但未获取到图片"
            elif task_status in [1, 2]:  # 待处理或处理中
                time.sleep(retry_interval)
                continue
            else:
                return f"生成失败：任务状态异常 - {task_status}"
        
        return "生成失败：任务超时"
    except requests.exceptions.RequestException as e:
        return f"生成失败：网络错误 - {str(e)}"
    except Exception as e:
        return f"生成失败：{str(e)}"
