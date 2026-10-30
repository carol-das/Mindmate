import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Add src folder to python path 
sys.path.append(os.path.abspath("src"))

from inference import chat_with_mindmate
from safety_guard import check_input_safety
from summary_engine import generate_pre_session_summary
from memory_vault import log_mood, get_mood_history, purge_vault 
from therapist_match import (
    find_therapist_matches, 
    EXTERNAL_RESOURCES, 
    CLINICIAN_DIRECTORY,
    generate_first_contact_email,
    recommend_clinician_for_expression
)
from anxiety_engine import (
    ANXIETY_PROFILES, 
    RESEARCH_LIBRARY, 
    search_research_by_query
)

# Page configuration
st.set_page_config( 
    page_title="MindMate — The Living Gallery of the Mind & Therapy Bridge",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Museum-Grade Art Gallery CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #FAF7F2 !important;
    background: radial-gradient(circle at 15% 15%, #FFFDF9 0%, #FAF6F0 50%, #F4EFE6 100%) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #26382F !important;
}

h1, h2, h3, .brand-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #173827 !important;
    font-weight: 700 !important;
}

/* Header & Artwork Banner */
.museum-entry-banner {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 22px 28px;
    margin-bottom: 14px;
    border: 1px solid #E6DED2;
    box-shadow: 0 4px 20px rgba(40, 56, 46, 0.03);
}

.museum-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #153826;
    line-height: 1.1;
    margin: 0 0 4px 0;
}

.gallery-subhead {
    font-size: 1rem;
    color: #4A6354;
    line-height: 1.5;
    margin-bottom: 10px;
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

.gallery-badge {
    background: #EBF2EC;
    color: #19432E;
    border: 1px solid #CFE0D3;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.gallery-badge-terracotta {
    background: #FBF0EB;
    color: #92452A;
    border-color: #EFCDBE;
}

.gallery-badge-lavender {
    background: #F2EFF8;
    color: #4D416D;
    border-color: #DAD1EC;
}

/* Permission Notice Card */
.permission-box {
    background: linear-gradient(135deg, #FBF8F2 0%, #F5EFE7 50%, #EBF4EE 100%);
    border-radius: 14px;
    border: 1px solid #DCD2C3;
    border-left: 5px solid #C86D51;
    padding: 12px 18px;
    margin-bottom: 12px;
}

.permission-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.05rem;
    color: #8C4023;
    font-weight: 700;
    margin-bottom: 2px;
}

.permission-body {
    font-size: 0.88rem;
    color: #385143;
    line-height: 1.45;
}

/* Visual Artwork Frame Cards */
.art-exhibit-card {
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #E6DED2;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.02);
    text-align: center;
}

.art-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #173827;
    margin: 8px 0 3px 0;
}

.art-caption {
    font-size: 0.84rem;
    color: #556E61;
    line-height: 1.45;
}

/* In-Chat Plaque Styles */
.gallery-plaque {
    background: #FAF8F4;
    border: 1px solid #E5DDD0;
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 10px;
    border-left: 4px solid #736B86;
}

.plaque-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #2D273B;
}

