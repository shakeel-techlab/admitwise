import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from utils.predictor import predict, get_merit_gap
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO
from data.universities import PAKISTAN_CITIES, FIELDS

st.set_page_config(page_title="Admission Predictor - AdmitWise", page_icon="🎯", layout="wide")
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

st.markdown('<div class="aw-section-title">🎯 Admission Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Enter your academic marks to get instant admission probability across Pakistan\'s top universities</div>', unsafe_allow_html=True)

with st.form("predictor_form"):
    st.markdown('<div style="font-weight:800;font-size:1rem;color:#1e1b4b;margin-bottom:16px;">📋 Your Academic Profile</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="font-weight:700;color:#475569;font-size:0.88rem;margin-bottom:8px;">🎓 Matric Marks</div>', unsafe_allow_html=True)
        mc1, mc2 = st.columns(2)
        matric_obtained = mc1.number_input("Obtained", 0, 1100, 950, key="mat_obt")
        matric_total = mc2.number_input("Total", 100, 1100, 1100, key="mat_tot")
        matric_pct = (matric_obtained / matric_total * 100) if matric_total > 0 else 0
        st.progress(min(matric_pct/100, 1.0), text=f"Matric: **{matric_pct:.1f}%**")
    with col2:
        st.markdown('<div style="font-weight:700;color:#475569;font-size:0.88rem;margin-bottom:8px;">📚 FSc / Intermediate Marks</div>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        fsc_obtained = fc1.number_input("Obtained", 0, 1200, 880, key="fsc_obt")
        fsc_total = fc2.number_input("Total", 100, 1200, 1100, key="fsc_tot")
        fsc_pct = (fsc_obtained / fsc_total * 100) if fsc_total > 0 else 0
        st.progress(min(fsc_pct/100, 1.0), text=f"FSc: **{fsc_pct:.1f}%**")

    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4, c5 = st.columns(3)
    with c3:
        net_score = st.number_input("🧪 Entry Test Score (%)", 0, 100, 65, help="NET, ECAT, NAT, SAT, MDCAT etc. — as a percentage")
    with c4:
        field = st.selectbox("📖 Field of Study", FIELDS)
    with c5:
        city = st.selectbox("📍 Your City", ["Select City"] + PAKISTAN_CITIES)

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔮 Predict My Chances", use_container_width=True, type="primary")

if submitted:
    selected_city = city if city != "Select City" else None
    results = predict(matric_obtained, matric_total, fsc_obtained, fsc_total, net_score, field, selected_city)

    if not results:
        st.warning(f"No universities found offering **{field}**. Try Computer Science, Engineering, or Business.")
    else:
        high = sum(1 for r in results if r["probability"] == "High")
        medium = sum(1 for r in results if r["probability"] == "Medium")

        st.markdown("<br>", unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Universities Found", len(results))
        m2.metric("High Chances", high)
        m3.metric("Medium Chances", medium)
        m4.metric("Your FSc %", f"{fsc_pct:.1f}%")

        st.markdown("---")
        st.markdown(f'<div class="aw-section-title">📊 Results for {field}</div>', unsafe_allow_html=True)

        fc1, fc2 = st.columns(2)
        with fc1:
            show_prob = st.multiselect("Filter by Probability", ["High","Medium","Low","Very Low"], default=["High","Medium","Low"])
        with fc2:
            sort_by = st.selectbox("Sort by", ["Merit Score","Fee (Low→High)","Fee (High→Low)","Deadline"])

        filtered = [r for r in results if r["probability"] in show_prob]
        if sort_by == "Fee (Low→High)": filtered.sort(key=lambda x: x["university"]["fee_per_year"])
        elif sort_by == "Fee (High→Low)": filtered.sort(key=lambda x: x["university"]["fee_per_year"], reverse=True)
        elif sort_by == "Deadline": filtered.sort(key=lambda x: x["university"]["deadline"])

        if not filtered:
            st.info("No results match the selected filters.")
        else:
            for r in filtered:
                uni = r["university"]
                prob = r["probability"]
                merit = r["merit_score"]
                days_left = r["days_left"]
                gap = get_merit_gap(merit, prob)

                badge_map = {
                    "High": '<span class="badge-high">🟢 High</span>',
                    "Medium": '<span class="badge-medium">🟡 Medium</span>',
                    "Low": '<span class="badge-low">🔴 Low</span>',
                    "Very Low": '<span class="badge-vlow">⚫ Very Low</span>',
                }

                with st.expander(f"**{uni['name']}** — {uni['city']}   |   Merit: {merit:.1f}%   |   {prob} chance"):
                    # Card header
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
                        <div>
                            <div class="aw-card-title">{uni['full_name']}</div>
                            <div class="aw-card-sub">{uni['city']} · {uni.get('province','')}</div>
                        </div>
                        <div>{badge_map.get(prob,'')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.progress(min(merit/100, 1.0), text=f"Merit Score: {merit:.1f}%")

                    c1, c2, c3 = st.columns([2,1,1])
                    with c1:
                        st.caption(uni["description"])
                        st.markdown(f'🏢 Entry Test: <span class="aw-tag">{uni["entry_test"]}</span>', unsafe_allow_html=True)
                        if gap:
                            st.markdown(f'<div class="aw-info-box" style="margin-top:8px;"><div class="aw-info-label">Merit Gap</div><div class="aw-info-value" style="font-size:0.85rem;color:#7c3aed;">📈 {gap}</div></div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">Deadline</div><div class="aw-info-value" style="font-size:0.85rem;">{uni["deadline"]}</div></div>', unsafe_allow_html=True)
                        if days_left is not None:
                            if days_left < 0:
                                st.error("❌ Deadline passed")
                            elif days_left <= 7:
                                st.warning(f"⏰ {days_left} days left!")
                            else:
                                st.success(f"✅ {days_left} days left")
                        st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">Annual Fee</div><div class="aw-info-value">PKR {uni["fee_per_year"]:,}</div></div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">Ranking</div><div class="aw-info-value">#{uni["ranking"]}</div></div>', unsafe_allow_html=True)
                        if r["distance"]:
                            icon = "📍" if r["distance"] == "Nearby" else "🚗"
                            st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">Distance</div><div class="aw-info-value" style="font-size:0.85rem;">{icon} {r["distance"]}</div></div>', unsafe_allow_html=True)
                        st.markdown(f"🌐 **[Website]({uni['website']})**")

                    if uni.get("scholarships"):
                        st.markdown("**🎓 Available Scholarships:**")
                        tags = "".join(f'<span class="aw-tag">{s}</span>' for s in uni["scholarships"])
                        st.markdown(tags, unsafe_allow_html=True)
