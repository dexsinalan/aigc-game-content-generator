import streamlit as st
import requests
import json
import os
import pandas as pd
import base64
from io import BytesIO
from dotenv import load_dotenv
from utils.text_generator import generate_text_baidu, generate_text_ali, generate_text_zhipu, generate_text_xunfei
from utils.image_generator import generate_image_baidu, generate_image_ali, generate_image_zhipu
from utils.data_generator import generate_json_data, generate_xlsx_data, generate_xmind_data

# 加载环境变量
load_dotenv()

# ==================== 函数定义（必须在调用之前）====================

# 文本生成函数
def generate_text(prompt, model):
    """使用国产大模型生成文本"""
    if model == "百度文心一言":
        return generate_text_baidu(prompt)
    elif model == "阿里通义千问":
        return generate_text_ali(prompt)
    elif model == "智谱AI":
        return generate_text_zhipu(prompt)
    elif model == "讯飞星火":
        return generate_text_xunfei(prompt)
    else:
        return "不支持的模型"

# 图像生成函数
def generate_image(prompt, model):
    """使用国产大模型生成图像"""
    if model == "百度文心一言":
        return generate_image_baidu(prompt)
    elif model == "阿里通义千问":
        return generate_image_ali(prompt)
    elif model == "智谱AI":
        return generate_image_zhipu(prompt)
    elif model == "讯飞星火":
        return generate_image_xunfei(prompt)
    else:
        return "不支持的模型"

# 数据生成函数
def generate_data(prompt, data_type, model):
    """使用国产大模型生成数据"""
    if data_type == "JSON":
        return generate_json_data(prompt, model)
    elif data_type == "XLSX":
        return generate_xlsx_data(prompt, model)
    elif data_type == "XMind":
        return generate_xmind_data(prompt, model)
    else:
        return None, "不支持的数据类型"

# 初始化session state
def init_session_state():
    """初始化session state"""
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "文本生成"
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = {
            'baidu': {
                'api_key': os.getenv('BAIDU_API_KEY', ''),
                'secret_key': os.getenv('BAIDU_SECRET_KEY', '')
            },
            'ali': {
                'api_key': os.getenv('ALI_API_KEY', '')
            },
            'zhipu': {
                'api_key': os.getenv('ZHIPU_API_KEY', '')
            },
            'xunfei': {
                        'app_id': os.getenv('XUNFEI_APP_ID', ''),
                        'api_key': os.getenv('XUNFEI_API_KEY', ''),
                        'api_secret': os.getenv('XUNFEI_API_SECRET', '')
                    }
        }

# ==================== 页面配置 ====================

# 设置页面配置
st.set_page_config(
    page_title="AI内容生成器 - 游戏开发工具",
    page_icon="🎮",
    layout="wide"
)

# 初始化session state
init_session_state()

# 页面标题
st.title("🎮 AI内容生成器 - 游戏开发工具")

# 应用介绍
with st.expander("📖 应用介绍"):
    st.write("""
    这是一个专为游戏开发设计的AI内容生成工具，使用国产免费大模型提供文本、图像和数据生成服务。
    
    **功能特点：**
    - 📝 文本生成：生成游戏角色描述、剧情对话、任务文本等
    - 🖼️ 图像生成：生成游戏场景、角色设计、道具图标等
    - � 数据生成：生成JSON数据表、Excel表格、XMind思维导图等
    - � 多模型支持：集成百度文心一言、阿里通义千问、智谱AI、讯飞星火等国产大模型
    - 📚 API文档：提供完整的API接口文档，方便游戏开发直接调用
    
    **使用说明：**
    1. 先在"API设置"页面配置API密钥
    2. 选择功能模块（文本生成、图像生成、数据生成）
    3. 输入提示词
    4. 选择要使用的AI模型
    5. 点击生成按钮
    6. 查看生成结果并下载
    """)

# ==================== 侧边栏导航 ====================

st.sidebar.title("功能选择")

# 使用按钮组替代单选按钮
if st.sidebar.button("🔑 API设置", use_container_width=True, key="btn_api_settings"):
    option = "API设置"
    st.session_state.current_page = "API设置"
