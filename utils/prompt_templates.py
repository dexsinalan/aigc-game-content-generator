# 游戏开发专用提示词模板库

# 通用预prompt
# 文本生成预prompt
TEXT_PROMPT = """请根据以下提示词生成游戏相关的文本内容：
{prompt}

要求：
1. 内容要与游戏相关，符合提示词的要求
2. 生成的内容要详细、丰富、有创意
3. 语言表达要流畅、自然
4. 不要包含任何无关的内容

请直接返回生成的文本内容："""

# 图像生成预prompt
IMAGE_PROMPT = """请根据以下提示词生成游戏相关的图像：
{prompt}

要求：
1. 图像要与游戏相关，符合提示词的要求
2. 图像要清晰、细节丰富
3. 构图合理，色彩协调
4. 风格统一，符合游戏的整体风格

请生成并返回图像："""

# 数据生成预prompt
JSON_PROMPT = """请根据以下描述生成JSON数据：
{prompt}

要求：
1. 只返回JSON数据，不要包含任何解释文字
2. 确保JSON格式正确，可以被Python的json.loads()解析
3. 数据应该包含合理的字段和示例数据
4. 如果是表格数据，使用数组格式，数据量根据用戶要求而定

请直接返回JSON数据："""

XLSX_PROMPT = """请根据以下描述生成表格数据，并返回JSON数组格式：
{prompt}

要求：
1. 返回JSON数组格式，每个元素是一个对象，代表一行数据
2. 确保所有对象具有相同的字段
3. 只返回JSON数组，不要包含任何解释文字
4. 数据量根据用戶要求而定

请直接返回JSON数组："""

MINDMAP_PROMPT = """请根据以下描述生成思维导图数据，使用Markdown列表格式：
{prompt}

要求：
1. 使用Markdown列表格式（- 和缩进）
2. 第一行是中心主题
3. 使用2个空格作为缩进表示层级关系
4. 包含多个主要分支，每个分支可以有多个子节点
5. 只返回思维导图内容，不要包含任何解释文字
6. 确保格式干净，没有多余的空行或注释

示例格式：
游戏设计
- 角色系统
  - 战士
  - 法师
  - 弓箭手
- 战斗系统
  - 回合制
  - 实时战斗
- 任务系统
  - 主线任务
  - 支线任务

请直接返回思维导图内容："""

# 翻译提示词
TRANSLATION_PROMPT = """请将以下游戏相关文本翻译成{target_language}：
{text}

要求：
1. 准确翻译，保持原文意思
2. 只返回翻译结果，不要包含任何解释文字
3. 翻译结果要流畅自然，符合游戏语境
4. 对于游戏术语和专有名词，保持一致性
5. 考虑游戏本地化的特点，使翻译更符合目标语言玩家的习惯

请直接返回翻译结果："""

# 关卡生成提示词
LEVEL_PROMPT = """请根据以下描述生成一个 {width}x{height} 的游戏关卡地图。

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
  "ascii_map": "##########\n#P.......#\n#...M....#\n#........#\n#....E...#\n##########",
  "json_map": [["#","#","#","#","#","#","#","#","#","#"],["#","P",".",".",".",".",".",".",".","#"],["#",".",".",".","M",".",".",".",".","#"],["#",".",".",".",".",".",".",".",".","#"],["#",".",".",".",".","E",".",".",".","#"],["#","#","#","#","#","#","#","#","#","#"]],
  "description": "关卡的简要描述"
}}

注意：
- ascii_map 使用 \n 作为换行符
- json_map 是一个二维数组
- 确保 JSON 格式有效
- 只输出 JSON，不要有其他文字"""

STORY_PROMPT = """请根据以下 ASCII 地图生成关卡的背景故事和怪物配置。

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

# PXI分析提示词
PXI_PROMPT = """请根据 Player Experience Inventory (PXI) 框架，客观分析以下游戏玩法描述，并提供各维度的预测分值（0-10分）。

游戏玩法描述：
{gameplay_description}

PXI维度包括：
1. Challenge (挑战感)
2. Immersion (沉浸感)
3. Autonomy (自主性)
4. Competence (能力感)
5. Relatedness (关联性)
6. Flow (心流体验)

评分标准（请严格遵循）：
- 0-3分：该维度存在明显缺陷或不足
- 4-6分：该维度表现一般，有改进空间
- 7-8分：该维度表现良好
- 9-10分：该维度表现优秀，几乎无缺陷

