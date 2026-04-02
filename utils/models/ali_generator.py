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
def generate_data_ali(data_prompt, data_type):
    """使用阿里通义千问生成数据"""
    api_key = os.getenv('ALI_API_KEY')
    
    if not api_key:
        return None, "请配置阿里通义千问API密钥"
    
    try:
        import json
        import pandas as pd
        from io import BytesIO
        
        # 验证数据类型
        if data_type not in ["JSON", "XLSX", "mindmap"]:
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
        elif data_type == "mindmap":
            return result, f"generated_mindmap_ali.txt"
        else:
            return None, "不支持的数据类型"
            
    except Exception as e:
        return None, f"生成失败：{str(e)}"

def translate_text_ali(prompt):
    """使用阿里通义千问翻译文本"""
    api_key = os.getenv('ALI_API_KEY')
    
    if not api_key:
        return None, "请配置阿里通义千问API密钥"
    
    try:
        result = generate_text_ali(prompt)
        return result, "翻译成功"
    except Exception as e:
        return None, f"翻译失败：{str(e)}"

