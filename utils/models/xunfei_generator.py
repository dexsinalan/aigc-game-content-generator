import os
import requests

# 讯飞星火文本生成
def generate_text_xunfei(prompt):
    """使用讯飞星火生成文本"""
    app_id = os.getenv('XUNFEI_APP_ID')
    api_key = os.getenv('XUNFEI_API_KEY')
    api_secret = os.getenv('XUNFEI_API_SECRET')
    
    if not app_id or not api_key or not api_secret:
        return "请配置讯飞星火API密钥"
    
    try:
        import websocket
        import json
        import time
        import hmac
        import hashlib
        import base64
        
        # 计算签名
        timestamp = str(int(time.time()))
        host = "spark-api.xf-yun.com"
        request_uri = "/v1/x1"
        
        # 拼接待签名字符串
        signature_origin = f"host: {host}\n"
        signature_origin += f"date: {timestamp}\n"
        signature_origin += f"GET {request_uri} HTTP/1.1"
        
        # 生成签名
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(signature_sha).decode('utf-8')
        
        # 构建WebSocket URL
        ws_url = f"wss://{host}{request_uri}?appid={app_id}&api_key={api_key}&signature={signature}&timestamp={timestamp}&host={host}"
        
        # 构建请求数据
        data = {
            "header": {
                "app_id": app_id,
                "uid": "user123"
            },
            "parameter": {
                "chat": {
                    "domain": "spark-x",
                    "temperature": 0.7,
                    "max_tokens": 8000
                }
            },
            "payload": {
                "message": {
                    "text": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            }
        }
        
        # 连接WebSocket并发送请求
        ws = websocket.WebSocket()
        ws.connect(ws_url)
        ws.send(json.dumps(data))
        
        # 接收响应
        response = ""
        while True:
            try:
                message = ws.recv()
                result = json.loads(message)
                
                # 检查响应状态
                if result.get('header', {}).get('code') != 0:
                    return f"生成失败：{result.get('header', {}).get('message', '未知错误')}"
                
                # 获取内容
                choices = result.get('payload', {}).get('choices', {})
                status = choices.get('status', 0)
                content = choices.get('content', [])
                
                for item in content:
                    response += item.get('content', '')
                
                # 检查是否结束
                if status == 2:
                    break
                    
            except websocket.WebSocketTimeoutException:
                return "生成失败：WebSocket连接超时"
            except Exception as e:
                return f"生成失败：{str(e)}"
        
        ws.close()
        return response
        
    except ImportError:
        return "请安装websocket-client库：pip install websocket-client"
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

# 讯飞星火数据生成
def generate_data_xunfei(prompt, data_type):
    """使用讯飞星火生成数据"""
    app_id = os.getenv('XUNFEI_APP_ID')
    api_key = os.getenv('XUNFEI_API_KEY')
    api_secret = os.getenv('XUNFEI_API_SECRET')
    
    if not app_id or not api_key or not api_secret:
        return None, "请配置讯飞星火API密钥"
    
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
        result = generate_text_xunfei(data_prompt)
        
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
                return data, f"generated_data_xunfei.json"
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
                    return df, f"generated_data_xunfei.xlsx"
                else:
                    return None, "生成的数据格式不正确，应该是一个数组"
            except json.JSONDecodeError as e:
                return None, f"JSON解析失败：{str(e)}\n生成的内容：{result[:500]}"
        elif data_type == "XMind":
            return result, f"generated_mindmap_xunfei.txt"
        else:
            return None, "不支持的数据类型"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"
