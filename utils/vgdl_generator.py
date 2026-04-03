import json
import re
import streamlit as st
from utils.text_generator import generate_text_for_model

# 学术背景介绍
ACADEMIC_BACKGROUND = """
**学术背景：**
- VGDL (视频游戏描述语言) 最初由 Ebner 等人提出，并在 Perez-Liebana (2019) 关于 GVGAI (通用视频游戏 AI) 框架的研究中被确立为国际标准
- 核心理念是「高度抽象化」，通过简洁的文字定义（而非复杂的代码），描述一个游戏的物件组成、互动逻辑与胜利条件
- 在学术界，VGDL 是研究 General Game AI (通用游戏 AI) 的基石，因为它允许同一个 AI 代理（Agent）在完全不修改代码的情况下，仅通过读取 VGDL 文件就能理解并游玩成千上万种不同的游戏
- 实现「自然语言转 VGDL」本质上是在挑战「自动化游戏设计 (Automated Game Design)」这一尖端领域，将人类的直觉创意自动转化为机器可读的逻辑规范

**VGDL 核心组件：**
- **SpriteSet (物件定义层)：** 定义游戏中所有的视觉物件与物理属性
- **InteractionSet (互动规则层)：** 定义物件碰撞或触发时的逻辑
- **LevelMapping (地图映射层)：** 定义符号（如 #, .）在关卡中代表哪个物件
- **TerminationSet (终止条件层)：** 定义如何赢或输

**使用教学：**
1. **输入游戏描述**：在左侧文本框中用自然语言描述游戏玩法，例如 "一个射击游戏，玩家控制飞船发射子弹攻击外星飞船"
2. **选择AI模型**：在侧边栏选择一个已配置的AI模型
3. **生成VGDL代码**：点击「生成VGDL代码」按钮，AI会将自然语言描述转换为标准VGDL代码
4. **查看生成结果**：右侧会显示生成的VGDL代码，可以直接复制或下载
5. **逻辑检查**：点击「逻辑检查」按钮，系统会检查生成的代码是否包含所有必要的组件
6. **下载使用**：点击「下载VGDL文件」按钮，将代码保存为 .vgdl 文件
7. **环境中使用**：
   - 安装 py-vgdl 库：`pip install py-vgdl`
   - 使用 VGDLParser 加载生成的文件
   - 运行极简游戏窗口进行测试

**技术价值：**
- 展示了「自然语言到机器可读逻辑」的转换能力
- 证明了自动化游戏设计的可行性
- 为通用游戏AI研究提供了标准化的游戏描述格式
"""


# VGDL 语法模板
VGDL_TEMPLATE = """
SpriteSet
    moving > Physics=Grid
        avatar > FlakAvatar speed=0.5
        alien > Bombed color=RED
        bullet > Missile orientation=UP speed=1
        wall > Passive color=GREY

InteractionSet
    bullet wall > bounceForward
    bullet alien > killSprite scoreChange=10
    alien avatar > killSprite

LevelMapping
    avatar > a
    alien > x
    wall > w
    bullet > b

TerminationSet
    SpriteCounter stype=alien limit=0 win=True
    SpriteCounter stype=avatar limit=0 win=False
"""

# 逻辑检查正则表达式
VGDL_PATTERNS = {
    'spriteset': r'SpriteSet',
    'interactionset': r'InteractionSet',
    'levelmapping': r'LevelMapping',
    'terminationset': r'TerminationSet'
}


def generate_vgdl_prompt(game_description):
    """构建VGDL生成提示词"""
    prompt = f"""你现在是一个 VGDL (视频游戏描述语言) 专家。请根据用户描述，仅输出符合 VGDL 规范的代码块。

用户描述：
{game_description}

VGDL 语法要求：
1. 必须包含以下四个核心部分：
   - SpriteSet (物件定义层)
   - InteractionSet (互动规则层)
   - LevelMapping (地图映射层)
   - TerminationSet (终止条件层)

2. 语法格式示例：
{VGDL_TEMPLATE}

3. 转换逻辑：
   - 当用户提到「玩家」或「主角」，对应到 avatar
   - 当用户提到「敌人」或「怪物」，对应到 alien 或其他合适的类型
   - 当用户提到「子弹」，对应到 Missile
   - 当用户提到「墙壁」，对应到 wall
   - 当用户提到「碰撞」或「反弹」，使用 bounceForward 或 stepBack
   - 当用户提到「得分」，使用 scoreChange
   - 当用户提到「胜利条件」，在 TerminationSet 中定义

4. 输出要求：
   - 仅输出 VGDL 代码，不要有其他文字
   - 确保代码格式正确，符合 VGDL 语法规范
   - 代码要完整，包含所有必要的部分
"""
    return prompt


def generate_vgdl(game_description, model):
    """生成VGDL代码"""
    try:
        prompt = generate_vgdl_prompt(game_description)
        result, elapsed_time, tokens = generate_text_for_model(prompt, model)
        
        if not result:
            return None, elapsed_time, tokens, "AI调用失败"
        
        # 清理结果，确保只包含VGDL代码
        vgdl_code = result.strip()
        
        return vgdl_code, elapsed_time, tokens, None
        
    except Exception as e:
        return None, 0, 0, f"生成失败：{str(e)}"


def check_vgdl_logic(vgdl_code):
    """检查VGDL代码的逻辑完整性"""
    issues = []
    
    # 检查是否包含所有必要部分
    for name, pattern in VGDL_PATTERNS.items():
        if not re.search(pattern, vgdl_code, re.IGNORECASE):
            issues.append(f"缺少 {name} 部分")
    
    # 检查SpriteSet中是否有avatar
    if 'avatar' not in vgdl_code.lower():
        issues.append("SpriteSet 中缺少 avatar (玩家) 定义")
    
    # 检查InteractionSet中是否有交互规则
    if '>' not in vgdl_code:
        issues.append("InteractionSet 中缺少交互规则")
    
    # 检查TerminationSet中是否有终止条件
    if 'win=' not in vgdl_code:
        issues.append("TerminationSet 中缺少胜利条件")
    
    return issues


def display_academic_background():
    """显示学术背景介绍"""
    with st.expander("📚 学术背景与VGDL介绍"):
        st.write(ACADEMIC_BACKGROUND)


def display_vgdl_template():
    """显示VGDL语法模板"""
    with st.expander("📝 VGDL语法模板"):
        st.code(VGDL_TEMPLATE, language="plaintext")


def test_vgdl_code(vgdl_code):
    """测试VGDL代码"""
    try:
        # 检查是否安装了py-vgdl
        import importlib
        vgdl = importlib.import_module('pyvgdl')
        
        # 保存VGDL代码到临时文件
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vgdl', delete=False) as f:
            f.write(vgdl_code)
            temp_file = f.name
        
        # 尝试解析VGDL代码
        from pyvgdl.parser import VGDLParser
        game = VGDLParser().parseGame(temp_file)
        
        # 清理临时文件
        os.unlink(temp_file)
        
        return True, "✅ VGDL代码解析成功！代码格式正确。"
        
    except ImportError:
        return False, "⚠️ py-vgdl库未安装。请在本地环境中运行：`pip install py-vgdl` 来测试VGDL代码。"
    except Exception as e:
        return False, f"❌ 解析失败：{str(e)}"

