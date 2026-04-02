#!/usr/bin/env python3
"""
测试讯飞星火API配置和签名计算
"""

import os
import time
import hmac
import hashlib
import base64
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_xunfei_signature():
    """测试讯飞星火签名计算"""
    print("🔍 测试讯飞星火签名计算...")
    
    app_id = os.getenv('XUNFEI_APP_ID')
    api_key = os.getenv('XUNFEI_API_KEY')
    api_secret = os.getenv('XUNFEI_API_SECRET')
    
    if not all([app_id, api_key, api_secret]):
        print("❌ 请先配置讯飞星火API密钥")
        print("请在.secrets.toml中设置:")
        print("XUNFEI_APP_ID = 'your-app-id'")
        print("XUNFEI_API_KEY = 'your-api-key'")
        print("XUNFEI_API_SECRET = 'your-api-secret'")
        return False
    
    print(f"✅ App ID: {app_id}")
    print(f"✅ API Key: {api_key}")
    print(f"✅ API Secret: {api_secret}")
    
    # 测试签名计算
    timestamp = str(int(time.time()))
    host = "spark-api.xf-yun.com"
    request_uri = "/v3.1/chat"
    
    # 拼接待签名字符串
    signature_origin = f"host: {host}\n"
    signature_origin += f"date: {timestamp}\n"
    signature_origin += f"POST {request_uri} HTTP/1.1"
    
    print(f"\n📝 签名字符串:")
    print(repr(signature_origin))
    
    # 生成签名
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(signature_sha).decode('utf-8')
    
    print(f"\n🔑 计算签名: {signature}")
    
    # 构建Authorization头部
    authorization = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    print(f"\n📋 Authorization头部:")
    print(authorization)
    
    return True

def test_xunfei_api():
    """测试讯飞星火API调用"""
    print("\n🚀 测试讯飞星火API调用...")
    
    app_id = os.getenv('XUNFEI_APP_ID')
    api_key = os.getenv('XUNFEI_API_KEY')
    api_secret = os.getenv('XUNFEI_API_SECRET')
    
    if not all([app_id, api_key, api_secret]):
        return False
    
    # 计算签名
    timestamp = str(int(time.time()))
    host = "spark-api.xf-yun.com"
    request_uri = "/v3.1/chat"
    
    signature_origin = f"host: {host}\n"
    signature_origin += f"date: {timestamp}\n"
    signature_origin += f"POST {request_uri} HTTP/1.1"
    
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(signature_sha).decode('utf-8')
    
    # 构建请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"',
        'Host': host,
        'Date': timestamp
    }
    
    # 构建请求数据
    data = {
        "header": {
            "app_id": app_id,
            "uid": "test-user"
        },
        "parameter": {
            "chat": {
                "domain": "generalv3",
                "temperature": 0.7,
                "max_tokens": 8000
            }
        },
        "payload": {
            "message": {
                "text": [
                    {
                        "role": "user",
                        "content": "你好，请回复'测试成功'"
                    }
                ]
            }
        }
    }
    
    try:
        url = f"https://{host}{request_uri}"
        print(f"🌐 请求URL: {url}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📋 响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('header', {}).get('code') == 0:
                print("✅ API调用成功！")
                return True
            else:
                print(f"❌ API错误: {result.get('header', {}).get('message', '未知错误')}")
        else:
            print(f"❌ HTTP错误: {response.status_code} {response.reason}")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
    
    return False

def main():
    """主测试函数"""
    print("🚀 开始测试讯飞星火API配置...")
    print("=" * 50)
    
    # 测试签名计算
    sig_success = test_xunfei_signature()
    
    if sig_success:
        # 测试API调用
        api_success = test_xunfei_api()
        
        if api_success:
            print("\n🎉 所有测试通过！讯飞星火API配置正确。")
        else:
            print("\n⚠️ API调用失败，请检查API密钥和网络连接。")
    else:
        print("\n❌ 签名计算测试失败。")
    
    print("\n💡 提示：请确保已在.secrets.toml中正确配置讯飞星火API密钥")

if __name__ == "__main__":
    main()