.clinician-rec-block {
    background: linear-gradient(135deg, #F9FAF7 0%, #EEF4F0 100%);
    border: 1px solid #D3E2D8;
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 10px;
    border-left: 4px solid #2B533E;
}

/* Warm Human Letter Box (Zero Code Snippet) */
.human-letter-box {
    background: #FFFFFF;
    border: 1px solid #E2D9CC;
    border-radius: 12px;
    padding: 18px 20px;
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.92rem;
    color: #243E30;
    line-height: 1.6;
    margin-bottom: 8px;
    white-space: pre-wrap;
}

/* Chat & Interactive Elements */
[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid #EAE3D6 !important;
    padding: 14px 20px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}

.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: 1px solid #D8D0C3 !important;
    background: #FFFFFF !important;
    color: #213D2D !important;
    padding: 6px 14px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    border-color: #2B533E !important;
    color: #2B533E !important;
    background: #F7FAF8 !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="primary"] {
    background: #234B36 !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 3px 10px rgba(35, 75, 54, 0.2) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #EDE6DA;
    padding: 6px;
    border-radius: 30px;
    border: 1px solid #DFD5C5;
    margin-bottom: 18px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 20px !important;
    padding: 6px 16px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: #556D60 !important;
    background-color: transparent !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #173826 !important;
    box-shadow: 0 2px 8px rgba(23, 56, 38, 0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# Curated comforting quotes
COMFORT_QUOTES = [
    {
        "quote": "When someone really hears you without passing judgment, it feels remarkably freeing. The curious paradox is that when I accept myself just as I am, then I can change.",
        "author": "Carl Rogers",
        "tag": "Self-Acceptance"
    },
    {
        "quote": "You can't get through pain by diminishing it. You get through it by accepting it and figuring out what to do with it.",
        "author": "Lori Gottlieb",
        "tag": "Emotional Honesty"
    },
    {
        "quote": "Owning our story and loving ourselves through that process is the bravest thing we will ever do.",
        "author": "Dr. Brené Brown",
        "tag": "Courage"
    },
    {
        "quote": "Therapy is not for broken people. It is for people brave enough to stop passing unhealed wounds onto the ones they love.",
        "author": "Dr. Ramani Durvasula",
        "tag": "The Ripple Effect"
    },
    {
        "quote": "When you love someone, the best thing you can offer is your presence. Emotional regulation allows you to show up with an open, steady heart.",
        "author": "Thich Nhat Hanh",
        "tag": "Presence"
    }
]

if "quote_index" not in st.session_state:
    st.session_state.quote_index = 0

current_q = COMFORT_QUOTES[st.session_state.quote_index % len(COMFORT_QUOTES)]

# ==================== ARTWORKS (CLEAN SVGS WITH ZERO CODE LEAK) ====================
# The Sanctuary Arch & Dawn Wave (From user's screenshot)
SVG_SANCTUARY_ARCH = """<svg viewBox="0 0 850 130" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-height:120px; display:block; margin:auto;">
<defs>
<linearGradient id="waveG" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#C86D51" stop-opacity="0.45"/>
<stop offset="50%" stop-color="#736B86" stop-opacity="0.35"/>
<stop offset="100%" stop-color="#2C523B" stop-opacity="0.45"/>
</linearGradient>
<linearGradient id="sunG" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#F2DFCA"/>
<stop offset="100%" stop-color="#D9A873"/>
</linearGradient>
</defs>
<path d="M425 15 C460 15 485 40 485 75 L485 115 L365 115 L365 75 C365 40 390 15 425 15 Z" stroke="#2C523B" stroke-width="1.6" stroke-dasharray="4 3" fill="none"/>
<circle cx="425" cy="48" r="15" fill="url(#sunG)" opacity="0.8"/>
<path d="M20 100 C 130 55, 210 120, 350 78 C 420 55, 510 115, 630 68 C 700 40, 780 92, 830 78" stroke="url(#waveG)" stroke-width="2.6" stroke-linecap="round" fill="none"/>
<path d="M10 112 C 150 75, 260 130, 370 85 C 470 45, 570 105, 700 75 C 760 58, 800 98, 840 92" stroke="#4A755D" stroke-width="1.2" stroke-opacity="0.35" stroke-linecap="round" fill="none"/>
<circle cx="210" cy="120" r="4" fill="#C86D51"/>
<circle cx="630" cy="68" r="4" fill="#2C523B"/>
<circle cx="700" cy="40" r="3" fill="#736B86"/>
</svg>"""

# Artwork 2: Interconnected Co-Regulation Rings (Relational Ripple)
SVG_RIPPLE_ART = """<svg viewBox="0 0 260 110" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-height:100px; display:block; margin:auto;">
<circle cx="95" cy="55" r="38" stroke="#2C523B" stroke-width="1.5" stroke-opacity="0.6"/>
<circle cx="165" cy="55" r="38" stroke="#C86D51" stroke-width="1.5" stroke-opacity="0.6"/>
<path d="M130 25 C142 40 142 70 130 85 C118 70 118 40 130 25 Z" fill="#E8F1EC" opacity="0.75"/>
<circle cx="130" cy="55" r="5" fill="#736B86"/>
</svg>"""

# Artwork 3: Minimalist Botanical Leaf (Gentle Healing)
SVG_BOTANICAL_ART = """<svg viewBox="0 0 260 110" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-height:100px; display:block; margin:auto;">
<path d="M130 95 C130 65 110 35 155 15 C135 45 155 70 130 95 Z" fill="#EAF3ED" stroke="#2C523B" stroke-width="1.5"/>
<path d="M130 95 C130 75 125 55 105 40 C115 60 120 78 130 95 Z" fill="#F8EFEB" stroke="#C86D51" stroke-width="1.2"/>
<circle cx="155" cy="15" r="3" fill="#2C523B"/>
</svg>"""

# Artwork 4: Zen Balance Stones (Grounding & Stillness)
SVG_STONES_ART = """<svg viewBox="0 0 260 110" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-height:100px; display:block; margin:auto;">
<ellipse cx="130" cy="85" rx="42" ry="14" fill="#EFE8DE" stroke="#8C5438" stroke-width="1.3"/>
<ellipse cx="130" cy="58" rx="30" ry="11" fill="#E8F0EA" stroke="#2C523B" stroke-width="1.3"/>
<ellipse cx="130" cy="36" rx="18" ry="8" fill="#F0ECF6" stroke="#736B86" stroke-width="1.3"/>
<circle cx="130" cy="20" r="4" fill="#D9A873"/>
</svg>"""

# ================================================================
# SECTION 1: TOP HERO BANNER & CHATBOT (FIRST THING VISIBLE)
# ================================================================
top_banner_html = f"""<div class="museum-entry-banner">
<div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 0.92rem; font-style: italic; color: #8C5438; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 2px;">
Pavilion of Well-Being • Exhibition of the Human Mind
</div>
<div class="museum-title">🏛️ MindMate</div>
<div class="gallery-subhead">
A tranquil space to unpack what you feel. Express a thought or tap a sensation below to match with a human specialist.
</div>
<div style="margin: 8px 0;">{SVG_SANCTUARY_ARCH}</div>
<div class="badge-row">
<span class="gallery-badge">🔒 100% On-Device & Private</span>
<span class="gallery-badge gallery-badge-terracotta">🎨 Therapy is Normal & Human</span>
<span class="gallery-badge gallery-badge-lavender">📚 Grounded in Science</span>
</div>
</div>"""

st.markdown(top_banner_html, unsafe_allow_html=True)

# Compact Permission Reassurance Notice
permission_html = """<div class="permission-box">
<div class="permission-title">🌿 Take your time — You never have to force an opening up</div>
<div class="permission-body">
You don't need to tell a long story today. Just tap what you feel in this moment, and MindMate will understand your state and recommend the right clinician.
</div>
</div>"""
st.markdown(permission_html, unsafe_allow_html=True)

# Single-Touch Sensation & Feeling Chips
st.markdown("<p style='font-weight: 600; font-size: 0.86rem; color: #2B4E3A; margin-bottom: 6px;'>💡 Single-touch expression chips (click any to begin):</p>", unsafe_allow_html=True)

c_p1, c_p2, c_p3 = st.columns(3)
selected_prompt = None

if c_p1.button("🫀 Chest tight & racing", use_container_width=True):
    selected_prompt = "My chest feels tight and heart is racing, I feel high somatic panic."
if c_p2.button("🤐 I don't want to open up", use_container_width=True):
    selected_prompt = "I don't really want to open up or talk about this right now, it feels like too much."
if c_p3.button("🌊 Stuck in worry loops", use_container_width=True):
    selected_prompt = "My mind is stuck in restless 'what-if' loops and chronic anticipatory worry."

c_p4, c_p5, c_p6 = st.columns(3)
if c_p4.button("💔 Stress affecting loved ones", use_container_width=True):
    selected_prompt = "I've noticed my stress is leaking into how I interact with my partner and family."
if c_p5.button("⚡ Burnt out & depleted", use_container_width=True):
    selected_prompt = "I am completely depleted from work deadlines and chronic burnout."
if c_p6.button("🌱 Ready for therapy (Find near me)", use_container_width=True):
    selected_prompt = "I think I am ready to take the step into therapy; can you help me find a therapist near me?"

st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

# ----------------- CHATBOT SUITE (ON TOP) -----------------
col_chat, col_summary = st.columns([3, 2], gap="large")

with col_chat:
    st.markdown("### 💬 Reflection Space")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Welcome to your quiet reflection gallery. 🌿 "
                    "You are in complete control here. Whether you share a physical feeling, a relationship stress, "
                    "or state that you don't feel like talking—you are welcome. What is present in you today?"
                )
            }
        ]

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            avatar = "🌿" if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"], unsafe_allow_html=True)

    prompt_input = st.chat_input("Tell us what you feel in this moment...")
    user_text = selected_prompt or prompt_input

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_text)

        safety_check = check_input_safety(user_text)
        if not safety_check["is_safe"]:
            response = safety_check["response"]
        else:
            with st.spinner("Reflecting with care..."):
                response = chat_with_mindmate(user_text)

        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col_summary:
    st.markdown("### 📋 Intake Companion")
    st.caption("Synthesizes your dialogue into a clear 3-part sheet for your therapist consultation.")

    user_has_spoken = any(m["role"] == "user" for m in st.session_state.get("messages", []))
    
    if st.button("✨ Synthesize Clinical Intake Sheet", use_container_width=True, type="primary"):
        if user_has_spoken:
            with st.spinner("Synthesizing your insights..."):
                summary_output = generate_pre_session_summary(st.session_state.messages)
                st.session_state["current_summary"] = summary_output
        else:
            st.warning("Please tap a chip or type a reflection first!")
            
    if "current_summary" in st.session_state:
        st.markdown(st.session_state["current_summary"])
        st.download_button(
            label="📥 Download Intake Sheet",
            data=st.session_state["current_summary"],
            file_name=f"mindmate_intake_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Warm Human Outreach Message (Zero Code Snippet)
    user_msgs = [m["content"] for m in st.session_state.get("messages", []) if m["role"] == "user"]
    if user_msgs:
        latest_msg = user_msgs[-1]
        rec_match = recommend_clinician_for_expression(latest_msg)
        matched_doc = rec_match["clinician"]
        
        with st.expander(f"✉️ **Draft Message for {matched_doc['name']}**"):
            st.caption(f"Ready to send directly to {matched_doc['name']}:")
            quick_draft = generate_first_contact_email(matched_doc["name"], matched_doc["specialties"][0], "A prospective client")
            
            st.markdown(f"""<div class="human-letter-box">{quick_draft}</div>""", unsafe_allow_html=True)
            st.caption(f"Clinician email: **{matched_doc['contact']}**")
        
    st.divider()
    if st.button("🔄 Clear Reflection Conversation", use_container_width=True):
        st.session_state.messages = []
        if "current_summary" in st.session_state:
            del st.session_state["current_summary"]
        st.rerun()

# ================================================================
# SECTION 2: FOR THE CURIOUS MIND — SCIENCE, VAULT & CLINICIANS (DOWN BELOW)
# ================================================================
st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, #F8F4EC 0%, #EFE8DC 100%); border-radius: 18px; border: 1px solid #D8CFC0; padding: 20px 26px; margin-bottom: 20px;">
    <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-size: 0.95rem; font-style: italic; color: #8A4F35; letter-spacing: 0.1em; text-transform: uppercase;">
        For the Inquiring Mind
    </div>
    <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.65rem; font-weight: 700; color: #153826; margin: 3px 0 6px 0;">
        🖼️ Visual Gallery, Research Literature & Private Vault
    </div>
    <div style="font-size: 0.9rem; color: #3C5547; line-height: 1.55;">
        Explore research papers matching your feelings, manage your private mood vault, and view our verified clinicians.
    </div>
</div>
""", unsafe_allow_html=True)

# Separate Tabs: Visual Gallery, Research Chatbox/Library, Mood Vault & Delivery, Clinicians
gallery_tab1, gallery_tab2, gallery_tab3, gallery_tab4 = st.tabs([
    "🖼️ Visual Artworks & Relational Ripple",
    "📚 Research Literature & Paper Finder Chatbot",
    "🔒 Sensitive Cubicle Mood Vault & Doctor Delivery",
    "🩺 Verified Clinicians & Outreach Directory"
])

# ----------------- TAB 1: VISUAL ARTWORKS -----------------
with gallery_tab1:
    st.markdown("### 🖼️ The Visual Gallery of Connection")
    st.caption("Artworks depicting the courage to heal and the ripple effect on those we cherish.")
    
    a_col1, a_col2, a_col3 = st.columns(3)
    
    with a_col1:
        st.markdown(f"""
        <div class="art-exhibit-card">
            {SVG_RIPPLE_ART}
            <div class="art-title">The Relational Ripple</div>
            <div class="art-caption">
                Our emotions touch our partners and children. Healing yourself brings calm co-regulation to everyone you love.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with a_col2:
        st.markdown(f"""
        <div class="art-exhibit-card">
            {SVG_BOTANICAL_ART}
            <div class="art-title">The Unfolding Bloom</div>
            <div class="art-caption">
                Therapy is mental hygiene. Unpacking heavy thoughts allows natural resilience and vitality to return.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with a_col3:
        st.markdown(f"""
        <div class="art-exhibit-card">
            {SVG_STONES_ART}
            <div class="art-title">The Balanced Harbor</div>
            <div class="art-caption">
                Emotional regulation is not holding tension; it is learning to release weights that were never yours to carry.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Comforting quote
    st.markdown(f"""
    <div style="background: #FFF; border-radius: 14px; border: 1px solid #E6DED2; border-left: 4px solid #234B36; padding: 16px 22px; margin-top: 10px;">
        <div style="font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 1.1rem; color: #173826; line-height: 1.6;">
            "{current_q['quote']}"
        </div>
        <div style="font-size: 0.85rem; font-weight: 700; color: #587566; text-transform: uppercase; margin-top: 6px;">
            ✦ {current_q['author']} — <em>{current_q['tag']}</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 2: RESEARCH CHATBOX & PAPER FINDER -----------------
with gallery_tab2:
    st.markdown("### 📚 Research Paper Finder & Science Library")
    st.caption("Tell us what you are experiencing, and we will find the peer-reviewed psychological research papers that explain it.")

    # Interactive Research Chatbox / Query Box
    st.markdown("<p style='font-weight: 600; font-size: 0.9rem; color: #1C3B2B; margin-bottom: 4px;'>💬 Express what you feel to find matching papers:</p>", unsafe_allow_html=True)
    
    # Quick topic chip buttons
    rc_col1, rc_col2, rc_col3 = st.columns(3)
    quick_research_topic = None
    if rc_col1.button("🫀 Panic & Racing Heartbeat", use_container_width=True):
        quick_research_topic = "My heart is racing and I feel sudden somatic panic."
    if rc_col2.button("🌊 Chronic Worry & What-Ifs", use_container_width=True):
        quick_research_topic = "I can't stop overthinking and worrying about worst-case scenarios."
    if rc_col3.button("💔 Relationship Conflict & Attachment", use_container_width=True):
        quick_research_topic = "My partner and I keep having emotional fights and feeling distant."

    rc_col4, rc_col5, rc_col6 = st.columns(3)
    if rc_col4.button("⚡ Work Burnout & Exhaustion", use_container_width=True):
        quick_research_topic = "I am deeply exhausted from high work pressure and burnout."
    if rc_col5.button("🪞 Fear of Social Judgment", use_container_width=True):
        quick_research_topic = "I fear being judged or scrutinized by other people."
    if rc_col6.button("🛡️ Hesitation & Self-Protection", use_container_width=True):
        quick_research_topic = "I feel guarded and hesitant about being vulnerable."

    research_input = st.text_input(
        "Or type any feeling, author, or keyword (e.g., 'Polyvagal theory', 'CBT for anxiety', 'Chest tightness'):", 
        value=quick_research_topic if quick_research_topic else "",
        placeholder="Type here..."
    )

    if research_input:
        search_res = search_research_by_query(research_input)
        profile = search_res["profile"]
        papers = search_res["papers"]

        st.markdown(f"""
        <div style="background: #FFFFFF; border-radius: 14px; border: 1px solid #D6DFD9; border-left: 5px solid #2C523B; padding: 18px 22px; margin: 14px 0;">
            <div style="font-size: 1.25rem; font-weight: 700; color: #173827; margin-bottom: 4px;">
                {profile['icon']} Identified Phenotype: {profile['label']}
            </div>
            <div style="font-size: 0.88rem; color: #4B6355; margin-bottom: 8px;">
                <strong>Nervous System State:</strong> <span style="background: #EAF2EC; padding: 2px 8px; border-radius: 6px; font-weight: 600; color: #1D4330;">{profile['nervous_system_state']}</span>
            </div>
            <p style="font-size: 0.9rem; color: #385143; line-height: 1.5; margin-bottom: 10px;">
                {profile['description']}
            </p>
            <div style="font-size: 0.88rem; font-weight: 700; color: #8C4023; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
                📄 Matched Peer-Reviewed Literature ({len(papers)} Papers Found):
            </div>
        </div>
        """, unsafe_allow_html=True)

        for p in papers:
            with st.expander(f"📖 {p['title']} ({p['year']})"):
                st.write(f"**Authors:** {p['authors']}")
                st.write(f"**Journal:** *{p['journal']}*")
                st.write(f"**Why this explains your feeling:** {p['key_finding']}")
                st.markdown(f"🔗 **[Read on DOI / Academic Publisher]({p['doi']})**")

    st.divider()
    st.markdown("#### 📖 Browse All 6 Anxiety & Well-Being Phenotypes")
    phenotype_keys = list(ANXIETY_PROFILES.keys())
    lib_col1, lib_col2 = st.columns(2)
    
    for idx, p_key in enumerate(phenotype_keys):
        p_data = ANXIETY_PROFILES[p_key]
        papers = RESEARCH_LIBRARY[p_key]
        col = lib_col1 if idx % 2 == 0 else lib_col2
        
        with col:
            st.markdown(f"""
            <div style="background:#FFF; border-radius:14px; border:1px solid #E6DED2; padding:16px 20px; margin-bottom:12px;">
                <div style="font-size: 1.3rem;">{p_data['icon']}</div>
                <div style="font-family:'Playfair Display', serif; font-size:1.1rem; font-weight:700; color:#173827;">
                    {p_data['aesthetic_title']}
                </div>
                <div style="font-size:0.8rem; color:#8A4F35; font-weight:600; margin-bottom:6px;">{p_data['label']}</div>
                <p style="font-size:0.86rem; color:#354E41; line-height:1.45; margin-bottom:6px;">{p_data['description']}</p>
                <div style="font-size:0.78rem; font-weight:700; color:#625776; text-transform:uppercase;">Attached Research:</div>
            </div>
            """, unsafe_allow_html=True)
            
            for doc in papers:
                with st.expander(f"📄 {doc['title']} ({doc['year']})"):
                    st.write(f"**Authors:** {doc['authors']}")
                    st.write(f"**Key Finding:** {doc['key_finding']}")
                    st.markdown(f"🔗 **[View Study]({doc['doi']})**")

# ----------------- TAB 3: MOOD VAULT & DOCTOR DELIVERY (BESIDE EACH OTHER) -----------------
with gallery_tab3:
    st.markdown("### 🔒 Sensitive Cubicle Mood Vault & Doctor Delivery Pipeline")
    st.caption("Your mood logs remain strictly on your local device. You retain full data sovereignty.")

    v_col1, v_col2 = st.columns([1, 1], gap="large")
    
    with v_col1:
        st.markdown("#### 🧭 Daily Emotional Check-In")
        st.caption("Record your mood and personal reflections:")
        
        mood_score = st.select_slider(
            "Select your current balance:",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: {
                1: "1 • 😖 Heavily Overwhelmed",
                2: "2 • 😟 Restless & Anxious",
                3: "3 • 😐 Grounded & Steady",
                4: "4 • 🙂 Reflective & Hopeful",
                5: "5 • 🌿 Centered & Peaceful"
            }[x]
        )

        mood_notes_map = {
            1: "🚨 **Heavy Weight:** Be gentle with yourself today.",
            2: "🌊 **Restless Currents:** Mind or body feels uneasy.",
            3: "⚓ **Steady Harbor:** Observing thoughts without overwhelm.",
            4: "🌱 **Gentle Light:** Open to insights and growth.",
            5: "✨ **Deep Peace:** Grounded and centered."
        }
        st.info(mood_notes_map[mood_score])

        # Sensation / Feeling Tags
        st.markdown("**What subtle feeling describes your day?**")
        tag_cols = st.columns(4)
        selected_tags = []
        tags = ["Exhausted", "Vulnerable", "Restless", "Hopeful", "Grateful", "Guarded", "Grounded", "Tender"]
        for idx, tag in enumerate(tags):
            col = tag_cols[idx % 4]
            if col.checkbox(tag, key=f"v_tag_{tag}"):
                selected_tags.append(tag)

        mood_note = st.text_area("Personal reflection note (optional):", placeholder="Noticed feelings that arose during the day...")
        
        if st.button("💾 Save Entry to Private Vault", use_container_width=True, type="primary"):
            full_note = mood_note
            if selected_tags:
                tag_str = " | Tags: " + ", ".join(selected_tags)
                full_note = (full_note + tag_str) if full_note else tag_str
            log_mood(mood_score, full_note)
            st.success("Entry saved safely in your encrypted local database.")
            st.rerun()

    with v_col2:
        st.markdown("#### 📊 Local Reflection Logs")
        st.caption("Your historical records stored in `data/mindmate_vault.db`:")
        
        history = get_mood_history()
        if history:
            total_entries = len(history)
            scores = [row[1] for row in history]
            avg_score = sum(scores) / len(scores)

            m1, m2 = st.columns(2)
            m1.metric("Total Check-ins", f"{total_entries} sessions")
            m2.metric("Average Balance", f"{avg_score:.1f} / 5.0")

            df = pd.DataFrame(history, columns=["Timestamp", "Score (1-5)", "Note"])
            st.dataframe(df, use_container_width=True, height=240)
        else:
            st.write("🌿 No entries recorded yet. Record your first check-in on the left!")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("**🛡️ Data Sovereignty Zone**")
        if st.button("🗑️ Permanently Erase All Vault History", type="secondary", use_container_width=True):
            purge_vault()
            st.warning("All records wiped permanently.")
            st.rerun()

    st.divider()

    # How Summaries Reach Doctor (Positioned Beside & Grouped with the Vault)
    st.markdown("### 🚚 How Your Summaries Actually Reach Your Doctor")
    st.caption("Because your data is private, nothing is sent automatically. You decide if, when, and how your clinician receives it.")

    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 10px;">
        <div style="background: #FFF; border-radius: 14px; border: 1px solid #E6DFD4; padding: 16px 18px;">
            <div style="font-size: 1.8rem; color: #C86D51; font-weight: 700;">01</div>
            <strong style="color: #173826;">Local Synthesis</strong>
            <p style="font-size: 0.85rem; color: #4B6356; margin-top: 4px;">Runs 100% on your device. No data is sent to cloud data brokers.</p>
        </div>
        <div style="background: #FFF; border-radius: 14px; border: 1px solid #E6DFD4; padding: 16px 18px;">
            <div style="font-size: 1.8rem; color: #8C4023; font-weight: 700;">02</div>
            <strong style="color: #173826;">You Hold the Key</strong>
            <p style="font-size: 0.85rem; color: #4B6356; margin-top: 4px;">Nothing is shared until you explicitly download or email it.</p>
        </div>
        <div style="background: #FFF; border-radius: 14px; border: 1px solid #E6DFD4; padding: 16px 18px;">
            <div style="font-size: 1.8rem; color: #4D416D; font-weight: 700;">03</div>
            <strong style="color: #173826;">3 Delivery Channels</strong>
            <p style="font-size: 0.85rem; color: #4B6356; margin-top: 4px;">Upload to HIPAA portal, send pre-filled email, or open on phone in session.</p>
        </div>
        <div style="background: #FFF; border-radius: 14px; border: 1px solid #E6DFD4; padding: 16px 18px;">
            <div style="font-size: 1.8rem; color: #1F4932; font-weight: 700;">04</div>
            <strong style="color: #173826;">Faster Healing</strong>
            <p style="font-size: 0.85rem; color: #4B6356; margin-top: 4px;">Saves 2–3 intake sessions by giving your clinician an immediate roadmap.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 4: SEPARATE CLINICIANS DIRECTORY & FIRST MESSAGE -----------------
with gallery_tab4:
    st.markdown("### 🩺 Verified Clinician Directory & First Message Generator")
    st.caption("Browse licensed practitioners matched to different emotional phenotypes, or draft your first message with zero intimidation.")

    # Locality & Regional Matcher
    st.markdown("""
    <div style="background: #FFFFFF; border-radius: 14px; border: 1px solid #E6DED2; padding: 18px 22px; margin-bottom: 16px;">
        <div style="font-size: 1.05rem; font-weight: 700; color: #173827; margin-bottom: 2px;">
            📍 Find Clinicians in Your Area (In-Person or State-Licensed Telehealth)
        </div>
        <div style="font-size: 0.85rem; color: #587163; margin-bottom: 12px;">
            🔒 <strong>100% On-Device Privacy:</strong> Your location is processed locally in this session to match nearby clinics. It is never stored or tracked.
        </div>
    </div>
    """, unsafe_allow_html=True)

    loc_c1, loc_c2 = st.columns([3, 2], gap="medium")
    with loc_c1:
        # Quick locality buttons
        st.markdown("<span style='font-size: 0.84rem; font-weight: 600; color: #2B4E3A;'>Quick Regional Selection:</span>", unsafe_allow_html=True)
        q_loc1, q_loc2, q_loc3, q_loc4, q_loc5 = st.columns(5)
        chosen_loc = st.session_state.get("user_locality", "")
        
        if q_loc1.button("📍 Austin, TX", use_container_width=True):
            st.session_state.user_locality = "Austin, TX"
            chosen_loc = "Austin, TX"
        if q_loc2.button("📍 San Francisco", use_container_width=True):
            st.session_state.user_locality = "San Francisco, CA"
            chosen_loc = "San Francisco, CA"
        if q_loc3.button("📍 New York, NY", use_container_width=True):
            st.session_state.user_locality = "New York, NY"
            chosen_loc = "New York, NY"
        if q_loc4.button("📍 Chicago, IL", use_container_width=True):
            st.session_state.user_locality = "Chicago, IL"
            chosen_loc = "Chicago, IL"
        if q_loc5.button("📍 Boulder, CO", use_container_width=True):
            st.session_state.user_locality = "Boulder, CO"
            chosen_loc = "Boulder, CO"

        user_loc_input = st.text_input(
            "Or enter your City, State, or Zip Code:",
            value=st.session_state.get("user_locality", ""),
            placeholder="e.g. Austin, TX, San Francisco, 10010, or California"
        )
        if user_loc_input != st.session_state.get("user_locality", ""):
            st.session_state.user_locality = user_loc_input

    with loc_c2:
        care_mode = st.pills(
            "Care Setting Preference:",
            ["All Formats", "📍 In-Person Local Clinics Only", "💻 Telehealth Available"],
            default="All Formats"
        )
        if st.session_state.get("user_locality"):
            st.info(f"📍 Matching clinicians for: **{st.session_state.user_locality}**")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    d_col1, d_col2 = st.columns([3, 2], gap="large")
    
    with d_col1:
        st.markdown("#### 🔍 Filter Clinicians (Clickable Pills — Zero Typing)")
        specialties_options = ["All Specialties", "Anxiety", "Work Stress", "Burnout", "Intimate Emotions", "Relationships", "Trauma", "Communication"]
        specialty_filter = st.pills("Filter by primary concern:", specialties_options, default="All Specialties")
        
        active_concern = "" if specialty_filter == "All Specialties" else specialty_filter
        in_person_only = (care_mode == "📍 In-Person Local Clinics Only")
        
        clinicians = find_therapist_matches(
            user_concern=active_concern,
            user_location=st.session_state.get("user_locality", ""),
            in_person_only=in_person_only
        )
        
        for doc in clinicians:
            telehealth_str = "✅ Telehealth Available" if doc.get("telehealth") else "🏥 In-Person Practice"
            loc_badge = doc.get("locality_badge", "")
            clinic_addr = doc.get("in_person_address", "")
            
            st.markdown(f"""
            <div style="background:#FFF; border-radius:14px; border:1px solid #E6DED2; padding:16px 18px; margin-bottom:12px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                    <div style="font-family:'Playfair Display', serif; font-size:1.15rem; font-weight:700; color:#173827;">
                        {doc['name']} <span style="font-size:0.85rem; font-weight:normal; color:#6E5A4D;">— {doc.get('title','')}</span>
                    </div>
                    <span style="background: #FBF0EB; color: #92452A; padding: 2px 8px; border-radius: 6px; font-size: 0.78rem; font-weight: 600;">
                        {loc_badge}
                    </span>
                </div>
                <div style="font-size:0.84rem; color:#2B533E; font-weight:600; margin:4px 0;">
                    <span style="background:#E8EFEA; padding:2px 8px; border-radius:6px;">{doc['modality']}</span> • <em>{telehealth_str}</em>
                </div>
                <div style="font-size:0.82rem; color:#5D7467; margin-bottom: 4px;">
                    📍 <strong>Clinic Location:</strong> {clinic_addr}
                </div>
                <p style="font-size:0.88rem; color:#3C5547; margin:6px 0;">{doc.get('bio','')}</p>
                <div style="font-size:0.82rem; color:#647B6F;">
                    <strong>Specialties:</strong> {", ".join(doc['specialties'])}<br/>
                    <strong>Direct Email:</strong> <span style="font-weight:600; color:#1E3F2E;">{doc['contact']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"✉️ Select {doc['name']} for Message Draft", key=f"sel_doc_{doc['id']}", use_container_width=True):
                st.session_state.active_selected_doc = doc["name"]
                st.rerun()

    with d_col2:
        st.markdown("#### ✉️ 'Draft My First Message' Assistant")
        st.caption("Click any clinician name below to automatically draft your message:")
        
        doc_names = [d["name"] for d in CLINICIAN_DIRECTORY]
        cur_doc = st.session_state.get("active_selected_doc", doc_names[0])
        if cur_doc not in doc_names:
            cur_doc = doc_names[0]
            
        selected_doc = st.pills("Choose clinician to message (Click to switch):", doc_names, default=cur_doc)
        if selected_doc:
            st.session_state.active_selected_doc = selected_doc

        concern_input = st.text_input(
            "Concern to mention in email:", 
            value=specialty_filter if specialty_filter != "All Specialties" else "anxiety and personal emotional regulation"
        )
        user_name = st.text_input("Your preferred name:", value="A prospective client", key="tab4_user")
        
        email_draft = generate_first_contact_email(
            selected_doc, 
            concern_input, 
            user_name, 
            user_location=st.session_state.get("user_locality", "")
        )
        
        st.markdown(f"""<div class="human-letter-box">{email_draft}</div>""", unsafe_allow_html=True)
        st.caption("You can copy this text and email it directly to the clinician.")

    st.divider()
    st.markdown("#### 📬 How Do You Deliver Your Reflection Summary to This Particular Doctor?")
    st.caption("Three simple, patient-controlled ways to share your generated intake sheet with your selected clinician:")
    
    deliv_col1, deliv_col2, deliv_col3 = st.columns(3)
    with deliv_col1:
        st.markdown(f"""
        <div style="background: #FFF; border-radius: 12px; border: 1px solid #E6DED2; padding: 14px 16px;">
            <strong style="color: #173826;">1. Attach to Your Initial Email</strong>
            <p style="font-size: 0.85rem; color: #435E4E; margin-top: 4px; line-height: 1.45;">
                Copy your downloaded summary or paste its bullet points directly into the outreach email draft above when contacting <strong>{selected_doc}</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with deliv_col2:
        st.markdown(f"""
        <div style="background: #FFF; border-radius: 12px; border: 1px solid #E6DED2; padding: 14px 16px;">
            <strong style="color: #8C4023;">2. Direct Patient Portal Upload</strong>
            <p style="font-size: 0.85rem; color: #435E4E; margin-top: 4px; line-height: 1.45;">
                Once the clinician responds and invites you to their HIPAA-compliant portal (e.g. <em>SimplePractice</em> or <em>TherapyNotes</em>), upload your downloaded intake file under 'Client Documents'.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with deliv_col3:
        st.markdown(f"""
        <div style="background: #FFF; border-radius: 12px; border: 1px solid #E6DED2; padding: 14px 16px;">
            <strong style="color: #4D416D;">3. In-Session Phone Anchor</strong>
            <p style="font-size: 0.85rem; color: #435E4E; margin-top: 4px; line-height: 1.45;">
                Open your summary sheet on your smartphone during your 15-minute consultation call. When they ask <em>"What brings you in?"</em>, reference your organized prompts with confidence.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 🌐 National Directories & Low-Cost Care")
    r_cols = st.columns(3)
    resources_list = list(EXTERNAL_RESOURCES.items())
    for idx, (res_name, res_url) in enumerate(resources_list):
        r_cols[idx % 3].markdown(f"• **[{res_name}]({res_url})**")

# ==================== FOOTER ====================
st.markdown("""
<div style="border-top: 1px solid #E4DCD0; margin-top: 40px; padding: 22px 0; color: #657D71; font-size: 0.85rem; line-height: 1.6;">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
        <div>
            <strong style="color: #1A3D2C;">🏛️ MindMate Mental Health Initiative</strong><br/>
            On-device AI mediator for self-reflection & therapy preparation. Not a medical or diagnostic substitute.
        </div>
        <div>
            <strong style="color: #A33A22;">🚨 24/7 Crisis Support:</strong> Call or text <strong>988</strong> (US/Canada) • Text HOME to <strong>741741</strong> • <a href="https://findahelpline.com" target="_blank" style="color: #2B533E; font-weight: 600;">findahelpline.com</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
