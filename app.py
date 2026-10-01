import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="AI Task Automation Benchmark & Evaluation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tùy chỉnh giao diện CSS
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

# Dữ liệu thực nghiệm được tích hợp sẵn 
DATA_SOURCE = """task_id,role_category,task_name,complexity,human_hours_per_week,ai_feasibility_score,automation_category,suggested_agent_architecture,prompt_template_key
T01,Software Engineering,API Integration & Endpoint Testing,Medium,6.5,88,High Automation,ReAct Agent + OpenAPI Tool,code_gen_test
T02,Software Engineering,Legacy Code Refactoring & Linting,Medium,5.0,78,Moderate Automation,AST Parser + LLM Refactor,refactor_lint
T03,Software Engineering,System Architecture & Distributed Consensus,High,8.0,32,Human-in-the-Loop,RAG Architect Assistant,arch_rag
T04,Data Science,Exploratory Data Analysis (EDA) & Summary Stats,Low,6.0,92,High Automation,Code Interpreter Agent,auto_eda
T05,Data Science,Feature Engineering & Correlation Screening,Medium,7.0,84,High Automation,Tabular Feature Pipeline Agent,feat_eng
T06,Data Science,Causal Inference & Business Decision Framing,High,9.0,36,Human-in-the-Loop,Decision Tree CoT Analyzer,causal_cot
T07,Technical Content & Learning,Curriculum Outline & Syllabus Drafting,Low,5.5,90,High Automation,Few-shot Syllabus Generator,curriculum_draft
T08,Technical Content & Learning,Slide Deck Scripting & Concept Breakdown,Medium,7.5,86,High Automation,Analogy-driven Explanation Agent,concept_explainer
T09,Technical Content & Learning,Technical Fact-Checking & Code Verification,Medium,6.0,74,Moderate Automation,Self-Reflective Critic Agent,critic_factcheck
T10,Business Operations,Customer Inquiry Categorization & Routing,Low,8.0,95,Full Automation,Zero-Shot Intent Classifier,intent_routing
T11,Business Operations,Standard Operating Procedure (SOP) Drafting,Medium,6.0,82,High Automation,Process Documentation Agent,sop_generator
T12,Business Operations,Cross-Department Conflict Resolution & Negotiation,High,7.0,18,Human Dominant,Communication Coach Persona,negotiation_coach
"""

@st.cache_data
def load_data():
    return pd.read_csv(io.StringIO(DATA_SOURCE))

df = load_data()

# Bộ lọc thanh bên (Sidebar)
st.sidebar.title("🛠️ Điều hướng & Bộ lọc")
st.sidebar.markdown("Lọc dữ liệu đo lường mức độ khả thi tự động hóa theo nhóm ngành.")

roles = ["Tất cả vị trí"] + sorted(df["role_category"].unique().tolist())
selected_role = st.sidebar.selectbox("Chọn nhóm vị trí / Phòng ban", roles)

min_feasibility = st.sidebar.slider("Mức độ khả thi tối thiểu (%)", 0, 100, 30)

# Lọc dữ liệu
filtered_df = df if selected_role == "Tất cả vị trí" else df[df["role_category"] == selected_role]
filtered_df = filtered_df[filtered_df["ai_feasibility_score"] >= min_feasibility]

# Tiêu đề giao diện chính
st.markdown('<div class="main-header">🤖 AI Task Automation & Evaluation Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Phân tích mức độ khả thi tự động hóa của AI, kiến trúc Agent và kiểm định chất lượng Prompt đào tạo.</div>', unsafe_allow_html=True)

# Thẻ chỉ số tổng quan (KPIs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tác vụ đã đánh giá", len(filtered_df))
with col2:
    avg_score = filtered_df["ai_feasibility_score"].mean() if not filtered_df.empty else 0
    st.metric("Khả thi tự động hóa TB", f"{avg_score:.1f}%")
with col3:
    total_hours = filtered_df["human_hours_per_week"].sum() if not filtered_df.empty else 0
    st.metric("Tổng giờ làm thủ công/tuần", f"{total_hours:.1f} giờ")
with col4:
    high_auto_cnt = len(filtered_df[filtered_df["ai_feasibility_score"] >= 80])
    st.metric("Mức khả thi cao (>80%)", high_auto_cnt)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Phân tích Khả thi", "🧩 Sơ đồ Kiến trúc Agent", "🧪 Kiểm định Kỹ thuật (Fact-Checking)"])