重要提示：
1. 请保持客观公正，不要过度乐观，严格一点，要严格批评不足，打分可以压低一些
2. 根据描述中明确提到的元素评分，不要假设未提及的优点
3. 如果描述中缺少某维度的关键要素，请给出较低或者最低分数
4. 指出每个维度的潜在问题和改进建议

请按照以下JSON格式输出结果：
{{
  "dimensions": {{
    "Challenge": 0-10,
    "Immersion": 0-10,
    "Autonomy": 0-10,
    "Competence": 0-10,
    "Relatedness": 0-10,
    "Flow": 0-10
  }},
  "analysis": "客观分析各维度评分的原因，指出潜在问题和改进建议"
}}

请确保输出是有效的JSON格式，只包含上述内容，不要有其他文字。"""

# VGDL生成提示词
VGDL_PROMPT = """你现在是一个游戏架构师。请根据用户描述，首先生成符合 Perez-Liebana (2019) 标准的 VGDL 代码，然后将该 VGDL 逻辑转译为一段完整的、可运行的 Pygame 脚本。

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
{vgdl_template}

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
10. 必须包含边界检查，防止对象超出屏幕范围
11. 必须正确管理Pygame资源，确保在游戏结束时正确释放
12. 确保所有精灵组都正确初始化和管理
13. 确保所有必要的Pygame初始化步骤都已完成
14. **重要**：所有游戏对象（玩家、敌人、金币等）必须在 main() 函数内部创建和初始化
15. **重要**：精灵组必须在 main() 函数内部创建，不要在全局作用域创建
16. **重要**：确保游戏开始时就有必要的对象（如玩家、敌人、金币等），不要等到游戏运行后才生成

重要：
- 所有的碰撞逻辑必须直接翻译自 InteractionSet，例如：
  如果 VGDL 里有 'bullet alien > killSprite'，
  Pygame 代码里必须有对应的 spritecollide 逻辑。
- 确保代码可以直接运行，不需要额外的文件或依赖
- 代码必须健壮，能够处理各种边缘情况，不会因为缺少对象或错误的索引而崩溃
- 必须使用try-except-finally结构确保游戏能够正常退出
- 必须确保所有变量和对象都正确初始化，避免使用未定义的变量

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

