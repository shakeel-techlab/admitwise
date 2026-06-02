import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO

st.set_page_config(page_title="AI Advisor - AdmitWise", page_icon="🤖", layout="wide")
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
    st.markdown('<div class="aw-section-title">🤖 AI University Advisor</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:20px;margin-top:30px;">
        <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
        <div style="font-size:1.3rem;font-weight:800;color:#1e1b4b;margin-bottom:12px;">Login Required</div>
        <div style="color:#64748b;font-size:0.95rem;margin-bottom:24px;">Sign in to chat with our AI university counselor<br>for personalized admission guidance.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.page_link("pages/6_Login.py", label="👤 Sign In / Create Account →")
    st.stop()

st.markdown('<div class="aw-section-title">🤖 AI University Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Chat with our AI counselor — personalized guidance for your university journey</div>', unsafe_allow_html=True)

from utils.ai_chat import get_ai_response


quick_suggestions = [
    ("🎓 Best CS unis", "Which universities are best for Computer Science in Pakistan? Compare NUST, FAST, LUMS."),
    ("📊 Merit formula", "How is merit calculated at NUST and FAST? What entry test score do I need?"),
    ("💰 Scholarships", "What scholarships are available in Pakistan? I'm from a middle-income family."),
    ("📍 Karachi unis", "What are the best universities in Karachi for engineering and CS?"),
    ("⚖️ NUST vs LUMS", "Compare NUST and LUMS for Computer Science — fees, reputation, job placement."),
    ("🏥 Medical path", "What are the best medical universities in Pakistan? Tell me about AKU and entry tests."),
    ("📚 NET prep tips", "How do I prepare for the NUST NET entry test? Give me a study plan."),
    ("💸 Low fee unis", "Which good universities have the lowest fees? I need affordable options."),
]

st.markdown("**💬 Quick Questions — click to ask:**")
rows = [quick_suggestions[:4], quick_suggestions[4:]]
for row in rows:
    cols = st.columns(4)
    for col, (label, prompt) in zip(cols, row):
        if col.button(label, use_container_width=True):
            st.session_state.setdefault("chat_messages", [])
            st.session_state.pending_message = prompt

st.markdown("---")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

chat_container = st.container(height=440)
with chat_container:
    if not st.session_state.chat_messages:
        st.markdown("""
        <div class="chat-empty">
            <div style="font-size:2.5rem;margin-bottom:12px;">🎓</div>
            <div style="font-weight:700;color:#1e1b4b;font-size:1rem;margin-bottom:8px;">Assalam-o-Alaikum! I'm AdmitWise AI</div>
            <div>I know everything about Pakistani university admissions — entry tests, deadlines, scholarships, merit formulas, and more.<br>Ask me anything or use the quick buttons above!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div style="display:flex;justify-content:flex-end;"><div class="chat-user-msg">🧑‍🎓 {msg["content"]}</div></div>', unsafe_allow_html=True)
            else:
                content = msg["content"].replace("\n", "<br>")
                st.markdown(f'<div class="chat-bot-msg">🎓 {content}</div>', unsafe_allow_html=True)

if "pending_message" in st.session_state:
    user_input = st.session_state.pop("pending_message")
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    with st.spinner("AdmitWise AI is thinking..."):
        response = get_ai_response(st.session_state.chat_messages[:-1], user_input)
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    st.rerun()

prompt = st.chat_input("Ask about universities, admissions, scholarships, entry tests...")
if prompt:
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.spinner("AdmitWise AI is thinking..."):
        response = get_ai_response(st.session_state.chat_messages[:-1], prompt)
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    st.rerun()

if st.session_state.chat_messages:
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.chat_messages = []
        st.rerun()
