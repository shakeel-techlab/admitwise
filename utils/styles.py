"""Shared CSS styles for AdmitWise — clean white + purple design."""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800;900&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif !important;
}
.stApp {
    background: #fafaf9 !important;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1160px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e8e4ff !important;
}
[data-testid="stSidebar"] .stButton > button {
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    color: #475569 !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    transition: all 0.15s !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #f5f3ff !important;
    color: #7c3aed !important;
    transform: none !important;
}
[data-testid="stSidebar"] h2 {
    color: #7c3aed !important;
    font-weight: 800 !important;
}

/* ── Cards ── */
.aw-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 14px;
    transition: box-shadow 0.2s, border-color 0.2s;
    position: relative;
    overflow: hidden;
}
.aw-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #7c3aed, #9333ea);
    border-radius: 16px 0 0 16px;
}
.aw-card:hover {
    border-color: #c4b5fd;
    box-shadow: 0 4px 24px rgba(124,58,237,0.10);
}
.aw-card-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #1e1b4b;
    margin-bottom: 4px;
}
.aw-card-sub {
    font-size: 0.82rem;
    color: #64748b;
}

/* ── Probability Badges ── */
.badge-high {
    display: inline-block;
    background: #dcfce7; color: #166534;
    padding: 3px 12px; border-radius: 99px;
    font-size: 0.78rem; font-weight: 700;
    border: 1px solid #bbf7d0;
}
.badge-medium {
    display: inline-block;
    background: #fef9c3; color: #854d0e;
    padding: 3px 12px; border-radius: 99px;
    font-size: 0.78rem; font-weight: 700;
    border: 1px solid #fde68a;
}
.badge-low {
    display: inline-block;
    background: #fee2e2; color: #991b1b;
    padding: 3px 12px; border-radius: 99px;
    font-size: 0.78rem; font-weight: 700;
    border: 1px solid #fecaca;
}
.badge-vlow {
    display: inline-block;
    background: #f1f5f9; color: #475569;
    padding: 3px 12px; border-radius: 99px;
    font-size: 0.78rem; font-weight: 700;
    border: 1px solid #e2e8f0;
}

/* ── Tags / Pills ── */
.aw-tag {
    display: inline-block;
    background: #f5f3ff; color: #7c3aed;
    padding: 2px 10px; border-radius: 6px;
    font-size: 0.76rem; font-weight: 600;
    margin: 2px;
    border: 1px solid #ede9fe;
}

/* ── Section Headers ── */
.aw-section-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #1e1b4b;
    margin-bottom: 4px;
}
.aw-section-sub {
    font-size: 0.88rem;
    color: #64748b;
    margin-bottom: 20px;
}

/* ── Info Box ── */
.aw-info-box {
    background: #f5f3ff;
    border: 1px solid #ede9fe;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 12px;
}
.aw-info-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #7c3aed;
    font-weight: 700;
    margin-bottom: 3px;
}
.aw-info-value {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1e1b4b;
}

/* ── Stat Cards ── */
.aw-stat {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
}
.aw-stat-num {
    font-size: 2rem;
    font-weight: 900;
    color: #7c3aed;
    line-height: 1;
}
.aw-stat-label {
    font-size: 0.78rem;
    color: #64748b;
    font-weight: 600;
    margin-top: 4px;
}