# 文本生成模板
TEXT_TEMPLATES = {
    "游戏角色设计": """请为游戏项目设计一个完整的角色角色方案，要求包含以下内容：

【基础信息】
1. 角色ID与名称（英文/中文）
2. 角色职业/定位：{character_class}
3. 角色等级设定（初始等级～满级）：{level_range}
4. 角色背景故事（200-300字）

【属性设定】
5. 基础属性：生命值、魔法值、攻击力、防御力、敏捷、暴击率、闪避率
6. 属性成长曲线（每级属性增长值）
7. 角色抗性：物理抗性、魔法抗性、控制抗性

【技能系统】
8. 主动技能（3-4个）：技能名称、冷却时间、消耗、效果描述
9. 被动技能（1-2个）：触发条件、效果描述
10. 终极技能：冷却时间、消耗、战斗表现描述

【视觉表现】
11. 角色外观描述：{art_style}风格，服装风格、武器造型、体型特征
12. 角色配色方案（{color_scheme}）
13. 角色动画表现：待机、移动、攻击、技能释放

【游戏平衡】
14. 角色优势分析：{character_strength}
15. 角色劣势/克制关系：机动性差
16. 皮肤/外观自定义选项

要求：设计符合{game_world}世界观，技能机制有趣且平衡，视觉表现具有辨识度。""",

    "游戏剧情对话": """请为游戏项目编写一段专业的剧情对话脚本，要求包含以下内容：

【场景设定】
1. 场景名称与编号
2. 场景环境描述（{time_period}，{location}，{atmosphere}）
3. 触发条件：主线进度50%

【角色信息】
4. 参与对话的角色（{character_count}人）
5. 每个角色的性格特点：勇敢/狡猾
6. 角色关系设定：{character_relationships}

【对话内容】
7. 对话文本（至少8-12轮）
8. 每轮对话的情感标注（neutral/angry）
9. 角色语气与表达方式：正式
10. 关键台词高亮标记

【分支选项】
11. 选择分支（至少{branch_count}个分支）
12. 每个分支的后果影响说明
13. 隐藏选项与特殊触发条件：好感度>80

【技术规格】
14. 语音时长估算：2-3分钟
15. 口型同步时间码
16. 背景音乐/音效提示：背景音乐+音效

要求：对话推动剧情发展，展现角色性格差异，选项有实际意义和影响。""",

    "游戏任务设计": """请为游戏项目设计一个完整的任务方案，要求包含以下内容：

【任务概述】
1. 任务ID与名称（英文/中文）
2. 任务类型：{quest_type}
3. 任务难度等级（{difficulty_level}星）
4. 推荐等级范围与人数限制：{level_requirement}
5. 任务标签：剧情/战斗

【任务背景】
6. 任务背景故事（100-200字）：{quest_background}
7. 任务发起NPC信息：{npc_info}
8. 任务在世界观中的意义：推动主线

【任务目标】
9. 主目标（1-2个）
10. 支线目标（2个）
11. 隐藏目标（1个）
12. 目标完成条件量化指标：击杀BOSS

【任务流程】
13. 任务接取阶段：接取条件、对话内容
14. 任务执行阶段：前往副本
15. 任务完成阶段：结算流程

【奖励系统】
16. 经验值奖励（根据难度计算）：5000
17. 金币/货币奖励：1000
18. 物品奖励（装备/道具/材料）：{item_rewards}
19. 特殊奖励（称号/成就/声望）：称号

【技术规格】
20. 任务追踪文本
21. 任务提示文本（普通/详细）
22. 失败条件与重试机制：死亡

要求：任务设计有趣味性，难度曲线合理，奖励有吸引力。""",

    "游戏技能系统": """请为游戏项目设计一个完整的技能系统方案，要求包含以下内容：

【技能基础信息】
1. 技能ID与名称（英文/中文）
2. 技能类型：{skill_type}
3. 技能分类：{skill_category}
4. 技能适用对象：{skill_target}

【数值设定】
5. 技能基础伤害/治疗值：{base_damage}
6. 技能冷却时间（秒）：{cooldown}
7. 能量/魔法消耗：100
8. 施法时间/前摇/后摇：2秒
9. 技能范围：圆形

【效果系统】
10. 主要效果描述（伤害/治疗/增益/减益）：{main_effect}
11. 附加效果（眩晕/减速/沉默等）：减速
12. 效果持续时间：5秒
13. 效果叠加规则：不可叠加

【等级成长】
14. 技能等级上限：10
15. 每级提升效果（百分比/固定值）：+10%
16. 技能升级材料需求：金币+经验书

【视觉表现】
17. 技能图标设计描述：火焰图标
18. 施法动画描述：举杖施法
19. 命中特效描述：爆炸效果
20. 音效/语音要求：爆炸音效

【游戏平衡】
21. 技能优势对线：远程输出
22. 技能克制关系：被刺客克制
23. 反制手段：打断施法

要求：技能机制独特且平衡，视觉效果震撼，符合角色定位。""",

    "游戏世界观": """请为游戏项目构建一个完整的世界观体系，要求包含以下内容：

【世界概述】
1. 世界名称与含义：{world_name}
2. 世界基本设定：{world_setting}
3. 世界规模与结构：多大陆

【历史体系】
4. 纪元划分与重大历史事件（至少3个时代）：上古战争
5. 历史传说与神话：创世神话
6. 历史对现在的影响：影响至今

【地理环境】
7. 主要地区/大陆划分：{geographical_regions}
8. 各地区环境特征（气候、地形、资源）：森林/山地
9. 重要城市/据点介绍：暴风城
10. 危险区域/禁地设定：黑石深渊

【种族与势力】
11. 主要种族介绍（至少3个）：{main_races}
12. 种族特性与文化：勇敢/野蛮
13. 主要势力/组织（至少3个）：{main_factions}
14. 势力关系图谱（友好/中立/敌对）：敌对

【规则体系】
15. 力量/魔法体系设定：魔法
16. 社会制度与规则：君主制
17. 经济体系：金币交易
18. 科技水平：中世纪

【核心冲突】
19. 世界主要矛盾：{main_conflict}
20. 势力纷争背景：历史仇恨
21. 玩家阵营选择：联盟/部落

要求：世界观完整自洽，设定有深度，便于扩展和延伸。""",

    "游戏物品装备": """请为游戏项目设计物品/装备系统方案，要求包含以下内容：

【物品基础】
1. 物品ID与名称（英文/中文）
2. 物品分类：{item_category}
3. 物品稀有度：{item_rarity}
4. 物品等级（{item_level_range}级）
5. 物品描述文案：传说之剑

【装备系统】
6. 装备部位：{equipment_slot}
7. 装备属性：基础属性/附加属性/随机属性：{item_stats}
8. 装备套装效果（3件套/5件套）
9. 装备强化/进阶系统：强化+10

【物品效果】
10. 物品使用效果：无
11. 被动效果（装备时触发）：攻击+10%
12. 触发效果（概率触发）：暴击时
13. 叠加规则：不可叠加

【获取方式】
14. 获取途径：{acquisition_method}
15. 掉落条件与概率：BOSS掉落
16. 制作配方（材料需求）：无

【显示规格】
17. 物品图标描述：剑形图标
18. 3D模型规格（如果是装备）：3D模型
19. 物品栏显示规格：1x1格子

要求：物品设计有辨识度，属性分配合理，获取途径多样。""",


}

