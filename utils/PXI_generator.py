import json
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from utils.text_generator import generate_text_for_model

# PXI维度定义
PXI_DIMENSIONS = [
    "Challenge",
    "Immersion", 
    "Autonomy",
    "Competence",
    "Relatedness",
    "Flow"
]

# PXI维度中文映射
PXI_DIMENSIONS_CN = {
    "Challenge": "挑战感",
    "Immersion": "沉浸感",
    "Autonomy": "自主性",
    "Competence": "能力感",
    "Relatedness": "关联性",
    "Flow": "心流体验"
}

# PXI维度详细解释
PXI_DIMENSIONS_EXPLANATION = """
**PXI维度解释：**

1. **Challenge (挑战感)**：
   - 定义：玩家感知到的游戏难度与自身技能的匹配程度
   - 高分代表：该设计能激发玩家克服困难的欲望，不至于产生挫败感
2. **Immersion (沉浸感)**：
   - 定义：玩家对游戏世界的感官投入度，以及对现实世界感知的暂时丧失
   - 高分代表：音效、视觉与叙事高度融合，玩家感到「身临其境」
3. **Autonomy (自主性)**：
   - 定义：玩家在游戏中感受到选择权与意志自由的程度
   - 高分代表：设计提供了多种解决问题的路径，玩家觉得是「自己在做决定」
4. **Competence (能力感)**：
   - 定义：玩家感知到自己技能进步或完成目标后的自我肯定感
   - 高分代表：反馈系统强大，玩家能明显感受到自己变强了
5. **Relatedness (关联性)**：
   - 定义：玩家与游戏角色/其他玩家的连接感
   - 高分代表：角色塑造丰满，社交系统完善，玩家产生情感共鸣
6. **Flow (心流体验)**：
   - 定义：玩家全神贯注于游戏的状态
   - 高分代表：挑战与技能平衡，玩家进入忘我的游戏状态
"""

# 学术背景介绍
ACADEMIC_BACKGROUND = """
**学术背景：**
- PXI (Player Experience Inventory) 是由游戏研究学者 Veroons 等人 (2018) 提出的一套标准化评估工具
- 在 Michael Lankes (2023) 的研究中被证明可以有效地与大型语言模型（LLM）结合
- 基于自我决定理论（Self-Determination Theory），旨在探讨游戏设计元素如何转化为玩家的心理感受
- 核心逻辑在于「功能性」与「情感性」的平衡，将模糊的「好玩」转化为科学的可测量维度
- 在 AIGC 语境下，利用 PXI 框架作为 Prompt 的约束条件，可以让 AI 生成的游戏内容具备可预测的心理影响力

**评分说明：**
- 评分范围：0-10分
- 0分：该维度体验极差
- 5分：该维度体验中等
- 10分：该维度体验极佳
- 评分由 AI 根据玩法描述分析生成，基于 PXI 框架的理论基础
"""


def build_pxi_prompt(gameplay_description):
    """构建PXI分析提示词"""
    prompt = f"""请根据 Player Experience Inventory (PXI) 框架，分析以下游戏玩法描述，并提供各维度的预测分值（0-10分）。

游戏玩法描述：
{gameplay_description}

PXI维度包括：
1. Challenge (挑战感)
2. Immersion (沉浸感)
3. Autonomy (自主性)
4. Competence (能力感)
5. Relatedness (关联性)
6. Flow (心流体验)

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
  "analysis": "对各维度评分的简要分析和解释"
}}

请确保输出是有效的JSON格式，只包含上述内容，不要有其他文字。"""
    return prompt


def analyze_pxi_dimensions(gameplay_description, model):
    """分析游戏玩法的PXI维度"""
    try:
        # 构建提示词
        prompt = build_pxi_prompt(gameplay_description)
        
        # 调用AI生成分析结果
        result, elapsed_time, tokens = generate_text_for_model(prompt, model)
        
        if not result:
            return None, None, None, elapsed_time, tokens, f"AI调用失败"
        
        # 解析JSON结果
        try:
            analysis_data = json.loads(result)
            dimensions = analysis_data.get('dimensions', {})
            analysis = analysis_data.get('analysis', '')
            
            # 验证数据格式
            if not isinstance(dimensions, dict):
                raise ValueError("Invalid dimensions format")
            
            # 提取维度数据
            scores = []
            for dim in PXI_DIMENSIONS:
                score = dimensions.get(dim, 0)
                scores.append(float(score) if isinstance(score, (int, float)) else 0)
            
            return dimensions, scores, analysis, elapsed_time, tokens, None
            
        except json.JSONDecodeError:
            return None, None, None, elapsed_time, tokens, "AI返回的结果格式错误，请重试"
        except Exception as e:
            return None, None, None, elapsed_time, tokens, f"解析结果失败：{str(e)}"
            
    except Exception as e:
        return None, None, None, 0, 0, f"分析失败：{str(e)}"


def create_radar_chart(scores):
    """创建PXI雷达图"""
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 生成雷达图
    plt.figure(figsize=(5, 4))
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(PXI_DIMENSIONS), endpoint=False).tolist()
    angles += angles[:1]
    
    # 复制最后一个值以闭合图形
    scores_circle = scores + scores[:1]
    
    # 绘制雷达图
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, scores_circle, 'o-', linewidth=2, label='预测分值')
    ax.fill(angles, scores_circle, alpha=0.25)
    
    # 设置标签
    ax.set_thetagrids(np.degrees(angles[:-1]), PXI_DIMENSIONS, fontsize=8)
    ax.set_ylim(0, 10)
    ax.set_title('玩家体验维度评分', size=10, y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=7)
    
    return plt


def display_pxi_results(dimensions, scores, analysis, elapsed_time, tokens):
    """显示PXI分析结果"""
    # 显示雷达图
    plt = create_radar_chart(scores)
    
    # 使用列布局限制图表宽度
    col1, col2 = st.columns([2, 1])
    with col1:
        st.pyplot(plt, use_container_width=True)
    
    # 显示分析结果
    st.success("分析完成！")
    st.markdown("### 分析结果")
    
    # 显示各维度评分
    col1, col2, col3 = st.columns(3)
    for i, (dim, score) in enumerate(dimensions.items()):
        if i < 3:
            with col1:
                st.metric(label=dim, value=f"{score}/10")
        elif i < 6:
            with col2:
                st.metric(label=dim, value=f"{score}/10")
    
    # 显示分析解释
    st.markdown("### 分析解释")
    st.write(analysis)
    
    # 显示耗时和Token消耗
    st.info(f"本次耗时：{elapsed_time:.2f}秒 | 消耗Token：{tokens}")


def display_academic_background():
    """显示学术背景介绍"""
    with st.expander("📚 学术背景与评分说明"):
        st.write(ACADEMIC_BACKGROUND)
        st.write(PXI_DIMENSIONS_EXPLANATION)
