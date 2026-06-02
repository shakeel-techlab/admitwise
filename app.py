import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import datetime
from data.universities import UNIVERSITIES, SCHOLARSHIPS_DB
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO

st.set_page_config(
    page_title="AdmitWise — Pakistan University Admission Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.get("user"):
        u = st.session_state.user
        st.markdown(f'<div style="background:#f5f3ff;border-radius:12px;padding:12px 14px;margin-bottom:12px;"><div style="font-weight:800;color:#7c3aed;font-size:0.9rem;">👤 {u["name"]}</div><div style="font-size:0.78rem;color:#64748b;">{u["email"]}</div></div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="sidebar_logout"):
            st.session_state.user = None
            st.rerun()
    else:
        st.markdown('<div style="background:#fef3c7;border-radius:10px;padding:10px 12px;margin-bottom:12px;font-size:0.82rem;color:#92400e;">🔒 <strong>Sign in</strong> to access Universities, Scholarships & more</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Admission_Predictor.py", label="🎯 Admission Predictor")
    st.page_link("pages/2_Universities.py", label="🏫 Universities")
    st.page_link("pages/3_Scholarships.py", label="🎓 Scholarships")
    st.page_link("pages/4_Location_Finder.py", label="📍 Location Finder")
    st.page_link("pages/7_Compare.py", label="⚖️ Compare Universities")
    st.page_link("pages/5_AI_Chatbot.py", label="🤖 AI Advisor")
    st.page_link("pages/8_Guide_and_Resources.py", label="📚 Guide & Resources")
    st.page_link("pages/6_Login.py", label="👤 Login / Account")
    closing = []
    for u in UNIVERSITIES:
        try:
            days = (datetime.strptime(u["deadline"], "%Y-%m-%d") - datetime.now()).days
            if 0 <= days <= 14:
                closing.append((u["name"], days))
        except Exception:
            pass
    if closing:
        st.markdown("---")
        st.markdown("**⏰ Closing Soon**")
        for name, days in sorted(closing, key=lambda x: x[1]):
            st.caption(f"{'🔴' if days<=3 else '🟡'} **{name}** — {days}d")

urgent = [u["name"] for u in UNIVERSITIES if 0 <= (datetime.strptime(u["deadline"], "%Y-%m-%d") - datetime.now()).days <= 7]
if urgent:
    st.markdown(f'<div class="aw-alert">⏰ <strong>Deadline alert:</strong> {", ".join(urgent)} closing within 7 days!</div>', unsafe_allow_html=True)

total_unis = len(UNIVERSITIES)
total_cities = len(set(u["city"] for u in UNIVERSITIES if u["city"] != "Multiple Campuses"))

st.markdown(f"""
<div class="aw-hero">
    <div class="aw-hero-pill"><span class="aw-hero-dot">●</span>{total_unis} universities tracked &nbsp;·&nbsp; Live admission data</div>
    <h1 class="aw-hero-title">Find your <span class="aw-hero-accent">perfect university</span><br>in under a minute.</h1>
    <p class="aw-hero-sub">Enter your marks, pick your field, and get instant admission probability across top universities — with merit gap analysis, deadlines, and prep tips.</p>
</div>
""", unsafe_allow_html=True)

s1,s2,s3,s4,s5 = st.columns(5)
for col,num,lbl in [(s1,str(total_unis),"Universities"),(s2,str(len(SCHOLARSHIPS_DB)),"Scholarships"),(s3,f"{total_cities}+","Cities"),(s4,"7","Fields"),(s5,"Free","Always")]:
    col.markdown(f'<div class="aw-stat"><div class="aw-stat-num">{num}</div><div class="aw-stat-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="aw-feature-grid">
    <div class="aw-feature"><div class="aw-feature-icon">🎯</div><div class="aw-feature-title">Admission Predictor</div><div class="aw-feature-desc">Enter your Matric &amp; FSc marks and entry test score. Get instant probability with merit gap analysis.</div></div>
    <div class="aw-feature"><div class="aw-feature-icon">🏫</div><div class="aw-feature-title">University Directory</div><div class="aw-feature-desc">Browse 15+ top Pakistani universities — criteria, entry tests, fees, deadlines, and facilities.</div></div>
    <div class="aw-feature"><div class="aw-feature-icon">🎓</div><div class="aw-feature-title">Scholarships</div><div class="aw-feature-desc">Discover HEC, PEEF, Ehsaas, and university scholarships with eligibility and application links.</div></div>
    <div class="aw-feature"><div class="aw-feature-icon">📍</div><div class="aw-feature-title">Location Finder</div><div class="aw-feature-desc">Find nearest universities to your city. Sort by distance to save on travel and accommodation.</div></div>
    <div class="aw-feature"><div class="aw-feature-icon">🤖</div><div class="aw-feature-title">AI Advisor</div><div class="aw-feature-desc">Chat with our AI counselor (powered by Claude) for personalized admission guidance.</div></div>
    <div class="aw-feature"><div class="aw-feature-icon">⚖️</div><div class="aw-feature-title">Compare Universities</div><div class="aw-feature-desc">Compare up to 3 universities side-by-side — fees, merit formula, scholarships, and more.</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="aw-section-title">⏰ Upcoming Deadlines</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Stay on top of admission timelines — apply before it\'s too late</div>', unsafe_allow_html=True)

deadline_data = []
for u in UNIVERSITIES:
    try:
        days = (datetime.strptime(u["deadline"], "%Y-%m-%d") - datetime.now()).days
        deadline_data.append((u["name"], u["city"], u["deadline"], days))
    except Exception:
        pass
deadline_data.sort(key=lambda x: x[3])

cols = st.columns(3)
for i, (name, city, dl, days) in enumerate(deadline_data[:9]):
    with cols[i % 3]:
        if days < 0: cls,icon,txt = "chip-closed","❌","Closed"
        elif days <= 7: cls,icon,txt = "chip-urgent","🔴",f"{days} days left!"
        elif days <= 30: cls,icon,txt = "chip-soon","🟡",f"{days} days"
        else: cls,icon,txt = "chip-ok","✅",f"{days} days"
        st.markdown(f'<div class="{cls}"><div style="font-weight:800;font-size:0.88rem;">{name}</div><div style="font-size:0.75rem;opacity:0.8;margin:2px 0;">{city} · {dl}</div><div style="font-weight:700;font-size:0.82rem;">{icon} {txt}</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align:center;padding:20px 0;color:#94a3b8;font-size:13px;"><strong style="color:#7c3aed;">AdmitWise</strong> · Smart University Admission Portal for Pakistan · Predictions are estimates based on historical merit data.<br>Built with ❤️ by Shakeel  for Pakistani students</div>', unsafe_allow_html=True)
