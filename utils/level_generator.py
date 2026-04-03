import json
import streamlit as st
from utils.text_generator import generate_text_for_model

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
**学术背景：**
- 基于 Togelius (2015) 与 Ratican (2024) 提出的混合主动式设计（Mixed-Initiative）理念
- 强调 AI 与人类设计师的协同工作，而非完全自动化
- 核心理念：AI 生成基础结构，人类设计师进行微调和创意补充
- 技术价值：展示数据驱动的生成逻辑，生成的内容可直接导入游戏引擎（如 Unity）使用

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
    
    prompt = f"""请根据以下描述生成一个 {width}x{height} 的游戏关卡地图。

关卡描述：
{description}

地图元素说明：
# = 墙壁 (不可通行)
. = 道路 (可通行)
P = 玩家起点
E = 出口
M = 怪物
T = 陷阱
C = 宝箱
K = 钥匙
D = 门（需要钥匙）
H = 治疗点
S = 商店
B = Boss

要求：
1. 生成一个 {width}x{height} 的 ASCII 地图，确保地图宽度为 {width} 字符，高度为 {height} 行
2. 必须包含玩家起点(P)和出口(E)
3. 确保地图有可行路径从P到E
4. 合理分布怪物、陷阱、宝箱等元素
5. 地图应该有挑战性但不过于困难
{shape_requirement}
6. 每次生成不同的地图布局，不要重复之前的设计

请按照以下JSON格式输出结果：
{{
  "ascii_map": "##########\\n#P.......#\\n#...M....#\\n#........#\\n#....E...#\\n##########",
  "json_map": [["#","#","#","#","#","#","#","#","#","#"],["#","P",".",".",".",".",".",".",".","#"],["#",".",".",".","M",".",".",".",".","#"],["#",".",".",".",".",".",".",".",".","#"],["#",".",".",".",".","E",".",".",".","#"],["#","#","#","#","#","#","#","#","#","#"]],
  "description": "关卡的简要描述"
}}

注意：
- ascii_map 使用 \\n 作为换行符
- json_map 是一个二维数组
- 确保 JSON 格式有效
- 只输出 JSON，不要有其他文字"""
    return prompt


def generate_story_prompt(ascii_map):
    """构建背景故事生成提示词"""
    prompt = f"""请根据以下 ASCII 地图生成关卡的背景故事和怪物配置。

地图：
{ascii_map}

请按照以下JSON格式输出结果：
{{
  "background_story": "关卡的背景故事，包括场景设定、氛围描述等（200-300字）",
  "monster_config": [
    {{
      "symbol": "M",
      "name": "怪物名称",
      "description": "怪物描述",
      "hp": 100,
      "attack": 20,
      "behavior": "怪物行为模式"
    }}
  ],
  "level_design_notes": "关卡设计要点和建议"
}}

要求：
1. 背景故事要与地图结构相符
2. 为地图中的每个怪物(M)和Boss(B)提供详细配置
3. 怪物配置要平衡，符合关卡难度
4. 提供关卡设计建议

请确保输出是有效的JSON格式。"""
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
    with st.expander("📚 学术背景与功能说明"):
        st.write(ACADEMIC_BACKGROUND)
