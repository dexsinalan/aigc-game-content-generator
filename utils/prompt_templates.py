# 游戏开发专用提示词模板库

# 文本生成模板
TEXT_TEMPLATES = {
    "游戏角色设计": """请为游戏项目设计一个完整的角色角色方案，要求包含以下内容：

【基础信息】
1. 角色ID与名称（英文/中文）
2. 角色职业/定位（如：战士、法师、辅助等）
3. 角色等级设定（初始等级～满级）
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
11. 角色外观描述：服装风格、武器造型、体型特征
12. 角色配色方案（主色/辅色/点缀色）
13. 角色动画表现：待机、移动、攻击、技能释放

【游戏平衡】
14. 角色优势分析
15. 角色劣势/克制关系
16. 皮肤/外观自定义选项

要求：设计符合游戏世界观，技能机制有趣且平衡，视觉表现具有辨识度。""",

    "游戏剧情对话": """请为游戏项目编写一段专业的剧情对话脚本，要求包含以下内容：

【场景设定】
1. 场景名称与编号
2. 场景环境描述（时间、地点、氛围）
3. 触发条件（主线进度/前置任务完成等）

【角色信息】
4. 参与对话的角色（2-4人）
5. 每个角色的性格特点简述
6. 角色关系设定

【对话内容】
7. 对话文本（至少8-12轮）
8. 每轮对话的情感标注（neutral/happy/angry/sad/surprised等）
9. 角色语气与表达方式
10. 关键台词高亮标记

【分支选项】
11. 选择分支（至少2个分支）
12. 每个分支的后果影响说明
13. 隐藏选项与特殊触发条件

【技术规格】
14. 语音时长估算
15. 口型同步时间码
16. 背景音乐/音效提示

要求：对话推动剧情发展，展现角色性格差异，选项有实际意义和影响。""",

    "游戏任务设计": """请为游戏项目设计一个完整的任务方案，要求包含以下内容：

【任务概述】
1. 任务ID与名称（英文/中文）
2. 任务类型：主线/支线/日常/活动/成就
3. 任务难度等级（1-5星）
4. 推荐等级范围与人数限制
5. 任务标签（剧情/战斗/收集/探索等）

【任务背景】
6. 任务背景故事（100-200字）
7. 任务发起NPC信息
8. 任务在世界观中的意义

【任务目标】
9. 主目标（1-2个）
10. 支线目标（可选）
11. 隐藏目标（可选）
12. 目标完成条件量化指标

【任务流程】
13. 任务接取阶段：接取条件、对话内容
14. 任务执行阶段：详细步骤指引
15. 任务完成阶段：结算流程

【奖励系统】
16. 经验值奖励（根据难度计算）
17. 金币/货币奖励
18. 物品奖励（装备/道具/材料）
19. 特殊奖励（称号/成就/声望）

【技术规格】
20. 任务追踪文本
21. 任务提示文本（普通/详细）
22. 失败条件与重试机制

要求：任务设计有趣味性，难度曲线合理，奖励有吸引力。""",

    "游戏技能系统": """请为游戏项目设计一个完整的技能系统方案，要求包含以下内容：

【技能基础信息】
1. 技能ID与名称（英文/中文）
2. 技能类型：主动/被动/终结技/光环
3. 技能分类：物理/魔法/混合/控制/辅助
4. 技能适用对象：自己/友方/敌方/范围

【数值设定】
5. 技能基础伤害/治疗值
6. 技能冷却时间（秒）
7. 能量/魔法消耗
8. 施法时间/前摇/后摇
9. 技能范围：单体/圆形/矩形/扇形/全图

【效果系统】
10. 主要效果描述（伤害/治疗/增益/减益）
11. 附加效果（眩晕/减速/沉默等）
12. 效果持续时间
13. 效果叠加规则

【等级成长】
14. 技能等级上限
15. 每级提升效果（百分比/固定值）
16. 技能升级材料需求

【视觉表现】
17. 技能图标设计描述
18. 施法动画描述
19. 命中特效描述
20. 音效/语音要求

【游戏平衡】
21. 技能优势对线
22. 技能克制关系
23. 反制手段

要求：技能机制独特且平衡，视觉效果震撼，符合角色定位。""",

    "游戏世界观": """请为游戏项目构建一个完整的世界观体系，要求包含以下内容：

【世界概述】
1. 世界名称与含义
2. 世界基本设定（科幻/魔幻/奇幻/现代等）
3. 世界规模与结构

【历史体系】
4. 纪元划分与重大历史事件（至少3个时代）
5. 历史传说与神话
6. 历史对现在的影响

【地理环境】
7. 主要地区/大陆划分
8. 各地区环境特征（气候、地形、资源）
9. 重要城市/据点介绍
10. 危险区域/禁地设定

【种族与势力】
11. 主要种族介绍（至少3个）
12. 种族特性与文化
13. 主要势力/组织（至少3个）
14. 势力关系图谱（友好/中立/敌对）

【规则体系】
15. 力量/魔法体系设定
16. 社会制度与规则
17. 经济体系
18. 科技水平

【核心冲突】
19. 世界主要矛盾
20. 势力纷争背景
21. 玩家阵营选择

要求：世界观完整自洽，设定有深度，便于扩展和延伸。""",

    "游戏物品装备": """请为游戏项目设计物品/装备系统方案，要求包含以下内容：

【物品基础】
1. 物品ID与名称（英文/中文）
2. 物品分类：消耗品/装备/材料/任务物品/货币
3. 物品稀有度：普通/优秀/稀有/史诗/传说
4. 物品等级（1-100级）
5. 物品描述文案

【装备系统】
6. 装备部位：武器/头盔/胸甲/护腿/鞋子/饰品
7. 装备属性：基础属性/附加属性/随机属性
8. 装备套装效果（3件套/5件套）
9. 装备强化/进阶系统

【物品效果】
10. 物品使用效果
11. 被动效果（装备时触发）
12. 触发效果（概率触发）
13. 叠加规则

【获取方式】
14. 获取途径：掉落/商店/任务/制作
15. 掉落条件与概率
16. 制作配方（材料需求）

【显示规格】
17. 物品图标描述
18. 3D模型规格（如果是装备）
19. 物品栏显示规格

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
- level: 当前等级（1-100）
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

请生成5-10个不同等级和职业的角色数据，数值平衡合理。""",

    "游戏物品数据": """请生成游戏物品数据库，包含以下完整字段定义：

基础信息：
- item_id: 物品唯一标识符（格式：ITM_XXXXXX）
- item_name_cn: 物品中文名称
- item_name_en: 物品英文名称
- item_type: 物品类型（weapon/armor/accessory/consumable/material/quest/coin）
- item_subtype: 物品子类型（如：sword/bow/staff/shield等）
- item_rarity: 稀有度（common/uncommon/rare/epic/legendary）
- item_level: 物品等级需求（1-100）
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

请生成10-15个不同类型和稀有度的物品数据。""",

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

请生成8-12个不同类型的任务数据。""",

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

请生成10-15个不同等级和类型的敌人数据。""",

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

请生成15-20个完整的对话脚本数据。""",

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

请生成12-18个不同类型和等级的技能数据。"""
}
