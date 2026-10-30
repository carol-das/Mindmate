from anxiety_engine import infer_anxiety_pattern

def generate_pre_session_summary(chat_history: list) -> str:
    """
    Synthesizes user conversation messages into a clinically useful, structured
    3-part intake preparation sheet for a human therapist consultation,
    including inferred surface-level anxiety patterns and empirical research references.
    """
    user_notes = [m["content"] for m in chat_history if m.get("role") == "user"]
    
    if not user_notes:
        return "No reflection data available yet. Please have a brief conversation with MindMate first."
    
    # Analyze themes from user inputs
    all_text = " ".join(user_notes).lower()
    inferred = infer_anxiety_pattern(all_text)
    profile = inferred["profile"]
    papers = inferred["papers"]
    
    themes = []
    if any(k in all_text for k in ["overwhelm", "stress", "work", "burnout", "busy", "pressure", "drowning"]):
        themes.append("Workplace and cognitive overwhelm, chronic allostatic stress loading")
    if any(k in all_text for k in ["hesitant", "scared", "nervous", "anxiety", "judge", "afraid", "freeze"]):
        themes.append("Apprehension regarding clinical vulnerability, fear of negative appraisal")
    if any(k in all_text for k in ["partner", "relationship", "family", "friend", "love", "lonely", "fight"]):
        themes.append("Interpersonal friction, relational co-regulation challenges, boundary repair")
    if any(k in all_text for k in ["words", "express", "numb", "fog", "shut down", "can't talk", "tight"]):
        themes.append("Difficulty labeling visceral feelings, somatic tension & autonomic guarding")
    if any(k in all_text for k in ["sad", "loss", "grief", "hopeless", "down"]):
        themes.append("Persistent emotional heaviness, grief processing, depressive fatigue")
        
    if not themes:
        themes.append("General emotional grounding and proactive self-reflection")

    # Sample user excerpts
    key_quotes = "\n".join([f'  - *"{u[:100]}..."*' if len(u) > 100 else f'  - *"{u}"*' for u in user_notes[-3:]])
    
    papers_list = "\n".join([f"  • *{p['title']}* ({p['authors']}, {p['year']}) — {p['key_finding']}" for p in papers[:2]])

    summary = f"""### 📋 Pre-Session Intake & Clinical Preparation Sheet
*Generated on-device by MindMate (Sensitive Cubicle Architecture). Confidential & Patient-Controlled.*

---

#### 1. Primary Concerns & Observed Themes
- **Core Emotional Themes Identified:**
{chr(10).join([f"  • {t}" for t in themes])}
- **In the Client's Own Expression:**
{key_quotes}

#### 2. Surface Pattern Inference & Scientific Context
- **Identified Phenotype:** {profile['label']} (`{profile['nervous_system_state']}`)
- **Compassionate Reframe:** {profile['comforting_reframe']}
- **Relevant Empirical Research:**
{papers_list}

#### 3. Targeted Discussion Prompts for Your Intake Session
- *"Here is how my internal emotional state has been affecting my energy and how I show up for people I love."*
- *"I sometimes find it hard to put feelings into words; can we practice somatic or grounding cues when I feel frozen?"*
- *"What therapeutic modalities (CBT, ACT, Somatic experiencing) do you think best fit what I have outlined here?"*
- *"How can we build emotional regulation tools I can use at home between our sessions?"*

---
🔒 **Patient Delivery Protocol**:
This summary is stored locally on your device. To share it with your clinician:
1. **Direct Portal Upload:** Download this sheet as Markdown/PDF and upload to your clinician's HIPAA-compliant portal (e.g., SimplePractice, TherapyNotes).
2. **Encrypted Email Outreach:** Use the 'Draft My First Message' tool to attach this summary directly to your chosen specialist.
3. **In-Session Anchor:** Open this sheet on your phone during your first consultation to guide the discussion with confidence.
"""
    return summary