# 图像生成模板
IMAGE_TEMPLATES = {
    "游戏角色原画": """游戏角色设计稿，专业游戏美术风格，高清细节展示，正面/侧面/背面三视图，角色全身展示，
包括：
- 角色完整外观造型设计
- 角色配色方案（主色调/辅色调/点缀色）
- 角色装备细节特写
- 角色表情姿态展示
- 游戏引擎兼容格式，层次分明，线稿+上色分离，{additional_style}，专业游戏原画品质""",

    "游戏场景概念": """游戏场景概念设计，专业游戏美术风格，超宽视角全景展示，包含：
- 场景整体氛围与光线设计
- 场景主要元素与构图
- 场景纵深感与层次
- 场景色彩基调
- 场景可交互元素标记
风格要求：{style_type}，{mood}，{time_of_day}，{weather}，{technical_specs}，专业游戏场景概念设计品质""",

    "游戏道具图标": """游戏道具/装备图标设计，{icon_type}类型，专业游戏图标风格，干净简洁的图标设计，包含：
- 道具完整造型
- 道具发光/特效效果
- 道具品质边框（{rarity}稀有度）
- 道具缩略图版本
风格要求：{style}，{color_scheme}，{background}，{specs}，游戏道具图标标准尺寸，支持缩放""",

    "游戏UI界面": """游戏用户界面设计，{ui_type}界面，专业游戏UI风格，现代简约设计，包含：
- 界面整体布局
- 按钮与交互元素
- 图标与标识系统
- 信息展示模块
- 界面主题风格
风格要求：{ui_style}，{color_scheme}，{typography}，{effects}，游戏引擎UI系统兼容格式""",

    "游戏特效动画": """游戏技能特效设计，{skill_type}技能特效，专业游戏特效风格，包含：
- 技能起手特效
- 技能主体效果
- 技能消散特效
- 粒子效果细节
- 光效与色彩
风格要求：{effect_style}，{color_palette}，{intensity}，{particles}，{technical_format}，游戏特效序列帧/粒子系统兼容""",

    "游戏地图设计": """游戏地图/关卡设计，{map_type}类型，专业游戏地图风格，俯视角/斜45度视角，包含：
- 地图整体布局
- 地形特征与障碍物
- 资源点分布
- 敌人生成点
- 玩家出生点与目标点
风格要求：{map_style}，{grid_type}，{color_scheme}，{icons}，游戏关卡编辑器兼容格式""",

    "游戏加载界面": """游戏加载界面设计，{loading_type}风格，专业游戏美术风格，包含：
- 背景图片设计
- 加载进度条样式
- 加载提示文案
- 装饰元素
- 品牌标识位置
风格要求：{bg_style}，{progress_bar_style}，{text_style}，{animations}，{resolution}，游戏加载界面标准尺寸"""
}