elif st.sidebar.button("📝 文本生成", use_container_width=True, key="btn_text_gen"):
    option = "文本生成"
    st.session_state.current_page = "文本生成"
elif st.sidebar.button("🖼️ 图像生成", use_container_width=True, key="btn_image_gen"):
    option = "图像生成"
    st.session_state.current_page = "图像生成"
elif st.sidebar.button("📊 数据生成", use_container_width=True, key="btn_data_gen"):
    option = "数据生成"
    st.session_state.current_page = "数据生成"
elif st.sidebar.button("📚 API文档", use_container_width=True, key="btn_api_docs"):
    option = "API文档"
    st.session_state.current_page = "API文档"
else:
    # 默认选择
    if 'current_page' not in st.session_state:
        option = "API设置"
    else:
        option = st.session_state.current_page

# ==================== API设置页面 ====================

if option == "API设置":
    st.header("🔑 API密钥设置")
    st.write("请配置您要使用的国产大模型API密钥。这些密钥将保存在当前会话中。")
    
    st.info("💡 提示：您可以从以下平台获取API密钥：\n"
            "- 百度文心一言：https://ai.baidu.com/\n"
            "- 阿里通义千问：https://tongyi.aliyun.com/\n"
            "- 智谱AI：https://open.bigmodel.cn/\n"
            "- 讯飞星火：https://xinghuo.xfyun.cn/")
    
    # 免费API (国产大模型)
    st.subheader("🆓 免费API")
    st.write("以下是国产免费大模型，适合个人开发者使用：")
    
    # 阿里通义千问配置
    with st.expander("阿里通义千问"):
        ali_api_key = st.text_input("API Key", 
                                    value=st.session_state.api_keys['ali']['api_key'],
                                    type="password", 
                                    placeholder="输入阿里API Key",
                                    key="ali_api_key")
        if st.button("保存阿里配置"):
            st.session_state.api_keys['ali']['api_key'] = ali_api_key
            os.environ['ALI_API_KEY'] = ali_api_key
            st.success("阿里配置已保存！")
    
    # 智谱AI配置
    with st.expander("智谱AI"):
        zhipu_api_key = st.text_input("API Key", 
                                      value=st.session_state.api_keys['zhipu']['api_key'],
                                      type="password", 
                                      placeholder="输入智谱AI API Key",
                                      key="zhipu_api_key")
        if st.button("保存智谱配置"):
            st.session_state.api_keys['zhipu']['api_key'] = zhipu_api_key
            os.environ['ZHIPU_API_KEY'] = zhipu_api_key
            st.success("智谱配置已保存！")
    
    # 讯飞星火配置
    with st.expander("讯飞星火"):
        st.info("💡 提示：请使用讯飞星火的 HiDream 图像生成 API 配置")
        st.write("获取方式：登录讯飞开放平台控制台，在「星火大模型」的设置页面中获取")
        xunfei_app_id = st.text_input("APP ID", 
                                       value=st.session_state.api_keys['xunfei']['app_id'],
                                       type="password", 
                                       placeholder="输入讯飞APP ID",
                                       key="xunfei_app_id")
        xunfei_api_key = st.text_input("API Key", 
                                       value=st.session_state.api_keys['xunfei']['api_key'],
                                       type="password", 
                                       placeholder="输入讯飞API Key",
                                       key="xunfei_api_key")
        xunfei_api_secret = st.text_input("API Secret", 
                                       value=st.session_state.api_keys['xunfei']['api_secret'],
                                       type="password", 
                                       placeholder="输入讯飞API Secret",
                                       key="xunfei_api_secret")
        if st.button("保存讯飞配置"):
            st.session_state.api_keys['xunfei']['app_id'] = xunfei_app_id
            st.session_state.api_keys['xunfei']['api_key'] = xunfei_api_key
            st.session_state.api_keys['xunfei']['api_secret'] = xunfei_api_secret
            os.environ['XUNFEI_APP_ID'] = xunfei_app_id
            os.environ['XUNFEI_API_KEY'] = xunfei_api_key
            os.environ['XUNFEI_API_SECRET'] = xunfei_api_secret
            st.success("讯飞配置已保存！")
    
    # 付费API
    st.subheader("💲 付费API")
    st.write("以下是需要付费的API，功能更强大：")
    
    # 百度文心一言配置
    with st.expander("百度文心一言"):
        baidu_api_key = st.text_input("API Key", 
                                      value=st.session_state.api_keys['baidu']['api_key'],
                                      type="password", 
                                      placeholder="输入百度API Key",
                                      key="baidu_api_key")
        baidu_secret_key = st.text_input("Secret Key", 
                                         value=st.session_state.api_keys['baidu']['secret_key'],
                                         type="password", 
                                         placeholder="输入百度Secret Key",
                                         key="baidu_secret_key")
        if st.button("保存百度配置"):
            st.session_state.api_keys['baidu']['api_key'] = baidu_api_key
            st.session_state.api_keys['baidu']['secret_key'] = baidu_secret_key
            os.environ['BAIDU_API_KEY'] = baidu_api_key
            os.environ['BAIDU_SECRET_KEY'] = baidu_secret_key
            st.success("百度配置已保存！")
    
    # 一键保存所有配置
    st.divider()
    if st.button("💾 保存所有配置", type="primary"):
        # 保存所有配置到session state和环境变量
        st.session_state.api_configured = True
        st.success("✅ 所有API配置已保存！您可以开始使用其他功能了。")

