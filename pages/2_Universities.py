import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from data.universities import UNIVERSITIES, PAKISTAN_CITIES, FIELDS
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO

st.set_page_config(page_title="Universities - AdmitWise", page_icon="🏫", layout="wide")
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
    st.markdown('<div class="aw-section-title">🏫 Pakistan Universities Directory</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:20px;margin-top:30px;">
        <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
        <div style="font-size:1.3rem;font-weight:800;color:#1e1b4b;margin-bottom:12px;">Login Required</div>
        <div style="color:#64748b;font-size:0.95rem;margin-bottom:24px;">Create a free account or sign in to browse all Pakistani universities,<br>view admission criteria, deadlines, fees, and more.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.page_link("pages/6_Login.py", label="👤 Sign In / Create Account →")
    st.stop()

st.markdown('<div class="aw-section-title">🏫 Pakistan Universities Directory</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Browse all tracked universities with admission criteria, deadlines, and contact info</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    search = st.text_input("🔍 Search university", placeholder="e.g. NUST, LUMS, Karachi...")
with col2:
    field_filter = st.selectbox("Filter by Field", ["All Fields"] + FIELDS)
with col3:
    city_filter = st.selectbox("Filter by City", ["All Locations"] + PAKISTAN_CITIES + ["Multiple Campuses"])

filtered = UNIVERSITIES
if search:
    filtered = [u for u in filtered if search.lower() in u["name"].lower() or search.lower() in u["full_name"].lower() or search.lower() in u["city"].lower()]
if field_filter != "All Fields":
    filtered = [u for u in filtered if field_filter in u["fields"]]
if city_filter != "All Locations":
    filtered = [u for u in filtered if u["city"].lower() == city_filter.lower() or u["city"] == "Multiple Campuses"]

st.caption(f"Showing **{len(filtered)}** of {len(UNIVERSITIES)} universities")
st.markdown("<br>", unsafe_allow_html=True)

if not filtered:
    st.warning("No universities match your filters. Try adjusting your search.")
else:
    for uni in filtered:
        with st.expander(f"🏫  {uni['name']}  —  {uni['full_name']}  |  {uni['city']}  |  #{uni['ranking']} Ranked"):
            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px;">
                <span class="aw-tag">📍 {uni['city']}</span>
                <span class="aw-tag">🏛️ {uni.get('province','')}</span>
                <span class="aw-tag">🏆 #{uni['ranking']} Ranked</span>
                <span class="aw-tag">💰 PKR {uni['fee_per_year']//1000}k/yr</span>
                <span class="aw-tag">📅 Deadline: {uni['deadline']}</span>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**About:** {uni['description']}")
                st.markdown("**Fields & Specializations:**")
                for field in uni["fields"]:
                    subfields = uni.get("subfields", {}).get(field, [])
                    if subfields:
                        subs_html = "".join(f'<span class="aw-tag" style="font-size:0.72rem;background:#e0e7ff;color:#3730a3;">{s}</span>' for s in subfields)
                        st.markdown(f'<div style="margin-bottom:6px;"><span class="aw-tag" style="background:#7c3aed;color:#fff;font-weight:700;">📚 {field}</span> {subs_html}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="aw-tag" style="background:#7c3aed;color:#fff;font-weight:700;">📚 {field}</span>', unsafe_allow_html=True)

                st.markdown(f'<br>🧪 Entry Test: <span class="aw-tag">{uni["entry_test"]}</span> &nbsp; Min FSc: <span class="aw-tag">{uni["min_fsc_percent"]}%</span>', unsafe_allow_html=True)

                st.markdown("🎫**Admission Merit Formula:**")
                for field, crit in uni["merit_criteria"].items():
                    st.caption(f"• **{field}**: Matric {crit['matric_weight']}% + FSc {crit['fsc_weight']}% + Test {crit['net_weight']}%" + (f" (Min test: {crit.get('min_net',0)}%)" if crit.get('min_net') else ""))

                if uni.get("scholarships"):
                    st.markdown("**Scholarships:**")
                    sch_tags = "".join(f'<span class="aw-tag">🎓 {s}</span>' for s in uni["scholarships"])
                    st.markdown(sch_tags, unsafe_allow_html=True)

            with c2:
                st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">Annual Fee</div><div class="aw-info-value">PKR {uni["fee_per_year"]:,}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">Pakistan Ranking</div><div class="aw-info-value">#{uni["ranking"]}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">Deadline</div><div class="aw-info-value" style="font-size:0.85rem;">{uni["deadline"]}</div></div>', unsafe_allow_html=True)
                if uni.get("facilities"):
                    st.markdown("**Facilities:**")
                    for fac in uni["facilities"]:
                        st.caption(f"✓ {fac}")
                st.markdown("<br>", unsafe_allow_html=True)
                st.link_button("🌐 Visit Website", uni["website"], use_container_width=True)
                if uni.get("contact"):
                    st.caption(f"📧 {uni['contact']}")
