import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from utils.auth import login_user, register_user, get_saved_universities
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO
from data.universities import UNIVERSITIES, PAKISTAN_CITIES

st.set_page_config(page_title="Login - AdmitWise", page_icon="👤", layout="centered")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.get("user"):
        u = st.session_state.user
        st.markdown(f'<div style="background:#f5f3ff;border-radius:10px;padding:10px 12px;margin-bottom:8px;"><div style="font-weight:800;color:#7c3aed;font-size:0.85rem;">👤 {u["name"]}</div></div>', unsafe_allow_html=True)
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

st.markdown('<div class="aw-section-title" style="text-align:center;">👤 Account</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub" style="text-align:center;">Sign in to save universities and access your profile</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.get("user"):
    user = st.session_state.user
    st.markdown(f"""
    <div class="aw-info-box" style="text-align:center;padding:24px;">
        <div style="font-size:2.5rem;margin-bottom:8px;">👤</div>
        <div style="font-size:1.1rem;font-weight:800;color:#1e1b4b;">Welcome back, {user['name']}!</div>
        <div style="font-size:0.85rem;color:#64748b;margin-top:4px;">{user['email']} &nbsp;·&nbsp; {user.get('city','')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="aw-section-title">⭐ My Saved Universities</div>', unsafe_allow_html=True)
    saved_ids = get_saved_universities(user["email"])
    saved_unis = [u for u in UNIVERSITIES if u["id"] in saved_ids]
    if saved_unis:
        for uni in saved_unis:
            st.markdown(f"""
            <div class="aw-card">
                <div class="aw-card-title">{uni['name']} — {uni['full_name']}</div>
                <div class="aw-card-sub">{uni['city']} · Fee: PKR {uni['fee_per_year']:,} · Deadline: {uni['deadline']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button("🌐 Website", uni["website"])
    else:
        st.markdown('<div class="aw-info-box"><div style="color:#94a3b8;font-size:0.88rem;text-align:center;padding:12px 0;">No saved universities yet. Use the Predictor to find and save universities.</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        st.session_state.user = None
        st.success("Logged out successfully.")
        st.rerun()
else:
    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="you@example.com")
            password = st.text_input("🔑 Password", type="password", placeholder="••••••••")
            login_btn = st.form_submit_button("Sign In →", use_container_width=True, type="primary")
        if login_btn:
            if email and password:
                success, user_data, msg = login_user(email, password)
                if success:
                    st.session_state.user = user_data
                    st.success(f"Welcome back, {user_data['name']}! 🎉")
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please fill in both fields.")
        
        st.markdown('<div style="text-align:center;margin:18px 0;color:#94a3b8;font-size:0.85rem;">— OR —</div>', unsafe_allow_html=True)
        st.markdown('<div style="background:#f5f3ff;border:1px dashed #c4b5fd;border-radius:12px;padding:16px;text-align:center;margin-bottom:12px;"><div style="font-weight:800;color:#7c3aed;font-size:0.88rem;margin-bottom:4px;">⚡ Testing AdmitWise?</div><div style="font-size:0.78rem;color:#64748b;">Sign in instantly with a single click using our pre-configured demo account. No registration needed.</div></div>', unsafe_allow_html=True)
        if st.button("🔑 Quick Sign In as Guest", use_container_width=True, type="secondary"):
            email_guest = "guest@admitwise.edu"
            pw_guest = "password123"
            from utils.auth import _load_users
            users = _load_users()
            if email_guest not in users:
                register_user(email_guest, pw_guest, "Guest Student", "Lahore")
            success, user_data, msg = login_user(email_guest, pw_guest)
            if success:
                st.session_state.user = user_data
                st.success("Logged in successfully as Guest Student! 🎉")
                st.rerun()
            else:
                st.error("Error logging in: " + msg)


    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("register_form"):
            name = st.text_input("👤 Full Name", placeholder="Muhammad Ahmed")
            email_r = st.text_input("📧 Email Address", placeholder="you@example.com")
            city_r = st.selectbox("📍 Your City", [""] + PAKISTAN_CITIES)
            password_r = st.text_input("🔑 Password", type="password", help="At least 6 characters")
            confirm_pw = st.text_input("🔑 Confirm Password", type="password")
            register_btn = st.form_submit_button("Create Account →", use_container_width=True, type="primary")
        if register_btn:
            if password_r != confirm_pw:
                st.error("Passwords do not match.")
            elif not all([name, email_r, password_r]):
                st.warning("Please fill in all required fields.")
            else:
                success, msg = register_user(email_r, password_r, name, city_r)
                if success:
                    st.success(msg + " Please sign in now.")
                else:
                    st.error(msg)
