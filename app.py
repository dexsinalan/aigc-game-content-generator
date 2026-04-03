import streamlit as st
import requests
import json
import os
import pandas as pd
import base64
import time
from io import BytesIO
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from utils.text_generator import generate_text_for_model
from utils.image_generator import generate_image_for_model
from utils.data_generator import generate_json_data, generate_xlsx_data, generate_mindmap_data
from utils.translation_generator import translate_text_for_model, SUPPORTED_LANGUAGES
from utils.prompt_templates import TEXT_TEMPLATES, IMAGE_TEMPLATES, DATA_TEMPLATES
from utils.PXI_generator import analyze_pxi_dimensions, display_pxi_results, display_academic_background
from utils.level_generator import (
    generate_level, generate_level_story, validate_ascii_map, 
    parse_ascii_map, display_level_elements_reference, display_academic_background as display_level_academic_background
)
from utils.vgdl_generator import (
    generate_vgdl, check_vgdl_logic, display_academic_background as display_vgdl_academic_background,
    display_vgdl_template
)

# 加载环境变量
load_dotenv()

# ==================== 函数定义（必须在调用之前）====================

# 文本生成函数
def generate_text(prompt, model):
    """使用大模型生成文本"""
    return generate_text_for_model(prompt, model)

# 图像生成函数
def generate_image(prompt, model):
    """使用大模型生成图像"""
    return generate_image_for_model(prompt, model)

# 数据生成函数
def generate_data(prompt, data_type, model):
    """使用大模型生成数据"""
    if data_type == "JSON":
        return generate_json_data(prompt, model)
    elif data_type == "XLSX":
        return generate_xlsx_data(prompt, model)
    elif data_type == "mindmap":
        return generate_mindmap_data(prompt, model)
    else:
        return None, "不支持的数据类型", 0, 0

# 初始化session state
def init_session_state():
    """初始化session state"""
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "首页"
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
                    },
            'claude': {
                'api_key': os.getenv('CLAUDE_API_KEY', '')
            },
            'gpt': {
                'api_key': os.getenv('CHATGPT_API_KEY', '')
            },
            'deepseek': {
                'api_key': os.getenv('DEEPSEEK_API_KEY', '')
            },
            'silicon': {
                'api_key': os.getenv('SILICON_API_KEY', '')
            }
        }
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "阿里通义千问"  # 默认选择免费模型

# 检查API密钥是否配置
def check_api_configured(model_name):
    """检查指定模型的API密钥是否已配置"""
    api_keys = st.session_state.api_keys
    
    model_map = {
        "百度文心一言": 'baidu',
        "阿里通义千问": 'ali',
        "智谱AI": 'zhipu',
        "讯飞星火": 'xunfei',
        "Claude": 'claude',
        "ChatGPT": 'gpt',
        "DeepSeek": 'deepseek',
        "硅基流动": 'silicon'
    }
    
    provider = model_map.get(model_name)
    if not provider:
        return False
    
    keys = api_keys.get(provider, {})
    
    if provider == 'baidu':
        return bool(keys.get('api_key') and keys.get('secret_key'))
    elif provider == 'xunfei':
        return bool(keys.get('app_id') and keys.get('api_key') and keys.get('api_secret'))
    else:
        return bool(keys.get('api_key'))

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



# ==================== 侧边栏导航 ====================

st.sidebar.title("功能选择")

# 初始化current_page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "首页"

# 显示所有按钮（调整顺序，将home按钮放在第一位）
home_btn = st.sidebar.button("🏠 首页", use_container_width=True, key="btn_home")
intro_btn = st.sidebar.button("📖 介绍文档", use_container_width=True, key="btn_intro")
api_settings_btn = st.sidebar.button("🔑 API设置", use_container_width=True, key="btn_api_settings")
text_gen_btn = st.sidebar.button("📝 游戏文本设计", use_container_width=True, key="btn_text_gen")
image_gen_btn = st.sidebar.button("🖼️ 游戏美术资源", use_container_width=True, key="btn_image_gen")
data_gen_btn = st.sidebar.button("📊 游戏数据配置", use_container_width=True, key="btn_data_gen")
translation_btn = st.sidebar.button("🌍 游戏多语言本地化", use_container_width=True, key="btn_translation")
player_exp_btn = st.sidebar.button("🎮 玩家体验预测器", use_container_width=True, key="btn_player_exp")
level_gen_btn = st.sidebar.button("🏗️ 关卡原型生成器", use_container_width=True, key="btn_level_gen")
vgdl_gen_btn = st.sidebar.button("🎮 VGDL生成器", use_container_width=True, key="btn_vgdl_gen")
thanks_btn = st.sidebar.button("🙏 致谢及免责声明", use_container_width=True, key="btn_thanks")


# 处理按钮点击
if home_btn:
    st.session_state.current_page = "首页"
elif intro_btn:
    st.session_state.current_page = "介绍文档"
elif api_settings_btn:
    st.session_state.current_page = "API设置"
elif text_gen_btn:
    st.session_state.current_page = "文本生成"
elif image_gen_btn:
    st.session_state.current_page = "图像生成"
elif data_gen_btn:
    st.session_state.current_page = "数据生成"
elif translation_btn:
    st.session_state.current_page = "多语言在地化"
elif player_exp_btn:
    st.session_state.current_page = "玩家体验预测器"
elif level_gen_btn:
    st.session_state.current_page = "关卡原型生成器"
elif vgdl_gen_btn:
    st.session_state.current_page = "VGDL生成器"
elif thanks_btn:
    st.session_state.current_page = "致谢"


# 设置当前选项
option = st.session_state.current_page

# ==================== 模型选择 ====================
if option in ["文本生成", "图像生成", "数据生成", "多语言在地化", "玩家体验预测器", "关卡原型生成器", "VGDL生成器"]:
    st.sidebar.divider()
    st.sidebar.subheader("🤖 模型选择")
    
    # 定义所有模型
    all_models = ["百度文心一言", "阿里通义千问", "智谱AI", "讯飞星火", "Claude", "ChatGPT", "DeepSeek", "硅基流动"]
    
    # 检查每个模型的API配置状态
    model_status = {}
    for model in all_models:
        model_status[model] = check_api_configured(model)
    
    # 创建模型选项列表（已配置的在前，未配置的在后）
    configured_models = [model for model in all_models if model_status[model]]
    unconfigured_models = [model for model in all_models if not model_status[model]]
    ordered_models = configured_models + unconfigured_models
    
    # 显示模型选择
    selected_model = st.sidebar.selectbox(
        "选择AI模型",
        ordered_models,
        index=ordered_models.index(st.session_state.selected_model) if st.session_state.selected_model in ordered_models else 0,
        key="model_selector"
    )
    
    # 更新选择的模型
    st.session_state.selected_model = selected_model
    
    # 显示API配置提示
    if not model_status[selected_model]:
        st.sidebar.warning(f"⚠️ {selected_model} 的API密钥未配置")
        st.sidebar.info("请在「API设置」页面配置API密钥")
    else:
        st.sidebar.success(f"✅ {selected_model} 已配置")
    
    # 显示所有模型的状态
    st.sidebar.subheader("📋 所有模型状态")
    for model in all_models:
        status = "✅ 已配置" if model_status[model] else "❌ 未配置"
        st.sidebar.write(f"{model}: {status}")

# ==================== 首页页面 ====================

