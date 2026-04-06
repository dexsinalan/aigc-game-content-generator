import json
import streamlit as st
from utils.text_generator import generate_text_for_model
from utils.prompt_templates import LEVEL_PROMPT, STORY_PROMPT

# 关卡元素定义
LEVEL_ELEMENTS = {
    '#': '墙壁 (Wall)',
    '.': '道路 (Path)',
    'P': '玩家起点 (Player)',
    'E': '出口 (Exit)',
    'M': '怪物 (Monster)',
    'T': '陷阱 (Trap)',
    'C': '宝箱 (Chest)',
    'K': '钥匙 (Key)',
    'D': '门 (Door)',
    'H': '治疗点 (Heal)',
    'S': '商店 (Shop)',
    'B': 'Boss (Boss)'
}

# 学术背景介绍
ACADEMIC_BACKGROUND = """

**功能说明：**
- 生成结构化关卡数据（ASCII 地图 / JSON 数组）
- 支持用户手动编辑地图
- AI 根据修改后的地图生成背景故事和怪物配置
- 实现人机协同的关卡设计流程

**ASCII 关卡导入游戏引擎：**
将 ASCII 关卡（以文字字符代表地图）导入游戏引擎，通常通过读取文字档（.txt）并将每个字符映射到相应的游戏物件（如墙壁、地板、敌人）来实现。常用 Libtcod 库进行 Rogue-like 开发，或是自行编写解析器读取数组资料。

**实作步骤：**
1. **准备资料**：建立一个包含 ASCII 字符的文字档（如 '#' 为墙，'.' 为地板）
2. **档案读取与解析**：在游戏引擎（如 Unity、Godot）或代码中编写函数，读取该文字档并逐行处理
3. **字元映射（Mapping）**：使用字典或条件判断，将特定的 ASCII 字元映射到对应的预制件（Prefab）或 Tile
4. **生成关卡**：根据字元的坐标，在场景中实例化（Instantiate）物件
"""


def generate_level_prompt(description, width=10, height=10, shape="矩形"):
    """构建关卡生成提示词"""
    # 根据形状添加特定要求
    shape_requirement = ""
    if shape == "不规则":
        shape_requirement = "6. 地图形状应该是不规则的，不要是完美的矩形"
    elif shape == "圆形":
        shape_requirement = "6. 地图形状应该接近圆形，中心区域较大，边缘逐渐收缩"
    elif shape == "L形":
        shape_requirement = "6. 地图形状应该是L形，有明显的拐角"
    elif shape == "十字形":
        shape_requirement = "6. 地图形状应该是十字形，有主要通道和分支"
    elif shape == "U形":
        shape_requirement = "6. 地图形状应该是U形，有明显的凹陷区域"
    
    prompt = LEVEL_PROMPT.format(
        width=width,
        height=height,
        description=description,
        shape_requirement=shape_requirement
    )
    return prompt


def generate_story_prompt(ascii_map):
    """构建背景故事生成提示词"""
    prompt = STORY_PROMPT.format(ascii_map=ascii_map)
    return prompt


def parse_ascii_map(ascii_map):
    """解析ASCII地图为二维数组"""
    lines = ascii_map.strip().split('\n')
    return [list(line) for line in lines]


def generate_level(description, width, height, model, shape="矩形"):
    """生成关卡"""
    try:
        prompt = generate_level_prompt(description, width, height, shape)
        result, elapsed_time, tokens = generate_text_for_model(prompt, model)
        
        if not result:
            return None, None, None, elapsed_time, tokens, "AI调用失败"
        
        # 解析JSON结果
        try:
            level_data = json.loads(result)
            ascii_map = level_data.get('ascii_map', '')
            json_map = level_data.get('json_map', [])
            level_desc = level_data.get('description', '')
            
            return ascii_map, json_map, level_desc, elapsed_time, tokens, None
            
        except json.JSONDecodeError:
            return None, None, None, elapsed_time, tokens, "AI返回的结果格式错误"
        except Exception as e:
            return None, None, None, elapsed_time, tokens, f"解析结果失败：{str(e)}"
            
    except Exception as e:
        return None, None, None, 0, 0, f"生成失败：{str(e)}"


def generate_level_story(ascii_map, model):
    """生成关卡背景故事"""
    try:
        prompt = generate_story_prompt(ascii_map)
        result, elapsed_time, tokens = generate_text_for_model(prompt, model)
        
        if not result:
            return None, elapsed_time, tokens, "AI调用失败"
        
        # 解析JSON结果
        try:
            story_data = json.loads(result)
            return story_data, elapsed_time, tokens, None
            
        except json.JSONDecodeError:
            return None, elapsed_time, tokens, "AI返回的结果格式错误"
        except Exception as e:
            return None, elapsed_time, tokens, f"解析结果失败：{str(e)}"
            
    except Exception as e:
        return None, 0, 0, f"生成失败：{str(e)}"


def validate_ascii_map(ascii_map):
    """验证ASCII地图的有效性"""
    lines = ascii_map.strip().split('\n')
    
    if not lines:
        return False, "地图为空"
    
    # 检查是否有玩家起点和出口
    has_player = False
    has_exit = False
    
    for line in lines:
        if 'P' in line:
            has_player = True
        if 'E' in line:
            has_exit = True
    
    if not has_player:
        return False, "地图缺少玩家起点(P)"
    if not has_exit:
        return False, "地图缺少出口(E)"
    
    return True, "地图有效"


def display_level_elements_reference():
    """显示关卡元素参考"""
    with st.expander("📋 关卡元素参考"):
        st.write("**可用元素：**")
        for symbol, name in LEVEL_ELEMENTS.items():
            st.text(f"{symbol} = {name}")


def display_academic_background():
    """显示学术背景介绍"""
    with st.expander("📚 功能说明"):
        st.write(ACADEMIC_BACKGROUND)