/* ── Hero ── */
.aw-hero {
    background: linear-gradient(135deg, #f5f3ff 0%, #faf9ff 60%, #f0fdf4 100%);
    border: 1px solid #ede9fe;
    border-radius: 24px;
    padding: 56px 40px 48px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.aw-hero::after {
    content: '';
    position: absolute;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(124,58,237,0.06) 0%, transparent 70%);
    top: -100px; right: -100px;
    border-radius: 50%;
    pointer-events: none;
}
.aw-hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 99px;
    padding: 6px 18px;
    font-size: 13px;
    color: #475569;
    font-weight: 600;
    margin-bottom: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.aw-hero-dot { color: #22c55e; font-size: 10px; }
.aw-hero-title {
    font-size: 54px;
    font-weight: 900;
    line-height: 1.1;
    color: #0f172a;
    margin: 0 0 18px 0;
    letter-spacing: -1px;
}
.aw-hero-accent { color: #7c3aed; }
.aw-hero-sub {
    font-size: 17px;
    color: #64748b;
    max-width: 520px;
    margin: 0 auto 32px;
    line-height: 1.65;
    font-weight: 500;
}

/* ── Feature Cards ── */
.aw-feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 32px;
}
.aw-feature {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.aw-feature:hover {
    border-color: #c4b5fd;
    box-shadow: 0 4px 18px rgba(124,58,237,0.09);
}
.aw-feature-icon { font-size: 26px; margin-bottom: 10px; }
.aw-feature-title { font-size: 14px; font-weight: 800; color: #1e1b4b; margin-bottom: 5px; }
.aw-feature-desc { font-size: 12.5px; color: #64748b; line-height: 1.55; }

/* ── Deadline chip ── */
.chip-urgent { background:#fef2f2; color:#dc2626; border:1px solid #fecaca; border-radius:8px; padding:10px 14px; margin-bottom:8px; }
.chip-soon { background:#fffbeb; color:#b45309; border:1px solid #fde68a; border-radius:8px; padding:10px 14px; margin-bottom:8px; }
.chip-ok { background:#f0fdf4; color:#166534; border:1px solid #bbf7d0; border-radius:8px; padding:10px 14px; margin-bottom:8px; }
.chip-closed { background:#f1f5f9; color:#94a3b8; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; margin-bottom:8px; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed 0%, #9333ea 100%) !important;
    color: #fff !important;
    box-shadow: 0 3px 12px rgba(124,58,237,0.28) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 5px 20px rgba(124,58,237,0.38) !important;
    transform: translateY(-1px) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #9333ea) !important;
}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stSelectbox > div > div {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    background: #fff !important;
    font-family: 'Manrope', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.10) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #f5f3ff !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-family: 'Manrope', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: #7c3aed !important;
    color: #fff !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    color: #1e1b4b !important;
}
.streamlit-expanderContent {
    border: 1px solid #e2e8f0 !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* ── Metrics ── */
div[data-testid="stMetricValue"] {
    color: #7c3aed !important;
    font-weight: 800 !important;
    font-family: 'Manrope', sans-serif !important;
}

/* ── Forms ── */
.stForm {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 18px !important;
    padding: 24px !important;
}

/* ── Scholarship card ── */
.sch-card {
    background: #fafaf9;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    border-left: 3px solid #7c3aed;
}
.sch-name { font-weight: 800; color: #1e1b4b; font-size: 0.95rem; }
.sch-amount { font-size: 1.15rem; font-weight: 900; color: #7c3aed; margin: 4px 0; }
.sch-detail { font-size: 0.82rem; color: #64748b; line-height: 1.5; }

/* ── Chat ── */
.chat-user-msg {
    background: linear-gradient(135deg, #7c3aed, #9333ea);
    color: #fff;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    font-size: 0.9rem;
    max-width: 82%;
    margin-left: auto;
    line-height: 1.5;
}
.chat-bot-msg {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    color: #1e1b4b;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    font-size: 0.9rem;
    max-width: 88%;
    line-height: 1.6;
}
.chat-empty {
    text-align: center;
    padding: 40px;
    color: #94a3b8;
    font-size: 0.9rem;
}

/* ── Alert banner ── */
.aw-alert {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 12px 18px;
    color: #92400e;
    font-weight: 600;
    font-size: 0.88rem;
    margin-bottom: 16px;
}

/* ── Compare table ── */
.cmp-header {
    background: #f5f3ff;
    border-radius: 10px;
    padding: 14px 16px;
    font-weight: 800;
    color: #1e1b4b;
    margin-bottom: 4px;
}
.cmp-row {
    background: #ffffff;
    border: 1px solid #f1f5f9;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 4px;
}
.cmp-label {
    font-weight: 700;
    color: #475569;
    font-size: 0.85rem;
}

/* ── Location card ── */
.loc-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.loc-card:hover { border-color: #c4b5fd; }
.loc-dist-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #f5f3ff;
    color: #7c3aed;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 0.8rem;
    font-weight: 700;
}

hr { border-color: #e8e4ff !important; border-width: 1px !important; }
</style>
"""

SIDEBAR_LOGO = """
<div style="padding: 8px 4px 16px;">
    <div style="font-size:1.5rem;font-weight:900;color:#7c3aed;letter-spacing:-0.5px;">🎓 AdmitWise</div>
    <div style="font-size:0.75rem;color:#94a3b8;font-weight:600;margin-top:2px;">Pakistan University Portal</div>
</div>
"""
