import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Task Automation Benchmark & Evaluation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Clean Dashboard Presentation
st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: 700; color: #1E293B; margin-bottom: 4px; }
    .sub-header { font-size: 14px; color: #64748B; margin-bottom: 20px; }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/tasks_benchmark.csv")

df = load_data()

# Sidebar Navigation & Filters
st.sidebar.title("🛠️ Navigation & Filter")
st.sidebar.markdown("Filter benchmark data across technical job functions.")

roles = ["All Roles"] + sorted(df["role_category"].unique().tolist())
selected_role = st.sidebar.selectbox("Select Job Role / Department", roles)

min_feasibility = st.sidebar.slider("Minimum AI Feasibility Score (%)", 0, 100, 40)

# Filter logic
filtered_df = df if selected_role == "All Roles" else df[df["role_category"] == selected_role]
filtered_df = filtered_df[filtered_df["ai_feasibility_score"] >= min_feasibility]

# Header
st.markdown('<div class="main-header">🤖 AI Task Automation & Evaluation Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyzing task automation feasibility, agent architectures, and instructional prompt validation.</div>', unsafe_allow_html=True)

# Overview KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Evaluated Tasks", len(filtered_df))
with col2:
    avg_score = filtered_df["ai_feasibility_score"].mean() if not filtered_df.empty else 0
    st.metric("Avg. Automation Feasibility", f"{avg_score:.1f}%")
with col3:
    total_hours = filtered_df["human_hours_per_week"].sum() if not filtered_df.empty else 0
    st.metric("Total Weekly Human Effort", f"{total_hours:.1f} hrs")
with col4:
    high_auto_cnt = len(filtered_df[filtered_df["ai_feasibility_score"] >= 80])
    st.metric("High Feasibility (>80%)", high_auto_cnt)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Feasibility Analytics", "🧩 Agent Architecture Mapping", "🧪 Prompt Fact-Checking Sandbox"])

with tab1:
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.subheader("Automation Score vs. Human Effort (Hours/Week)")
        if not filtered_df.empty:
            fig_scatter = px.scatter(
                filtered_df,
                x="human_hours_per_week",
                y="ai_feasibility_score",
                size="human_hours_per_week",
                color="role_category",
                hover_name="task_name",
                hover_data=["suggested_agent_architecture", "automation_category"],
                labels={
                    "human_hours_per_week": "Weekly Human Hours",
                    "ai_feasibility_score": "AI Feasibility Score (%)",
                    "role_category": "Role"
                },
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_scatter.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="Automation Threshold")
            fig_scatter.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No tasks match current filter parameters.")

    with col_chart2:
        st.subheader("Automation Category Breakdown")
        if not filtered_df.empty:
            cat_counts = filtered_df["automation_category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig_pie = px.pie(
                cat_counts,
                names="Category",
                values="Count",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("Task Matrix & Suggested Autonomous Agent Workflows")
    st.markdown("Recommended multi-step agent designs and human-in-the-loop validation criteria:")
    
    display_cols = [
        "task_name", "role_category", "complexity", "ai_feasibility_score", 
        "suggested_agent_architecture", "automation_category"
    ]
    st.dataframe(
        filtered_df[display_cols].rename(columns={
            "task_name": "Task Name",
            "role_category": "Category",
            "complexity": "Complexity",
            "ai_feasibility_score": "Score (%)",
            "suggested_agent_architecture": "Suggested Agent Pattern",
            "automation_category": "Class"
        }),
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.subheader("Instructional Prompt Fact-Checking & Output Validation")
    st.markdown("Simulate prompt execution and perform technical validation on generated learning materials.")
    
    sample_templates = {
        "curriculum_draft": {
            "title": "Technical Syllabus Generation",
            "prompt": "Create a 4-week beginner syllabus for 'Understanding LLM Agents & Tool Use'. Include prerequisites, weekly modules, hands-on lab topics, and self-check quiz questions.",
            "simulated_output": """Week 1: Foundations of LLMs & Tokenization
- Lab: Inspecting Tokens & System Prompts using Python tiktoken.
- Quiz: What differentiates context window from parametric knowledge?

Week 2: Function Calling & OpenAPI Integration
- Lab: Building a Weather Tool Caller with structured JSON schema.
- Quiz: Why must schemas strictly define parameter types?

Week 3: ReAct Architecture & Multi-Step Reasoning
- Lab: Implementing Thought-Action-Observation loops without frameworks.
- Quiz: How does an agent recognize when to terminate a tool execution cycle?

Week 4: Evaluation, Groundedness & Fact-Checking
- Lab: Validating outputs against knowledge base references (RAG).
- Quiz: What metrics quantify hallucination in closed-domain QA?""",
            "fact_check_notes": "Verified: Concepts sequence adheres to Bloom's taxonomy. Lab topics reflect reproducible industry patterns."
        },
        "refactor_lint": {
            "title": "Code Refactoring & PEP8 Quality Audit",
            "prompt": "Refactor this raw data cleaning script to follow PEP8 guidelines, include docstrings, and handle edge cases for missing values.",
            "simulated_output": """def clean_tabular_records(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Sanitizes tabular input data by imputing missing values and formatting column names.
    
    Args:
        df (pd.DataFrame): Raw ingested dataframe.
    Returns:
        pd.DataFrame: Cleaned dataframe ready for downstream analytics.
    \"\"\"
    cleaned_df = df.copy()
    cleaned_df.columns = [col.strip().lower().replace(' ', '_') for col in cleaned_df.columns]
    cleaned_df.dropna(subset=['task_id'], inplace=True)
    return cleaned_df""",
            "fact_check_notes": "Verified: Type annotations accurate; prevents chained assignment side-effects using df.copy()."
        }
    }

    selected_test = st.selectbox(
        "Choose an Instructional Template to Inspect",
        list(sample_templates.keys()),
        format_func=lambda k: sample_templates[k]["title"]
    )

    item = sample_templates[selected_test]
    
    col_p, col_r = st.columns(2)
    with col_p:
        st.markdown("**Structured Prompt Input:**")
        st.text_area("Prompt", item["prompt"], height=140, disabled=True)
        st.markdown("**Technical Fact-Checking Checklist:**")
        st.checkbox("Prerequisites explicitly stated", value=True)
        st.checkbox("Code snippets adhere to PEP8 / Python best practices", value=True)
        st.checkbox("Reproducible without undocumented external API keys", value=True)

    with col_r:
        st.markdown("**Generated Output:**")
        st.code(item["simulated_output"], language="markdown")
        st.success(f"🔍 **Fact-Check Assessment:** {item['fact_check_notes']}")
