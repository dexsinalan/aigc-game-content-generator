import json
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.text_generator import generate_text_for_model
from utils.prompt_templates import PXI_PROMPT

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
    prompt = PXI_PROMPT.format(gameplay_description=gameplay_description)
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


def create_radar_chart(dimensions, scores):
    """创建PXI雷达图"""
    # 准备数据
    pxi_data = {
        "Metric": list(dimensions.keys()),
        "Score": list(dimensions.values())
    }
    
    df = pd.DataFrame(pxi_data)
    
    # 创建雷达图
    fig = px.line_polar(
        df, 
        r='Score', 
        theta='Metric', 
        line_close=True,
        title='Player Experience Dimensions',
        range_r=[0, 10],
        markers=True,
        color_discrete_sequence=['#636EFA']
    )
    
    # 自定义布局
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], dtick=2),
            angularaxis=dict(tickfont=dict(size=10))
        ),
        title=dict(font=dict(size=14))
    )
    
    return fig


def display_pxi_results(dimensions, scores, analysis, elapsed_time, tokens):
    """显示PXI分析结果"""
    # 显示雷达图
    fig = create_radar_chart(dimensions, scores)
    
    # 使用列布局限制图表宽度
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
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
    st.info(f"本次耗时：{elapsed_time:.2f}秒 | 本次预计消耗Token：{tokens}")


def display_academic_background():
    """显示学术背景介绍"""
    with st.expander("📚 学术背景与评分说明"):
        st.write(ACADEMIC_BACKGROUND)
        st.write(PXI_DIMENSIONS_EXPLANATION)