# 数据生成模板
DATA_TEMPLATES = {
    "游戏角色属性": """请生成游戏角色属性数据表，包含以下完整字段定义：

基础信息：
- character_id: 角色唯一标识符（格式：CHR_XXXXXX）
- character_name_cn: 角色中文名称
- character_name_en: 角色英文名称
- character_type: 角色类型（ warrior/mage/rogue/priest/ranger）
- character_race: 角色种族
- character_gender: 性别（male/female/other）
- character_age: 角色年龄

属性数值：
- level: 当前等级（LV1-100）
- exp: 当前经验值
- exp_to_next: 升级所需经验
- health: 生命值（基础值+装备加成）
- mana: 魔法值（基础值+装备加成）
- health_regen: 生命恢复速度
- mana_regen: 魔法恢复速度

战斗属性：
- attack: 物理攻击力
- defense: 物理防御力
- magic_attack: 魔法攻击力
- magic_defense: 魔法防御力
- critical_rate: 暴击率（0-100%）
- critical_damage: 暴击伤害倍率
- dodge_rate: 闪避率（0-100%）
- hit_rate: 命中率（0-100%）
- attack_speed: 攻击速度
- move_speed: 移动速度

抗性属性：
- fire_resist: 火属性抗性
- ice_resist: 冰属性抗性
- lightning_resist: 雷属性抗性
- poison_resist: 毒属性抗性
- control_resist: 控制效果抗性

技能配置：
- active_skills: 主动技能列表（JSON数组）
- passive_skills: 被动技能列表（JSON数组）
- ultimate_skill: 终极技能ID

装备栏位：
- equipped_weapon: 武器栏位
- equipped_armor: 护甲栏位
- equipped_accessory: 饰品栏位

请生成{character_count}个不同等级和职业的角色数据，数值平衡合理。职业类型：{character_types}，等级范围：{level_range}。""",

    "游戏物品数据": """请生成游戏物品数据库，包含以下完整字段定义：

基础信息：
- item_id: 物品唯一标识符（格式：ITM_XXXXXX）
- item_name_cn: 物品中文名称
- item_name_en: 物品英文名称
- item_type: 物品类型（weapon/armor/accessory/consumable/material/quest/coin）
- item_subtype: 物品子类型（如：sword/bow/staff/shield等）
- item_rarity: 稀有度（common/uncommon/rare/epic/legendary）
- item_level: 物品等级需求（LV1-100）
- item_quality: 物品品质（1-5星）

属性数值：
- base_stats: 基础属性（JSON对象）
- additional_stats: 附加属性（JSON数组）
- set_bonus: 套装效果（如果有）
- set_count: 套装所需件数

物品效果：
- passive_effect: 被动效果（装备时触发）
- active_effect: 主动效果（使用时触发）
- trigger_effect: 触发效果（概率触发）
- effect_description: 效果描述文本

获取方式：
- droprate: 掉落概率（0-100%）
- drop_source: 掉落来源（怪物ID/副本ID/任务ID）
- shop_price: 商店售价
- sell_price: 出售价格
- craft_recipe: 制作配方（如果有）

显示信息：
- icon_name: 图标资源名称
- model_name: 3D模型名称（如果是装备）
- description: 物品描述文本
- lore: 物品背景故事

请生成{item_count}个不同类型和稀有度的物品数据。物品类型：{item_types}，稀有度：{rarities}。""",

    "游戏任务数据": """请生成游戏任务数据库，包含以下完整字段定义：

任务基础：
- quest_id: 任务唯一标识符（格式：QST_XXXXXX）
- quest_name_cn: 任务中文名称
- quest_name_en: 任务英文名称
- quest_type: 任务类型（main/branch/daily/achievement/event）
- quest_difficulty: 任务难度（1-5星）
- quest_level: 推荐等级范围
- quest_phase: 任务阶段

任务流程：
- quest_giver: 任务发布NPC ID
- quest_goals: 任务目标列表（JSON数组）
- quest_steps: 任务步骤列表（JSON数组）
- quest_progress: 当前进度
- quest_status: 任务状态（not_started/in_progress/completed/failed）

目标配置：
- goal_type: 目标类型（kill/collect/interact/talk/explore）
- goal_target: 目标对象
- goal_count: 目标数量
- goal_current: 当前完成数
- goal_location: 目标位置

奖励配置：
- exp_reward: 经验奖励
- gold_reward: 金币奖励
- item_rewards: 物品奖励列表
- reputation_rewards: 声望奖励
- achievement_reward: 成就奖励

前置条件：
- prerequisite_quests: 前置任务列表
- prerequisite_level: 等级要求
- prerequisite_items: 物品要求

时间限制：
- time_limit: 时间限制（秒，0表示无限制）
- daily_reset: 是否每日重置
- weekly_reset: 是否每周重置

请生成{quest_count}个不同类型的任务数据。任务类型：{quest_types}，难度范围：{difficulty_range}。""",

    "游戏敌人数据": """请生成游戏敌人/NPC数据库，包含以下完整字段定义：

基础信息：
- enemy_id: 敌人唯一标识符（格式：ENM_XXXXXX）
- enemy_name_cn: 敌人中文名称
- enemy_name_en: 敌人英文名称
- enemy_type: 敌人类型（normal/elite/boss/minion/npc）
- enemy_race: 敌人种族
- enemy_faction: 敌人阵营
- enemy_level: 敌人等级

属性数值：
- health: 生命值
- mana: 魔法值
- attack: 物理攻击力
- defense: 物理防御力
- magic_attack: 魔法攻击力
- magic_defense: 魔法防御力
- attack_speed: 攻击速度
- move_speed: 移动速度

战斗AI：
- ai_behavior: AI行为模式（aggressive/defensive/passive）
- attack_range: 攻击范围
- detection_range: 感知范围
- patrol_path: 巡逻路径
- skills: 技能列表（JSON数组）

掉落配置：
- drop_table_id: 掉落表ID
- gold_drop: 金币掉落范围
- exp_drop: 经验掉落
- item_drops: 物品掉落列表

视觉配置：
- model_id: 模型ID
- animation_set: 动画集
- scale: 模型缩放
- voice_id: 语音ID

位置信息：
- spawn_area: 生成区域
- spawn_condition: 生成条件
- respawn_time: 重生时间

请生成{enemy_count}个不同等级和类型的敌人数据。敌人类型：{enemy_types}，等级范围：{level_range}。""",

    "游戏对话脚本": """请生成游戏对话数据库，包含以下完整字段定义：

对话基础：
- dialogue_id: 对话唯一标识符（格式：DLG_XXXXXX）
- dialogue_type: 对话类型（npc_to_player/player_to_npc/system/event）
- speaker_id: 说话者ID
- listener_id: 倾听者ID

对话内容：
- dialogue_text_cn: 中文对话文本
- dialogue_text_en: 英文对话文本
- dialogue_emotion: 说话者情绪（neutral/happy/angry/sad/surprised/afraid）
- voice_line: 语音文件路径
- subtitle_duration: 字幕显示时长（秒）

对话选项：
- dialogue_choices: 对话选项列表（JSON数组）
- choice_text_cn: 选项中文文本
- choice_text_en: 选项英文文本
- choice_condition: 选项触发条件
- next_dialogue: 选择后跳转的对话ID
- choice_effect: 选择产生的效果

触发条件：
- trigger_type: 触发类型（auto/talk/quest/event/time）
- trigger_condition: 触发条件
- prerequisite_dialogues: 前置对话列表

对话流程：
- dialogue_order: 对话顺序
- next_dialogue_auto: 自动跳转的下一对话ID
- end_dialogue: 是否为对话结束

分支管理：
- branch_id: 分支ID
- branch_conditions: 分支触发条件
- branch_variable: 影响分支的变量

请生成{dialogue_count}个完整的对话脚本数据。对话类型：{dialogue_types}，平均每段对话{dialogue_rounds}轮。""",

    "游戏技能配置": """请生成游戏技能数据库，包含以下完整字段定义：

技能基础：
- skill_id: 技能唯一标识符（格式：SKL_XXXXXX）
- skill_name_cn: 技能中文名称
- skill_name_en: 技能英文名称
- skill_type: 技能类型（active/passive/ultimate）
- skill_category: 技能分类（physical/magic/control/buff/debuff）
- skill_element: 技能属性（fire/ice/lightning/nature/dark/holy/physical）

施放条件：
- level_required: 等级要求
- skill_level: 技能当前等级
- skill_cost_type: 消耗类型（mana/energy/rage/cooldown）
- skill_cost_amount: 消耗数值
- cast_time: 施法时间（秒）
- cooldown: 冷却时间（秒）

效果数值：
- base_damage: 基础伤害值
- damage_type: 伤害类型（physical/magical/true）
- effect_duration: 效果持续时间（秒）
- effect_range: 效果范围
- effect_target: 效果目标（self/ally/enemy/all）
- damage_scaling: 属性加成系数

附加效果：
- status_effects: 状态效果列表（JSON数组）
- effect_application: 效果施加概率
- effect_stacking: 效果叠加规则
- crowd_control: 控制效果类型（stun/slow/silence/fear等）

等级成长：
- max_level: 技能最高等级
- level_up_bonus: 每级提升效果
- upgrade_cost: 升级消耗
- upgrade_materials: 升级材料

视觉表现：
- icon_name: 图标名称
- animation_name: 动画名称
- effect_particle: 特效粒子名称
- sound_effect: 音效文件名称

请生成{skill_count}个不同类型和等级的技能数据。技能类型：{skill_types}，技能分类：{skill_categories}。"""
}
