# Streamlit Cloud 部署配置

## 部署步骤

### 1. 创建GitHub仓库
1. 访问 https://github.com/new 创建新的仓库
2. 仓库名称：`aigc-game-content-generator`
3. 设置为公开仓库
4. 点击"Create repository"

### 2. 上传代码
1. 在项目目录打开终端
2. 执行以下命令：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/aigc-game-content-generator.git
git push -u origin main
```

### 3. 部署到Streamlit Cloud
1. 访问 https://share.streamlit.io/
2. 点击"New app"
3. 连接您的GitHub账号
4. 选择刚创建的仓库
5. 配置应用设置：
   - Repository: `aigc-game-content-generator`
   - Branch: `main`
   - Main file path: `app.py`

### 4. 配置环境变量
在Streamlit Cloud的设置页面添加以下环境变量：

```
ALI_API_KEY=你的阿里通义千问API密钥
ZHIPU_API_KEY=你的智谱AI API密钥
XUNFEI_API_KEY=你的讯飞星火API密钥
BAIDU_API_KEY=你的百度文心一言API密钥
BAIDU_SECRET_KEY=你的百度文心一言Secret密钥
```

### 5. 部署
点击"Deploy"按钮，等待部署完成（通常需要1-2分钟）

### 6. 访问应用
部署成功后，您可以通过以下地址访问应用：
`https://aigcskc.streamlit.app`

## 注意事项

1. **API密钥安全**：
   - 不要将API密钥提交到GitHub
   - 使用Streamlit Cloud的环境变量功能
   - 确保`.env`文件在`.gitignore`中

2. **依赖管理**：
   - `requirements.txt`文件必须包含所有依赖
   - Streamlit Cloud会自动安装这些依赖

3. **文件结构**：
   - 确保`app.py`在仓库根目录
   - 确保`utils/`目录包含所有工具文件

4. **免费限制**：
   - Streamlit Cloud免费版有资源限制
   - 适合个人和小型项目使用
   - 如需更多资源可升级到付费版

## 故障排除

如果部署失败，检查以下几点：
1. 确保`requirements.txt`格式正确
2. 检查Python版本兼容性
3. 查看Streamlit Cloud的部署日志
4. 确保所有导入的模块都在`requirements.txt`中

## 更新应用

更新代码后：
1. 提交更改到GitHub
2. Streamlit Cloud会自动检测并重新部署
3. 或者在Streamlit Cloud手动点击"Rerun"按钮