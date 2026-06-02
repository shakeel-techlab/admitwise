import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from data.universities import UNIVERSITIES, FIELDS
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO

st.set_page_config(page_title="Compare - AdmitWise", page_icon="⚖️", layout="wide")
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
    st.markdown('<div class="aw-section-title">⚖️ Compare Universities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:20px;margin-top:30px;">
        <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
        <div style="font-size:1.3rem;font-weight:800;color:#1e1b4b;margin-bottom:12px;">Login Required</div>
        <div style="color:#64748b;font-size:0.95rem;margin-bottom:24px;">Sign in to compare universities side-by-side — fees, merit formulas, scholarships, and more.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.page_link("pages/6_Login.py", label="👤 Sign In / Create Account →")
    st.stop()

st.markdown('<div class="aw-section-title">⚖️ Compare Universities</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Compare up to 3 universities side by side — fees, merit, scholarships, and facilities</div>', unsafe_allow_html=True)

uni_names = [u["name"] for u in UNIVERSITIES]
uni_map = {u["name"]: u for u in UNIVERSITIES}

col1, col2, col3 = st.columns(3)
u1 = col1.selectbox("University 1", ["Select..."] + uni_names, key="u1")
u2 = col2.selectbox("University 2", ["Select..."] + uni_names, key="u2")
u3 = col3.selectbox("University 3 (optional)", ["Select..."] + uni_names, key="u3")

selected = [n for n in [u1, u2, u3] if n != "Select..."]

if len(selected) < 2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="aw-info-box" style="text-align:center;padding:32px;">
        <div style="font-size:2rem;margin-bottom:8px;">⚖️</div>
        <div style="font-weight:700;color:#1e1b4b;">Select at least 2 universities above to compare them</div>
        <div style="color:#64748b;font-size:0.85rem;margin-top:6px;">You can compare up to 3 universities side by side</div>
    </div>
    """, unsafe_allow_html=True)
else:
    unis = [uni_map[n] for n in selected]
    n = len(unis)
    st.markdown("---")

    # Header row
    header = st.columns([1.8] + [1]*n)
    header[0].markdown('<div class="cmp-label">Category</div>', unsafe_allow_html=True)
    for i, uni in enumerate(unis):
        header[i+1].markdown(f"""
        <div class="cmp-header">
            <div style="font-size:1.05rem;">{uni['name']}</div>
            <div style="font-size:0.75rem;font-weight:500;color:#64748b;">{uni['city']}</div>
        </div>
        """, unsafe_allow_html=True)

    rows = [
        ("Full Name", lambda u: u["full_name"]),
        ("City", lambda u: u["city"]),
        ("Province", lambda u: u.get("province","-")),
        ("Pakistan Ranking", lambda u: f"#{u['ranking']}"),
        ("Annual Fee (PKR)", lambda u: f"{u['fee_per_year']:,}"),
        ("Min FSc %", lambda u: f"{u['min_fsc_percent']}%"),
        ("Entry Test", lambda u: u["entry_test"]),
        ("Deadline", lambda u: u["deadline"]),
    ]

    for label, fn in rows:
        row = st.columns([1.8] + [1]*n)
        row[0].markdown(f'<div class="cmp-label" style="padding:10px 0;">{label}</div>', unsafe_allow_html=True)
        for i, uni in enumerate(unis):
            row[i+1].markdown(f'<div class="cmp-row">{fn(uni)}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="aw-section-title" style="font-size:1.1rem;">🎓 Scholarships</div>', unsafe_allow_html=True)
    sch_cols = st.columns([1.8] + [1]*n)
    sch_cols[0].markdown('<div class="cmp-label">Scholarships</div>', unsafe_allow_html=True)
    for i, uni in enumerate(unis):
        tags = "".join(f'<div style="margin:3px 0;"><span class="aw-tag">🎓 {s}</span></div>' for s in uni.get("scholarships",[]))
        sch_cols[i+1].markdown(tags or "—", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="aw-section-title" style="font-size:1.1rem;">📐 Merit Formula by Field</div>', unsafe_allow_html=True)
    all_fields = set()
    for uni in unis:
        all_fields.update(uni["merit_criteria"].keys())

    for field in sorted(all_fields):
        fc = st.columns([1.8] + [1]*n)
        fc[0].markdown(f'<div class="cmp-label" style="padding:10px 0;">{field}</div>', unsafe_allow_html=True)
        for i, uni in enumerate(unis):
            if field in uni["merit_criteria"]:
                c = uni["merit_criteria"][field]
                fc[i+1].markdown(f'<div class="cmp-row" style="font-size:0.8rem;">Matric {c["matric_weight"]}% + FSc {c["fsc_weight"]}% + Test {c["net_weight"]}%{(" · Min: "+str(c.get("min_net",0))+"%") if c.get("min_net") else ""}</div>', unsafe_allow_html=True)
            else:
                fc[i+1].markdown('<div class="cmp-row" style="color:#94a3b8;font-size:0.8rem;">Not offered</div>', unsafe_allow_html=True)
