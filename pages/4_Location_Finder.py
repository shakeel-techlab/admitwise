import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from data.universities import UNIVERSITIES, PAKISTAN_CITIES, FIELDS
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO

st.set_page_config(page_title="Location Finder - AdmitWise", page_icon="📍", layout="wide")
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

CITY_COORDS = {
    "Islamabad":(33.6844,73.0479),"Rawalpindi":(33.5651,73.0169),"Lahore":(31.5204,74.3587),
    "Karachi":(24.8607,67.0011),"Peshawar":(34.0151,71.5249),"Quetta":(30.1798,66.9750),
    "Faisalabad":(31.4504,73.1350),"Multan":(30.1575,71.5249),"Gujranwala":(32.1877,74.1945),
    "Sialkot":(32.4945,74.5229),"Hyderabad":(25.3960,68.3578),"Abbottabad":(34.1463,73.2117),
    "Muzaffarabad":(34.3693,73.4717),"Gilgit":(35.9220,74.3087),"Topi":(34.0902,72.6328),
}

def haversine(lat1,lon1,lat2,lon2):
    R=6371; dlat=math.radians(lat2-lat1); dlon=math.radians(lon2-lon1)
    a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))


# Login guard
if not st.session_state.get("user"):
    st.markdown('<div class="aw-section-title">📍 Location Finder</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:20px;margin-top:30px;">
        <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
        <div style="font-size:1.3rem;font-weight:800;color:#1e1b4b;margin-bottom:12px;">Login Required</div>
        <div style="color:#64748b;font-size:0.95rem;margin-bottom:24px;">Sign in to find universities near your city and sort by distance.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.page_link("pages/6_Login.py", label="👤 Sign In / Create Account →")
    st.stop()

st.markdown('<div class="aw-section-title">📍 Location Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Find universities nearest to you — save on travel and accommodation costs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    your_city = st.selectbox("📍 Your City", PAKISTAN_CITIES, index=0)
with col2:
    field_filter = st.selectbox("📖 Field of Interest", ["All Fields"] + FIELDS)

if st.button("🔍 Find Nearest Universities", use_container_width=True, type="primary"):
    your_coords = CITY_COORDS.get(your_city)
    results = []
    for uni in UNIVERSITIES:
        if field_filter != "All Fields" and field_filter not in uni.get("fields", []):
            continue
        dist = haversine(your_coords[0], your_coords[1], uni["location"]["lat"], uni["location"]["lng"]) if your_coords else 9999
        results.append({**uni, "_dist": round(dist, 1)})
    results.sort(key=lambda x: x["_dist"])

    st.markdown("---")
    st.markdown(f'<div class="aw-section-title">Universities near {your_city}</div>', unsafe_allow_html=True)

    nearby = [r for r in results if r["_dist"] <= 100]
    m1,m2,m3 = st.columns(3)
    m1.metric("Nearby (<100 km)", len(nearby))
    m2.metric("Total Found", len(results))
    if results: m3.metric("Closest", results[0]["name"])
    st.markdown("<br>", unsafe_allow_html=True)

    for i, uni in enumerate(results):
        dist = uni["_dist"]
        if dist <= 50: dist_label,dist_cls = f"📍 {dist} km — Very Close","chip-ok"
        elif dist <= 150: dist_label,dist_cls = f"🚌 {dist} km — Moderate","chip-soon"
        elif dist <= 400: dist_label,dist_cls = f"✈️ {dist} km — Far","chip-urgent"
        else: dist_label,dist_cls = f"🗺️ {dist} km — Very Far","chip-closed"

        medal = ["🥇","🥈","🥉"][i] if i<3 else f"#{i+1}"

        st.markdown(f"""
        <div class="loc-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
                <div>
                    <div class="aw-card-title">{medal} {uni['name']} — {uni['full_name']}</div>
                    <div class="aw-card-sub">{uni['city']} · {uni.get('province','')} · #{uni['ranking']} Ranked</div>
                </div>
                <div>
                    <span class="loc-dist-badge">{dist_label}</span>
                </div>
            </div>
            <div style="font-size:0.82rem;color:#475569;margin-bottom:8px;">{uni['description']}</div>
            <div>
                {"".join(f'<span class="aw-tag">{f}</span>' for f in uni["fields"])}
            </div>
            <div style="margin-top:10px;font-size:0.82rem;color:#64748b;">
                🧪 {uni['entry_test']} &nbsp;·&nbsp; 💰 PKR {uni['fee_per_year']//1000}k/yr &nbsp;·&nbsp; 📅 Deadline: {uni['deadline']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not results:
        st.warning("No universities found for the selected field.")
else:
    st.markdown("---")
    st.markdown('<div class="aw-section-title">📋 All University Locations</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, uni in enumerate(UNIVERSITIES):
        with cols[i % 3]:
            st.markdown(f'<div class="aw-info-box"><div class="aw-info-label">{uni["name"]}</div><div class="aw-info-value" style="font-size:0.85rem;">{uni["city"]}</div></div>', unsafe_allow_html=True)
