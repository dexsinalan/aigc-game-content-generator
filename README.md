# AI游戏内容生成器

基于Streamlit的AI内容生成工具，专为游戏开发设计，集成先进的大模型技术，帮助游戏开发者快速生成游戏开发所需的各种内容。

## 功能特性

- 📝 **游戏文本设计**：生成角色描述、剧情对话、任务文本、技能描述、物品描述等
- 🖼️ **游戏美术资源**：生成游戏场景、角色设计、道具图标、UI元素、特效概念图等
- 📊 **游戏数据配置**：生成角色属性表、任务列表、物品数据、技能参数、敌人AI行为等
- 🌍 **游戏多语言本地化**：将游戏文本翻译为18种语言版本，支持游戏国际化部署
- 🎮 **玩家体验预测器**：基于PXI (Player Experience Inventory) 框架，分析游戏玩法描述并预测玩家体验维度评分
- 🏗️ **关卡原型生成器**：基于混合主动式设计理念，生成ASCII地图和JSON格式关卡，支持地图编辑和背景故事生成
- 🎲 **VGDL生成器**：将自然语言游戏描述转换为标准VGDL (Video Game Description Language) 代码，支持生成Pygame脚本
- 🔑 **多模型支持**：集成多个AI模型API，满足不同的生成需求


## 支持的AI模型

### 免费API
- 🆓 **阿里通义千问**：强大的文本和图像生成能力
- 🆓 **智谱AI**：GLM-4大模型，性能优秀

### 付费API
- 💲 **百度文心一言**：文心大模型，功能全面
- 💲 **讯飞星火**：星火大模型，支持多种任务
- 💲 **Claude**：Anthropic的Claude模型
- 💲 **ChatGPT**：OpenAI的ChatGPT模型
- 💲 **DeepSeek**：DeepSeek大模型
- 💲 **硅基流动**：硅基流动大模型

## 在线访问

直接访问：[aigcsysu.streamlit.app](https://aigcsysu.streamlit.app)

## 使用说明

### 1. API设置
1. 在侧边栏选择"API设置"
2. 为每个模型填写对应的API密钥
3. 点击"保存配置"按钮
4. 或使用"保存所有配置"一键保存

### 2. 游戏文本设计
1. 在侧边栏选择"游戏文本设计"
2. 选择提示词模板或直接输入提示词
3. 选择AI模型
4. 点击"生成文本"
5. 查看并下载生成结果

### 3. 游戏美术资源
1. 在侧边栏选择"游戏美术资源"
2. 选择提示词模板或直接输入图像描述
3. 选择AI模型
4. 点击"生成图像"
5. 查看并下载生成的图像

### 4. 游戏数据配置
1. 在侧边栏选择"游戏数据配置"
2. 输入数据需求
3. 选择数据格式（JSON/XLSX/Mindmap）
4. 选择AI模型
5. 点击"生成数据"
6. 下载生成的文件

### 5. 游戏多语言本地化
1. 在侧边栏选择"游戏多语言本地化"
2. 输入需要翻译的文本
3. 选择目标语言（支持18种语言）
4. 选择AI模型
5. 点击"翻译文本"
6. 查看并下载翻译结果

### 6. 玩家体验预测器
1. 在侧边栏选择"玩家体验预测器"
2. 输入游戏玩法描述
3. 选择AI模型
4. 点击"分析体验"
5. 查看生成的雷达图和分析结果

### 7. 关卡原型生成器
1. 在侧边栏选择"关卡原型生成器"
2. 输入关卡需求
3. 选择地图形状和大小
4. 选择AI模型
5. 点击"生成关卡"
6. 查看生成的ASCII地图和JSON数据
7. 可以编辑地图并重新生成

### 8. VGDL生成器
1. 在侧边栏选择"VGDL生成器"
2. 输入游戏描述
3. 选择AI模型
4. 点击"生成VGDL代码"
5. 查看生成的VGDL代码和Pygame脚本
6. 下载生成的文件

## 项目结构

```
AIGC/
├── app.py                 # Streamlit主应用
├── utils/                 # 工具函数目录
│   ├── models/            # 模型实现目录
│   │   ├── ali_generator.py      # 阿里通义千问实现
│   │   ├── baidu_generator.py    # 百度文心一言实现
│   │   ├── claude_generator.py   # Claude实现
│   │   ├── deepseek_generator.py # DeepSeek实现
│   │   ├── gpt_generator.py      # ChatGPT实现
│   │   ├── silicon_generator.py  # 硅基流动实现
│   │   ├── xunfei_generator.py   # 讯飞星火实现
│   │   └── zhipu_generator.py    # 智谱AI实现
│   ├── PXI_generator.py   # 玩家体验预测器
│   ├── data_generator.py  # 数据生成函数
│   ├── image_generator.py # 图像生成函数
│   ├── level_generator.py # 关卡原型生成器
│   ├── prompt_templates.py # 提示词模板
│   ├── text_generator.py  # 文本生成函数
│   ├── translation_generator.py # 多语言翻译
│   └── vgdl_generator.py  # VGDL生成器
├── requirements.txt        # Python依赖
├── .gitignore           # Git忽略文件
├── DEPLOYMENT.md        # 部署指南
└── README.md            # 项目说明
```

## 技术栈

- **前端框架**：Streamlit
- **后端语言**：Python
- **数据处理**：Pandas, OpenPyXL
- **HTTP请求**：Requests
- **环境管理**：Python-dotenv
- **数据可视化**：Plotly
- **游戏逻辑**：VGDL (Video Game Description Language)
- **游戏原型**：Pygame

## API密钥获取

### 阿里通义千问
访问：[阿里通义千问控制台](https://dashscope.aliyun.com/)

### 智谱AI
访问：[智谱AI开放平台](https://open.bigmodel.cn/)

### 百度文心一言
访问：[百度AI开放平台](https://ai.baidu.com/)

### 讯飞星火
访问：[讯飞开放平台](https://xinghuo.xfyun.cn/)

### Claude
访问：[Anthropic控制台](https://console.anthropic.com/)

### ChatGPT
访问：[OpenAI控制台](https://platform.openai.com/)

### DeepSeek
访问：[DeepSeek控制台](https://platform.deepseek.com/)

### 硅基流动
访问：[硅基流动控制台](https://cloud.siliconflow.cn/)

## 常见问题

### Q: 为什么生成失败？
A: 检查API密钥是否正确配置，网络连接是否正常。

### Q: 如何提高生成质量？
A: 使用更详细的提示词，调整temperature参数，多次尝试。

### Q: 支持哪些数据格式？
A: 目前支持JSON、XLSX和Mindmap格式。

### Q: 可以添加更多AI模型吗？
A: 可以，在utils/models目录中添加新的模型实现即可。

### Q: 如何使用生成的Pygame脚本？
A: 1. 安装pygame：`pip install pygame`
   2. 下载生成的.py文件
   3. 在命令行中运行：`python game_prototype.py`

## 学术价值

- 集成了Player Experience Inventory (PXI) 框架，用于游戏体验分析
- 实现了混合主动式关卡设计，支持AI与人类设计师协同工作
- 支持VGDL (Video Game Description Language) 标准，为通用游戏AI研究提供基础
- 展示了自然语言到机器可读逻辑的转换能力，挑战自动化游戏设计领域

## 许可证

MIT License

## 联系方式

如有问题，请提交Issue或联系开发者。