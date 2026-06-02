import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from data.universities import UNIVERSITIES, FIELDS
from utils.styles import GLOBAL_CSS, SIDEBAR_LOGO

st.set_page_config(page_title="Guide & Resources - AdmitWise", page_icon="📚", layout="wide")
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
    st.markdown('<div class="aw-section-title">📚 Student Guide & Resources</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-radius:20px;margin-top:30px;">
        <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
        <div style="font-size:1.3rem;font-weight:800;color:#1e1b4b;margin-bottom:12px;">Login Required</div>
        <div style="color:#64748b;font-size:0.95rem;margin-bottom:24px;">Sign in to access student guides, entry test timetables, checklists, and the career quiz.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.page_link("pages/6_Login.py", label="👤 Sign In / Create Account →")
    st.stop()

st.markdown('<div class="aw-section-title">📚 Student Guide & Resources</div>', unsafe_allow_html=True)
st.markdown('<div class="aw-section-sub">Tools, guides, and resources designed to simplify your Pakistani university admission journey</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🎯 Career Advisor Quiz", "📝 Entry Test Study Guide", "📋 Application Checklist"])

# ── TAB 1: Career Advisor Quiz ──
with tab1:
    st.markdown("""
    ### 🧭 Find Your Perfect Career Path
    Unsure about which degree is right for you? Take this quick 5-question interest quiz to discover your recommended fields of study and see matching top Pakistani universities!
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("career_quiz_form"):
        q1 = st.radio(
            "1. What do you enjoy doing most in your free time?",
            [
                "💻 Building websites, writing simple scripts, or playing around with tech apps",
                "⚙️ Dismantling/fixing gadgets, understanding machinery, or designing physics models",
                "🔬 Reading about diseases, doing biology lab experiments, or helping sick family members",
                "📈 Analyzing stock markets, selling products online, or leading team projects",
                "✍️ Writing articles, debating social issues, or reading legal cases/policy books",
                "🔢 Solving complex puzzle games, logic problems, or math assignments"
            ]
        )
        
        q2 = st.radio(
            "2. Which subject in Intermediate/A-Levels did you find most engaging?",
            [
                "🖥️ Computer Science / Information Technology",
                "⚡ Physics or Applied Mathematics",
                "🧬 Biology or Organic Chemistry",
                "📊 Accounting, Economics, or Business Studies",
                "📖 English Literature, Civics, or Social Sciences",
                "📐 Pure Mathematics or Algebra"
            ]
        )
        
        q3 = st.radio(
            "3. Describe your ideal daily working environment:",
            [
                "🏠 Sitting at a comfortable desk, writing code, and enjoying flexible or remote work",
                "🏭 Working on site, in research labs, construction zones, or engineering plants",
                "🏥 Working in hospitals, sterile laboratory clinics, or patient wards",
                "🏢 Working in modern corporate boardrooms, managing assets, or marketing products",
                "🏛️ Working in courts, government departments, NGOs, or writing research papers",
                "🏫 Working in research facilities, teaching institutions, or analytical labs"
            ]
        )
        
        q4 = st.radio(
            "4. What is your ultimate career goal?",
            [
                "🚀 To build innovative software, lead a tech company, or work as an AI scientist",
                "🏗️ To build massive infrastructure, manufacture hardware, or design electrical grids",
                "🩺 To save lives, cure diseases, or conduct breakthrough medical research",
                "💼 To run a successful business, manage investment funds, or lead marketing operations",
                "⚖️ To advocate for citizens' rights, write public policy, or address social inequities",
                "📈 To analyze big data, solve mathematical theories, or model statistical forecasts"
            ]
        )
        
        q5 = st.radio(
            "5. Which skill do you consider your greatest strength?",
            [
                "🧠 Algorithmic thinking and writing logical step-by-step solutions",
                "🛠️ Spatial awareness, mechanical reasoning, and physical construction",
                "🩺 Patience, deep memory retention, and high empathy for others",
                "🗣️ Excellent communication, persuasion, and leadership qualities",
                "📜 Critical reading, reasoning, writing arguments, and social observation",
                "🔢 Fast mental arithmetic, logical derivation, and pattern spot-finding"
            ]
        )
        
        submit_quiz = st.form_submit_button("🔮 Predict My Career Path", use_container_width=True, type="primary")

    if submit_quiz:
        # Score calculation
        scores = {
            "Computer Science": 0,
            "Engineering": 0,
            "Medical": 0,
            "Business": 0,
            "Social Sciences": 0,
            "Law": 0,
            "Mathematics": 0
        }
        
        # Map selections
        mapping = {
            "💻": "Computer Science", "🖥️": "Computer Science", "🚀": "Computer Science",
            "⚙️": "Engineering", "⚡": "Engineering", "🏭": "Engineering", "🏗️": "Engineering", "🛠️": "Engineering",
            "🔬": "Medical", "🧬": "Medical", "🏥": "Medical", "🩺": "Medical",
            "📈": "Business", "📊": "Business", "🏢": "Business", "💼": "Business", "🗣️": "Business",
            "✍️": "Social Sciences", "📖": "Social Sciences", "🏛️": "Social Sciences", "⚖️": "Law", "📜": "Social Sciences",
            "🔢": "Mathematics", "📐": "Mathematics", "🏫": "Mathematics"
        }
        
        for q in [q1, q2, q3, q4, q5]:
            icon = q[0]
            field = mapping.get(icon)
            if field:
                scores[field] += 1
                
        # Find maximum score
        recommended_field = max(scores, key=scores.get)
        
        field_descriptions = {
            "Computer Science": "Focuses on programming, software engineering, artificial intelligence, cyber security, and data structures. Highly dynamic with high global and local job demand, flexible working conditions, and rapid startup potential.",
            "Engineering": "Applies mathematics and science to build infrastructure, machinery, chemical processes, and electrical grids. Ideal for logical minds interested in physical manufacturing and technical designs.",
            "Medical": "Centered on human health, biological research, medical practice (MBBS/BDS), and healthcare management. Requires immense dedication, deep memory skills, and a strong sense of service to humanity.",
            "Business": "Focuses on corporate management, finance, accounting, marketing, and entrepreneurship. Perfect for leaders with good communication skills, numerical abilities, and organizational strategy.",
            "Social Sciences": "Studies human society, social relationships, psychology, and public policy. Ideal for critical writers, researchers, educators, and social advocates.",
            "Law": "Covers legal advocacy, judicial processes, and corporate compliance. Recommended for strong speakers, critical readers, and individuals with high integrity.",
            "Mathematics": "Deals with abstract theories, numerical modeling, statistical analysis, and quantitative research. Great for analytical thinkers and data analysts."
        }
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); border: 1.5px solid #c4b5fd; border-radius: 18px; padding: 24px; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 8px;">🎯</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #1e1b4b;">Your Career Path Match: {recommended_field}</div>
            <div style="font-size: 0.92rem; color: #475569; max-width: 600px; margin: 12px auto; line-height: 1.6;">
                {field_descriptions[recommended_field]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### 🏫 Recommended Universities for {recommended_field}:")
        
        # Filter and rank universities for this field
        uni_matches = [u for u in UNIVERSITIES if recommended_field in u["fields"]]
        uni_matches.sort(key=lambda x: x["ranking"])
        
        cols = st.columns(3)
        for i, uni in enumerate(uni_matches[:6]):  # Display top 6
            with cols[i % 3]:
                st.markdown(f"""
                <div class="aw-card">
                    <div style="font-weight: 800; color: #7c3aed; font-size: 0.8rem; text-transform: uppercase;">RANK #{uni['ranking']}</div>
                    <div class="aw-card-title">{uni['name']}</div>
                    <div style="font-size: 0.82rem; color: #475569; margin: 4px 0;">{uni['full_name']}</div>
                    <div style="font-size: 0.76rem; color: #64748b;">📍 {uni['city']} · Entry Test: {uni['entry_test']}</div>
                    <div style="font-weight: 700; font-size: 0.8rem; color: #1e1b4b; margin-top: 8px;">Annual Fee: PKR {uni['fee_per_year']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                st.page_link("pages/2_Universities.py", label=f"View {uni['name']} Details →")
                st.markdown("<br>", unsafe_allow_html=True)


# ── TAB 2: Entry Test Study Guide ──
with tab2:
    st.markdown("""
    ### 📝 Pakistan University Entry Test Guides
    Securing admissions in Pakistan's top-tier universities depends heavily on entry test performances, which carry up to 50% of the total admission merit weightage.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    test_options = st.radio(
        "Select Entry Test Guide to Explore:",
        ["NUST NET (Engineering & CS)", "UET ECAT (Engineering)", "FAST NU Test / NAT", "Medical MDCAT"],
        horizontal=True
    )
    st.markdown("---")
    
    if test_options == "NUST NET (Engineering & CS)":
        st.markdown("""
        #### 🏛️ NUST Entrance Test (NET) Guide
        NET is computer-based (for Islamabad) or paper-based (for Karachi & Quetta) and is held in 4 series throughout the academic year.
        
        **📊 Subject Weightage Breakdown:**
        - 🧮 **Mathematics**: 40% (80 MCQs)
        - ⚡ **Physics**: 30% (60 MCQs)
        - 🧪 **Chemistry**: 15% (30 MCQs) (or Computer Science for CS students)
        - 🗣️ **English**: 10% (20 MCQs)
        - 🧠 **Intelligence**: 5% (10 MCQs)
        *Total: 200 Questions | Time: 3 hours | No Negative Marking!*
        
        **📚 Recommended Preparation Resources:**
        - Punjab Textbook Board (PTB) Math and Physics textbooks (XI & XII) - *Essential core concepts!*
        - KIPS Entry Test Series (Prep Books + Practice Books)
        - OET/Dogar Brothers NET Practice Booklets
        - Online portal tests (e.g., Step, Taleem360)
        
        **💡 Pro Prep Tips:**
        1. **Conceptual Grip**: Focus heavily on Physics derivations, formulas, and Math concepts (Integration, Derivations, Conic sections).
        2. **Time Management**: 200 MCQs in 180 minutes means less than a minute per question. Do not get stuck on tough physics calculations.
        3. **Series Strategy**: Try to take at least two NET series (e.g. NET-2 in March and NET-3 in June) to maximize your score. The highest score is accepted.
        """)
        
    elif test_options == "UET ECAT (Engineering)":
        st.markdown("""
        #### 🏗️ Punjab Engineering Common Admission Test (ECAT) Guide
        ECAT is a mandatory test conducted by UET Lahore for admission into public sector engineering programs in Punjab.
        
        **📊 Subject Weightage Breakdown:**
        - 🧮 **Mathematics**: 30% (30 MCQs)
        - ⚡ **Physics**: 30% (30 MCQs)
        - 🧪 **Chemistry / Computer**: 30% (30 MCQs)
        - 🗣️ **English**: 10% (10 MCQs)
        *Total: 100 Questions | Time: 100 minutes | Negative Marking: Yes! (-1 for wrong answers, +4 for correct).*
        
        **📚 Recommended Preparation Resources:**
        - Intermediate (FSc) textbooks of Punjab Textbook Board (PTB).
        - ECAT past papers collection (very helpful for identifying recurring patterns).
        - STEP/KIPS ECAT booklets.
        
        **💡 Pro Prep Tips:**
        1. **Avoid Guesswork**: Since there is negative marking, leave a question blank if you are completely unsure. Don't risk losing marks.
        2. **Math & Physics Dominance**: The core calculation sections constitute 60% of the paper. Memorize key formulas, trigonometric constants, and speed shortcuts.
        3. **Practice with Timers**: Solve past papers with a 100-minute countdown to train your brain under pressure.
        """)
        
    elif test_options == "FAST NU Test / NAT":
        st.markdown("""
        #### 🖥️ FAST-NUCES Entry Test & National Aptitude Test (NAT) Guide
        FAST accepts both its own NU Entrance Test and NTS NAT. However, the NU Test is highly recommended as FAST allocates a major portion of seats to it.
        
        **📊 FAST NU Test Pattern (Computing):**
        - 🧠 **Basic Math**: 20%
        - 🧮 **Advanced Math**: 50%
        - 📝 **Analytical Reasoning & IQ**: 20%
        - 🗣️ **English**: 10%
        *Negative marking is applied on the NU Test!*
        
        **📚 Recommended Preparation Resources:**
        - FSc Mathematics textbooks (specifically Calculus, Functions, Matrices, Trigonometry).
        - Dogar NAT-IE/IM Prep Books for Analytical Reasoning.
        - FAST NU entry test past sample questions.
        
        **💡 Pro Prep Tips:**
        1. **Master Analytical Reasoning**: Learn the strategies for solving logic grids and coding-decoding puzzles quickly to secure easy points.
        2. **FSc Math Focus**: High proficiency in FSc Algebra, Trigonometry, and Calculus is necessary for the Advanced Math section.
        3. **Speed is Key**: The test is fast-paced. Do not spend too much time on complex calculus integrations during the first pass.
        """)
        
    elif test_options == "Medical MDCAT":
        st.markdown("""
        #### 🩺 Medical & Dental College Admission Test (MDCAT) Guide
        MDCAT is a highly competitive, standardized national test mandatory for getting into MBBS and BDS programs in public and private medical colleges in Pakistan.
        
        **📊 Subject Weightage Breakdown:**
        - 🧬 **Biology**: 34% (68 MCQs)
        - 🧪 **Chemistry**: 27% (54 MCQs)
        - ⚡ **Physics**: 27% (54 MCQs)
        - 🗣️ **English**: 9% (18 MCQs)
        - 🧠 **Logical Reasoning**: 3% (6 MCQs)
        *Total: 200 Questions | Time: 3.5 hours | No Negative Marking!*
        
        **📚 Recommended Preparation Resources:**
        - Provincial Textbooks (Punjab, Sindh, KPK depending on your domicile). PMDC syllabus is federal, so consult Federal Board books too.
        - Redspot A-Level Biology and Chemistry MCQs.
        - MDCAT Past Papers (National and Provincial).
        
        **💡 Pro Prep Tips:**
        1. **Line-by-Line Textbook Reading**: Biology questions are often lifted word-for-word directly from provincial textbooks. Highlight important facts and lines.
        2. **Physics Simplification**: Medical students often struggle with physics calculations. Focus on formulas, units, ratios, and basic arithmetic shortcuts (no calculators allowed!).
        3. **Syllabus Alignment**: Prepare strictly according to the syllabus officially released by PMDC/Provincial admitting universities (like UHS, KMU, DUHS).
        """)


# ── TAB 3: Application Checklist ──
with tab3:
    st.markdown("""
    ### 📋 Application Documents Checklist
    Don't let missing paperwork delay your application! Check off these essential documents as you prepare them. Your checklist progress is saved during your session.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize checklist in session state
    checklist_items = {
        "doc_matric": "🎓 Matriculation (SSC) Marks Sheet / Transcript",
        "doc_matric_cert": "📜 Matriculation Certificate (Sanad)",
        "doc_fsc": "📚 FSc Part 1 Marks Sheet (or A-Level equivalents)",
        "doc_cnic": "💳 CNIC (or B-Form if under 18)",
        "doc_f_cnic": "👨 Father/Guardian's CNIC Copy",
        "doc_domicile": "📍 Domicile Certificate (essential for provincial/public quotas)",
        "doc_photos": "📷 8x Passport-Sized Photographs (with blue background)",
        "doc_test": "🎫 Entry Test Admit Card / Result Sheet (NET/ECAT/NAT/MDCAT)",
        "doc_challan": "🏦 Paid Bank Application Challan Copy",
        "doc_character": "🏫 Character Certificate from last attended institution"
    }
    
    if "checklist_state" not in st.session_state:
        st.session_state.checklist_state = {k: False for k in checklist_items}
        
    # Layout checklist and progress
    total_docs = len(checklist_items)
    checked_docs = sum(1 for v in st.session_state.checklist_state.values() if v)
    percentage = int((checked_docs / total_docs) * 100) if total_docs > 0 else 0
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("#### 📁 Mark Prepared Documents:")
        for key, label in checklist_items.items():
            st.session_state.checklist_state[key] = st.checkbox(
                label,
                value=st.session_state.checklist_state[key],
                key=f"chk_{key}"
            )
            
    with c2:
        st.markdown("#### 📊 Preparation Progress")
        st.markdown(f"**{checked_docs} of {total_docs}** documents ready.")
        st.progress(percentage / 100.0, text=f"**{percentage}% Complete**")
        
        if percentage == 100:
            st.balloons()
            st.success("🎉 Excellent! All documents are ready. You are fully prepared to submit your applications!")
        elif percentage >= 70:
            st.info("👍 You have gathered almost all key documents. Just a few more to go!")
        elif percentage >= 30:
            st.warning("⚡ Good start, but make sure to prepare the remaining documents before the university deadline!")
        else:
            st.caption("ℹ️ Click the checkboxes on the left as you photocopy, attest, and organize each document.")
            
        st.markdown("""
        <div style="background:#fafaf9;border:1px solid #e2e8f0;border-radius:12px;padding:14px;margin-top:16px;">
            <div style="font-weight:700;color:#1e1b4b;font-size:0.8rem;text-transform:uppercase;margin-bottom:6px;">⚠️ Important Reminder:</div>
            <div style="font-size:0.75rem;color:#64748b;line-height:1.5;">
                Most public universities require photocopies of transcripts, CNICs, and domicile certificates to be <strong>attested</strong> by a Grade 17+ government officer before submission. Keep at least 4 sets of attested copies ready!
            </div>
        </div>
        """, unsafe_allow_html=True)