if option == "首页":
    st.header("🎉 欢迎使用游戏开发辅助工具")
    st.write("""
    欢迎来到AI内容生成器 - 游戏开发工具！
    
    这是一个专为游戏开发者设计的AI辅助工具，集成了先进的大模型技术，帮助您快速生成游戏开发所需的各种内容，显著提高开发效率。
    
    **为什么选择我们：**
    - 🎯 专为游戏开发场景优化
    - 🚀 快速生成高质量内容
    - 🌐 支持多种AI模型
    - 💾 一键导出多种格式
    
    **开始您的创作之旅：**
    1. 在左侧「API设置」中配置您的API密钥
    2. 选择您需要的功能模块
    3. 输入详细的设计需求
    4. 选择合适的AI模型
    5. 点击生成按钮，获取高质量的内容
    
    无论您是独立开发者还是大型团队，我们都能为您的游戏开发提供有力的支持！
    """)

# ==================== 介绍文档页面 ====================

if option == "介绍文档":
    st.header("📖 游戏开发辅助工具使用指南")
    st.write("""
    这是一个专为游戏开发设计的AI辅助工具，使用先进的大模型技术为游戏开发者提供全方位的内容生成和设计支持。
    
    **核心功能详解：**
    - 📝 游戏文本设计：生成游戏角色描述、剧情对话、任务文本、技能描述、物品描述等各种游戏文案内容
    - 🖼️ 游戏美术资源：生成游戏场景、角色设计、道具图标、UI元素、特效概念图等视觉素材
    - 📊 游戏数据配置：生成角色属性表、任务列表、物品数据、技能参数、敌人AI行为等结构化数据
    - 🌍 游戏多语言本地化：将游戏文本翻译为18种语言版本，支持游戏国际化部署
    
    **详细使用流程：**
    1. **配置API密钥**：在"API设置"页面配置您要使用的AI模型API密钥
    2. **选择功能模块**：根据您的需求选择相应的功能模块（游戏文本设计、游戏美术资源、游戏数据配置、游戏多语言本地化）
    3. **输入设计需求**：在文本输入框中详细描述您的设计需求，越详细越好
    4. **选择AI模型**：从下拉菜单中选择您要使用的AI模型
    5. **生成内容**：点击生成按钮，等待AI生成内容
    6. **查看和下载**：查看生成结果，根据需要下载为相应格式
    
    **支持的AI模型：**
    - 阿里通义千问（免费）
    - 智谱AI（免费）
    - 百度文心一言
    - 讯飞星火
    - Claude
    - ChatGPT
    - DeepSeek
    - 硅基流动
    
    **使用注意事项：**
    - 提示词越详细，生成结果越符合您的需求
    - 不同模型的生成风格和能力有所不同，建议根据具体需求选择合适的模型
    - 对于复杂的生成任务，可能需要多次调整提示词以获得最佳结果
    - 生成的内容可能需要人工编辑和调整，以确保符合游戏的整体风格
    - API密钥请妥善保管，不要分享给他人
    - 部分模型可能有调用次数限制，请合理使用
    
    **技术架构：**
    - 前端：Streamlit（交互式Web界面）
    - 后端：Python（核心逻辑处理）
    
    **最佳实践：**
    - 对于文本生成，提供具体的角色背景、场景设定和风格要求
    - 对于图像生成，描述清晰的场景、角色特征和艺术风格
    - 对于数据生成，明确数据结构、字段含义和数据范围
    - 对于多语言本地化，确保原文清晰易懂，避免使用过于复杂的表达方式
    """)

# ==================== API设置页面 ====================

if option == "API设置":
    st.header("🔑 API密钥设置")
    st.write("请配置您要使用的AI模型API密钥。这些密钥将保存在当前会话中。")
    
    st.info("💡 提示：您可以从以下平台获取API密钥：\n"
            "- 阿里通义千问：https://dashscope.aliyun.com/\n"
            "- 智谱AI：https://open.bigmodel.cn/\n"
            "- 百度文心一言：https://ai.baidu.com/\n"
            "- 讯飞星火：https://xinghuo.xfyun.cn/\n"
            "- Claude：https://console.anthropic.com/\n"
            "- ChatGPT：https://platform.openai.com/\n"
            "- DeepSeek：https://platform.deepseek.com/\n"
            "- 硅基流动：https://cloud.siliconflow.cn/")
    
    # 免费API (国产大模型)
    st.subheader("🆓 免费API")
    st.write("以下是国产免费大模型，适合个人开发者使用：")
    
    # 阿里通义千问配置
    with st.expander("阿里通义千问"):
        st.info("💡 提示：请使用阿里通义千问API")
        st.write("获取方式：登录阿里云计算平台控制台，创建API密钥")
        st.markdown("[阿里通义千问控制台](https://dashscope.aliyun.com/)")
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
        st.info("💡 提示：请使用智谱AI API")
        st.write("获取方式：登录智谱AI开放平台，创建API密钥")
        st.markdown("[智谱AI开放平台](https://open.bigmodel.cn/)")
        zhipu_api_key = st.text_input("API Key", 
                                      value=st.session_state.api_keys['zhipu']['api_key'],
                                      type="password", 
                                      placeholder="输入智谱AI API Key",
                                      key="zhipu_api_key")
        if st.button("保存智谱配置"):
            st.session_state.api_keys['zhipu']['api_key'] = zhipu_api_key
            os.environ['ZHIPU_API_KEY'] = zhipu_api_key
            st.success("智谱配置已保存！")
    
    # 付费API
    st.subheader("💲 付费API")
    st.write("以下是需要付费的API，功能更强大：")
    
    # 百度文心一言配置
    with st.expander("百度文心一言"):
        st.info("💡 提示：请使用百度文心一言API")
        st.write("获取方式：登录百度AI开放平台，创建API密钥")
        st.markdown("[百度AI开放平台](https://ai.baidu.com/)")
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
    
    # 讯飞星火配置
    with st.expander("讯飞星火"):
        st.info("💡 提示：请使用讯飞星火的 HiDream 图像生成 API 配置")
        st.write("获取方式：登录讯飞开放平台控制台，在「星火大模型」的设置页面中获取")
        st.markdown("[讯飞开放平台](https://xinghuo.xfyun.cn/)")
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
    
    # Claude配置
    with st.expander("Claude"):
        st.info("💡 提示：请使用Anthropic的Claude API")
        st.write("获取方式：登录Anthropic控制台，创建API密钥")
        st.markdown("[Anthropic控制台](https://console.anthropic.com/)")
        claude_api_key = st.text_input("API Key", 
                                      value=st.session_state.api_keys.get('claude', {}).get('api_key', ''),
                                      type="password", 
                                      placeholder="输入Claude API Key",
                                      key="claude_api_key")
        if st.button("保存Claude配置"):
            if 'claude' not in st.session_state.api_keys:
                st.session_state.api_keys['claude'] = {}
            st.session_state.api_keys['claude']['api_key'] = claude_api_key
            os.environ['CLAUDE_API_KEY'] = claude_api_key
            st.success("Claude配置已保存！")
    
    # ChatGPT配置
    with st.expander("ChatGPT"):
        st.info("💡 提示：请使用OpenAI的ChatGPT API")
        st.write("获取方式：登录OpenAI控制台，创建API密钥")
        st.markdown("[OpenAI控制台](https://platform.openai.com/)")
        gpt_api_key = st.text_input("API Key", 
                                    value=st.session_state.api_keys.get('gpt', {}).get('api_key', ''),
                                    type="password", 
                                    placeholder="输入ChatGPT API Key",
                                    key="gpt_api_key")
        if st.button("保存ChatGPT配置"):
            if 'gpt' not in st.session_state.api_keys:
                st.session_state.api_keys['gpt'] = {}
            st.session_state.api_keys['gpt']['api_key'] = gpt_api_key
            os.environ['CHATGPT_API_KEY'] = gpt_api_key
            st.success("ChatGPT配置已保存！")
    
    # DeepSeek配置
    with st.expander("DeepSeek"):
        st.info("💡 提示：请使用DeepSeek的API")
        st.write("获取方式：登录DeepSeek控制台，创建API密钥")
        st.markdown("[DeepSeek控制台](https://platform.deepseek.com/)")
        deepseek_api_key = st.text_input("API Key", 
                                         value=st.session_state.api_keys.get('deepseek', {}).get('api_key', ''),
                                         type="password", 
                                         placeholder="输入DeepSeek API Key",
                                         key="deepseek_api_key")
        if st.button("保存DeepSeek配置"):
            if 'deepseek' not in st.session_state.api_keys:
                st.session_state.api_keys['deepseek'] = {}
            st.session_state.api_keys['deepseek']['api_key'] = deepseek_api_key
            os.environ['DEEPSEEK_API_KEY'] = deepseek_api_key
            st.success("DeepSeek配置已保存！")
    
    # 硅基流动配置
    with st.expander("硅基流动"):
        st.info("💡 提示：请使用硅基流动的API")
        st.write("获取方式：登录硅基流动控制台，创建API密钥")
        st.markdown("[硅基流动控制台](https://cloud.siliconflow.cn/)")
        silicon_api_key = st.text_input("API Key", 
                                        value=st.session_state.api_keys.get('silicon', {}).get('api_key', ''),
                                        type="password", 
                                        placeholder="输入硅基流动API Key",
                                        key="silicon_api_key")
        if st.button("保存硅基流动配置"):
            cleaned_api_key = clean_api_key(silicon_api_key)
            if 'silicon' not in st.session_state.api_keys:
                st.session_state.api_keys['silicon'] = {}
            st.session_state.api_keys['silicon']['api_key'] = cleaned_api_key
            os.environ['SILICON_API_KEY'] = cleaned_api_key
            st.success("硅基流动配置已保存！")
    
    # 一键保存所有配置
    st.divider()
    if st.button("💾 保存所有配置", type="primary"):
        # 保存所有配置到session state和环境变量
        st.session_state.api_configured = True
        st.success("✅ 所有API配置已保存！您可以开始使用其他功能了。")

