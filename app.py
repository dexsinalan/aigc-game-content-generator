import streamlit as st
import requests
import json
import os
import pandas as pd
import base64
import time
from io import BytesIO
from dotenv import load_dotenv
from utils.text_generator import generate_text_for_model
from utils.image_generator import generate_image_for_model
from utils.data_generator import generate_json_data, generate_xlsx_data, generate_mindmap_data
from utils.translation_generator import translate_text_for_model, SUPPORTED_LANGUAGES

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
        return None, "不支持的数据类型"

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
thanks_btn = st.sidebar.button("🙏 致谢", use_container_width=True, key="btn_thanks")


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
elif thanks_btn:
    st.session_state.current_page = "致谢"


# 设置当前选项
option = st.session_state.current_page

# ==================== 模型选择 ====================
if option in ["文本生成", "图像生成", "数据生成", "多语言在地化"]:
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
        # 输入提示词
        prompt = st.text_area("提示词", placeholder="例如：游戏角色描述、剧情对话、任务文本等", height=150)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            generate_btn = st.button("🚀 生成文本", type="primary")
        
        # 显示保存的生成结果
        if 'generated_text' in st.session_state and st.session_state.generated_text:
            st.success("生成成功！")
            st.markdown("### 生成结果")
            st.write(st.session_state.generated_text)
            st.code(st.session_state.generated_text, language="text")
        
        if generate_btn:
            if not prompt:
                st.error("请输入提示词")
            else:
                with st.spinner("生成中..."):
                    try:
                        # 调用文本生成函数
                        result = generate_text(prompt, st.session_state.selected_model)
                        # 保存结果到会话状态
                        st.session_state.generated_text = result
                        # 直接显示结果，不需要刷新页面
                        st.success("生成成功！")
                        st.markdown("### 生成结果")
                        st.write(result)
                        st.code(result, language="text")
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
        # 输入提示词
        prompt = st.text_area("提示词", placeholder="例如：游戏场景、角色设计、道具图标等", height=150)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            generate_btn = st.button("🚀 生成图像", type="primary")
        
        # 显示保存的生成结果
        if 'generated_image' in st.session_state and st.session_state.generated_image:
            st.success("生成成功！")
            st.markdown("### 生成结果")
            st.image(st.session_state.generated_image, use_container_width=True)
            
            # 提供下载按钮
            if st.session_state.generated_image.startswith('http'):
                response = requests.get(st.session_state.generated_image)
                if response.status_code == 200:
                    st.download_button(
                        label="💾 下载图像",
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
                        image_url = generate_image(prompt, st.session_state.selected_model)
                        # 保存结果到会话状态
                        st.session_state.generated_image = image_url
                        # 直接显示结果，不需要刷新页面
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
                                    file_name=f"generated_image_{st.session_state.selected_model}.png",
                                    mime="image/png"
                                )
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
        # 输入提示词
        prompt = st.text_area("提示词", placeholder="例如：生成一个RPG游戏的角色属性表，包含名称、等级、生命值、攻击力等字段", height=150)
        
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
                        data, filename = generate_data(prompt, data_type, st.session_state.selected_model)
                        
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

# ==================== 致谢页面 ====================

elif option == "致谢":
    st.header("🙏 致谢")
    st.write("""
    感谢所有支持和帮助本项目的人员！
    
    **作者:** 
    
    **联系方式:** 
    
    **指导老师:** 
    """)


