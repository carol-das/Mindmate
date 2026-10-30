import streamlit as st
import sys
import os
import pandas as pd

# Add src folder to python path 
sys.path.append(os.path.abspath("src"))

from inference import chat_with_mindmate
from safety_guard import check_input_safety
from summary_engine import generate_pre_session_summary
from memory_vault import log_mood, get_mood_history, purge_vault 
from therapist_match import find_therapist_matches, EXTERNAL_RESOURCES

# Page configuration
st.set_page_config( 
    page_title="MindMate — Your Private Reflection Companion",
    page_icon="🌿", layout="wide", initial_sidebar_state="collapsed" 
    ) 

# Custom Light, Warm, & Comforting CSS
st.markdown("""

""", unsafe_allow_html=True)

# Prominent Hero Title &amp; Site Header
st.markdown("""
<div>
    <div>🌿 MindMate</div>
    <div>A gentle, privacy-first space to organize your thoughts and bridge into human therapy.</div>
    <span>🔒 100% Local &amp; Confidential • Your data never leaves your device</span>
</div>
""", unsafe_allow_html=True)

# Comforting Quotes &amp; Normalizing Therapy Banner
st.markdown("""
<div>
    <div>
        "Taking care of your mind is just as natural as taking care of your body. Seeking therapy isn't a sign that something is broken—it is a courageous choice to understand yourself better. When we learn to navigate our deepest emotions, it gently transforms how we connect, love, and spend time with everyone in our lives."
    </div>
    <div>✦ Gentle Reminder • Therapy is for Everyone</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["💬 Reflection Space", "🔒 Private Mood Vault", "🩺 Human Therapist Directory"])

# ==================== TAB 1: REFLECTION CHAT ====================
with tab1:
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("### How are you feeling today?")
        st.caption("Take your time. MindMate is an empathetic AI mediator designed to help you unpack thoughts before meeting a human therapist.")
        
        # Inclusive, Emotion-Centered Prompt Starters
        st.markdown("**💡 Need a starting point? Click any prompt below:**")
        p_col1, p_col2, p_col3 = st.columns(3)
        
        selected_prompt = None
        if p_col1.button("🌊 Feeling overwhelmed", use_container_width=True):
            selected_prompt = "I'm feeling really overwhelmed right now and don't know where to begin."
        if p_col2.button("🌧️ Hesitant about therapy", use_container_width=True):
            selected_prompt = "I'm anxious about starting therapy and worried I won't know what to say."
        if p_col3.button("💭 Hard to express feelings", use_container_width=True):
            selected_prompt = "I want to share what's on my mind, but I find it really difficult to put my emotions into words."

        st.divider()

        # Chat history session state
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display conversation
        for message in st.session_state.messages:
            avatar = "🌿" if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

        # Determine user prompt (either typed or chip clicked)
        prompt_input = st.chat_input("Share whatever is on your mind...")
        user_text = selected_prompt or prompt_input

        if user_text:
            st.session_state.messages.append({"role": "user", "content": user_text})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_text)

            # Safety Shield Intercept Check
            safety_check = check_input_safety(user_text)
            
            if not safety_check["is_safe"]:
                response = safety_check["response"]
            else:
                with st.spinner("MindMate is listening and reflecting..."):
                    response = chat_with_mindmate(user_text)

            with st.chat_message("assistant", avatar="🌿"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    with col2:
        st.markdown("### 📋 Therapy Prep Sheet")
        st.caption("Summarize your reflection history into a clear 3-part sheet ready for your next clinician appointment.")
        
        if st.button("✨ Generate Reflection Sheet", use_container_width=True, type="primary"):
            if "messages" in st.session_state and st.session_state.messages:
                with st.spinner("MindMate is organizing your insights..."):
                    summary_output = generate_pre_session_summary(st.session_state.messages)
                    st.info("Here is your structured summary. You can copy or reference this during your intake session:")
                    st.markdown(summary_output)
            else:
                st.warning("Start a brief reflection conversation first so MindMate can summarize your insights!")

# ==================== TAB 2: MEMORY VAULT ====================
with tab2:
    st.markdown("### 🔒 Sensitive Cubicle Data Vault")
    st.caption("Your mood logs and notes remain stored locally in your private database. You maintain full data sovereignty.")
    
    v_col1, v_col2 = st.columns(2, gap="large")
    
    with v_col1:
        st.markdown("#### 📝 Daily Check-in")
        mood_score = st.slider("Select your current emotional state:", 1, 5, 3)
        mood_labels = {
            1: "😖 Overwhelmed &amp; Heavy", 
            2: "😟 Anxious &amp; Restless", 
            3: "😐 Neutral &amp; Grounded", 
            4: "🙂 Hopeful &amp; Reflective", 
            5: "😊 Calmer &amp; Focused"
        }
        st.info(f"**Current State:** {mood_labels[mood_score]}")
        mood_note = st.text_input("Reflection note (optional):", placeholder="e.g., Prepared questions for my therapist")
        
        if st.button("💾 Save Entry Locally", use_container_width=True):
            log_mood(mood_score, mood_note)
            st.success("Entry saved safely to your local vault!")

    with v_col2:
        st.markdown("#### 📊 Local Memory Controls")
        if st.checkbox("📖 View Local Reflection Logs"):
            history = get_mood_history()
            if history:
                df = pd.DataFrame(history, columns=["Timestamp", "Score", "Note"])
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No local entries recorded yet.")
                
        st.markdown("---")
        st.markdown("**Data Sovereignty Zone**")
        if st.button("🗑️ Permanently Delete All Vault Data", type="primary", use_container_width=True):
            purge_vault()
            st.warning("All local records have been erased permanently.")

# ==================== TAB 3: THERAPIST DIRECTORY ====================
with tab3:
    st.markdown("### 🩺 Transition to Human Clinical Care")
    st.caption("MindMate helps prepare you for therapy, but human connection is where healing happens. Browse verified practitioners below.")
    
    filter_keyword = st.selectbox(
        "Filter clinicians by primary specialty:",
        ["All Specialties", "Anxiety", "Work Stress", "Burnout", "Life Transitions", "Overwhelm"]
    )
    
    query = "" if filter_keyword == "All Specialties" else filter_keyword
    matches = find_therapist_matches(query)
    
    for doc in matches:
        with st.expander(f"👤 {doc['name']} — {doc['modality']}"):
            st.write(f"**Specialties:** {', '.join(doc['specialties'])}")
            st.write(f"**Telehealth Available:** {'Yes ✅' if doc['telehealth'] else 'In-Person Only 🏥'}")
            st.write(f"**Direct Contact:** `{doc['contact']}`")

    st.divider()
    st.markdown("### 🌐 Verified National Directories")
    for title, link in EXTERNAL_RESOURCES.items():
        st.markdown(f"• [{title}]({link})")