# ==================== 文本生成功能 ====================

elif option == "文本生成":
    st.header("📝 游戏文本设计")
    st.write("为游戏项目生成高质量的文本内容，包括角色描述、剧情对话、任务文本、技能描述等游戏开发所需的各种文案。")
    
    # 检查API是否配置
    if not check_api_configured(st.session_state.selected_model):
        st.warning(f"⚠️ {st.session_state.selected_model} 的API密钥未配置，请在侧边栏选择其他模型或前往「API设置」页面配置")
    else:
        # 提示词模板库
        st.subheader("🎨 提示词模板库")
        template_category = st.selectbox("选择模板类型", list(TEXT_TEMPLATES.keys()))
        
        # 根据模板类型显示不同的参数输入
        template_params = {}
        if template_category == "游戏角色设计":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["character_class"] = st.text_input("职业", "战士", label_visibility="collapsed", key="tc_char_class")
            with col2:
                template_params["level_range"] = st.text_input("等级范围", "1-100", label_visibility="collapsed", key="tc_level_range")
            with col3:
                template_params["art_style"] = st.text_input("美术风格", "写实", label_visibility="collapsed", key="tc_art_style")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["color_scheme"] = st.text_input("配色方案", "暗色调", label_visibility="collapsed", key="tc_color")
            with col2:
                template_params["character_strength"] = st.text_input("角色优势", "高爆发", label_visibility="collapsed", key="tc_strength")
            with col3:
                template_params["game_world"] = st.text_input("世界观", "奇幻", label_visibility="collapsed", key="tc_world")
        elif template_category == "游戏剧情对话":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["time_period"] = st.text_input("时间", "黄昏", label_visibility="collapsed", key="td_time")
            with col2:
                template_params["location"] = st.text_input("地点", "城堡大厅", label_visibility="collapsed", key="td_location")
            with col3:
                template_params["atmosphere"] = st.text_input("氛围", "紧张", label_visibility="collapsed", key="td_atmosphere")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["character_count"] = st.text_input("角色数量", "2-4", label_visibility="collapsed", key="td_char_count")
            with col2:
                template_params["character_relationships"] = st.text_input("角色关系", "敌对", label_visibility="collapsed", key="td_relationships")
            with col3:
                template_params["branch_count"] = st.text_input("分支数量", "2", label_visibility="collapsed", key="td_branches")
        elif template_category == "游戏任务设计":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["quest_type"] = st.text_input("任务类型", "主线", label_visibility="collapsed", key="tq_type")
            with col2:
                template_params["difficulty_level"] = st.text_input("难度", "3", label_visibility="collapsed", key="tq_difficulty")
            with col3:
                template_params["level_requirement"] = st.text_input("等级要求", "20-30级", label_visibility="collapsed", key="tq_level")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["quest_background"] = st.text_input("任务背景", "拯救村庄", label_visibility="collapsed", key="tq_background")
            with col2:
                template_params["npc_info"] = st.text_input("NPC", "村长", label_visibility="collapsed", key="tq_npc")
            with col3:
                template_params["item_rewards"] = st.text_input("物品奖励", "装备+材料", label_visibility="collapsed", key="tq_items")
        elif template_category == "游戏技能系统":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["skill_type"] = st.text_input("技能类型", "主动", label_visibility="collapsed", key="ts_type")
            with col2:
                template_params["skill_category"] = st.text_input("技能分类", "魔法", label_visibility="collapsed", key="ts_category")
            with col3:
                template_params["skill_target"] = st.text_input("技能对象", "敌方", label_visibility="collapsed", key="ts_target")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["base_damage"] = st.text_input("基础伤害", "500", label_visibility="collapsed", key="ts_damage")
            with col2:
                template_params["cooldown"] = st.text_input("冷却时间", "10秒", label_visibility="collapsed", key="ts_cooldown")
            with col3:
                template_params["main_effect"] = st.text_input("主要效果", "造成伤害", label_visibility="collapsed", key="ts_main")
        elif template_category == "游戏世界观":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["world_name"] = st.text_input("世界名称", "艾泽拉斯", label_visibility="collapsed", key="tw_name")
            with col2:
                template_params["world_setting"] = st.text_input("世界设定", "魔幻", label_visibility="collapsed", key="tw_setting")
            with col3:
                template_params["geographical_regions"] = st.text_input("地理区域", "东部王国", label_visibility="collapsed", key="tw_geo")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["main_races"] = st.text_input("主要种族", "人类/兽人", label_visibility="collapsed", key="tw_races")
            with col2:
                template_params["main_factions"] = st.text_input("主要势力", "联盟/部落", label_visibility="collapsed", key="tw_factions")
            with col3:
                template_params["main_conflict"] = st.text_input("主要矛盾", "资源争夺", label_visibility="collapsed", key="tw_conflict")
        elif template_category == "游戏物品装备":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["item_category"] = st.text_input("物品分类", "装备", label_visibility="collapsed", key="ti_category")
            with col2:
                template_params["item_rarity"] = st.text_input("稀有度", "史诗", label_visibility="collapsed", key="ti_rarity")
            with col3:
                template_params["item_level_range"] = st.text_input("物品等级", "1-100", label_visibility="collapsed", key="ti_level")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["equipment_slot"] = st.text_input("装备部位", "武器", label_visibility="collapsed", key="ti_slot")
            with col2:
                template_params["item_stats"] = st.text_input("物品属性", "攻击+100", label_visibility="collapsed", key="ti_stats")
            with col3:
                template_params["acquisition_method"] = st.text_input("获取途径", "副本掉落", label_visibility="collapsed", key="ti_acquisition")
        
        if st.button("📋 应用模板"):
            # 填充模板参数
            template = TEXT_TEMPLATES[template_category]
            filled_template = template.format(**template_params)
            st.session_state.text_prompt = filled_template
        
        # 输入提示词
        prompt = st.text_area("提示词", value=st.session_state.get('text_prompt', ''), placeholder="例如：游戏角色描述、剧情对话、任务文本等", height=150)
        st.session_state.text_prompt = prompt
        
        col1, col2 = st.columns([1, 1])
        with col1:
            generate_btn = st.button("🚀 生成文本", type="primary")
        with col2:
            save_text_btn = st.markdown("""
            <style>
            button[data-testid="baseButton-secondary"] {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            save_text_btn = st.button("💾 保存文本", key="save_text_btn")
        
        # 显示保存的生成结果
        if 'generated_text' in st.session_state and st.session_state.generated_text:
            st.success("生成成功！")
            st.markdown("### 生成结果")
            st.write(st.session_state.generated_text)
            st.code(st.session_state.generated_text, language="text")
        
        if save_text_btn:
            if 'generated_text' in st.session_state and st.session_state.generated_text:
                st.download_button(
                    label="💾 保存文本",
                    data=st.session_state.generated_text,
                    file_name=f"generated_text_{st.session_state.selected_model}.txt",
                    mime="text/plain"
                )
        
        if generate_btn:
            if not prompt:
                st.error("请输入提示词")
            else:
                with st.spinner("生成中..."):
                    try:
                        # 调用文本生成函数
                        result, elapsed_time, tokens = generate_text(prompt, st.session_state.selected_model)
                        # 保存结果到会话状态
                        st.session_state.generated_text = result
                        # 直接显示结果，不需要刷新页面
                        st.success("生成成功！")
                        st.markdown("### 生成结果")
                        st.write(result)
                        st.code(result, language="text")
                        # 显示耗时和Token消耗
                        st.info(f"本次耗时：{elapsed_time:.2f}秒 | 消耗Token：{tokens}")
                    except Exception as e:
                        st.error(f"生成失败：{str(e)}")

# ==================== 图像生成功能 ====================

elif option == "图像生成":
    st.header("🖼️ 游戏美术资源")
    st.write("为游戏项目生成高质量的美术资源，包括游戏场景、角色设计、道具图标、UI元素等游戏开发所需的各种视觉素材。")
    
    # 检查API是否配置
    if not check_api_configured(st.session_state.selected_model):
        st.warning(f"⚠️ {st.session_state.selected_model} 的API密钥未配置，请在侧边栏选择其他模型或前往「API设置」页面配置")
    else:
        # 提示词模板库
        st.subheader("🎨 提示词模板库")
        template_category = st.selectbox("选择模板类型", list(IMAGE_TEMPLATES.keys()))
        
        # 根据模板类型显示不同的参数输入
        template_params = {}
        if template_category == "游戏角色原画":
            template_params["additional_style"] = st.text_input("附加风格", "写实风格，光影效果丰富", label_visibility="collapsed", key="ic_additional_style")
        elif template_category == "游戏场景概念":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["style_type"] = st.text_input("风格类型", "奇幻风格", label_visibility="collapsed", key="ic_style_type")
            with col2:
                template_params["mood"] = st.text_input("氛围", "神秘", label_visibility="collapsed", key="ic_mood")
            with col3:
                template_params["time_of_day"] = st.text_input("时间", "黄昏", label_visibility="collapsed", key="ic_time")
            col1, col2 = st.columns(2)
            with col1:
                template_params["weather"] = st.text_input("天气", "多云", label_visibility="collapsed", key="ic_weather")
            with col2:
                template_params["technical_specs"] = st.text_input("技术规格", "4K分辨率，超宽视角", label_visibility="collapsed", key="ic_tech_specs")
        elif template_category == "游戏道具图标":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["icon_type"] = st.text_input("图标类型", "武器", label_visibility="collapsed", key="ic_icon_type")
            with col2:
                template_params["rarity"] = st.text_input("稀有度", "传说", label_visibility="collapsed", key="ic_rarity")
            with col3:
                template_params["style"] = st.text_input("风格", "扁平化", label_visibility="collapsed", key="ic_style")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["color_scheme"] = st.text_input("配色方案", "金色+红色", label_visibility="collapsed", key="ic_color_scheme")
            with col2:
                template_params["background"] = st.text_input("背景", "深色背景", label_visibility="collapsed", key="ic_background")
            with col3:
                template_params["specs"] = st.text_input("规格", "256x256像素", label_visibility="collapsed", key="ic_specs")
        elif template_category == "游戏UI界面":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["ui_type"] = st.text_input("界面类型", "主菜单", label_visibility="collapsed", key="ic_ui_type")
            with col2:
                template_params["ui_style"] = st.text_input("UI风格", "现代简约", label_visibility="collapsed", key="ic_ui_style")
            with col3:
                template_params["color_scheme"] = st.text_input("配色方案", "深色主题", label_visibility="collapsed", key="ic_ui_color")
            col1, col2 = st.columns(2)
            with col1:
                template_params["typography"] = st.text_input("字体风格", "无衬线字体", label_visibility="collapsed", key="ic_typography")
            with col2:
                template_params["effects"] = st.text_input("特效", "悬停动画", label_visibility="collapsed", key="ic_effects")
        elif template_category == "游戏特效动画":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["skill_type"] = st.text_input("技能类型", "火球术", label_visibility="collapsed", key="ic_skill_type")
            with col2:
                template_params["effect_style"] = st.text_input("特效风格", "粒子爆炸", label_visibility="collapsed", key="ic_effect_style")
            with col3:
                template_params["color_palette"] = st.text_input("配色", "橙色+红色", label_visibility="collapsed", key="ic_color_palette")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["intensity"] = st.text_input("强度", "高", label_visibility="collapsed", key="ic_intensity")
            with col2:
                template_params["particles"] = st.text_input("粒子效果", "火花+烟雾", label_visibility="collapsed", key="ic_particles")
            with col3:
                template_params["technical_format"] = st.text_input("技术格式", "序列帧+粒子系统", label_visibility="collapsed", key="ic_tech_format")
        elif template_category == "游戏地图设计":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["map_type"] = st.text_input("地图类型", "野外地图", label_visibility="collapsed", key="ic_map_type")
            with col2:
                template_params["map_style"] = st.text_input("地图风格", "手绘风格", label_visibility="collapsed", key="ic_map_style")
            with col3:
                template_params["grid_type"] = st.text_input("网格类型", "六边形", label_visibility="collapsed", key="ic_grid_type")
            col1, col2 = st.columns(2)
            with col1:
                template_params["color_scheme"] = st.text_input("配色方案", "自然色调", label_visibility="collapsed", key="ic_map_color")
            with col2:
                template_params["icons"] = st.text_input("图标", "简化图标", label_visibility="collapsed", key="ic_icons")
        elif template_category == "游戏加载界面":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["loading_type"] = st.text_input("加载类型", "游戏主题", label_visibility="collapsed", key="ic_loading_type")
            with col2:
                template_params["bg_style"] = st.text_input("背景风格", "动态背景", label_visibility="collapsed", key="ic_bg_style")
            with col3:
                template_params["progress_bar_style"] = st.text_input("进度条样式", "发光进度条", label_visibility="collapsed", key="ic_progress")
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["text_style"] = st.text_input("文字样式", "白色粗体", label_visibility="collapsed", key="ic_text_style")
            with col2:
                template_params["animations"] = st.text_input("动画", "旋转加载图标", label_visibility="collapsed", key="ic_animations")
            with col3:
                template_params["resolution"] = st.text_input("分辨率", "1920x1080", label_visibility="collapsed", key="ic_resolution")
        
        if st.button("📋 应用模板"):
            # 填充模板参数
            template = IMAGE_TEMPLATES[template_category]
            filled_template = template.format(**template_params)
            st.session_state.image_prompt = filled_template
        
        # 输入提示词
        prompt = st.text_area("提示词", value=st.session_state.get('image_prompt', ''), placeholder="例如：游戏场景、角色设计、道具图标等", height=150)
        st.session_state.image_prompt = prompt
        
        col1, col2 = st.columns([1, 1])
        with col1:
            generate_btn = st.button("🚀 生成图像", type="primary")
        with col2:
            st.markdown("""
            <style>
            button[data-testid="baseButton-secondary"] {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            save_image_btn = st.button("💾 保存图像", key="save_image_btn")
        
        # 显示保存的生成结果
        if 'generated_image' in st.session_state and st.session_state.generated_image:
            st.success("生成成功！")
            st.markdown("### 生成结果")
            st.image(st.session_state.generated_image, width=600, clamp=True, caption="生成的图像")
        
        if save_image_btn:
            if 'generated_image' in st.session_state and st.session_state.generated_image:
                # 提供下载按钮
                if st.session_state.generated_image.startswith('http'):
                    response = requests.get(st.session_state.generated_image)
                    if response.status_code == 200:
                        st.download_button(
                            label="💾 保存图像",
                            data=response.content,
                            file_name=f"generated_image_{st.session_state.selected_model}.png",
                            mime="image/png"
                        )
        
        if generate_btn:
            if not prompt:
                st.error("请输入提示词")
            else:
                with st.spinner("生成中..."):
                    try:
                        # 调用图像生成函数
                        image_url, elapsed_time, tokens = generate_image(prompt, st.session_state.selected_model)
                        # 保存结果到会话状态
                        st.session_state.generated_image = image_url
                        # 直接显示结果，不需要刷新页面
                        st.success("生成成功！")
                        st.markdown("### 生成结果")
                        st.image(image_url, width=600, clamp=True, caption="生成的图像")
                        
                        # 提供下载按钮
                        if image_url.startswith('http'):
                            response = requests.get(image_url)
                            if response.status_code == 200:
                                st.download_button(
                                    label="💾 下载图像",
                                    data=response.content,
                                    file_name=f"generated_image_{st.session_state.selected_model}.png",
                                    mime="image/png"
                                )
                        # 显示耗时和Token消耗
                        st.info(f"本次耗时：{elapsed_time:.2f}秒 | 消耗Token：{tokens}")
                    except Exception as e:
                        st.error(f"生成失败：{str(e)}")

# ==================== 数据生成功能 ====================

elif option == "数据生成":
    st.header("📊 游戏数据配置")
    st.write("为游戏项目生成结构化的数据配置，包括角色属性表、任务列表、物品数据、技能参数等游戏开发所需的各种数据表格。")
    
    # 检查API是否配置
    if not check_api_configured(st.session_state.selected_model):
        st.warning(f"⚠️ {st.session_state.selected_model} 的API密钥未配置，请在侧边栏选择其他模型或前往「API设置」页面配置")
    else:
        # 提示词模板库
        st.subheader("🎨 提示词模板库")
        template_category = st.selectbox("选择模板类型", list(DATA_TEMPLATES.keys()))
        
        # 根据模板类型显示不同的参数输入
        template_params = {}
        if template_category == "游戏角色属性":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["character_count"] = st.text_input("角色数量", "5-10", label_visibility="collapsed", key="dc_char_count")
            with col2:
                template_params["character_types"] = st.text_input("职业类型", "战士/法师/刺客", label_visibility="collapsed", key="dc_char_types")
            with col3:
                template_params["level_range"] = st.text_input("等级范围", "1-100", label_visibility="collapsed", key="dc_level_range")
        elif template_category == "游戏物品数据":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["item_count"] = st.text_input("物品数量", "10-15", label_visibility="collapsed", key="di_item_count")
            with col2:
                template_params["item_types"] = st.text_input("物品类型", "武器/护甲/饰品", label_visibility="collapsed", key="di_item_types")
            with col3:
                template_params["rarities"] = st.text_input("稀有度", "普通/稀有/史诗", label_visibility="collapsed", key="di_rarities")
        elif template_category == "游戏任务数据":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["quest_count"] = st.text_input("任务数量", "8-12", label_visibility="collapsed", key="dq_quest_count")
            with col2:
                template_params["quest_types"] = st.text_input("任务类型", "主线/支线/日常", label_visibility="collapsed", key="dq_quest_types")
            with col3:
                template_params["difficulty_range"] = st.text_input("难度范围", "1-5星", label_visibility="collapsed", key="dq_difficulty")
        elif template_category == "游戏敌人数据":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["enemy_count"] = st.text_input("敌人数量", "10-15", label_visibility="collapsed", key="de_enemy_count")
            with col2:
                template_params["enemy_types"] = st.text_input("敌人类型", "普通/精英/Boss", label_visibility="collapsed", key="de_enemy_types")
            with col3:
                template_params["level_range"] = st.text_input("等级范围", "1-100", label_visibility="collapsed", key="de_level_range")
        elif template_category == "游戏对话脚本":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["dialogue_count"] = st.text_input("对话数量", "15-20", label_visibility="collapsed", key="dd_dialogue_count")
            with col2:
                template_params["dialogue_types"] = st.text_input("对话类型", "NPC对话/系统对话", label_visibility="collapsed", key="dd_dialogue_types")
            with col3:
                template_params["dialogue_rounds"] = st.text_input("对话轮数", "3-5", label_visibility="collapsed", key="dd_dialogue_rounds")
        elif template_category == "游戏技能配置":
            col1, col2, col3 = st.columns(3)
            with col1:
                template_params["skill_count"] = st.text_input("技能数量", "12-18", label_visibility="collapsed", key="ds_skill_count")
            with col2:
                template_params["skill_types"] = st.text_input("技能类型", "主动/被动/终极", label_visibility="collapsed", key="ds_skill_types")
            with col3:
                template_params["skill_categories"] = st.text_input("技能分类", "物理/魔法/控制", label_visibility="collapsed", key="ds_skill_categories")
        
        if st.button("📋 应用模板"):
            # 填充模板参数
            template = DATA_TEMPLATES[template_category]
            filled_template = template.format(**template_params)
            st.session_state.data_prompt = filled_template
        
        # 输入提示词
        prompt = st.text_area("提示词", value=st.session_state.get('data_prompt', ''), placeholder="例如：生成一个RPG游戏的角色属性表，包含名称、等级、生命值、攻击力等字段", height=150)
        st.session_state.data_prompt = prompt
        
        # 选择数据类型
        data_type = st.selectbox(
            "选择数据格式",
            ("JSON", "XLSX", "mindmap")
        )
        
        # 初始化会话状态变量
        if 'generated_data' not in st.session_state:
            st.session_state.generated_data = None
        if 'generated_filename' not in st.session_state:
            st.session_state.generated_filename = None
        if 'generated_data_type' not in st.session_state:
            st.session_state.generated_data_type = None
        
        # 当数据格式切换时，清除之前生成的数据，减少卡顿
        if st.session_state.generated_data_type and st.session_state.generated_data_type != data_type:
            st.session_state.generated_data = None
            st.session_state.generated_filename = None
            st.session_state.generated_data_type = None
        
        # 生成按钮和操作按钮区域
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            generate_btn = st.button("🚀 生成数据", type="primary")
        
        # 显示保存的生成结果和下载按钮
        if st.session_state.generated_data is not None:
            current_data_type = st.session_state.generated_data_type
            
            st.success("生成成功！")
            st.markdown("### 生成结果")
            
            # 显示生成结果
            if current_data_type == "JSON":
                st.json(st.session_state.generated_data)
            elif current_data_type == "XLSX":
                st.dataframe(st.session_state.generated_data)
            elif current_data_type == "mindmap":
                st.text(st.session_state.generated_data)
            
            # 下载按钮
            with col2:
                if current_data_type == "JSON":
                    json_str = json.dumps(st.session_state.generated_data, ensure_ascii=False, indent=2)
                    st.download_button(
                        label="💾 下载当前数据",
                        data=json_str,
                        file_name=st.session_state.generated_filename,
                        mime="application/json"
                    )
                elif current_data_type == "XLSX":
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        st.session_state.generated_data.to_excel(writer, index=False, sheet_name='Sheet1')
                    st.download_button(
                        label="💾 下载当前数据",
                        data=buffer.getvalue(),
                        file_name=st.session_state.generated_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                elif current_data_type == "mindmap":
                    st.download_button(
                        label="💾 下载当前数据",
                        data=st.session_state.generated_data,
                        file_name=st.session_state.generated_filename,
                        mime="application/xmind"
                    )
        
        if generate_btn:
            if not prompt:
                st.error("请输入提示词")
            else:
                with st.spinner("生成中..."):
                    try:
                        # 调用数据生成函数
                        data, filename, elapsed_time, tokens = generate_data(prompt, data_type, st.session_state.selected_model)
                        
                        if data is not None:
                            # 保存生成的数据到会话状态
                            st.session_state.generated_data = data
                            st.session_state.generated_filename = filename
                            st.session_state.generated_data_type = data_type
                            
                            # 直接显示结果和下载按钮，不需要刷新页面
                            st.success("生成成功！")
                            st.markdown("### 生成结果")
                            
                            # 显示生成结果
                            if data_type == "JSON":
                                st.json(data)
                            elif data_type == "XLSX":
                                st.dataframe(data)
                            elif data_type == "mindmap":
                                st.text(data)
                            
                            # 下载按钮
                            with col2:
                                if data_type == "JSON":
                                    json_str = json.dumps(data, ensure_ascii=False, indent=2)
                                    st.download_button(
                                        label="💾 下载当前数据",
                                        data=json_str,
                                        file_name=filename,
                                        mime="application/json"
                                    )
                                elif data_type == "XLSX":
                                    buffer = BytesIO()
                                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                        data.to_excel(writer, index=False, sheet_name='Sheet1')
                                    st.download_button(
                                        label="💾 下载当前数据",
                                        data=buffer.getvalue(),
                                        file_name=filename,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                    )
                                elif data_type == "mindmap":
                                    st.download_button(
                                        label="💾 下载当前数据",
                                        data=data,
                                        file_name=filename,
                                        mime="application/xmind"
                                    )
                            # 显示耗时和Token消耗
                            st.info(f"本次耗时：{elapsed_time:.2f}秒 | 消耗Token：{tokens}")
                        else:
                            st.error(filename)  # 显示错误信息
                            
                    except Exception as e:
                        st.error(f"生成失败：{str(e)}")

# ==================== 多语言在地化功能 ====================

elif option == "多语言在地化":
    st.header("🌍 游戏多语言本地化")
    st.write("为游戏项目提供多语言支持，将游戏文本翻译为多种语言版本，并导出为游戏引擎通用的格式，方便游戏的国际化部署。")
    
    # 检查API是否配置
    if not check_api_configured(st.session_state.selected_model):
        st.warning(f"⚠️ {st.session_state.selected_model} 的API密钥未配置，请在侧边栏选择其他模型或前往「API设置」页面配置")
    else:
        # 输入文本
        text = st.text_area("输入要翻译的文本", placeholder="例如：游戏中的对话、物品描述、任务文本等", height=200)
        
        # 选择目标语言
        target_languages = st.multiselect(
            "选择目标语言",
            list(SUPPORTED_LANGUAGES.keys()),
            default=["英文", "日文", "韩文"]
        )
        
        # 初始化会话状态变量
        if 'translations' not in st.session_state:
            st.session_state.translations = {}
        if 'translated_text' not in st.session_state:
            st.session_state.translated_text = None
        
        # 生成按钮和操作按钮区域
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            translate_btn = st.button("🌐 开始翻译", type="primary")
        
        # 显示保存的翻译结果和下载按钮
        if st.session_state.translations:
            st.success("翻译成功！")
            st.markdown("### 翻译结果")
            
            # 显示翻译结果
            for lang, translation in st.session_state.translations.items():
                with st.expander(f"{lang}"):
                    st.text(translation)
            
            # 下载按钮
            with col2:
                # 生成CSV格式数据
                import csv
                import io
                
                # 创建CSV内容
                csv_output = io.StringIO()
                writer = csv.writer(csv_output)
                
                # 写入表头
                headers = ['原文'] + target_languages
                writer.writerow(headers)
                
                # 按行写入数据
                lines = text.split('\n')
                for line in lines:
                    if line.strip():
                        row = [line]
                        for lang in target_languages:
                            if lang in st.session_state.translations:
                                # 找到对应行的翻译
                                trans_lines = st.session_state.translations[lang].split('\n')
                                # 简单匹配：假设翻译结果的行数与原文相同
                                if len(trans_lines) > len(row) - 1:
                                    row.append(trans_lines[len(row) - 1])
                                else:
                                    row.append('')
                            else:
                                row.append('')
                        writer.writerow(row)
                
                csv_content = csv_output.getvalue()
                st.download_button(
                    label="💾 下载翻译结果 (CSV)",
                    data=csv_content,
                    file_name="translations.csv",
                    mime="text/csv"
                )
        
        if translate_btn:
            if not text:
                st.error("请输入要翻译的文本")
            elif not target_languages:
                st.error("请至少选择一种目标语言")
            else:
                with st.spinner("翻译中..."):
                    try:
                        # 初始化翻译结果字典
                        translations = {}
                        
                        # 翻译到每种目标语言
                        for lang in target_languages:
                            result, status = translate_text_for_model(text, lang, st.session_state.selected_model)
                            if result:
                                translations[lang] = result
                            else:
                                translations[lang] = f"翻译失败：{status}"
                        
                        # 保存翻译结果到会话状态
                        st.session_state.translations = translations
                        st.session_state.translated_text = text
                        
                        # 直接显示结果和下载按钮，不需要刷新页面
                        st.success("翻译成功！")
                        st.markdown("### 翻译结果")
                        
                        # 显示翻译结果
                        for lang, translation in translations.items():
                            with st.expander(f"{lang}"):
                                st.text(translation)
                        
                        # 下载按钮
                        with col2:
                            # 生成CSV格式数据
                            import csv
                            import io
                            
                            # 创建CSV内容
                            csv_output = io.StringIO()
                            writer = csv.writer(csv_output)
                            
                            # 写入表头
                            headers = ['原文'] + target_languages
                            writer.writerow(headers)
                            
                            # 按行写入数据
                            lines = text.split('\n')
                            for line in lines:
                                if line.strip():
                                    row = [line]
                                    for lang in target_languages:
                                        if lang in translations:
                                            # 找到对应行的翻译
                                            trans_lines = translations[lang].split('\n')
                                            # 简单匹配：假设翻译结果的行数与原文相同
                                            if len(trans_lines) > len(row) - 1:
                                                row.append(trans_lines[len(row) - 1])
                                            else:
                                                row.append('')
                                        else:
                                            row.append('')
                                    writer.writerow(row)
                            
                            csv_content = csv_output.getvalue()
                            st.download_button(
                                label="💾 下载翻译结果 (CSV)",
                                data=csv_content,
                                file_name="translations.csv",
                                mime="text/csv"
                            )
                        
                    except Exception as e:
                        st.error(f"翻译失败：{str(e)}")

# ==================== 玩家体验预测器 ====================

elif option == "玩家体验预测器":
    st.header("🎮 玩家体验预测器 (Player Experience Predictor)")
    st.write("基于 Lankes (2023) 提出的 Player Experience Inventory (PXI) 框架，利用 AI 分析游戏玩法描述，预测玩家体验维度的评分并生成雷達圖。")
    
    # 学术背景介绍
    display_academic_background()
    
    # 检查API是否配置
    if not check_api_configured(st.session_state.selected_model):
        st.warning(f"⚠️ {st.session_state.selected_model} 的API密钥未配置，请在侧边栏选择其他模型或前往「API设置」页面配置")
    else:
        # 输入游戏玩法描述
        gameplay_description = st.text_area(
            "输入游戏玩法描述", 
            placeholder="例如：玩家扮演一名能操纵阴影的刺客。在名为「光辉塔」的​​关卡中，地板会周期性地被强光照射。玩家必须在强光来临前，利用「影遁」技能跳跃到移动的守卫影子中躲避伤害。", 
            height=200
        )
        
        # 分析按钮
        if st.button("🔍 分析玩家体验", type="primary"):
            if not gameplay_description:
                st.error("请输入游戏玩法描述")
            else:
                with st.spinner("分析中..."):
                    # 调用PXI分析函数
                    dimensions, scores, analysis, elapsed_time, tokens, error = analyze_pxi_dimensions(gameplay_description, st.session_state.selected_model)
                    
                    if error:
                        st.error(error)
                    else:
                        # 显示分析结果
                        display_pxi_results(dimensions, scores, analysis, elapsed_time, tokens)

# ==================== 关卡原型生成器 ====================

elif option == "关卡原型生成器":
    st.header("🏗️ 关卡原型生成器 (Mixed-Initiative Level Designer)")
    st.write("基于 Togelius (2015) 与 Ratican (2024) 提出的混合主动式设计理念，实现 AI 与人类设计师协同的关卡设计工具。")
    
    # 学术背景介绍
    display_level_academic_background()
    display_level_elements_reference()
    
    # 检查API是否配置
    if not check_api_configured(st.session_state.selected_model):
        st.warning(f"⚠️ {st.session_state.selected_model} 的API密钥未配置，请在侧边栏选择其他模型或前往「API设置」页面配置")
    else:
        # 关卡参数设置
        col1, col2, col3 = st.columns(3)
        with col1:
            level_width = st.number_input("地图宽度", min_value=5, max_value=20, value=10)
        with col2:
            level_height = st.number_input("地图高度", min_value=5, max_value=20, value=10)
        with col3:
            level_shape = st.selectbox("地图形状", ["矩形", "不规则", "圆形", "L形", "十字形", "U形"], index=0, key="level_shape")
        
        # 关卡描述输入
        level_description = st.text_area(
            "关卡描述",
            placeholder="例如：一个地下城关卡，玩家需要从入口找到出口，途中会遇到怪物和陷阱...",
            height=100
        )
        
        # 生成关卡按钮
        col1, col2 = st.columns([2, 1])
        with col1:
            generate_btn = st.button("🎲 生成关卡", type="primary")
        with col2:
            if 'generated_ascii_map' in st.session_state and st.session_state.generated_ascii_map:
                # 下载ASCII为txt文件
                txt_content = st.session_state.generated_ascii_map
                st.download_button(
                    label="📥 下载ASCII地图",
                    data=txt_content,
                    file_name="level_map.txt",
                    mime="text/plain",
                    key="download_ascii"
                )
        
        if generate_btn:
            if not level_description:
                st.error("请输入关卡描述")
            else:
                with st.spinner("生成关卡中..."):
                    ascii_map, json_map, level_desc, elapsed_time, tokens, error = generate_level(
                        level_description, level_width, level_height, st.session_state.selected_model, level_shape
                    )
                    
                    if error:
                        st.error(error)
                    else:
                        # 清除之前的内容
                        for key in ['level_story', 'generated_ascii_map', 'generated_json_map', 'level_desc']:
                            if key in st.session_state:
                                del st.session_state[key]
                        
                        # 保存到session state
                        st.session_state.generated_ascii_map = ascii_map
                        st.session_state.generated_json_map = json_map
                        st.session_state.level_desc = level_desc
                        st.success("关卡生成成功！")
        
        # 显示生成的关卡
        if 'generated_ascii_map' in st.session_state and st.session_state.generated_ascii_map:
            st.markdown("### 🗺️ 生成的关卡地图")
            
            # 使用等宽字体显示ASCII地图
            st.text_area(
                "ASCII地图（可直接编辑）",
                value=st.session_state.generated_ascii_map,
                height=300,
                key="ascii_map_editor"
            )
            
            # 显示JSON格式
            with st.expander("📊 JSON格式"):
                st.json(st.session_state.generated_json_map)
            
            # 验证地图
            is_valid, message = validate_ascii_map(st.session_state.generated_ascii_map)
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
            
            # 生成背景故事按钮
            if st.button("📖 生成背景故事和怪物配置"):
                with st.spinner("生成中..."):
                    story_data, elapsed_time, tokens, error = generate_level_story(
                        st.session_state.generated_ascii_map, 
                        st.session_state.selected_model
                    )
                    
                    if error:
                        st.error(error)
                    else:
                        st.session_state.level_story = story_data
                        st.success("背景故事生成成功！")
            
            # 显示背景故事
            if 'level_story' in st.session_state and st.session_state.level_story:
                st.markdown("### 📚 关卡背景故事")
                st.write(st.session_state.level_story.get('background_story', ''))
                
                # 显示怪物配置
                st.markdown("### 👹 怪物配置")
                monster_config = st.session_state.level_story.get('monster_config', [])
                if monster_config:
                    for monster in monster_config:
                        with st.expander(f"{monster.get('name', '未知怪物')} ({monster.get('symbol', '?')})"):
                            st.write(f"**描述:** {monster.get('description', '')}")
                            st.write(f"**生命值:** {monster.get('hp', 0)}")
                            st.write(f"**攻击力:** {monster.get('attack', 0)}")
                            st.write(f"**行为模式:** {monster.get('behavior', '')}")
                
                # 显示设计要点
                st.markdown("### 💡 关卡设计要点")
                st.write(st.session_state.level_story.get('level_design_notes', ''))
                
                # 显示耗时和Token
                st.info(f"本次耗时：{elapsed_time:.2f}秒 | 消耗Token：{tokens}")

# ==================== VGDL生成器 ====================

elif option == "VGDL生成器":
    st.header("🎮 VGDL生成器 (Video Game Description Language)")
    st.write("将自然语言游戏描述转换为 VGDL 代码，实现游戏逻辑的数字化表达。")
    
    # 学术背景介绍
    display_vgdl_academic_background()
    display_vgdl_template()
    
    # 检查API是否配置
    if not check_api_configured(st.session_state.selected_model):
        st.warning(f"⚠️ {st.session_state.selected_model} 的API密钥未配置，请在侧边栏选择其他模型或前往「API设置」页面配置")
    else:
        # 双窗口布局
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("### 📝 自然语言描述")
            game_description = st.text_area(
                "输入游戏描述",
                placeholder="例如：一个射击游戏，玩家控制飞船发射子弹攻击外星飞船，外星飞船会向下移动，玩家被击中则游戏结束，消灭所有外星飞船则获胜...",
                height=300
            )
            
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                generate_vgdl_btn = st.button("🚀 生成VGDL代码", type="primary")
            with col1_2:
                if 'generated_vgdl' in st.session_state and st.session_state.generated_vgdl:
                    st.download_button(
                        label="📥 下载VGDL文件",
                        data=st.session_state.generated_vgdl,
                        file_name="game.vgdl",
                        mime="text/plain",
                        key="download_vgdl"
                    )
        
        with col2:
            st.markdown("### 🖥️ VGDL代码")
            if 'generated_vgdl' in st.session_state and st.session_state.generated_vgdl:
                st.code(st.session_state.generated_vgdl, language="plaintext")
                
                # 逻辑检查按钮
                if st.button("🔍 逻辑检查"):
                    issues = check_vgdl_logic(st.session_state.generated_vgdl)
                    if issues:
                        st.error("❌ 发现以下问题：")
                        for issue in issues:
                            st.write(f"- {issue}")
                    else:
                        st.success("✅ 代码逻辑检查通过！")
                
                # 显示耗时和Token
                if 'vgdl_elapsed_time' in st.session_state and 'vgdl_tokens' in st.session_state:
                    st.info(f"本次耗时：{st.session_state.vgdl_elapsed_time:.2f}秒 | 消耗Token：{st.session_state.vgdl_tokens}")
            else:
                st.info("生成的VGDL代码将显示在这里")
        
        if generate_vgdl_btn:
            if not game_description:
                st.error("请输入游戏描述")
            else:
                with st.spinner("生成VGDL代码中..."):
                    vgdl_code, elapsed_time, tokens, error = generate_vgdl(
                        game_description, st.session_state.selected_model
                    )
                    
                    if error:
                        st.error(error)
                    else:
                        # 保存到session state
                        st.session_state.generated_vgdl = vgdl_code
                        st.session_state.vgdl_elapsed_time = elapsed_time
                        st.session_state.vgdl_tokens = tokens
                        st.success("VGDL代码生成成功！")
                        
                        # 重新渲染页面以显示更新后的内容
                        st.experimental_rerun()

# ==================== 致谢页面 ====================

elif option == "致谢":
    st.header("🙏 致谢")
    st.write("""
    感谢所有支持和帮助本项目的人员！
    
    **作者:** 
    
    **联系方式:** 
    
    **指导老师:** 
    """)
    
    st.subheader("📝 免责声明")
    st.write("""
    **免责声明**
    
    本工具仅供学术交流和学习使用，不得用于商业目的。使用者在使用本工具前，请仔细阅读并理解以下免责声明内容：
    
    **1. 使用范围**
    - 本工具仅用于学术研究、教育教学和个人学习目的
    - 禁止将本工具用于任何商业活动、盈利目的或其他非学术用途
    - 禁止将本工具用于任何违法或不道德的活动
    
    **2. 责任限制**
    - 使用本工具产生的任何内容，由使用者自行承担全部责任，与工具开发者无关
    - 工具开发者不对使用本工具产生的任何直接或间接损失负责
    - 工具开发者不对使用本工具产生的内容的准确性、完整性或合法性负责
    - 工具开发者不保证本工具的稳定性、可靠性或安全性
    
    **3. 知识产权**
    - 本工具可能使用了第三方API和资源，使用者应确保遵守相关服务条款和知识产权规定
    - 使用本工具生成的内容可能受到相关法律法规的保护，使用者应确保合法使用
    - 禁止将本工具或其任何部分用于侵犯他人知识产权的行为
    
    **4. 数据处理与隐私**
    - 使用者应注意保护个人隐私和敏感信息，避免在工具中输入涉及个人隐私或商业机密的内容
    - 工具开发者不对因使用本工具而导致的任何数据泄露或信息安全问题负责
    - 使用者应自行承担数据备份和安全保障的责任
    
    **5. 法律合规**
    - 使用者应确保其使用行为符合所在国家和地区的法律法规
    - 使用者应遵守相关API提供商的服务条款和使用规定
    - 如因使用本工具违反相关法律法规，使用者应自行承担全部法律责任
    
    **6. 工具使用风险**
    - 本工具基于人工智能技术，可能存在生成内容不准确、不适当或有偏见的风险
    - 使用者应对生成内容进行审查和判断，不应盲目依赖
    - 工具开发者不对因使用生成内容而导致的任何损失负责
    
    **7. 变更与终止**
    - 工具开发者保留随时修改、暂停或终止本工具服务的权利
    - 工具开发者无义务提前通知使用者关于工具的变更或终止
    
    **8. 适用法律**
    - 本免责声明受中华人民共和国法律管辖
    - 如本免责声明的任何条款被认定为无效或不可执行，不影响其他条款的效力
    
    使用者使用本工具，即表示同意接受本免责声明的全部内容。如不同意本免责声明的任何部分，应立即停止使用本工具。
    """)

# ==================== 回到顶部按钮 ====================

# 添加回到顶部按钮
st.markdown("""
<style>
.back-to-top {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    background-color: #000000;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    text-decoration: none;
    border: 2px solid white;
}

.back-to-top:hover {
    background-color: #333333;
    transform: translateY(-5px);
}

.back-to-top svg {
    width: 24px;
    height: 24px;
}
</style>

<a href="#" class="back-to-top"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" /></svg></a>
""", unsafe_allow_html=True)


