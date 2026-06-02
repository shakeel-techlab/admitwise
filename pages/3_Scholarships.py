import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from data.universities import SCHOLARSHIPS_DB
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO

st.set_page_config(page_title="Scholarships - AdmitWise", page_icon="🎓", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.get("user"):
        u = st.session_state.user
        st.markdown(f'<div style="background:#f5f3ff;border-radius:10px;padding:10px 12px;margin-bottom:8px;"><div style="font-weight:800;color:#7c3aed;font-size:0.85rem;">👤 {u["name"]}</div></div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="sb_logout"):
            st.session_state.user = None
            st.rerun()
    else:
        st.markdown('<div style="background:#fef3c7;border-radius:10px;padding:10px 12px;margin-bottom:8px;font-size:0.82rem;color:#92400e;">🔒 Sign in to access all features</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Admission_Predictor.py", label="🎯 Admission Predictor")
    st.page_link("pages/2_Universities.py", label="🏫 Universities")
    st.page_link("pages/3_Scholarships.py", label="🎓 Scholarships")
    st.page_link("pages/4_Location_Finder.py", label="📍 Location Finder")
    st.page_link("pages/7_Compare.py", label="⚖️ Compare Universities")
    st.page_link("pages/5_AI_Chatbot.py", label="🤖 AI Advisor")
    st.page_link("pages/8_Guide_and_Resources.py", label="📚 Guide & Resources")
    st.page_link("pages/6_Login.py", label="👤 Login / Account")

# Login guard
if not st.session_state.get("user"):
    st.markdown('<div class="aw-section-title">🎓 Scholarships</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:20px;margin-top:30px;">
        <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
        <div style="font-size:1.3rem;font-weight:800;color:#1e1b4b;margin-bottom:12px;">Login Required</div>
        <div style="color:#64748b;font-size:0.95rem;margin-bottom:24px;">Sign in to explore HEC, PEEF, Ehsaas, and university scholarships<br>with eligibility criteria and direct application links.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.page_link("pages/6_Login.py", label="👤 Sign In / Create Account →")
    st.stop()

st.markdown('<div class="aw-section-title">🎓 Available Scholarships</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Funding opportunities for Pakistani students — HEC, government, and university scholarships</div>', unsafe_allow_html=True)

type_filter = st.selectbox("Filter by Type", ["All Types", "Need-based", "Merit-based", "Combined"])
filtered = SCHOLARSHIPS_DB if type_filter == "All Types" else [s for s in SCHOLARSHIPS_DB if s["type"] == type_filter]

st.caption(f"Showing **{len(filtered)}** scholarships")
st.markdown("<br>", unsafe_allow_html=True)

cols = st.columns(2)
for i, sch in enumerate(filtered):
    with cols[i % 2]:
        type_color = {"Need-based": "#dcfce7", "Merit-based": "#dbeafe", "Combined": "#f5f3ff"}.get(sch["type"], "#f1f5f9")
        type_text_color = {"Need-based": "#166534", "Merit-based": "#1e40af", "Combined": "#6b21a8"}.get(sch["type"], "#475569")
        st.markdown(f"""
        <div class="aw-card" style="margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <div class="aw-card-title" style="font-size:0.92rem;">{sch['name']}</div>
                <span style="background:{type_color};color:{type_text_color};padding:2px 8px;border-radius:20px;font-size:0.72rem;font-weight:700;white-space:nowrap;">{sch['type']}</span>
            </div>
            <div style="font-size:0.8rem;color:#7c3aed;font-weight:700;margin-bottom:6px;">🏛️ {sch['provider']}</div>
            <div style="font-size:0.82rem;color:#1e1b4b;font-weight:600;margin-bottom:4px;">💰 {sch['amount']}</div>
            <div style="font-size:0.78rem;color:#64748b;margin-bottom:4px;">✅ {sch['eligibility']}</div>
            <div style="font-size:0.78rem;color:#94a3b8;">📅 Deadline: {sch['deadline']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 Apply Now", sch["link"], use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
