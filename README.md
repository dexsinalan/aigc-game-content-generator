# AI游戏内容生成器

基于Streamlit的AI内容生成工具，专为游戏开发设计，支持文本、图像和数据生成。

## 功能特性

- 📝 **文本生成**：生成角色描述、剧情对话、任务文本等
- 🖼️ **图像生成**：生成游戏素材、角色立绘、场景图等
- 📊 **数据生成**：生成JSON、XLSX、XMind格式的游戏数据
- 🔑 **多模型支持**：集成多个AI模型API
- 📚 **API文档**：提供完整的API接口文档

## 支持的AI模型

### 免费API
- 🆓 **阿里通义千问**：强大的文本和图像生成能力
- 🆓 **智谱AI**：GLM-4大模型，性能优秀

### 付费API
- 💲 **百度文心一言**：文心大模型，功能全面
- 💲 **讯飞星火**：星火大模型，支持多种任务
- 💲 **Claude**：Anthropic的Claude模型
- 💲 **GPT**：OpenAI的GPT模型
- 💲 **DeepSeek**：DeepSeek大模型
- 💲 **硅基流动**：硅基流动大模型

## 快速开始

### 本地运行

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置API密钥**
创建`.env`文件，填入您的API密钥：
```
# 阿里通义千问
ALI_API_KEY=你的阿里API密钥

# 智谱AI
ZHIPU_API_KEY=你的智谱API密钥

# 百度文心一言
BAIDU_API_KEY=你的百度API密钥
BAIDU_SECRET_KEY=你的百度Secret密钥

# 讯飞星火
XUNFEI_APP_ID=你的讯飞APP ID
XUNFEI_API_KEY=你的讯飞API Key
XUNFEI_API_SECRET=你的讯飞API Secret

# Claude
CLAUDE_API_KEY=你的Claude API密钥

# GPT
GPT_API_KEY=你的GPT API密钥

# DeepSeek
DEEPSEEK_API_KEY=你的DeepSeek API密钥

# 硅基流动
SILICON_API_KEY=你的硅基流动API密钥
```

3. **运行应用**
```bash
streamlit run app.py
```

4. **访问应用**
打开浏览器访问：`http://localhost:8502`

## 在线部署

详细的部署步骤请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

### Streamlit Cloud（推荐）
- 免费托管
- 自动部署
- 无需服务器管理
- 在线访问地址：[aigcsysu.streamlit.app](https://aigcsysu.streamlit.app)

## 使用说明

### 文本生成
1. 输入提示词（如"中世纪战争世界观"）
2. 选择AI模型
3. 点击"生成文本"
4. 查看并复制结果

### 图像生成
1. 输入图像描述（如"一只可爱的小猫"）
2. 选择AI模型
3. 点击"生成图像"
4. 查看并下载图像

### 数据生成
1. 输入数据需求（如"生成20个游戏角色属性"）
2. 选择数据格式（JSON/XLSX/XMind）
3. 选择AI模型
4. 点击"生成数据"
5. 下载生成的文件

### API设置
1. 在侧边栏选择"API设置"
2. 为每个模型填写对应的API密钥
3. 点击"保存配置"按钮
4. 或使用"保存所有配置"一键保存

## 项目结构

```
AIGC/
├── app.py                 # Streamlit主应用
├── utils/                 # 工具函数目录
│   ├── text_generator.py   # 文本生成函数
│   ├── image_generator.py  # 图像生成函数
│   └── data_generator.py  # 数据生成函数
├── .env                  # 环境变量配置
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

### GPT
访问：[OpenAI控制台](https://platform.openai.com/)

### DeepSeek
访问：[DeepSeek控制台](https://platform.deepseek.com/)

### 硅基流动
访问：[硅基流动控制台](https://cloud.siliconflow.cn/)

## 注意事项

1. **API密钥安全**：
   - 不要将`.env`文件提交到版本控制
   - 使用环境变量管理敏感信息
   - 定期更换API密钥

2. **使用限制**：
   - 注意各API的调用频率限制
   - 合理使用免费额度
   - 监控API使用情况

3. **生成质量**：
   - 提供清晰具体的提示词
   - 根据需要调整参数
   - 多次尝试获得最佳结果

## 常见问题

### Q: 为什么生成失败？
A: 检查API密钥是否正确配置，网络连接是否正常。

### Q: 如何提高生成质量？
A: 使用更详细的提示词，调整temperature参数，多次尝试。

### Q: 支持哪些数据格式？
A: 目前支持JSON、XLSX和XMind格式。

### Q: 可以添加更多AI模型吗？
A: 可以，在对应的工具文件中添加新的生成函数即可。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请提交Issue或联系开发者。