with tab1:
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.subheader("Mức độ khả thi vs. Thời gian thực hiện của con người")
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
                    "human_hours_per_week": "Giờ làm việc mỗi tuần",
                    "ai_feasibility_score": "Điểm khả thi AI (%)",
                    "role_category": "Nhóm ngành"
                },
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_scatter.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="Ngưỡng tự động hóa cao")
            fig_scatter.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Không có tác vụ nào khớp với bộ lọc hiện tại.")

    with col_chart2:
        st.subheader("Phân bổ phân loại tự động hóa")
        if not filtered_df.empty:
            cat_counts = filtered_df["automation_category"].value_counts().reset_index()
            cat_counts.columns = ["Phân loại", "Số lượng"]
            fig_pie = px.pie(
                cat_counts,
                names="Phân loại",
                values="Số lượng",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("Ma trận tác vụ & Đề xuất kiến trúc Agent")
    st.markdown("Đề xuất quy trình Agent nhiều bước và tiêu chí giám sát Human-in-the-Loop:")
    
    display_cols = [
        "task_name", "role_category", "complexity", "ai_feasibility_score", 
        "suggested_agent_architecture", "automation_category"
    ]
    st.dataframe(
        filtered_df[display_cols].rename(columns={
            "task_name": "Tên tác vụ",
            "role_category": "Nhóm ngành",
            "complexity": "Độ phức tạp",
            "ai_feasibility_score": "Điểm (%)",
            "suggested_agent_architecture": "Kiến trúc Agent đề xuất",
            "automation_category": "Phân loại"
        }),
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.subheader("Kiểm định Prompt & Xác thực tính chuẩn xác kỹ thuật")
    st.markdown("Mô phỏng thực thi prompt đào tạo và đối soát kỹ thuật (fact-checking) đối với tài liệu học tập được tạo ra.")
    
    sample_templates = {
        "curriculum_draft": {
            "title": "Tạo khung giáo trình: LLM Agents & Tool Use",
            "prompt": "Create a 4-week beginner syllabus for 'Understanding LLM Agents & Tool Use'. Include prerequisites, weekly modules, hands-on lab topics, and self-check quiz questions.",
            "simulated_output": """Tuần 1: Nền tảng về LLM & Cơ chế Tokenization
- Bài thực hành: Khám phá Tokens & System Prompts bằng thư viện tiktoken trong Python.
- Câu hỏi ôn tập: Điểm khác biệt giữa context window và parametric knowledge là gì?

Tuần 2: Function Calling & Tích hợp OpenAPI
- Bài thực hành: Xây dựng công cụ gọi thời tiết bằng lược đồ JSON có cấu trúc.
- Câu hỏi ôn tập: Tại sao tham số schema cần định nghĩa kiểu dữ liệu chặt chẽ?

Tuần 3: Kiến trúc ReAct & Quy trình Suy luận Đa bước
- Bài thực hành: Tự cài đặt vòng lặp Thought-Action-Observation thuần bằng Python.
- Câu hỏi ôn tập: Làm thế nào để Agent nhận biết điểm dừng trong chu kỳ gọi công cụ?

Tuần 4: Đánh giá, Xác thực Tri thức & Fact-Checking
- Bài thực hành: Đối soát kết quả đầu ra với cơ sở tri thức cục bộ (RAG).
- Câu hỏi ôn tập: Chỉ số nào định lượng hiện tượng ảo giác (hallucination) trong QA?""",
            "fact_check_notes": "Đã kiểm định: Khung kiến thức tuân thủ thang đo Bloom. Các bài lab thực hành đảm bảo khả năng tái lập và chạy thực tế."
        },
        "refactor_lint": {
            "title": "Chuẩn hóa mã nguồn theo chuẩn PEP8",
            "prompt": "Refactor this raw data cleaning script to follow PEP8 guidelines, include docstrings, and handle edge cases for missing values.",
            "simulated_output": """def clean_tabular_records(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Làm sạch dữ liệu bảng đầu vào, xử lý giá trị thiếu và chuẩn hóa tên cột.
    
    Args:
        df (pd.DataFrame): DataFrame dữ liệu thô.
    Returns:
        pd.DataFrame: DataFrame đã chuẩn hóa sẵn sàng cho phân tích.
    \"\"\"
    cleaned_df = df.copy()
    cleaned_df.columns = [col.strip().lower().replace(' ', '_') for col in cleaned_df.columns]
    cleaned_df.dropna(subset=['task_id'], inplace=True)
    return cleaned_df""",
            "fact_check_notes": "Đã kiểm định: Định dạng Type Hint chuẩn xác; sử dụng df.copy() để tránh lỗi tham chiếu bộ nhớ trong Pandas."
        }
    }

    selected_test = st.selectbox(
        "Chọn mẫu học liệu để kiểm tra",
        list(sample_templates.keys()),
        format_func=lambda k: sample_templates[k]["title"]
    )

    item = sample_templates[selected_test]
    
    col_p, col_r = st.columns(2)
    with col_p:
        st.markdown("**Prompt đầu vào có cấu trúc:**")
        st.text_area("Prompt", item["prompt"], height=140, disabled=True)
        st.markdown("**Checklist đối soát kỹ thuật (Fact-Checking):**")
        st.checkbox("Kiến thức tiền đề được ghi rõ ràng", value=True)
        st.checkbox("Đoạn mã tuân thủ quy chuẩn PEP8 / Best practices", value=True)
        st.checkbox("Không phụ thuộc API key ngoài chưa được tài liệu hóa", value=True)

    with col_r:
        st.markdown("**Nội dung học liệu được sinh ra:**")
        st.code(item["simulated_output"], language="markdown")
        st.success(f"🔍 **Kết quả đối soát:** {item['fact_check_notes']}")