# ==================== 文本生成功能 ====================

elif option == "文本生成":
    st.header("📝 AI文本生成")
    st.write("输入提示词，生成游戏相关的文本内容，如角色描述、剧情对话、任务文本等。")
    
    # 输入提示词
    prompt = st.text_area("提示词", placeholder="例如：游戏角色描述、剧情对话、任务文本等", height=150)
    
    # 选择模型
    model = st.selectbox(
        "选择模型",
        ("百度文心一言", "阿里通义千问", "智谱AI", "讯飞星火")
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button("🚀 生成文本", type="primary")
    
    if generate_btn:
        if not prompt:
            st.error("请输入提示词")
        else:
            with st.spinner("生成中..."):
                try:
                    # 调用文本生成函数
                    result = generate_text(prompt, model)
                    st.success("生成成功！")
                    st.markdown("### 生成结果")
                    st.write(result)
                    
                    # 提供复制按钮
                    st.code(result, language="text")
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")

# ==================== 图像生成功能 ====================

elif option == "图像生成":
    st.header("🖼️ AI图像生成")
    st.write("输入提示词，生成游戏相关的图像内容，如游戏场景、角色设计、道具图标等。")
    
    # 输入提示词
    prompt = st.text_area("提示词", placeholder="例如：游戏场景、角色设计、道具图标等", height=150)
    
    # 选择模型
    model = st.selectbox(
        "选择模型",
        ("百度文心一言", "阿里通义千问", "智谱AI", "讯飞星火")
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button("🚀 生成图像", type="primary")
    
    if generate_btn:
        if not prompt:
            st.error("请输入提示词")
        else:
            with st.spinner("生成中..."):
                try:
                    # 调用图像生成函数
                    image_url = generate_image(prompt, model)
                    st.success("生成成功！")
                    st.markdown("### 生成结果")
                    st.image(image_url, use_container_width=True)
                    
                    # 提供下载按钮
                    if image_url.startswith('http'):
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            st.download_button(
                                label="💾 下载图像",
                                data=response.content,
                                file_name=f"generated_image_{model}.png",
                                mime="image/png"
                            )
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")

# ==================== 数据生成功能 ====================

elif option == "数据生成":
    st.header("📊 AI数据生成")
    st.write("输入提示词，生成游戏相关的数据内容，如角色属性表、任务列表、物品数据等。")
    
    # 输入提示词
    prompt = st.text_area("提示词", placeholder="例如：生成一个RPG游戏的角色属性表，包含名称、等级、生命值、攻击力等字段", height=150)
    
    # 选择数据类型
    data_type = st.selectbox(
        "选择数据格式",
        ("JSON", "XLSX", "XMind")
    )
    
    # 选择模型
    model = st.selectbox(
        "选择模型",
        ("百度文心一言", "阿里通义千问", "智谱AI", "讯飞星火")
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button("🚀 生成数据", type="primary")
    
    if generate_btn:
        if not prompt:
            st.error("请输入提示词")
        else:
            with st.spinner("生成中..."):
                try:
                    # 调用数据生成函数
                    data, filename = generate_data(prompt, data_type, model)
                    
                    if data is not None:
                        st.success("生成成功！")
                        st.markdown("### 生成结果")
                        
                        if data_type == "JSON":
                            # 显示JSON预览
                            st.json(data)
                            # 提供下载按钮
                            json_str = json.dumps(data, ensure_ascii=False, indent=2)
                            st.download_button(
                                label="💾 下载JSON文件",
                                data=json_str,
                                file_name=filename,
                                mime="application/json"
                            )
                        
                        elif data_type == "XLSX":
                            # 显示表格预览
                            st.dataframe(data)
                            # 提供下载按钮
                            buffer = BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                data.to_excel(writer, index=False, sheet_name='Sheet1')
                            st.download_button(
                                label="💾 下载Excel文件",
                                data=buffer.getvalue(),
                                file_name=filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        
                        elif data_type == "XMind":
                            # 显示思维导图预览（文本形式）
                            st.text(data)
                            # 提供下载按钮
                            st.download_button(
                                label="💾 下载XMind文件",
                                data=data,
                                file_name=filename,
                                mime="application/xmind"
                            )
                    else:
                        st.error(filename)  # 显示错误信息
                        
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")

# ==================== API文档页面 ====================

elif option == "API文档":
    st.header("📚 API接口文档")
    st.write("以下是本应用提供的API接口文档，可用于游戏开发直接调用。")
    
    tabs = st.tabs(["文本生成", "图像生成", "数据生成"])
    
    with tabs[0]:
        st.subheader("文本生成接口")
        st.code("""POST /api/text/generate

请求体：
{
  "prompt": "游戏角色描述",
  "model": "百度文心一言"  // 支持：百度文心一言、阿里通义千问、智谱AI、讯飞星火
}

响应：
{
  "text": "生成的文本内容"
}""", language="json")
    
    with tabs[1]:
        st.subheader("图像生成接口")
        st.code("""POST /api/image/generate

请求体：
{
  "prompt": "游戏场景描述",
  "model": "百度文心一言"  // 支持：百度文心一言、阿里通义千问、智谱AI、讯飞星火
}

响应：
{
  "imageUrl": "生成的图像URL"
}""", language="json")
    
    with tabs[2]:
        st.subheader("数据生成接口")
        st.code("""POST /api/data/generate

请求体：
{
  "prompt": "生成角色属性表",
  "data_type": "JSON",  // 支持：JSON、XLSX、XMind
  "model": "百度文心一言"  // 支持：百度文心一言、阿里通义千问、智谱AI、讯飞星火
}

响应：
{
  "data": {生成的数据},
  "filename": "data.json"
}""", language="json")
    
    st.divider()
    st.subheader("使用示例")
    st.code("""# Python示例
import requests

# 生成文本
response = requests.post('http://localhost:8503/api/text/generate', json={
    'prompt': '生成一个RPG游戏角色描述',
    'model': '百度文心一言'
})
data = response.json()
print(data['text'])

# 生成图像
response = requests.post('http://localhost:8503/api/image/generate', json={
    'prompt': '生成一个游戏场景',
    'model': '阿里通义千问'
})
data = response.json()
print(data['imageUrl'])

# 生成数据
response = requests.post('http://localhost:8503/api/data/generate', json={
    'prompt': '生成角色属性表',
    'data_type': 'JSON',
    'model': '智谱AI'
})
data = response.json()
print(data['data'])

# 使用讯飞星火生成文本
response = requests.post('http://localhost:8503/api/text/generate', json={
    'prompt': '生成游戏剧情对话',
    'model': '讯飞星火'
})
data = response.json()
print(data['text'])
""", language="python")
