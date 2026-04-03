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
3. **生成代码**：点击「生成VGDL代码」按钮，AI会同时生成：
   - 标准VGDL代码（符合Perez-Liebana 2019标准）
   - 对应的Pygame脚本（可直接运行的游戏原型）
4. **查看生成结果**：右侧会显示生成的VGDL代码
5. **逻辑检查**：点击「逻辑检查」按钮，系统会检查生成的代码是否包含所有必要的组件
6. **下载使用**：
   - 点击「下载VGDL文件」按钮，将VGDL代码保存为 .vgdl 文件
   - 点击「下载 Pygame 游戏文件」按钮，将Pygame脚本保存为 .py 文件

**如何使用Pygame脚本：**
1. **本地运行**：
   - 安装 pygame：`pip install pygame`
   - 将生成的Pygame代码保存为 .py 文件
   - 在命令行中运行：`python (文件名).py`
2. **白模测试**：
   - 使用方向键控制玩家（蓝色方块）
   - 与敌人（红色方块）战斗
   - 收集目标（绿色/黄色方块）
   - 避开墙壁（黑色/灰色方块）
3. **修改扩展**：
   - 可以根据需要修改Pygame代码
   - 添加更多游戏功能和视觉效果
   - 作为游戏开发的起点

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
    prompt = f"""你现在是一个游戏架构师。请根据用户描述，首先生成符合 Perez-Liebana (2019) 标准的 VGDL 代码，然后将该 VGDL 逻辑转译为一段完整的、可运行的 Pygame 脚本。

用户描述：
{game_description}

第一部分：VGDL 代码
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

第二部分：Pygame 脚本
Pygame 脚本要求：
1. 自我包含 (Self-contained) 的完整脚本，包含所有必要的导入和初始化
2. 必须包含 if __name__ == "__main__": 入口
3. 预设视窗大小为 800x600
4. 基本的方块渲染（白模），遵循以下视觉标准：
   - 蓝色方块：代表玩家 (Avatar)
   - 红色方块：代表敌人 (Aliens/Enemies)
   - 绿色/黄色方块：代表目标或金币 (Goals/Collectibles)
   - 黑色/灰色方块：代表墙壁 (Walls/Obstacles)
5. 键盘控制逻辑
6. 碰撞检测和游戏规则逻辑（必须直接翻译自InteractionSet）
7. 基本的游戏循环和渲染
8. 必须包含一个简单的「游戏结束」或「胜利」文字提示
9. 必须包含错误处理和异常捕获，确保游戏不会崩溃
10. 确保所有变量和对象都正确初始化

重要：
- 所有的碰撞逻辑必须直接翻译自 InteractionSet，例如：
  如果 VGDL 里有 'bullet alien > killSprite'，
  Pygame 代码里必须有对应的 spritecollide 逻辑。
- 确保代码可以直接运行，不需要额外的文件或依赖
- 确保代码健壮，不会因为缺少对象或错误的索引而崩溃
- 提供清晰的游戏控制说明

Pygame 代码结构示例：
```python
import pygame
import sys

# 初始化pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Prototype")

# 颜色定义
BLUE = (0, 0, 255)    # 玩家
RED = (255, 0, 0)      # 敌人
GREEN = (0, 255, 0)    # 目标
BLACK = (0, 0, 0)      # 墙壁
WHITE = (255, 255, 255) # 背景

# 游戏对象类
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # 边界检查
        self.rect.x = max(0, min(self.rect.x, WIDTH - 30))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - 30))

# 游戏主循环
def main():
    try:
        # 创建精灵组
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        walls = pygame.sprite.Group()
        goals = pygame.sprite.Group()

        # 创建玩家
        player = Player(50, 50)
        all_sprites.add(player)

        # 创建其他游戏对象...

        # 游戏循环
        running = True
        clock = pygame.time.Clock()

        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 获取键盘状态
            keys = pygame.key.get_pressed()

            # 更新游戏对象
            player.update(keys)
            # 更新其他对象...

            # 碰撞检测
            # 处理碰撞...

            # 渲染
            window.fill(WHITE)
            all_sprites.draw(window)
            # 绘制其他元素...

            # 显示游戏状态
            font = pygame.font.Font(None, 36)
            text = font.render("Score: 0", True, BLACK)
            window.blit(text, (10, 10))

            # 更新显示
            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
```

请严格按照上述结构生成Pygame代码，确保代码健壮且不会崩溃。

输出格式：
```vgdl
[VGDL代码]
```

```python
[Pygame脚本代码]
```

请确保：
- VGDL 代码符合语法规范
- Pygame 代码可以直接运行
- 输出格式严格按照上述要求
- 不要有其他额外的文字
"""
    return prompt


def generate_vgdl(game_description, model):
    """生成VGDL代码和Pygame脚本"""
    try:
        prompt = generate_vgdl_prompt(game_description)
        result, elapsed_time, tokens = generate_text_for_model(prompt, model)
        
        if not result:
            return None, None, elapsed_time, tokens, "AI调用失败"
        
        # 解析结果，提取VGDL代码和Pygame脚本
        import re
        
        # 提取VGDL代码
        vgdl_match = re.search(r'```vgdl\n(.*?)```', result, re.DOTALL)
        if not vgdl_match:
            return None, None, elapsed_time, tokens, "未能提取VGDL代码"
        vgdl_code = vgdl_match.group(1).strip()
        
        # 提取Pygame脚本
        pygame_match = re.search(r'```python\n(.*?)```', result, re.DOTALL)
        if not pygame_match:
            return None, None, elapsed_time, tokens, "未能提取Pygame脚本"
        pygame_code = pygame_match.group(1).strip()
        
        return vgdl_code, pygame_code, elapsed_time, tokens, None
        
    except Exception as e:
        return None, None, 0, 0, f"生成失败：{str(e)}"


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

